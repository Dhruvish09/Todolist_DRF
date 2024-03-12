from django.contrib import admin
from restapp.models import ToDoItem
# Register your models here.


@admin.register(ToDoItem)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description' , 'created_date']
    ordering = ['id']
