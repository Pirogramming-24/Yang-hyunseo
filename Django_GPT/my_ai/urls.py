from django.urls import path
from .views import main_view, translate_view, sentiment_view, generate_view, login_view, signup_view, logout_view, run_ai_view

urlpatterns = [
    path("", main_view, name="main"),
    path("translate/", translate_view, name="translate"),
    path("sentiment/", sentiment_view, name="sentiment"),
    path("generate/", generate_view, name="generate"),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    
    path("api/<str:model_type>/", run_ai_view, name="run_ai"),
]