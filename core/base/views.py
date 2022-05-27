from django.http import HttpResponse
from django.shortcuts import render

def call_transactions(request):
    return HttpResponse('<h1>Hello World</h1>')
