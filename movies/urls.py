from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Movie API",
#       default_version='v1',
#       description="Movie, Genre 정보",
#    ),
# )

app_name = 'movies'
urlpatterns = [
    path('movies/', views.movie_index, name='index'),
    path('movies/<int:movie_pk>/', views.movie_detail, name='detail'),
    path('genres/', views.genre_index, name='index'),
    path('genres/<int:genre_pk>/', views.genre_detail, name='detail'),
    path('movies/<int:movie_pk>/reviews/', views.review, name='review'),
    path('reviews/<int:review_pk>/', views.review_update_delete,name='update_delete'),

]
