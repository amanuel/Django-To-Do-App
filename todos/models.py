from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.timezone import now


class TodoList(models.Model):
    """model for todo list."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False)
    order = models.PositiveIntegerField(editable=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order = self.order or int(getattr(TodoList.objects.last(), 'id', 0)) + 1
        super(TodoList, self).save(*args, **kwargs)

    @property
    def done(self):
        return self.todo_items.filter(done=False).count() == 0

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Todo Lists'

    def __str__(self):
        return self.name


class Todo(models.Model):
    """model for todo items."""

    name = models.CharField(max_length=255)
    todolist = models.ForeignKey(TodoList, blank=False, related_name='todo_items')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False)
    order = models.PositiveIntegerField(editable=True, blank=True, null=True)
    done = models.BooleanField('Done', default=False)
    done_date = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField('Deleted', default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order = self.order or int(getattr(Todo.objects.last(), 'id', 0)) + 1
        self.done_date = self.done_date or now() if self.done else None
        super(Todo, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Todo Items'
