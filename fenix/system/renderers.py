import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        errors = data.get('results', None)
        response = renderer_context['response']
        # Here we get the token
        token = data.get('token', None)

        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            # we receive the token in byte format so we need
            # to decode it to make it easily serializable
            data['token'] = token.decode('utf-8')

        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'status_code': response.status_code,
            'results': data
        })


class GeneralRenderer(JSONRenderer):
    charset = 'utf-8'
    object_name = 'results'

    def render(self, data,  media_type=None, renderer_context=None):
        response = renderer_context['response']
        if type(data) != ReturnList:
            errors = data.get('results', None)
            if errors is not None:
                return super().render(data)
            else:
                return json.dumps({
                    'status_code': response.status_code,
                    self.object_name: data
                })
        else:
            return json.dumps({
                'status_code': response.status_code,
                self.object_name: data,
            })
