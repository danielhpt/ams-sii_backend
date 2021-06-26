from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response, status

from .models import *
from .serializers import *


# API
