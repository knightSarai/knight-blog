from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.posts_list, name='posts_list'),
    path('tag/<slug:tag_slug>/', views.posts_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='posts_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.get_post, name='get_post'
         ),
    path('<int:post_id>/share/', views.post_share, name='share_post'),
    path('search/', views.post_search, name='post_search')
]
