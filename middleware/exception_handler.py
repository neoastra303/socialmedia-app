import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.conf import settings
from django.contrib import messages

logger = logging.getLogger(__name__)


def is_ajax_request(req):
    return req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or \
           'application/json' in req.META.get('HTTP_ACCEPT', '') or \
           req.content_type == 'application/json'


class GlobalExceptionHandlerMiddleware:
    """
    Global exception handling middleware that catches common errors and 
    handles them gracefully, providing appropriate responses for both
    AJAX and regular requests.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Process exceptions that occur during request handling
        """
        # Log the exception
        logger.error(
            f"Exception occurred: {type(exception).__name__}: {str(exception)}",
            extra={
                'request': request,
                'user': request.user,
                'path': request.path,
                'method': request.method,
            },
            exc_info=True
        )
        
        # Handle different types of exceptions
        if isinstance(exception, Http404):
            if is_ajax_request(request):
                return JsonResponse({
                    'error': 'Resource not found',
                    'message': 'The requested resource could not be found.'
                }, status=404)
            else:
                return render(request, 'errors/404.html', status=404)
        
        elif isinstance(exception, PermissionDenied):
            if is_ajax_request(request):
                return JsonResponse({
                    'error': 'Permission denied',
                    'message': 'You do not have permission to access this resource.'
                }, status=403)
            else:
                return render(request, 'errors/403.html', status=403)
        
        elif isinstance(exception, ValueError):
            if is_ajax_request(request):
                return JsonResponse({
                    'error': 'Invalid value',
                    'message': 'The provided value is invalid.'
                }, status=400)
            else:
                messages.error(request, 'Invalid value provided.')
                return render(request, 'errors/400.html', status=400)
        
        # Handle all other exceptions
        if is_ajax_request(request):
            return JsonResponse({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred.'
            }, status=500)
        else:
            return render(request, 'errors/500.html', status=500)


class ValidationMiddleware:
    """
    Middleware to add validation for common request aspects
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Max upload size: 100MB for posts (to accommodate videos)
        self.max_upload_size = 100 * 1024 * 1024  # 100MB

    def __call__(self, request):
        # Validate upload size
        if request.method in ['POST', 'PUT', 'PATCH'] and request.FILES:
            total_size = sum(file.size for file in request.FILES.values())
            if total_size > self.max_upload_size:
                if is_ajax_request(request) or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                    return JsonResponse({
                        'error': 'File too large',
                        'message': f'Uploaded files exceed maximum size of {self.max_upload_size / (1024*1024)}MB.'
                    }, status=400)
                else:
                    messages.error(request, f'Uploaded files exceed maximum size of {self.max_upload_size / (1024*1024)}MB.')
                    from django.http import HttpResponseBadRequest
                    return HttpResponseBadRequest("File too large")
        
        response = self.get_response(request)
        return response