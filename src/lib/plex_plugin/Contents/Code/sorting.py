def append_controls(oc, handler, **params):
    if params['dir'] == 'asc':
        params['dir'] = 'desc'
    else:
        params['dir'] = 'asc'

    oc.add(DirectoryObject(
            key=Callback(handler, **params),
            title=unicode(L('Sort Items')),
            thumb="thumb"
    ))
