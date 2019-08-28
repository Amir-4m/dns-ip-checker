from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from notifier.tasks import send_notification
from .serializers import NotifierSerializer


class NotifierApiView(APIView):

    def post(self, request):
        serializer = NotifierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            send_notification.delay(serializer.validated_data['slug'], serializer.validated_data['template'])
        except Exception as e:
            raise ValidationError(dict(sent=False, error=str(e)))

        return Response(dict(sent=True))
