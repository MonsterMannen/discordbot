import requests
import Login

APIKey = Login.APIKey

def requestSummonerData(region, summonerName):
    url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(url)
    if response.status_code != 200:
        return False
    else:
        return response.json()

def requestRankedData(region, summonerID):
    url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + summonerID + "/entry?api_key=" + APIKey
    response = requests.get(url)
    if response.status_code != 200:
        return False
    else:
        return response.json()


def getRank(region, summoner):
    #summoner = 'Archivon'
    #region = 'euw'

    # get summoner data
    responseJSON = requestSummonerData(region, summoner)

    # check if summoner exists
    if responseJSON == False:
        return summoner + " (" + region + ") doesn't exist"

    # get summoner id
    summonerID = responseJSON[summoner.lower()]['id']
    summonerID = str(summonerID)
    
    # get ranked data
    responseJSON2 = requestRankedData(region, summonerID)
    
    # check if any ranked data was returned
    if responseJSON2 == False:
        # no ranked stats found
        return summoner + " is unranked"
    else:
        # get stats
        tier = responseJSON2[summonerID][0]['tier']
        div = responseJSON2[summonerID][0]['entries'][0]['division']
        wins = responseJSON2[summonerID][0]['entries'][0]['wins']
        losses = responseJSON2[summonerID][0]['entries'][0]['losses']

        # calculate winrate
        winrate = float(wins)/(wins+losses)
        winrate = int((winrate * 100 + 0.5)) / 100.0
        winrate = str(winrate)[2:]

        # return info
        return summoner + " - " + tier + " " + div + " - " + winrate + "% winrate"

    
