# Links

https://github.com/ReallyFuzzy/IceFilms.bundle
https://github.com/ReallyFuzzy/LetMeWatchThis.bundle
https://github.com/ReallyFuzzy/ITV-Player.bundle.git
https://github.com/kolsys/YouTubeTV.bundle
https://github.com/TroRg/plex.kino.pub
http://thingsinjars.com/post/297/writing-a-plex-plugin-part-i/
https://github.com/plex-unofficial/KartinaTV.bundle/blob/master/Contents/Code/__init__.py
https://github.com/plexinc-plugins/Services.bundle/blob/master/Contents/Service%20Sets/com.plexapp.plugins.cbcnewsnetwork/URL/CBC/ServiceCode.pys
https://github.com/meriko/NBCSportsLiveExtra.bundle

https://support.plex.tv/hc/en-us/articles/201382123
https://support.plex.tv/hc/en-us/articles/201169747-A-Beginner-s-Guide-to-v2-1
https://github.com/plex-unofficial/ETVnet.bundle

https://github.com/serge-v/ctv

# Install

xcode-select --install

brew install pyenv

pyenv install 3.5.1
pyenv install 2.7.10
pyenv rehash

pyenv local 2.7.10
pyenv global 3.5.1

python --version

easy_install pip
pip install invoke
pip install paramiko

pip install lxml
pip install requests

# Linux on flash

1.

hdiutil convert -format UDRW -o ~/Downloads/ubuntu-15.10-desktop-amd64 ~/Downloads/ubuntu-15.10-desktop-amd64.iso

2.

diskutil list

# /dev/disk3

3.

diskutil eject /dev/disk3
diskutil unmountDisk /dev/disk3

4.

sudo dd if=/Users/ashvets/Downloads/ubuntu-15.10-desktop-amd64.dmg of=/dev/rdisk3 bs=1m


# Ubuntu

/Users/cheeta/Library/Application Support/Plex Media Server/Plug-ins/Etvnet.bundle

tail -f /var/lib/plexmediaserver//Library/Application\ Support/Plex\ Media\ Server/Logs/PMS\ Plugin\ Logs/com.plexapp.plugins.etvnet.log
tail -f /var/lib/plexmediaserver//Library/Application\ Support/Plex\ Media\ Server/Logs/Plex\ Media\ Server.log

tail -f ~/Library/Logs/PMS Plugin Logs/com.plexapp.plugins.etvnet.log
tail -f ~/Library/Logs/Plex\ Media\ Server.log
