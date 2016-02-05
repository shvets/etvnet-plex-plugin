# Plex Plugin for watching russian movies online from Etvnet media library

# Requirements

- Python 2.7.x
- OSX or Ubuntu
- Plex Media Server

# Install PMS on Ubuntu

```bash
sudo dpkg -i /home/alex/Downloads/plexmediaserver_0.9.14.6.1620-e0b7243_amd64.deb
```

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
pip install paramiko
```

# Building and installing plugin

Plex Media Server (PMS) is located in (<plex_home>):

- Ubuntu: /var/lib/plexmediaserver
- OSX: /Applications/Plex\ Media\ Server.app

Plugins for PMS are located here (<plugins_home>):

- Ubuntu: /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins
- OSX:  ~/Library/Application\ Support/Plex\ Media\ Server/Plug-ins

- build plugin:

```bash
invoke build
```

After this command folder 'build' will have 'Etvnet.bundle.zip' archive.

You need to extract this archive into the <plugins_home>:

See how to manually install a channel [here] [manually-install-a-channel]

On Ubuntu, because of plugins folder location, you have to change the directory owner (plex):

```bash
sudo -S chown -R plex /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/Etvnet.plugin
```

You can build and deploy on OSX with this command:

```bash
invoke deploy
```

It also restarts plex server and displays log file.

# Install plugin on remote Ubuntu machine:

```bash
env USERNAME=user HOSTNAME=remote_host invoke rdeploy
```

# How to fix live streaming on tvOS

Files location:

* /Applications/Plex Media Server.app/Contents/Resources/Profiles/tvOS.xml
* /usr/lib/plexmediaserver/Resources/Profiles/tvOS.xml
* ..\Program Files (x86)\Plex Media Server\Resources\Profiles\tvOS.xml

- replace content:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Client name="tvOS">
  <!-- Author: Plex Inc. -->
  <!-- This profile is used by A8-based tvOS devices -->
  <Settings>
    <Setting name="DirectPlayStreamSelection" value="true" />
    <Setting name="StreamUnselectedIncompatibleAudioStreams" value="true" />
  </Settings>
  <TranscodeTargets>
    <VideoProfile protocol="hls" container="mpegts" codec="h264" audioCodec="aac,ac3,mp3" context="streaming">
      <Setting name="VideoEncodeFlags" value="-x264opts bframes=3:cabac=1" />
    </VideoProfile>
    <MusicProfile container="mp3" codec="mp3" />
    <PhotoProfile container="jpeg" />
    <SubtitleProfile protocol="hls" container="webvtt" subtitleCodec="webvtt"/>
  </TranscodeTargets>
  <DirectPlayProfiles>
    <VideoProfile container="mp4" codec="h264,mpeg4" audioCodec="aac,ac3,eac3" subtitleCodec="ttxt,tx3g,mov_text" />
    <!-- Since tvOS may have issues direct playing mov/*/eac3 it has its own profile  -->
    <VideoProfile container="mov" codec="h264,mpeg4" audioCodec="aac,ac3" subtitleCodec="ttxt,tx3g,mov_text" />
    <!-- Allow Direct Play of HLS content  -->
    <VideoProfile protocol="hls" container="mpegts" codec="h264" audioCodec="aac" />
    <MusicProfile container="mp3" codec="mp3" />
    <MusicProfile container="mp4" codec="aac" />
    <PhotoProfile container="jpeg" />
  </DirectPlayProfiles>
  <CodecProfiles>
    <VideoCodec name="h264">
      <Limitations>
        <UpperBound name="video.width" value="1920" />
        <UpperBound name="video.height" value="1080" />
        <UpperBound name="video.bitDepth" value="8" isRequired="false" />
      </Limitations>
    </VideoCodec>
    <VideoAudioCodec name="aac">
      <Limitations>
        <UpperBound name="audio.channels" value="2" />
      </Limitations>
    </VideoAudioCodec>
  </CodecProfiles>
</Client>
```

- restart PMS

<VideoProfile protocol="hls" container="mpegts" codec="h264" audioCodec="aac,mp3" context="streaming" />

# Logs

- Ubuntu:

/var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Logs/PMS\ Plugin\ Logs/com.plexapp.plugins.etvnet.log
/var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Logs/Plex\ Media\ Server.log

OSX:
~/Library/Logs/PMS\ Plugin\ Logs/com.plexapp.plugins.etvnet.log
~/Library/Logs/Plex\ Media\ Server.log

# Plugin Location

- Ubuntu:
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
