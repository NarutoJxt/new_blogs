from rest_framework.renderers import JSONRenderer


class UserInfoRender(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return super(UserInfoRender,self).render(data,accepted_media_type,renderer_context)
