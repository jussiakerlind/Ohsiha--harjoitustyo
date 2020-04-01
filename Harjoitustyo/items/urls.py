from django.urls import path
from .views import list_items, create_item, update_item, delete_item

urlpatterns = [
    path('', list_items, name='list_items'),
    path('new', create_item, name='create_items'),
    path('update/<int:id>', update_item, name='update_item'),
    path('delete/<int:id>', delete_item, name='delete_item')
]