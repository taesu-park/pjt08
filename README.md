# 08 - REST API

## 1. 목표

* API 요청에 대한 이해
* RESTful API 서버 구축
* API 문서화

## 2. 준비 사항

### 1. Python Web Framework

* Django 2.2.x
* Python 3.7.x

## 3. 요구 사항

### 1. 데이터베이스 설계

```python
from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=30)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=50)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):
    content = models.CharField(max_length=30)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

```

### 2. Seed Data 반영

```bash
$ python manage.py loaddata genre.json
Installed 11 object(s) from 1 fixture(s)
$ python manage.py loaddata movie.json
Installed 10 object(s) from 1 fixture(s)
```

### 3. `movies` API

```python
# urls.py

app_name = 'movies'
urlpatterns = [
    path('movies/', views.movie_index, name='index'),
    path('movies/<int:movie_pk>/', views.movie_detail, name='detail'),
    path('genres/', views.genre_index, name='index'),
    path('genres/<int:genre_pk>/', views.genre_detail, name='detail'),
    path('movies/<int:movie_pk>/reviews/', views.review, name='review'),
    path('reviews/<int:review_pk>/', views.review_update_delete,name='update_delete'),

]
```

```python
# views.py

@api_view(['GET']) # 허용된 HTTP 요청을 제외하고는 405 Method Not Allowed
def movie_index(request):
    '''
    영화 목록 정보
    '''
    movies = Movie.objects.all()
    serializer = MovieSerializers(movies,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genre_index(request):
    '''
    장르 목록 정보
    '''
    genres = Genre.objects.all()
    serializer = GenreSerializers(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk) 
    # 없는 경로 변수(pk)로 접근하는 경우 404 NOT Found
    serializer = MovieSerializers(movie)
    return Response(serializer.data)
    
@api_view(['GET'])
def genre_detail(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializer = GenreDetailSerializers(genre)
    return Response(serializer.data)

@api_view(['POST'])
def review(request, movie_pk):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # raise_exception : 예외처리, 필수 필드가 누락된 경우 400 Bad Request에러 응답.
        serializer.save(movie_id=movie_pk)
    return Response({'message':'작성되었습니다.'})

@api_view(['PUT','DELETE'])
def review_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method=='PUT':
        serializer = ReviewSerializer(data=request.data,instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'message':'수정되었습니다.'})
    else:
        review.delete()
        return Response({'message':'삭제되었습니다.'})
```





## 4. 느낀점

**내 코드가 비극인줄 알았는데, 코미디였다.**





