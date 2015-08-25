from __future__ import unicode_literals

from django.db.models import Manager

from rest_framework.utils import model_meta


class WithEmbeddedRecordsSerializerMixin(object):

    def create(self, validated_data):
        ModelClass = self.Meta.model

        # Remove to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass.objects.create(**validated_data)
        except TypeError as exc:
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception text was: %s.' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    exc
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if to_many:
            for field_name, value in to_many.items():
                related_field = getattr(instance, field_name)
                for record in value:
                    related_field.create(**record)

        return instance

    def update(self, instance, validated_data):
        embedded = []
        for attr, value in validated_data.items():
            attr_inst = getattr(instance, attr)
            if isinstance(attr_inst, Manager):
                embedded.append(attr)
            else:
                setattr(instance, attr, value)
        instance.save()

        fields = self.get_fields()
        for field in embedded:
            serializer = fields[field]
            assert hasattr(serializer.child, 'Meta'), (
                'Class {serializer_class} missing "Meta" attribute'.format(
                    serializer_class=serializer.child.__class__.__name__
                )
            )
            assert hasattr(serializer.child.Meta, 'model'), (
                'Class {serializer_class} missing "Meta.model" attribute'.format(
                    serializer_class=serializer.child.__class__.__name__
                )
            )
            queryset = serializer.child.Meta.model.objects.all()
            updated = serializer.update(queryset, validated_data[field])

            request_method = getattr(getattr(self.context.get('view'), 'request'), 'method', '')
            if request_method == 'PUT':
                related_manager = getattr(instance, field)
                related_id = serializer.child.Meta.model()._meta.pk.name

                to_delete = related_manager.exclude(**{
                    '{}__in'.format(related_id): [
                        getattr(record, related_id) for record in updated
                    ],
                })

                to_delete.delete()

        return instance


class EmbeddedRecordSerializerMixin(object):

    def to_internal_value(self, data):
        ret = super(EmbeddedRecordSerializerMixin, self).to_internal_value(data)

        id_attr = getattr(self.Meta, 'update_lookup_field', 'id')
        request_method = getattr(getattr(self.context.get('view'), 'request'), 'method', '')

        # add update_lookup_field field back to validated data
        # since super by default strips out read-only fields
        # hence id will no longer be present in validated_data
        if all((isinstance(self.root, WithEmbeddedRecordsSerializerMixin),
                id_attr,
                request_method in ('PUT', 'PATCH'))):
            id_field = self.fields[id_attr]
            id_value = id_field.get_value(data)
            if id_value:
                ret[id_attr] = id_value

        return ret
