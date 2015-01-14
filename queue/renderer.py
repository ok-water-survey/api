__author__ = 'mstacy'
from rest_framework.renderers import BrowsableAPIRenderer

class QueueRunBrowsableAPIRenderer(BrowsableAPIRenderer):
    #def get_default_renderer(self, view):
    #    return JSONRenderer()

    template = 'rest_framework/queue_run_api.html'
    def get_context(self, data, accepted_media_type, renderer_context):
        context= super(QueueRunBrowsableAPIRenderer,self).get_context(data, accepted_media_type, renderer_context)
        if context['request'].method.upper() == 'GET':
            context['content']=data
        return context