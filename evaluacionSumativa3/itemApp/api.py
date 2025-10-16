from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .models import Reserva
from .serializers import ReservaSerializer

class ReservaListCreate(APIView):
    def get(self, request):
        qs = Reserva.objects.all().order_by("-fecha", "-hora")
        return Response(ReservaSerializer(qs, many=True).data)

    def post(self, request):
        ser = ReservaSerializer(data=request.data)
        if ser.is_valid():
            try:
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"mesa": ["Esta mesa ya está reservada en esa fecha y hora."]},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservaDetail(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Reserva, pk=pk)
        return Response(ReservaSerializer(obj).data)

    def put(self, request, pk):
        obj = get_object_or_404(Reserva, pk=pk)
        ser = ReservaSerializer(obj, data=request.data)
        if ser.is_valid():
            try:
                ser.save()
                return Response(ser.data)
            except IntegrityError:
                return Response({"mesa": ["Esta mesa ya está reservada en esa fecha y hora."]},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Reserva, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
