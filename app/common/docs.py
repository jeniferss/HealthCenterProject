from drf_yasg import openapi

bad_request_response = openapi.Response(
    description="Bad Request",
    examples={
        "application/json": {
            "error": "Invalid data",
            "details": "Explanation of the validation error",
        }
    },
)


not_found_response = openapi.Response(
    description="Not Found",
    examples={
        "application/json": {"detail": "Not found."},
    },
)

no_content_response = openapi.Response(
    description="No Content",
    examples={
        "application/json": {},
    },
)


def paginated_response(serializer):
    return openapi.Response(
        description="Paginated response",
        examples={
            "application/json": {
                "count": 10,
                "next": "http://example.com/endpoint/?page=2",
                "previous": None,
                "results": [serializer().data],
            },
        },
    )
