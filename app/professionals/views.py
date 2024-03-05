from django.shortcuts import get_object_or_404
from rest_framework import status, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from app.professionals.models import Professional, ProfessionalSerializer
from app.common.docs import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


param = openapi.Parameter(
    "professional_id",
    openapi.IN_PATH,
    description="id of the professional you want to search, update or delete.",
    type=openapi.TYPE_INTEGER,
    required=True,
)

professional_detail_response = openapi.Response(
    "details for the required professional", ProfessionalSerializer
)


class ProfessionalView(APIView):
    permission_classes = [IsAuthenticated]

    pagination_class = pagination.PageNumberPagination

    @swagger_auto_schema(
        responses={
            200: paginated_response(ProfessionalSerializer),
        },
    )
    def get(self, request):
        paginator = self.pagination_class()

        professionals = Professional.objects.all().order_by("id")
        results = paginator.paginate_queryset(professionals, request)
        serializer = ProfessionalSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=ProfessionalSerializer,
        responses={
            200: professional_detail_response,
            400: bad_request_response,
        },
    )
    def post(self, request):
        serializer = ProfessionalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessionalDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[param],
        responses={
            200: professional_detail_response,
            404: not_found_response,
        },
    )
    def get(self, request, professional_id: int):
        professional = get_object_or_404(Professional, id=professional_id)
        serializer = ProfessionalSerializer(professional)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProfessionalSerializer,
        manual_parameters=[param],
        responses={
            200: professional_detail_response,
            400: bad_request_response,
            404: not_found_response,
        },
    )
    def put(self, request, professional_id: int):
        professional = get_object_or_404(Professional, id=professional_id)
        serializer = ProfessionalSerializer(
            professional, data=request.data, partial=True
        )

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
    def delete(self, request, professional_id: int):
        professional = get_object_or_404(Professional, id=professional_id)
        professional.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
