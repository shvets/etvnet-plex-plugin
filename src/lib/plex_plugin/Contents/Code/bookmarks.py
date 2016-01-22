import archive

def append_controls(oc, **params):
    bookmark = video_service.get_bookmark(params['id'])

    if bookmark:
        oc.add(DirectoryObject(
                key=Callback(HandleRemoveBookmark, **params),
                title=unicode(L('Remove Bookmark')),
                thumb=R(REMOVE_ICON)
        ))
    else:
        oc.add(DirectoryObject(
                key=Callback(HandleAddBookmark, **params),
                title=unicode(L('Add Bookmark')),
                thumb=R(ADD_ICON)
        ))

@route('/video/etvnet/add_bookmark')
def HandleAddBookmark(**params):
    video_service.add_bookmark(params['id'])

    return ObjectContainer(header=unicode(L(params['name'])), message=unicode(L('Bookmark Added')))

@route('/video/etvnet/remove_bookmark')
def HandleRemoveBookmark(**params):
    video_service.remove_bookmark(params['id'])

    return ObjectContainer(header=unicode(L(params['name'])), message=unicode(L('Bookmark Removed')))

@route('/video/etvnet/bookmarks')
def GetBookmarks():
    oc = ObjectContainer(title2=unicode(L('Bookmarks')))

    response = video_service.get_bookmarks()

    for media in archive.HandleMediaList(response['data']['bookmarks']):
        oc.add(media)

    return oc
