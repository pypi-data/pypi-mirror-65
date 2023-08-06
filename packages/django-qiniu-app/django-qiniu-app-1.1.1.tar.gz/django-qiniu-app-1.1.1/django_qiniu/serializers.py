from rest_framework import serializers
from django_qiniu import models


class ResourceShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Resource
        fields = ["id", "key", "bucket", "url", "duration"]
