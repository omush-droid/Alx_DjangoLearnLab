from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    target_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_type', 'timestamp', 'read']
        read_only_fields = ['id', 'actor', 'verb', 'target_type', 'timestamp']

    def get_target_type(self, obj):
        return obj.target_content_type.model