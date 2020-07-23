from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.parsers import JSONParser

from .models import Posts
from rest_framework import status
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class PostRegistrationView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)


class GetRegistrationView(RetrieveAPIView):
    def get(self, request, pk):
        post = Posts.objects.all()
        serializer = PostSerializer(post, many=True)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'data': {
                'data': serializer.data
            },
            'message': 'Retrived Successsfully ',
        }
        return Response(response, status=status_code)

    def put(self, request, pk):
        post = Posts.objects.get(id=pk)
        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status': status_code,
                'message': 'Updated Successfully ',
            }
            return Response(response, status=status_code)
        else:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                'success': 'False',
                'status': status_code,
                'message': 'Error',
            }
            return Response(response, status=status_code)

    def delete(self, request, pk):
        post = Posts.objects.get(id=pk)
        post.delete()
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status': status_code,
            'message': 'Deleted Successfully ',
        }
        return Response(response, status=status_code)



