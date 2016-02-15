from django.contrib import admin

from todos.models import Todo, TodoList


class TodoListAdmin(admin.ModelAdmin):
    list_display = ['order', 'name', 'user', 'done']
    list_editable = ['order']
    search_fields = ['name']
    filter_horizontal = []
    ordering = ['order']


class TodoAdmin(admin.ModelAdmin):
    list_display = ['order', 'name', 'done', 'todolist', 'user']
    list_editable = ['order']
    list_filter = ['todolist__name', 'done']
    search_fields = ['name', 'todolist__name']
    ordering = ['order']
    filter_horizontal = []

admin.site.register(Todo, TodoAdmin)
admin.site.register(TodoList, TodoListAdmin)
