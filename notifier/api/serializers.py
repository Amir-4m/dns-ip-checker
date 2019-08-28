from rest_framework import serializers
from notifier.models import NotificationMessage, NotificationRoute
from tel_tools.models import TelegramBot, TelegramChannel


class NotifierSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    template = serializers.JSONField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def save(self, **kwargs):
        pass


class TelegramBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramBot
        fields = "__all__"


class TelegramChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramChannel
        fields = "__all__"


class NotificationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationMessage
        fields = "__all__"


class NotificationRouteSerializer(serializers.ModelSerializer):
    channel = TelegramChannelSerializer()
    message = NotificationMessageSerializer()
    bot = TelegramBotSerializer()

    class Meta:
        model = NotificationRoute
        fields = "__all__"
