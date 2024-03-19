import http.client
import json
import datetime
import time

api_key = '6musfbnhsy2dembz5cxzxade'
connection = http.client.HTTPSConnection("api.sportradar.us")

month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year



# Get the game ID from the team name for the current day
def get_game_id(team_name) -> int:
    game_id = None

    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/15/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Loop through the games and find the game id the team name
        for game in json_data['games']:
            if game['home']['name'] == team_name:
                game_id = game['id']
            elif game['away']['name'] == team_name:
                game_id = game['id']

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return game_id



def get_game_id_from_date(team_name, year, month, day) -> int:
    game_id = None

    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Loop through the games and find the game id the team name
        for game in json_data['games']:
            if game['home']['name'] == team_name:
                game_id = game['id']
            elif game['away']['name'] == team_name:
                game_id = game['id']

        return game_id

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



# Get the team ID from the team name
def get_team_id(team_name) -> int:
    team_id = None

    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/{day}/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Loop through the games and find the team id from param team_name
        for game in json_data['games']:
            if game['home']['name'] == team_name:
                team_id = game['home']['id']
            elif game['away']['name'] == team_name:
                team_id = game['away']['id']

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return team_id



# Get the current schedule of games for today
def get_current_schedule() -> None:
    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{year}/{month}/15/schedule.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))
        
        if not json_data.get('games'):
            raise Exception("No games today!")
        else:

            home_teams = []
            away_teams = []

            print("Today's Schedule:\n")

            for game in json_data['games']:
                home_teams.append(game['home']['name'])
                away_teams.append(game['away']['name'])
                print(f"{game['home']['name']} vs {game['away']['name']}")

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



# Get the team roster in format of player name, position, and jersey number
def get_team_roster_from_id(team_id) -> None:
    try:
        connection.request("GET", f"/nba/trial/v8/en/teams/{team_id}//profile.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None

        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        for player in json_data['players']:
            print(f"{player['full_name']} / {player['position']} / {player['jersey_number']}")

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



def get_league_standings() -> None:
    try:
        connection.request("GET", f"/nba/trial/v8/en/seasons/2023/REG/standings.json?api_key={api_key}")
        response = connection.getresponse()

        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Print the standings for the Western and Eastern Conference
        print("Western Conference\n")
        print("Southwest Division:")
        for team in json_data['conferences'][0]['divisions'][0]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
        print("Pacific Division:")
        for team in json_data['conferences'][0]['divisions'][1]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
        print("Northwest Division:")
        for team in json_data['conferences'][0]['divisions'][2]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")

        print("\n\n\nEastern Conference\n")
        print("Southeast Division:")
        for team in json_data['conferences'][1]['divisions'][1]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
        print("Central Division:")
        for team in json_data['conferences'][1]['divisions'][0]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")
        print("Atlantic Division:")
        for team in json_data['conferences'][1]['divisions'][2]['teams']:
            print(f"{team['market']} {team['name']} | Wins:{team['wins']} |  Losses:{team['losses']}")

    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



def get_live_game_stats(game_id) -> None:
    
    try:
        connection.request("GET", f"/nba/trial/v8/en/games/{game_id}/summary.json?api_key={api_key}")
        response = connection.getresponse()
        
        if response.status != 200:
            print("Error: ", response.status, response.reason)
            return None
        
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))

        # Iterate through the home and away teams and print the player stats
        print(f"\nHome Team: {json_data['home']['market']} {json_data['home']['name']}\n")
        for player in json_data['home']['players']:
            if player['statistics']['minutes'] != "00:00":
                print(f"{player['full_name']} | Points:{player['statistics']['points']} | Assists:{player['statistics']['assists']} | Rebounds:{player['statistics']['rebounds']} | Field Goals:{player['statistics']['field_goals_made']}/{player['statistics']['field_goals_att']} | Three Pointers:{player['statistics']['three_points_made']}/{player['statistics']['three_points_att']} | Free Throws:{player['statistics']['free_throws_made']}/{player['statistics']['free_throws_att']}")
       
        print(f"\nAway Team: {json_data['away']['market']} {json_data['away']['name']}\n")
        for player in json_data['away']['players']:
           if player['statistics']['minutes'] != "00:00":
                print(f"{player['full_name']} | Points:{player['statistics']['points']} | Assists:{player['statistics']['assists']} | Rebounds:{player['statistics']['rebounds']} | Field Goals:{player['statistics']['field_goals_made']}/{player['statistics']['field_goals_att']} | Three Pointers:{player['statistics']['three_points_made']}/{player['statistics']['three_points_att']} | Free Throws:{player['statistics']['free_throws_made']}/{player['statistics']['free_throws_att']}")
    
    except json.JSONDecodeError as e:
        print(f"A JSONDecodeError occurred: {str(e)}")
    except http.client.HTTPException as e:
        print(f"An exception occurred: {str(e)}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return None



# Beginning of calls to the API

get_current_schedule()
time.sleep(1)
id = get_game_id_from_date('Milwaukee Bucks', 2024, '02', 15)
time.sleep(1)
get_live_game_stats(id)
time.sleep(1)
print ('\n\n\n')
print(get_league_standings())