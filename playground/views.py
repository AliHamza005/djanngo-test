from django.shortcuts import render
from django.http import HttpResponse

def calculate():
    x = 1
    y = 2*2
    return y

def say_hello(request):
    x =calculate()
    return render(request,'hello.html',{'name':'Ali Hamza'})