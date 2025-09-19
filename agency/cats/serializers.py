from cats.models import SpyCat
from rest_framework import serializers


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'experience', 'breed', 'salary']
        read_only_fields = ['id']


class SpyCatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['salary']
