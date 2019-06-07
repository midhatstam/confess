from django.shortcuts import render
from core.models import Confess, Comment, ItemMetaData
from core.serializers import ConfessSerializer,CommentSerializer,ItemMetaDataSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView


class ConfessView(APIView):
	def get(self, request, format=None):
		confesses = Confess.objects.all()
		serializer = ConfessSerializer(confesses, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = ConfessSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)


# class ConfessView(viewsets.ModelViewSet):
# 	serializer_class = ConfessSerializer
# 	detail_serializer_class = ItemMetaDataSerializer
# 	queryset = Confess.objects.all()
