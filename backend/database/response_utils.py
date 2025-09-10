from rest_framework import status
from rest_framework.response import Response
from typing import Any, Dict, Optional, List

class APIResponse:
    """
    Simple utility class for standardized API responses
    """
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK) -> Response:
        """Create a success response"""
        return Response({
            "success": True,
            "message": message,
            "data": data,
            "status_code": status_code
        }, status=status_code)
    
    @staticmethod
    def error(message: str = "An error occurred", status_code: int = status.HTTP_400_BAD_REQUEST, errors: Optional[Dict] = None) -> Response:
        """Create an error response"""
        response_data = {
            "success": False,
            "message": message,
            "status_code": status_code
        }
        if errors:
            response_data["errors"] = errors
        return Response(response_data, status=status_code)
    
    @staticmethod
    def paginated(data: List, page: int, page_size: int, total_count: int, message: str = "Success") -> Response:
        """Create a paginated response"""
        total_pages = (total_count + page_size - 1) // page_size
        return Response({
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            },
            "status_code": 200
        })
