from django.shortcuts import render
import requests
import json
from datetime import datetime

# Create your views here.

summoner_data_url = '/lol/summoner/v4/summoners/by-name/'
top20champions_data_url = '/lol/champion-mastery/v4/champion-masteries/by-summoner/'

api_key = "?api_key=RGAPI-ab4ceacb-5425-46e7-a52c-ccfa657111a6"


def homePage(request):
    return render(request, 'homepage/index.html', context={})


def aboutPage(request):
    return render(request, 'about/index.html', context={})


def summonerPage(request, region, summoner_name):
    request_url = f"https://{region}.api.riotgames.com"
    summoner_base_data_url = request_url + summoner_data_url + summoner_name + api_key
    summoner_response = requests.request('GET', summoner_base_data_url)
    if not summoner_response.status_code == 200:
        return render(request, 'summoner/index.html', context={'error': True})
    summoner_response = summoner_response.json()

    top20champions_base_data_url = request_url + top20champions_data_url + summoner_response[
        "id"] + "/top" + api_key + '&count=20'
    top20champions_response = requests.request('GET', top20champions_base_data_url)
    top20champions_response = top20champions_response.json()

    response_json = {

        'summoner': {
            'name': summoner_response["name"],
            'profileIconUrl': f'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{summoner_response["profileIconId"]}.jpg',
            'level': summoner_response["summonerLevel"],
            'puuid': summoner_response["puuid"],
            'accountId': summoner_response["accountId"]
        },
        'top20champions': [{'championId': champion["championId"],
                            'championLevel':champion["championLevel"],
                            'championPoints':champion["championPoints"],
                            'lastPlayTime': datetime.utcfromtimestamp(champion["lastPlayTime"]/1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
                            'championIcon': f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champion['championId']}.png"
                            } for champion in top20champions_response]

    }

    return render(request, 'summoner/index.html', response_json)
