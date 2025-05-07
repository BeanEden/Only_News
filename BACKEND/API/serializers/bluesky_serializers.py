from rest_framework import serializers

class BlueSkyPostSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=255)
    content = serializers.CharField()
    timestamp = serializers.DateTimeField()
    uri = serializers.CharField()

class BlueSkyPostDetailSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=255)
    content = serializers.CharField()
    timestamp = serializers.DateTimeField()
    uri = serializers.CharField()
    additional_data = serializers.DictField(child=serializers.CharField())

class BlueSkyFeedGeneratorSerializer(serializers.Serializer):
    creator = serializers.CharField()
    display_name = serializers.CharField()
    avatar = serializers.URLField()
    like_count = serializers.IntegerField()
