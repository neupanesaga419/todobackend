from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from todos.models import Todo
from todos.serializers import TodoSerializer
from todos.todo_parser import parse_todos


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)

    def get_queryset(self):

        return self.queryset.filter(created_by=self.request.user)

    @action(detail=False, methods=["POST"])
    def bulk_import_todos(self, request, *args, **kwargs):
        try:
            todo_file = request.FILES.get("todo_file")
            if not todo_file:
                return Response({"error": "Please provide a file"}, status=400)
            todos_to_create = parse_todos(todo_file, self.request.user)
            if not todos_to_create:
                return Response({"message": "No todos found in the file"}, status=400)
            serializer = TodoSerializer(data=todos_to_create, many=True)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": f"{len(todos_to_create)} todos created successfully"},
                status=201,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)
