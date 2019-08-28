import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from notifier.tasks import send_notification
from .serializers import NotifierSerializer


class NotifierApiView(APIView):

    def post(self, request):
        serializer = NotifierSerializer(request.POST).data

        try:
            send_notification.delay(serializer.get('slug'), serializer.get('template'))
        except Exception as e:
            raise ValidationError(dict(sent=False, error=str(e)))

        return Response(dict(sent=True))
