from rest_framework import serializers
from todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "created_at",
            "updated_at",
            "status",
            "created_by",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):

        return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update the instance with the provided data
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.completed = validated_data.get("completed", instance.completed)
        instance.status = validated_data.get("status", instance.status)
        instance.created_by = validated_data.get("created_by", instance.created_by)
        instance.save()
        return instance
