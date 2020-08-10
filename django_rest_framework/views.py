import jwt
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.parsers import JSONParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Posts, BlackListedToken
from rest_framework import status
from .serializers import PostSerializer, UserLoginSerializer, UserLogoutSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user_id =request.user.id
        token = request.auth.decode("utf-8")
        is_allowed_user = True
        try:
            token_blocked = BlackListedToken.objects.filter(user_id=user_id, token=token)
            if token_blocked:
                is_allowed_user = False
        except token_blocked.DoesNotExist:
            is_allowed_user = True
        return  is_allowed_user


class PostRegistrationView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_class = JSONWebTokenAuthentication

    serializer_class = PostSerializer

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
    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_class = JSONWebTokenAuthentication

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


class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'sucsess': 'True',
            'status_code': status.HTTP_200_OK,
            'message': 'User Loged In Successfully',
            'token': serializer.data['token'],
        }
        return Response(response, status=status.HTTP_200_OK)


class getDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        user_profile = User.objects.get(id=request.user.id)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'true',
            'status code': status_code,
            'message': 'User profile fetched successfully',
            'data': [{
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'email': user_profile.email,
            }]
        }

        return Response(response, status=status_code)


class getTokenDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        data = jwt.decode(request.auth,None,None)
        return Response({'response':data}, status=status.HTTP_200_OK)


class logOut(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = UserLogoutSerializer

    def post(self, request):
        request.data['user_id'] = request.user.id
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status':status.HTTP_200_OK,
                'message': 'logout successfully'
            }

            return Response(response, status.HTTP_200_OK)
        else:
            response = {
                'status': status.HTTP_403_FORBIDDEN,
                'message': 'Error'
            }

            return Response(response, status.HTTP_403_FORBIDDEN)



