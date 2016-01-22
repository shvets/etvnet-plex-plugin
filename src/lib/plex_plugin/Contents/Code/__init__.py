import common
import plex_video_service
import radio_service

ART = 'art-default.jpg'
ICON = 'icon-default.png'
SEARCH_ICON = 'icon-search.png'
OPTIONS_ICON = 'icon-options.png'
NEXT_ICON = 'icon-next.png'
BACK_ICON = 'icon-back.png'
ADD_ICON = 'icon-add.png'
REMOVE_ICON = 'icon-remove.png'

video_service = plex_video_service.PlexVideoService()
radio_service = radio_service.RadioService()

import live
import archive
import bookmarks
import radio

def Start():
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')
    Plugin.AddViewGroup('MediaPreview', viewMode='MediaPreview', mediaType='items')

    # DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)

    # VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)

    HTTP.CacheTime = CACHE_1HOUR

    common.validate_prefs()

@handler('/video/etvnet', 'Etvnet', thumb=ICON, art=ART)
def MainMenu(complete=False, offline=False):
    oc = ObjectContainer(title1='Etvnet', art=R(ART))

    if offline:
        video_service.reset_token()

    if not video_service.check_token():
        oc.add(DirectoryObject(
            key = Callback(Authorization),
            title = unicode(L('Authorize')),
            thumb = R(OPTIONS_ICON),
        ))

        oc.add(DirectoryObject(
            key=Callback(MainMenu, complete=True, offline=True),
            title=unicode(L('Reset Token')),
            summary=unicode(L('Reset Token')),
        ))

        if complete:
            oc.header = unicode(L('Authorize'))
            oc.message = unicode(L('You must enter code for continue'))

        return oc

    oc.http_cookies = HTTP.CookiesForURL(video_service.API_URL)

    oc.add(DirectoryObject(key=Callback(live.GetLiveChannelsMenu), title=unicode(L('Live'))))
    oc.add(DirectoryObject(key=Callback(archive.GetArchiveMenu), title=unicode(L('Archive'))))
    oc.add(DirectoryObject(key=Callback(archive.GetNewArrivals), title=unicode(L('New Arrivals'))))
    oc.add(DirectoryObject(key=Callback(archive.GetTopicsMenu), title=unicode(L('Topics'))))
    oc.add(DirectoryObject(key=Callback(bookmarks.GetBookmarks), title=unicode(L('Bookmarks'))))
    oc.add(DirectoryObject(key=Callback(radio.GetRadioMenu), title=unicode(L('Radio'))))
    oc.add(DirectoryObject(key=Callback(GetSystemMenu), title=unicode(L('System'))))

    oc.add(InputDirectoryObject(key=Callback(archive.SearchMovies), title=unicode(L("Movies Search")), thumb=R(SEARCH_ICON)))

    return oc

@route('/video/etvnet/system_menu')
def GetSystemMenu():
    oc = ObjectContainer(title2=unicode(L('System')))

    oc.add(DirectoryObject(key=Callback(archive.GetHistory), title=unicode(L('History'))))
    oc.add(DirectoryObject(key=Callback(MainMenu, complete=True, offline=True), title=unicode(L('Reset Token'))))

    return oc

@route('/video/etvnet/authorization')
def Authorization():
    return video_service.authorization(on_authorization_success=OnAuthorizationSuccess,
                                 on_authorization_failure=OnAuthorizationFailure)

def OnAuthorizationSuccess(user_code, device_code, activation_url):
    oc = ObjectContainer(
        # view_group='details',
        no_cache=True,
        objects=[
            DirectoryObject(
                key=Callback(MainMenu, complete=True),
                    title=unicode(F('codeIs', user_code)),
                    summary=unicode(F('enterCodeSite', user_code, activation_url)),
                    tagline=activation_url,
                ),
                DirectoryObject(
                    key=Callback(MainMenu, complete=True),
                    title=unicode(L('Authorize')),
                    summary=unicode(L('Complete authorization')),
                ),
            ]
    )

    return oc

def OnAuthorizationFailure():
    return ObjectContainer(
        header=uniocode(L('Error')),
        message=unicode(L('Service temporarily unavailable'))
    )
