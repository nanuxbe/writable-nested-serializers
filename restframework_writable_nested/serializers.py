from __future__ import unicode_literals
import inspect

from rest_framework.serializers import ListSerializer
from rest_framework.exceptions import ValidationError


class EmbeddedListSerializer(ListSerializer):
    update_lookup_field = 'id'

    def update(self, queryset, all_validated_data):
        id_attr = getattr(self.child.Meta, 'update_lookup_field', 'id')

        updatable_validated_data_by_id = {}
        to_add_validated_data = []
        for i in all_validated_data:
            id = i.pop(id_attr)
            if bool(id) and not inspect.isclass(id):
                updatable_validated_data_by_id[id] = i
            else:
                to_add_validated_data.append(i)

        # since this method is given a queryset which can have many
        # model instances, first find all objects to update
        # and only then update the models
        objects_to_update = queryset.filter(**{
            '{}__in'.format(id_attr): updatable_validated_data_by_id.keys(),
        })

        if len(updatable_validated_data_by_id) != objects_to_update.count():
            raise ValidationError('Could not find all objects to update.')

        updated_objects = []

        for obj in objects_to_update:
            obj_id = getattr(obj, id_attr)
            obj_validated_data = updatable_validated_data_by_id.get(obj_id)

            if obj_validated_data is None:
                obj_validated_data = updatable_validated_data_by_id.get(str(obj_id))

            # use model serializer to actually update the model
            # in case that method is overwritten
            updated_objects.append(self.child.update(obj, obj_validated_data))

        for data in to_add_validated_data:
            updated_objects.append(self.child.create(data))

        return updated_objects
