from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.posts_list, name='posts_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.get_post, name='get_post'
         )
]