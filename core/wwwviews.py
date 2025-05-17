from django.shortcuts import render, HttpResponse
from django.conf import settings as confsettings
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpRequest, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from . import models, enums, dataApis, consumers, email
import uuid
import json
import random
from functools import wraps
import jwt
import sys
import requests
import datetime
from dotenv import load_dotenv
import os
from colorama import Fore
import colorama
import re

def getenum(nameOrId, enum) -> (enums.Enum | None):
    """Converts a name or ID to an enum value.
    
    Args:
        nameOrId (str or int): The name or ID to convert.
        enum (enum): The enum class to convert to.
    
    Returns:
        enum: The corresponding enum value, or None if not found.
    """
    try:
        return enum(int(nameOrId))
    except:
        try:
            return enum[nameOrId]
        except:
            return None

JWT_SECRET = "Femboys"

from dateutil.parser import parse

def getCurrentTime():
  now = datetime.datetime.now()
  currentTime = now.isoformat()
  return currentTime

def getEndAtTime(EndAt: str):
  StartedAt = getCurrentTime()
  StartedAtSex = parse(StartedAt)
  EndAt = parse(EndAt)
  StartedAtSex = StartedAtSex.timestamp()
  EndAt = EndAt.timestamp()
  Duration = EndAt - StartedAtSex
  return int(Duration)

# Create your views here.

def authenticate(username: str, password: str):
    try:
        pl = models.Player.objects.get(Username=username)
    except:
        return {"error": "Invalid username or password."}
    password = bytes(password, "utf-8")
    password2 = bytes(pl.Password, "utf-8")
    if dataApis.checkHashPass(password, password2):
        time = dataApis.timeshit(datetime.datetime.utcnow())
        jwtD = {
            "iss": "https://auth.rec.net/",
            "client_id": "recnet",
            "role": ["webClient"],
            "sub": pl.id,
            "auth_time": time,
            "idp": "local",
            "iat": time,
            "scope": [],
        }
        return {"token": jwt.encode(jwtD, key=JWT_SECRET)}
    else:
        return {"error": "Invalid username or password."}

def login(request: HttpRequest):
   return render(request, "Login.html")

def loginApi(request: HttpRequest):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return JsonResponse({"message": "Please provide both username and password."})

    loginData = authenticate(username, password)

    if "token" in loginData:
        return JsonResponse({"token": loginData["token"]})
    else:
        return JsonResponse({"message": f"{loginData["error"]}"})

def tokenshit(token):
    try:
        tokenData = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        playerId = int(tokenData["sub"])
    except jwt.ExpiredSignatureError:
        print("1")
        return
    except jwt.InvalidTokenError:
        print("2")
        return
    except KeyError:
        print("3")
        return
    except Exception as e:
        print(f"Token decoding error: {e}")
        return

    return {
        "player": {
            "id": playerId
        },
        "accessToken": token
    }

def sessionApi(request: HttpRequest):
    authToken = request.COOKIES.get("authToken")
    if authToken is None:
        return JsonResponse({})
    ddd = tokenshit(authToken)
    if ddd is None:
        return JsonResponse({})
    return JsonResponse(ddd)
    

    
def index(request: HttpRequest):
    return render(request, "www/base.html")