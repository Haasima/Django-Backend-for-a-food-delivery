from collections.abc import Callable
from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponseForbidden
from django.middleware.csrf import CsrfViewMiddleware


class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_view(self, request: HttpRequest, callback: Callable[..., Any] | None, callback_args: tuple[Any, ...], callback_kwargs: dict[str, Any]) -> HttpResponseForbidden | None:
        if "HTTP_X_CSRFTOKEN" not in request.META:
            csrf_token = request.COOKIES.get('csrftoken')
            if csrf_token:
                request.CSRF_COOKIE = csrf_token
                request.META['HTTP_X_CSRFTOKEN'] = csrf_token
        return super().process_view(request, callback, callback_args, callback_kwargs)