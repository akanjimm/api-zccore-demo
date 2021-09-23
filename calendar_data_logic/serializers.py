
from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    topic = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    time_zone = serializers.CharField()
    description = serializers.CharField()
    event_tag = serializers.CharField()
    availability = serializers.BooleanField()
    visibility = serializers.CharField()

    def update(self, instance, validated_data):
        for data in validated_data:
            instance[data] = validated_data[data]

        return self.instance
