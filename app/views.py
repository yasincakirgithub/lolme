from django.shortcuts import render

# Create your views here.

def homePage(request):
    return render(request,'homepage/index.html',context={})

def aboutPage(request):
    return render(request,'about/index.html',context={})
