from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import ApiAccessKey, ApiKeyUsageLog
from rest_framework.request import Request
from django.urls import resolve

class ApiUsageLoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # We only want to log if the request was successfully authenticated with an API key
        # and if the status code is not an authentication error (401, 403)
        if (
            hasattr(request, 'auth')
            and isinstance(request.auth, ApiAccessKey)
            and response.status_code not in [401, 403]
        ):
            try:
                api_key = request.auth
                user = api_key.user

                # Update last_used timestamp on the API key
                api_key.last_used = timezone.now()
                api_key.save(update_fields=['last_used'])

                # Attempt to get the view name or URL pattern name
                # Default to request.path if resolution fails
                request_path = request.path
                try:
                    match = resolve(request.path_info)
                    if match.view_name:
                        request_path = match.view_name
                    elif match.url_name:
                         request_path = match.url_name
                except Exception:
                    pass # Ignore resolution errors

                # Create usage log entry
                ApiKeyUsageLog.objects.create(
                    api_key=api_key,
                    user=user,
                    request_path=request_path,
                    query_params=dict(request.query_params) if isinstance(request, Request) else None,
                    response_format=getattr(response, 'accepted_media_type', '').split('/')[-1] or 'unknown',
                    status_code=response.status_code,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            except Exception as e:
                # Log the error but don't prevent the response from being returned
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error logging API key usage in middleware: {str(e)}")

        return response 