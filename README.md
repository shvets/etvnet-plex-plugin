# Plex Plugin for watching library of russian movies online

# Requirements

- Python 2.7.x
- OSX or Ubuntu

# Installing core tools

- Install Python (OSX):

```bash
xcode-select --install

brew install pyenv

pyenv install 2.7.10
pyenv rehash

pyenv local 2.7.10

python --version
```

- Install pip and invoke:

```bash
easy_install pip
pip install invoke
```

# Building and installing plugin

- build plugin:

```bash
invoke build
```

After this command folder 'build' will contains 'Etvnet.bundle.zip' archive.

You need to extract this archive into the following folder:

- on OSX: ~/Library/Application\ Support/Plex\ Media\ Server

- on Ubuntu: /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server

See how to manually install a channel [here] [manually-install-a-channel]

You can build and deploy on OSX with this command:

```bash
invoke deploy
```

It also restarts plex server and displays log file.

# Install plugin on remote Ubuntu machine:

```bash
env USERNAME=user HOSTNAME=remote_host invoke rdeploy
```

[manually-install-a-channel]: https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-