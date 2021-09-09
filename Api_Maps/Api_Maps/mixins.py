"""Django project Mixins."""

# Utilities
import datetime
import json
from urllib.parse import urlencode
import requests
from humanfriendly import format_timespan

# Django
from django.conf import settings
from django.http import JsonResponse, response
from django.shortcuts import redirect


def form_errors(*args):
    """Handles form error that are passed back to AJAX calls."""
    message = ''
    for i in args:
        if i.errors:
            message = i.errors.as_text()
    return message


def re_captcha_validation(token):
    """reCAPTCHA validation."""
    result = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token})  
    return result.json()


def redirect_params(**kwargs):
    """Used to append url parameters when redirecting users."""
    url = kwargs.get('url')
    params = kwargs.get('params')
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string
    return response


class AjaxFormMixin(object):
    """Mixin to ajaxify django form - can be over written in view by calling."""

    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            message = form_errors(form)
            return JsonResponse({'result': 'Error', 'message': message})
        return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            return JsonResponse({'result': 'Success', 'message': ''})
        return response


def directions(*args, **kwargs):
    """Handle directions from Google."""
    # initial poit
    lat_a = kwargs.get('lat_a')
    long_a = kwargs.get('long_a')

    # final point
    lat_b = kwargs.get('lat_b')
    long_b = kwargs.get('long_b')

    # waypoints
    lat_c = kwargs.get('lat_c')
    long_c = kwargs.get('long_c')
    lat_d = kwargs.get('lat_d')
    long_d = kwargs.get('long_d')

    origin = f'{lat_a},{long_a}'
    destination = f'{lat_b},{long_b}'
    waypoints = f'{lat_c},{long_c} | {lat_d},{long_d}'

    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            'destination': destination,
            'waypoints': waypoints,
            'key': settings.GOOGLE_API_KEY})
    directions = result.json()

    if directions['status'] == 'OK':
        routes = directions['routes'][0]['legs']

        distance = 0
        duration = 0
        route_list = []

        for route in range(len(routes)):
            distance += int(routes[route]['distance']['value'])
            duration += int(routes[route]['duration']['value'])

            route_step = {
                'origin': routes[route]['start_address'],
                'destination': routes[route]['end_address'],
                'distance': routes[route]['distance']['text'],
                'duration': routes[route]['duration']['text'],
                'steps': [[]]}

    return {
        'origin': origin,
        'destination': destination,
        'distance': f'{round(distance/1000, 2)} Km.',
        'duration': format_timespan(duration),
        'route': route_list}
        