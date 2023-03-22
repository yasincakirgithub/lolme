from django.shortcuts import render
import requests
import json
from datetime import datetime

# Create your views here.

league_icon_dict = {
    'iron':"01",
    'bronze':"02",
    'silver':"03",
    'gold':"04",
    'platinum':"05",
    'diamond':"06",
    'master':"07",
    'grandmaster':"08",
    'challenger':"09",
}
league_rank_dict = {
    'I':"1",
    'II':"2",
    'III':"3",
    'IV':"4",
    'V':"5"
}


summoner_data_url = '/lol/summoner/v4/summoners/by-name/'
top20champions_data_url = '/lol/champion-mastery/v4/champion-masteries/by-summoner/'
league_entries_data_url = '/lol/league/v4/entries/by-summoner/'

api_key = "?api_key=RGAPI-41be0733-2b4f-474c-aa47-76b37724bee4"


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

    league_entries_base_data_url = request_url + league_entries_data_url + summoner_response["id"] + api_key
    league_entries_response = requests.request('GET', league_entries_base_data_url)
    league_entries_response = league_entries_response.json()

    response_json = {

        'summoner': {
            'name': summoner_response["name"],
            'profileIconUrl': f'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{summoner_response["profileIconId"]}.jpg',
            'level': summoner_response["summonerLevel"],
            'puuid': summoner_response["puuid"],
            'accountId': summoner_response["accountId"],
            'revisionDate': datetime.utcfromtimestamp(summoner_response["revisionDate"] / 1000).strftime('%d/%m/%Y')
        },
        'top20champions': [{'championId': champion["championId"],
                            'championLevel': champion["championLevel"],
                            'championLevelIcon': f"https://lolg-cdn.porofessor.gg/img/s/masteries/lvl{champion['championLevel']}.png" if champion['championLevel'] > 3 else None,
                            'championPoints': champion["championPoints"],
                            'lastPlayTime': datetime.utcfromtimestamp(champion["lastPlayTime"] / 1000).strftime(
                                '%d/%m/%Y'),
                            'championIcon': f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champion['championId']}.png"}
                           for champion in top20champions_response],

        'league_entries': [{'queue_type': league_entry["queueType"].replace("_"," "),
                            'tier': league_entry["tier"],
                            'rank': league_entry["rank"],
                            'leaguePoints': league_entry["leaguePoints"],
                            'wins': league_entry["wins"],
                            'icon': f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/content/src/leagueclient/rankedcrests/{league_icon_dict[league_entry['tier'].lower()]}_{league_entry['tier'].lower()}/images/{league_entry['tier'].lower()}_crown_d{league_rank_dict[league_entry['rank']]}.png",
                            'losses': league_entry["losses"]} for league_entry in league_entries_response]

    }

    return render(request, 'summoner/index.html', response_json)
