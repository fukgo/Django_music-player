from django.shortcuts import render
from django.views import View
def contact_us(request):
    return render(request,'other/contact_us.html')
def info(request):
    return render(request,'other/web_info.html')
