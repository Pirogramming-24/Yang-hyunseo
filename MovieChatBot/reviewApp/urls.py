from django.urls import path
from . import views
from . import forms
from reviewApp.views import ask, ping
from django.views.generic import TemplateView

app_name = "reviewApp"

urlpatterns = [
	    # path('', views.hello_world, name='hello'),
        path('', views.reviews_list, name="reviews_list"),
        path("<int:pk>/", views.reviews_read, name="read"),
        path("create/", views.reviews_create, name="create"),
        path("<int:pk>/update/", views.reviews_update, name="update"),
        path("<int:pk>/delete/", views.reviews_delete, name="delete"),
        path("ask", ask, name="ask"),
        path("ping", ping),
        path("chatbot/", TemplateView.as_view(template_name="reviews_chatbot.html"), name="chatbot"),
]