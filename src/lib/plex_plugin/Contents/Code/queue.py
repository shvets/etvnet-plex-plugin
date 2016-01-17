# import archive
# from media_info import MediaInfo
#
# def append_controls(oc, type, **params):
#     if item_already_added_to_storage(params['id']):
#         oc.add(DirectoryObject(
#                 key=Callback(HandleRemoveFromQueue, type=type, **params),
#                 title=unicode(L('Remove from Queue')),
#                 thumb=R(REMOVE_ICON)
#         ))
#     else:
#         oc.add(DirectoryObject(
#                 key=Callback(HandleAddToQueue, type=type, **params),
#                 title=unicode(L('Add to Queue')),
#                 thumb=R(ADD_ICON)
#         ))
#
# @route('/video/etvnet/add_to_queue')
# def HandleAddToQueue(type, **params):
#     media_info = MediaInfo(type=type, **params)
#
#     video_service.queue.add(media_info)
#     video_service.queue.save()
#
#     return ObjectContainer(
#         header=u'%s' % L(params['name']),
#         message=u'%s' % L('Media Added')
#     )
#
# @route('/video/etvnet/remove_from_queue')
# def HandleRemoveFromQueue(type, **params):
#     media_info = MediaInfo(type=type, **params)
#
#     video_service.queue.remove(media_info)
#     video_service.queue.save()
#
#     return ObjectContainer(
#         header=u'%s' % L(params['name']),
#         message=u'%s' % L('Media Removed')
#     )
#
# @route('/video/etvnet/queue')
# def GetQueue():
#     oc = ObjectContainer(title2=unicode(L('Queue')))
#
#     for media in archive.HandleMediaList(video_service.queue.data, in_queue=True):
#         oc.add(media)
#
#     return oc
#
# def item_already_added_to_storage(id):
#     added = False
#
#     for media in video_service.queue.data:
#         if id == media['id']:
#             added = True
#             break
#
#     return added