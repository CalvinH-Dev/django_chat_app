from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.


class ChatView(View):
    def get(self, request: HttpRequest):
        return HttpResponse("ok get")

    def post(self, request: HttpRequest):
        if not request.body:
            return HttpResponse(status=204)
        return HttpResponse("ok post")
