from django.urls import path
from .views import (main_view, user_search_view, make_post_view, myprofile_view, make_post_view
                    ,login_view
                    ,logout_view
                    ,follow_toggle_view
                    ,othersprofile_view
                    ,like_toggle_view
                    ,post_delete_view
                    ,post_edit_view
                    ,comment_create_view
                    ,comment_delete_view
                    ,story_create_view
                    ,story_list_view
                    ,story_detail_view
                    )

app_name = "instagram"

urlpatterns = [
    path("", main_view, name="main"), 
    
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"), 
    
    path("users/search/", user_search_view, name="user_search"),
    path("posts/new/", make_post_view, name="make_post"),
    path("me/", myprofile_view, name="myprofile"),
    path("users/<int:user_id>/", othersprofile_view, name="othersprofile"),
    path("users/<int:user_id>/follow/", follow_toggle_view, name="follow_toggle"),
    path("posts/<int:post_id>/like/", like_toggle_view, name="like_toggle"),
    path("posts/<int:post_id>/edit/", post_edit_view, name="post_edit"),
    path("posts/<int:post_id>/delete/", post_delete_view, name="post_delete"),
    path("posts/<int:post_id>/comments/", comment_create_view, name="comment_create"),
    path("comments/<int:comment_id>/delete/", comment_delete_view, name="comment_delete"),
    path("stories/create/", story_create_view, name="story_create"),
    path("stories/list/", story_list_view, name="story_list"),
    path("stories/<int:user_id>/", story_detail_view, name="story_detail"),
]
