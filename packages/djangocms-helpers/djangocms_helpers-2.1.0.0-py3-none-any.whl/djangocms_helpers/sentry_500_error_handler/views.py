from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.shortcuts import render
from sentry_sdk import last_event_id


# noinspection PyUnusedLocal
def collect_500_error_user_feedback_view(request: HttpRequest, *args, **argv) -> HttpResponseServerError:
    return render(
        request,
        template_name='error_handler/500.html',
        context={'sentry_event_id': last_event_id()},
        status=500,
    )


# noinspection PyUnusedLocal
def not_found_404_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(
        request,
        template_name='error_handler/404.html',
        status=404,
    )
