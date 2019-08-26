import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from notifier.models import NotificationMessage
from notifier.tasks import send_notification


class NotifierApiView(APIView):
    def post(self, request):
        slug = request.POST.get('slug')
        template = request.POST.get('template')
        dict_template = json.loads(template)

        try:
            message = NotificationMessage.objects.get(slug=slug)
            send_notification.delay(slug=message.slug, template_context=dict_template)
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
