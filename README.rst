=====
Todos
=====

Todos is a simple Django backend app to power a Singe Page ToDo WebApp

Requirements
-----------
	Django Rest Framework v3.3 or greater

Quick start
-----------

1. Add "Todo" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'todos',
    ]

2. Include the todos URLconf in your project urls.py like this::

	from rest_framework import routers
	
	from todos.views import TodoListsViewSet, TodosViewSet

	router = routers.DefaultRouter()
	router.register(r'todo', TodosViewSet)
	router.register(r'todolist', TodoListsViewSet)


3. Run `python manage.py migrate` to create the todos models.

PS: You can use DRF views or Django admin to CRUD objects