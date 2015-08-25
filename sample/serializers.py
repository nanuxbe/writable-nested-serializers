from rest_framework import serializers

from restframework_writable_nested.serializers import EmbeddedListSerializer
from restframework_writable_nested.mixins import (
    WithEmbeddedRecordsSerializerMixin,
    EmbeddedRecordSerializerMixin
)

from .models import Pet, Human


class PetSerializer(EmbeddedRecordSerializerMixin, serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(
        queryset=Human.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Pet
        fields = (
            'id',
            'name',
            'owner',
        )
        list_serializer_class = EmbeddedListSerializer


class HumanSerializer(WithEmbeddedRecordsSerializerMixin, serializers.ModelSerializer):

    pets = PetSerializer(many=True)

    class Meta:
        model = Human
        fields = (
            'id',
            'name',
            'pets'
        )
