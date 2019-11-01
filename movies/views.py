from django.shortcuts import render, get_object_or_404
from .models import Movie, Review, Genre
from .serializers import MovieSerializers, GenreSerializers, GenreDetailSerializers, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
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