from django.shortcuts import render, HttpResponse
from django.views import View


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "register.html")
