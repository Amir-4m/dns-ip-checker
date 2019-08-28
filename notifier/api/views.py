import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from notifier.tasks import send_notification


class NotifierApiView(APIView):

    def post(self, request):
        slug = request.POST.get('slug')
        template = request.POST.get('template')
        dict_template = json.loads(template)

        try:
            send_notification.delay(slug=slug, template_context=dict_template)
        except Exception as e:
            raise ValidationError(dict(sent=False, error=str(e)))

        return Response(dict(sent=True))
