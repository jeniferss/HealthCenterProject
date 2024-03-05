from django.shortcuts import get_object_or_404
from rest_framework import status, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from app.appointments.models import Appointment, AppointmentSerializer
from app.common.docs import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


param = openapi.Parameter(
    "appointment_id",
    openapi.IN_PATH,
    description="id of the appointment you want to search, update or delete.",
    type=openapi.TYPE_INTEGER,
)

param_professional = openapi.Parameter(
    "professional_id",
    openapi.IN_QUERY,
    description="id of the professional you want to search appointments for.",
    type=openapi.TYPE_INTEGER,
    required=False,
)

appointment_detail_response = openapi.Response(
    "details for the required appointment", AppointmentSerializer
)


class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    pagination_class = pagination.PageNumberPagination

    @swagger_auto_schema(
        manual_parameters=[param_professional],
        responses={
            200: paginated_response(AppointmentSerializer),
        },
    )
    def get(self, request):
        paginator = self.pagination_class()
        professional_id = request.query_params.get("professional_id")

        if professional_id:
            appointments = (
                Appointment.objects.filter(professional_id=professional_id)
                .all()
                .order_by("id")
            )
        else:
            appointments = Appointment.objects.all().order_by("id")

        results = paginator.paginate_queryset(appointments, request)
        serializer = AppointmentSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=AppointmentSerializer,
        responses={
            200: appointment_detail_response,
            400: bad_request_response,
        },
    )
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[param],
        responses={
            200: appointment_detail_response,
            404: not_found_response,
        },
    )
    def get(self, request, appointment_id: int = None):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[param],
        request_body=AppointmentSerializer,
        responses={
            200: appointment_detail_response,
            400: bad_request_response,
            404: not_found_response,
        },
    )
    def put(self, request, appointment_id: int):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[param],
        responses={
            204: no_content_response,
            404: not_found_response,
        },
    )
    def delete(self, request, appointment_id: int):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
