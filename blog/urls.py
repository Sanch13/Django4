from django.urls import path

from blog import views

app_name = "blog"


urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", views.PostListView.as_view(), name="post_list_by_tag"),
    # path("", views.post_list, name="post_list"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    # path("<slug:slug>/", views.post_detail, name="post_detail"),
    path('<slug:slug>/share/', views.post_share, name='post_share'),
    path('<slug:slug>/comment/', views.post_comment, name='post_comment'),
]
