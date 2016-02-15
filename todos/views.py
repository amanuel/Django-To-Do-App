from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from todos.serializers import TodoSerializer, TodoListSerializer
from todos.models import Todo, TodoList


class TodosViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('order')
    serializer_class = TodoSerializer
    filter_fields = ('deleted', 'done')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            if not self.request.query_params.get('show_all'):
                queryset = queryset.filter(deleted=False)

        # Show only todo items that belong to user
        if self.request.user.is_staff:
            queryset = queryset.order_by('order')
        else:
            user = self.request.user
            queryset = queryset.filter(user=user).order_by('order')

        return queryset


class TodoListsViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Show only todo lists that belong to user unless they are staff
        if self.request.user.is_staff:
            return TodoList.objects.all().order_by('order')
        else:
            user = self.request.user
            return user.todolist_set.all().order_by('order')
