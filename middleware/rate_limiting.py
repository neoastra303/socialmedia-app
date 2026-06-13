"""
Rate limiting utilities with improved error handling
"""
from django.http import JsonResponse
from django_ratelimit.core import is_ratelimited
from django_ratelimit.decorators import ratelimit
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


def custom_ratelimit(key=None, rate='5/m', method='POST', block=False):
    """
    Custom rate limiting decorator with improved error handling
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Use django-ratelimit to check rate limits
            was_limited = is_ratelimited(
                request=request,
                fn=view_func,  # Add the required view function parameter
                key=key,
                rate=rate,
                method=method,
                increment=True
            )
            
            if was_limited:
                if block:
                    # Return JSON response for API calls or regular response for web requests
                    ip = request.META.get('REMOTE_ADDR', 'unknown')
                    user = getattr(request, 'user', None)
                    identifier = str(user) if user and user.is_authenticated else ip
                    if hasattr(request, 'META') and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or \
                       request.content_type == 'application/json' or \
                       'application/json' in request.META.get('HTTP_ACCEPT', ''):
                        logger.warning(f"Rate limit exceeded for {key}: {identifier}")
                        return JsonResponse({
                            'error': 'Rate limit exceeded',
                            'message': f'You have exceeded the rate limit of {rate}. Please try again later.',
                            'retry_after': '60'
                        }, status=429)
                    else:
                        logger.warning(f"Rate limit exceeded for {key}: {identifier}")
                        return render(request, 'errors/rate_limit.html', {
                            'rate_limit': rate,
                            'retry_after': '60 seconds'
                        }, status=429)
                else:
                    ip = request.META.get('REMOTE_ADDR', 'unknown')
                    user = getattr(request, 'user', None)
                    identifier = str(user) if user and user.is_authenticated else ip
                    logger.info(f"Rate limit hit (not blocking) for {key}: {identifier}")
            
            # Call the original view function
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


# Create specific rate limiting decorators with better error handling
def user_ratelimit(view_func):
    """Rate limiting by user with improved error handling"""
    return custom_ratelimit(key='user', rate='5/m', method='POST', block=True)(view_func)


def ip_ratelimit(view_func):
    """Rate limiting by IP with improved error handling"""
    return custom_ratelimit(key='ip', rate='10/m', method='POST', block=True)(view_func)


def post_creation_ratelimit(view_func):
    """Rate limiting for post creation with custom settings"""
    return custom_ratelimit(key='user', rate='3/m', method='POST', block=True)(view_func)