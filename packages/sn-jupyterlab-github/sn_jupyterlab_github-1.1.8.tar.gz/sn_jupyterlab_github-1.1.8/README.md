# JupyterLab GitHub [![Build Status](https://travis.ibm.com/cognitive-class-labs/jupyterlab-github.svg?token=xeywPRUyHm9VWQkDxLoo&branch=master)](https://travis.ibm.com/cognitive-class-labs/jupyterlab-github)

This is a fork of [The official JupyterLab GitHub extension](https://github.com/jupyterlab/jupyterlab-github).

If you are developing a feature that would be useful for
general users, please make a PR to the official repo, get it merged, then bring the changes into this repo.

**Note**: the base directory is currently hardcoded to `/resources` ([see issue here](https://github.ibm.com/cognitive-class-labs/jupyterlab-github)). This means gist sharing is broken unless you go out of your way to run `jupyter lab` in `/resources`, which isn't recommended because you would need to run it as root. Fixing this issue should probably be the first concern before developing any other features for this extension.

## Getting Changes from Upstream

- `git fetch upstream`
- `git merge upstream/master`
- resolve conflicts
  - note: make sure you don't get any changes from the upstream's `.travis.yml`

## Initial Setup

- Create a conda environment for developing this extension: `conda create -n jupyterlab-github -y && conda activate jupyterlab-github`
- install jupyterlab: `conda install -c conda-forge jupyterlab==1.0.2 -y`
- Create a GitHub OAuth app, run `cp .env.example .env` and fill in `.env` with the client id and secret.

## Development

- install dependencies and build: `yarn install && yarn run build`
- install the lab extension: `jupyter labextension link .`
- install the server extension: `pip install .`
- To watch and automatically rebuild the lab extension run `yarn run watch`
- In a separate terminal window, run `jupyter lab` to start jupyterlab.
- Changes to the lab extension will trigger automatic rebuilds of the extension as you make changes.
- Changes made to the server extension (i.e. the python code in `sn_jupyterlab_github/`) will require a manual reinstall (`pip install .`) and restart (i.e. `ctrl+c` and `jupyter lab`).

## Release Publishing

To publish a new version of the lab extension and/or server extension:

- Update the version in [package.json](package.json)
- Update the version in [setup.py](setup.py)
  - note: you need to update _both_ versions, even if you modified just the lab extension or just the server extension one or the other
- Merge/push to the master branch.
- `git tag <TAG> && git push origin <TAG>` to trigger a travis build/release.
