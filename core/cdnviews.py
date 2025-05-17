from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpRequest, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import os
import json

from . import models

def abort(status_code: int):
    d = HttpResponse("")
    d.status_code = status_code
    return d

# Create your views here.

def img(request: HttpRequest, path):
    path = os.path.join("media", path)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='image/png')
        #response['Content-Disposition'] = 'attachment; filename="downloaded"'
        return response
    else:
        return abort(404)

def video(request: HttpRequest, path):
    path = os.path.join("media","video", path)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='video/ogv')
        response['Content-Disposition'] = 'attachment; filename="downloaded"'
        return response
    else:
        return abort(404)
    
def audio(request: HttpRequest, path):
    path = os.path.join("media","audio", path)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='audio/wav')
        return response
    else:
        return abort(404)