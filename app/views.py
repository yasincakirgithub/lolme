from django.shortcuts import render

# Create your views here.

def homePage(request):
    return render(request,'homepage/index.html',context={})

def aboutPage(request):
    return render(request,'about/index.html',context={})


def summonerPage(request,region,summoner_name):
    print(region,summoner_name)
    context = {
        'region':region,
        'summoner_name':summoner_name
    }
    return render(request,'summoner/index.html',context)
