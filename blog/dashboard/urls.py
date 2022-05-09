from  django.urls import path

from dashboard import views

app_name='dashboard'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/post/', views.PostView.as_view(), name='post'),
    path('<int:post_id>/<int:parent_comment_id>/comment/', views.CommentView, name='comment'),
    path('<int:post_id>/<int:comment_id>/<int:islike>/reaction/', views.ReactionView, name="reaction"),
]