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

# How to fix live streaming on iOS and tvOS

Files location:

/Applications/Plex Media Server.app/Contents/Resources/Profiles/iOS.xml
/Applications/Plex Media Server.app/Contents/Resources/Profiles/tvOS.xml

/usr/lib/plexmediaserver/Resources/Profiles/iOS.xml
/usr/lib/plexmediaserver/Resources/Profiles/tvOS.xml

..\Program Files (x86)\Plex Media Server\Resources\Profiles\iOS.xml

- comment hls profile from TranscodeTargets section
- add new section to DirectPlayProfiles section:
- restart PMS

<VideoProfile protocol="hls" container="mpegts" codec="h264" audioCodec="aac,mp3" context="streaming" />

# Logs

- Linux:

/var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Logs/PMS\ Plugin\ Logs/com.plexapp.plugins.etvnet.log
/var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Logs/Plex\ Media\ Server.log

OSX:
~/Library/Logs/PMS\ Plugin\ Logs/com.plexapp.plugins.etvnet.log
~/Library/Logs/Plex\ Media\ Server.log

# Plugin Location

- Linux:
/var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/Etvnet.bundle/

- OSX:
~/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/Etvnet.bundle/

# Inspired Projects

* Alternative YouTube plugin - https://github.com/kolsys/YouTubeTV.bundle

* ETVNET on XBMC - http://etvnet.com/xbmc

# Articles

* [A Beginner's Guide to v2.1] [beginner-guide]
* [Channels from Other Sources] [channels-from-other-sources]
* [The Power of the URL Service] [url-service]
* [How do I manually install a channel?] [manually-install-a-channel]
* [Plex Channels Forum] [plex-channels-forum]
* [Plex Channels Dev Forum] [plex-channels-dev-forum]
* [Services] [plex-services]
* [Plex Plugin Development Walkthrough] [plex-walkthrough]

[beginner-guide]: https://support.plex.tv/hc/en-us/articles/201169747
[channels-from-other-sources]: https://support.plex.tv/hc/en-us/articles/201375863-Channels-from-Other-Sources
[url-service]: https://support.plex.tv/hc/en-us/articles/201382123-The-Power-of-the-URL-Service
[manually-install-a-channel]: https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-
[plex-channels-forum]: https://forums.plex.tv/categories/plex-channels
[plex-channels-dev-forum]: https://forums.plex.tv/categories/channel-development
[plex-services]: https://github.com/plexinc-plugins/Services.bundle
[plex-walkthrough]: https://forums.plex.tv/discussion/28084/plex-plugin-development-walkthrough
