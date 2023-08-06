import re, json, copy, os, requests

import tornado.gen as gen
from tornado.httputil import url_concat
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from tornado.web import RequestHandler

from traitlets import Unicode, Bool
from traitlets.config import SingletonConfigurable

from notebook.utils import url_path_join, url_escape
from notebook.base.handlers import APIHandler

link_regex = re.compile(r'<([^>]*)>;\s*rel="([\w]*)\"')

class GitHubConfig(SingletonConfigurable):

    """
    Allows configuration of access to the GitHub api.
    Modified to use SingletonConfigurable to work better with CC Labs.
    """
    allow_client_side_access_token = Bool(
        False, config=True,
        help=(
            "If True the access token specified in the JupyterLab settings "
            "will take precedence. If False the token specified in JupyterLab "
            "will be ignored. Storing your access token in the client can "
            "present a security risk so be careful if enabling this setting."
        )
    )
    api_url = Unicode(
        'https://api.github.com', config=True,
        help="The url for the GitHub api"
    )
    access_token = Unicode(
        '', config=True,
        help=(
            "A personal access token for GitHub. If specified it takes "
            "precedence over the `client_id` and `client_secret`"
        )
    )
    client_id = Unicode(
        '', config=True,
        help="The Client ID for the GitHub OAuth app"
    )
    client_secret = Unicode(
        '', config=True,
        help="The Client secret for the GitHub OAuth app"
    )
    validate_cert = Bool(
        True, config=True,
        help=(
            "Whether to validate the servers' SSL certificate on requests "
            "made to the GitHub api. In general this is a bad idea so only "
            "disable SSL validation if you know what you are doing!"
        )
    )


class AuthHandler(RequestHandler):

    """
    Handles the GitHub OAuth callback (CC Labs specific).
    """

    @gen.coroutine
    def get(self, path=''):
        query = self.request.query_arguments
        params = { key: query[key][0].decode() for key in query }
        headers = {'Accept': 'application/json'}
        data = {
            'client_id':os.environ.get('GITHUB_CLIENT_ID'),
            'client_secret':os.environ.get('GITHUB_CLIENT_SECRET'),
            'code': params['code']
        }
        res = requests.post('https://github.com/login/oauth/access_token', json=data, headers=headers)
        access_token = res.json()['access_token']
        headers['Authorization'] = 'token {}'.format(access_token)

        res = requests.get('https://api.github.com/user', headers=headers)
        user = res.json()['login']

        c = GitHubConfig.instance()
        c.access_token = access_token

        self.finish("<script>window.opener.postMessage('{0}','*')</script>".format(user))

class GetClientIDHandler(APIHandler):
    """
    Used to get the GitHub Oauth ClientID (CC Labs Specific).
    """

    @gen.coroutine
    def get(self, path=''):
        self.finish(json.dumps({'client_id': os.environ.get('GITHUB_CLIENT_ID')}))

class GistShareHandler(APIHandler):
    """
    Creates GitHub gists for a given file (CC Labs Specific).
    """

    @gen.coroutine
    def post(self, path=''):

        gist = {
            "description": "Created on Skills Network Labs",
            "public": True,
            "files": {}
        }

        with open('{}/{}'.format(os.getcwd(),json.loads(self.request.body)['path'])) as f:
            gist['files'][os.path.basename(f.name)] = {'content': f.read()}

        # Get access to the notebook config object
        c = GitHubConfig.instance()
        if not c.access_token:
            self.finish(json.dumps({'error': 'unauthenticated'}))
        else:
            headers = {'Authorization': 'token {}'.format(c.access_token)}
            res = requests.post('https://api.github.com/gists', json=gist, headers=headers)
            self.finish(json.dumps(res.json()))

class GitHubHandler(APIHandler):
    """
    A proxy for the GitHub API v3.

    The purpose of this proxy is to provide authentication to the API requests
    which allows for a higher rate limit. Without this, the rate limit on
    unauthenticated calls is so limited as to be practically useless.
    """
    @gen.coroutine
    def get(self, path):
        """
        Proxy API requests to GitHub, adding authentication parameter(s) if
        they have been set.
        """

        # Get access to the notebook config object
        c = GitHubConfig.instance()
        try:
            query = self.request.query_arguments
            params = {key: query[key][0].decode() for key in query}
            api_path = url_path_join(c.api_url, url_escape(path))
            params['per_page'] = 100

            access_token = params.pop('access_token', None)
            if access_token and c.allow_client_side_access_token == True:
                params['access_token'] = access_token
            elif access_token and c.allow_client_side_access_token == False:
                msg = (
                    "Client side (JupyterLab) access tokens have been "
                    "disabled for security reasons.\nPlease remove your "
                    "access token from JupyterLab and instead add it to "
                    "your notebook configuration file:\n"
                    "c.GitHubConfig.access_token = '<TOKEN>'\n"
                )
                raise HTTPError(403, msg)
            elif c.access_token != '':
                # Preferentially use the access_token if set
                params['access_token'] = c.access_token
            elif c.client_id != '' and c.client_secret != '':
                # Otherwise use client_id and client_secret if set
                params['client_id'] = c.client_id
                params['client_secret'] = c.client_secret

            api_path = url_concat(api_path, params)
            client = AsyncHTTPClient()
            request = HTTPRequest(
                api_path, validate_cert=c.validate_cert,
                user_agent='JupyterLab GitHub'
            )
            response = yield client.fetch(request)
            data = json.loads(response.body.decode('utf-8'))

            # Check if we need to paginate results.
            # If so, get pages until all the results
            # are loaded into the data buffer.
            next_page_path = self._maybe_get_next_page_path(response)
            while next_page_path:
                request = copy.copy(request)
                request.url = next_page_path
                response = yield client.fetch(request)
                next_page_path = self._maybe_get_next_page_path(response)
                data.extend(json.loads(response.body.decode('utf-8')))

            # Send the results back.
            self.finish(json.dumps(data))

        except HTTPError as err:
            self.set_status(err.code)
            message = err.response.body if err.response else str(err.code)
            self.finish(message)

    def _maybe_get_next_page_path(self, response):
        # If there is a 'Link' header in the response, we
        # need to paginate.
        link_headers = response.headers.get_list('Link')
        next_page_path = None
        if link_headers:
            links = {}
            matched = link_regex.findall(link_headers[0])
            for match in matched:
                links[match[1]] = match[0]
            next_page_path = links.get('next', None)

        return next_page_path

def _jupyter_server_extension_paths():
    return [{
        'module': 'sn_jupyterlab_github'
    }]

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    base_url = web_app.settings['base_url']
    endpoint = url_path_join(base_url, 'github')
    handlers = [
        (url_path_join(endpoint, 'auth') + "(.*)", AuthHandler),
        (url_path_join(endpoint, 'client-id') + "(.*)", GetClientIDHandler),
        (url_path_join(endpoint, 'share-gist') + "(.*)", GistShareHandler),
        (endpoint + "(.*)", GitHubHandler)
    ]
    web_app.add_handlers('.*$', handlers)
