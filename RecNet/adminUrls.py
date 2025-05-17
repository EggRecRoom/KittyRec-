from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpRequest, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

def re(request: HttpRequest):
    return redirect("https://www.urbandictionary.com/define.php?term=skid")
    

urlpatterns = [
    path("login", re),#
    path("login/", re),
    path("", admin.site.urls),
]


admin.site.site_header = "KittyRec Admin Development"
admin.site.site_title = "KittyRec Admin Portal"
admin.site.index_title = "Welcome to KittyRec Admin Portal"
admin.site.site_url = None  # Disable the admin site link in the header
admin.site.name = "KittyRec Admin"  # Set the admin site name