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


@csrf_exempt
def emailw(request: HttpRequest):
   return render(request, "CreateU.html")