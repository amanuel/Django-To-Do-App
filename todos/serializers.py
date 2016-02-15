from rest_framework import serializers

from todos.models import Todo, TodoList


class FilterRelatedMixin(object):
    """
    DRF doesn't properly filter related fields under some situations.

    This Mixin provides ability to do additional filtering in a serializer
    by defining a method filter_<fieldname> in a serializer.

    see https://github.com/tomchristie/django-rest-framework/issues/1985
    """

    def __init__(self, *args, **kwargs):
        super(FilterRelatedMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.iteritems():
            if isinstance(field, serializers.RelatedField):
                method_name = 'filter_%s' % name
                try:
                    func = getattr(self, method_name)
                except AttributeError:
                    pass
                else:
                    field.queryset = func(field.queryset)


class UserFilteredModelSerializer(FilterRelatedMixin, serializers.ModelSerializer):

    def filter_user(self, queryset):
        # Restrict user to only see/select themselves in DRF pages unless they are staff
        request = self.context.get('request')
        if request:
            user = request.user
            return queryset if user.is_staff else queryset.filter(pk=user.id)


class TodoSerializer(UserFilteredModelSerializer):

    def filter_todolist(self, queryset):
        # Restrict user to only see their todo lists unless they are staff
        request = self.context.get('request')
        if request:
            user = request.user
            return queryset if user.is_staff else queryset.filter(user=request.user)

    class Meta:
        model = Todo


class TodoListSerializer(UserFilteredModelSerializer):
    todo_items = TodoSerializer(read_only=True, many=True)

    class Meta:
        model = TodoList
