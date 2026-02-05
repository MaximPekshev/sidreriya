from rest_framework import serializers

class PinSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    type = serializers.ChoiceField(choices=['sms', 'email'])