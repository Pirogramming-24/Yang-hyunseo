from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "myIdeas" #URL namespace를 지정

urlpatterns = [
        path("idea/<int:pk>/star/", views.toggle_star, name="toggle_star"),
        path("idea/<int:pk>/interest/", views.update_interest, name="update_interest"),

	path('', views.ideas_list, name='ideas_list'),
        path("<int:pk>", views.ideas_read, name="ideas_read"),
        path("create/", views.ideas_create, name="ideas_create"),
        path("<int:pk>/update/", views.ideas_update, name="update"),
        path("<int:pk>/delete/", views.ideas_delete, name="delete"),
        
        path('devtool', views.devtool_list, name="devtool_list"),
        path("devtool_create", views.devtool_create, name="devtool_create"),
        path("devtool_read/<int:pk>/", views.devtool_read, name="devtool_read"),
        #devtool_update
        path("<int:pk>/devtool_update/", views.devtool_update, name="devtool_update"),
        #devtool_delete
        path("<int:pk>/devtool_delete/", views.devtool_delete, name="devtool_delete"),
        
]
