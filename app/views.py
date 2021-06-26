from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response, status

from .models import *
from .serializers import *


# API
class UserList(APIView):
    """List all Users"""

    def get(self, request):
        users = User.objects.all()
        serializer = UserSimplifiedSerializer(users, many=True)

        return Response(serializer.data)

class TeamList(APIView):
    """List all Teams"""

    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamDetailsSerializer(teams, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = TeamDetailsSerializer(data=request.data.copy())

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
