import http.client
import json
import datetime
import time
import csv

api_key = '284s83ypFD8LAEu1Y6WFK5peMLz1KF0Y7jSFHizV'
month = datetime.datetime.now().month
month = str(month).zfill(2)
day = datetime.datetime.now().day
day = str(day).zfill(2)
year = str(datetime.datetime.now().year)

## Player class ##
class PlayerStats:
    def __init__(self, name, team, points, assists, rebounds, blocks, steals, field_goals_percent, three_pointers_percent, free_throws_percent):
        self.name = name
        self.team = team
        self.points = points
        self.assists = assists
        self.rebounds = rebounds
        self.blocks = blocks
        self.steals = steals
        self.field_goals_percent = field_goals_percent
        self.three_pointers_percent = three_pointers_percent
        self.free_throws_percent = free_throws_percent
## End of player class ## 
        


## Team roster class ##
class TeamRoster:
    def __init__(self, full_name, position, jersey_number):
        self.full_name = full_name
        self.position = position
        self.jersey_number = jersey_number
## End of team roster class ##
        


## Team standings class ##
class TeamStandings:
    def __init__(self, team_name, wins, losses, team_id):
        self.team_name = team_name
        self.wins = wins
        self.losses = losses
        self.team_id = team_id
## End of team standings class ##
        


## Team stats class ##
class TeamStats:
    def __init__(self,team_name, team_points, team_assists, team_rebounds, team_blocks, team_steals, team_field_goals_pct, team_three_points_pct, team_free_throws_pct):
        self.team_name = team_name
        self.team_points = team_points
        self.team_assists = team_assists
        self.team_rebounds = team_rebounds
        self.team_blocks = team_blocks
        self.team_steals = team_steals
        self.team_field_goals_pct = team_field_goals_pct
        self.team_three_points_pct = team_three_points_pct
        self.team_free_throws_pct = team_free_throws_pct




## Facade class for the API calls ##
class GameFacade:
    ''' Constructor for the class '''
    def __init__(self):
        self.api_key = api_key
        self.connection = http.client.HTTPSConnection("api.sportradar.us")





    ### Download methods ###
    ''' ONLY USE THESE METHODS WHEN INITIALIZING SYSTEM TO DOWNLOAD 
        NEEDED INFORMATION FOR REDUCING AMOUNT OF API CALLS SUCH AS 
        GETTING FULL ROSTER, SCHEDULE, AND TEAM NAMES/TEAM ID
    '''
    def download_season_schedule(self)-> None:
        nba_year = datetime.datetime.now().year - 1
        nba_year = str(nba_year)

        try:
            self.connection.request("GET", f"/nba/trial/v8/en/games/{nba_year}/REG/schedule.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None

            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Creating csv file with the schedule and writing each line as a game '''
            with open(f"{nba_year}_season_schedule.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Game ID", "Home Team", "Away Team",  "Date", "Time"])

                for game in json_data['games']:

                    ''' Convert GMT time to EST '''
                    gmt_time = datetime.datetime.strptime(game['scheduled'], "%Y-%m-%dT%H:%M:%SZ")
                    est_time = gmt_time - datetime.timedelta(hours=4)
                    est_time_str = est_time.strftime("%Y-%m-%d %H:%M:%S")

                    writer.writerow([game['id'], game['home']['name'], game['away']['name'], est_time_str[:10], est_time_str[11:16]])

        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None
    


    def download_nba_teams(self) -> None:
        try:
            self.connection.request("GET", f"/nba/trial/v8/en/league/hierarchy.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None

            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            with open(f"nba_teams.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Team ID", "Team Name"])
                for conference in json_data['conferences']:
                    for division in conference['divisions']:
                        for team in division['teams']:
                            writer.writerow([team['id'], team['market'] + " " + team['name']])

        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return None
    


    ''' Get the team roster in format of player name, position, and jersey number and player_id'''
    def download_nba_roster(self):
        nba_team_ids = []
        nba_year = datetime.datetime.now().year - 1
        nba_year = str(nba_year)

        with open("nba_teams.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                nba_team_ids.append(row[0])


        '''create new csv file for the roster each time the method is called'''
        with open(f"{nba_year}_nba_roster.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Team ID", "Team Name", "Player Name", "Position", "Jersey Number", "Player ID"])

            for team in nba_team_ids:
                time.sleep(3)
                try:
                    self.connection.request("GET", f"/nba/trial/v8/en/teams/{team}//profile.json?api_key={api_key}")
                    response = self.connection.getresponse()
                    
                    if response.status != 200:
                        print("Error: ", response.status, response.reason)
                        return None

                    data = response.read()
                    json_data = json.loads(data.decode("utf-8"))

                    for player in json_data['players']:
                        writer.writerow([team, json_data['market'] + " " + json_data['name'], player['full_name'], player['position'], player['jersey_number'], player['id']])
                # Catching exceptions #
                except json.JSONDecodeError as e:
                    print(f"A JSONDecodeError occurred: {str(e)}")
                except http.client.HTTPException as e:
                    print(f"An exception occurred: {str(e)}")
                except Exception as e:
                    print(f"An exception occurred: {str(e)}")
        return None
    ### End of download methods ###
    


    def test(self,id):
        try:
                self.connection.request("GET", f"/nba/trial/v8/en/teams/583ec928-fb46-11e1-82cb-f4ce4684ea4c//profile.json?api_key={api_key}")
                response = self.connection.getresponse()
                
                if response.status != 200:
                    print("Error: ", response.status, response.reason)
                    return None

                data = response.read()
                json_data = json.loads(data.decode("utf-8"))

                for player in json_data['players']:
                    print(player['full_name'], player['position'], player['jersey_number'], player['id'])
            # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")


    ### Game methods ###
    def get_league_standings(self):
        year = datetime.datetime.now().year - 1
        year = str(year)

        standings = []

        try:
            self.connection.request("GET", f"/nba/trial/v8/en/seasons/{year}/REG/standings.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200:
                print("Error: ", response.status, response.reason)
                return None
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Add the teams to the standings list into objects of TeamStandings '''
            for conference in json_data['conferences']:
                for division in conference['divisions']:
                    for team in division['teams']:
                        standings.append(TeamStandings(team['market'] + " " + team['name'], team['wins'], team['losses'], team['id']))

        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return standings
    


    def get_current_schedule(self):
        schedule = []
        try:
            date_col = 3

            with open("2023_season_schedule.csv", "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[date_col] == f"{year}-{month}-{day}":
                        schedule.append(f"{row[1]} vs {row[2]} on {row[3]} at {row[4]}")

        
        
        # Catching exceptions #
        except Exception as e:
            print(f"An exception occurred: {str(e)}")

        return schedule
    ### End of game methods ###

    



    ### ID methods (Not used on website) ###
    '''Get game id from reading pre-generated nba schedule file'''
    def get_game_id(self, team_name, year, month, day) -> int:
        game_id = None

        try:
            with open("2023_season_schedule.csv", "r") as file:
                reader = csv.reader(file)
                
                for row in reader:
                    if row[1] == team_name or row[2] == team_name:
                        if row[3] == f"{year}-{month}-{day}":
                            game_id = row[0]

        # Catching exceptions #
        except csv.Error as e:
            print(f"A CSV error occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return game_id
    
    '''Get team id from reading pre-generated nba teams file'''
    def get_team_id(self, team_name) -> int:
        team_id = None
        try:
            with open("nba_teams.csv", "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[1] == team_name:
                        team_id = row[0]

        # Catching exceptions #
        except csv.Error as e:
            print(f"A CSV error occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        
        return team_id
    
    '''Get player id from reading the pre-generated nba roster'''
    def get_player_id(self, player_name) -> int:
        player_id = None
        try:
            with open("2023_nba_roster.csv", "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[2] == player_name:
                        player_id = row[5]

        # Catching exceptions #
        except csv.Error as e:
            print(f"A CSV error occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        
        return player_id
    ### End of ID methods ###





    ### Roster method ###
    def get_team_roster_from_id(self,team_id):
        roster = []

        try:
            with open("2023_nba_roster.csv", "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[0] == team_id:
                        roster.append(TeamRoster(row[2], row[3], row[4]))
            
        # Catching exceptions #
        except csv.Error as e:
            print(f"A CSV error occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return roster
    ### End of roster methods ###





    ### Stats methods ###
    '''Live game stats for the whole team that has requirements minutes > 0 and will append each player with their respective stats to a list of objects'''
    def get_live_game_stats(self, game_id):
        players = []

        try:
            self.connection.request("GET", f"/nba/trial/v8/en/games/{game_id}/summary.json?api_key={api_key}")
            response = self.connection.getresponse()
<<<<<<< HEAD
            
            if response.status == 404:
                print("is not playing a game today.")
                return players
=======
>>>>>>> 52a7c4bed429d6d864d67399696161bd66325a45

            if response.status != 200 and response.status != 404:
                print("Error: ", response.status, response.reason)
                return players
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Iterate through the home and away teams and add to the players list if the player has played in the game'''
            for player in json_data['home']['players']:
                if player['statistics']['minutes'] != "00:00":
                    players.append(PlayerStats(player['full_name'], json_data['home']['market'] + " " + json_data['home']['name'], player['statistics']['points'], player['statistics']['assists'], player['statistics']['rebounds'], player['statistics']['blocks'], player['statistics']['steals'], player['statistics']['field_goals_pct'], player['statistics']['three_points_pct'], player['statistics']['free_throws_pct']))
            for player in json_data['away']['players']:
                if player['statistics']['minutes'] != "00:00":
                    players.append(PlayerStats(player['full_name'], json_data['away']['market'] + " " + json_data['away']['name'], player['statistics']['points'], player['statistics']['assists'], player['statistics']['rebounds'], player['statistics']['blocks'], player['statistics']['steals'], player['statistics']['field_goals_pct'], player['statistics']['three_points_pct'], player['statistics']['free_throws_pct']))

        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        return players
    


    '''Obtains live stats for a specific player that is inputted into the function that will be obtain via website.'''
    def get_player_stats(self, player_name,year,month,day):
        player_team = None
        game_id = None
        player_stats = []
        all_player_stats = []
        
        try:
            with open("2023_nba_roster.csv", "r") as file:
                reader = csv.reader(file)
                reader.__next__()
                for row in reader:
                    if row[2] == player_name:
                        player_team = row[1]
<<<<<<< HEAD
                        all_player_stats = api.get_live_game_stats(api.get_game_id(player_team,year,month,day))
                        
                        if all_player_stats is None:
                            return all_player_stats
=======
            
            with open("2023_season_schedule.csv", "r") as file:
                reader = csv.reader(file)
                reader.__next__()
                for row in reader:
                    if row[1] == player_team or row[2] == player_team and row[3] == f"{year}-{month}-{day}":
                        game_id = row[0]
>>>>>>> 52a7c4bed429d6d864d67399696161bd66325a45

            self.connection.request("GET", f"/nba/trial/v8/en/games/{game_id}/summary.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status == 404:
                print(player_name + " is not currently playing.")
                return player_stats

            elif response.status != 200:
                print("Error: ", response.status, response.reason)
                return player_stats
            
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            for player in json_data['home']['players']:
                    print(player)  


        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        
        return player_stats
    

    def get_live_team_stats(self, game_id):
        teams = []

        try:
            self.connection.request("GET", f"/nba/trial/v8/en/games/{game_id}/summary.json?api_key={api_key}")
            response = self.connection.getresponse()

            if response.status != 200 and response.status != 404:
                print("Error: ", response.status, response.reason)
                return teams
                
            data = response.read()
            json_data = json.loads(data.decode("utf-8"))

            ''' Add the home and away team stats to the teams list '''
            teams.append(TeamStats(json_data['home']['market'] + " " + json_data['home']['name'], json_data['home']['statistics']['points'], json_data['home']['statistics']['assists'], json_data['home']['statistics']['offensive_rebounds']+json_data['home']['statistics']['defensive_rebounds'], json_data['home']['statistics']['blocks'], json_data['home']['statistics']['steals'], json_data['home']['statistics']['field_goals_pct'], json_data['home']['statistics']['three_points_pct'], json_data['home']['statistics']['free_throws_pct']))
            teams.append(TeamStats(json_data['away']['market'] + " " + json_data['away']['name'], json_data['away']['statistics']['points'], json_data['away']['statistics']['assists'], json_data['away']['statistics']['offensive_rebounds']+json_data['away']['statistics']['defensive_rebounds'], json_data['away']['statistics']['blocks'], json_data['away']['statistics']['steals'], json_data['away']['statistics']['field_goals_pct'], json_data['away']['statistics']['three_points_pct'], json_data['away']['statistics']['free_throws_pct']))
        
        # Catching exceptions #
        except json.JSONDecodeError as e:
            print(f"A JSONDecodeError occurred: {str(e)}")
        except http.client.HTTPException as e:
            print(f"An exception occurred: {str(e)}")
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
        
        return teams
    ### End of stats methods ###
## End of facade class for the API calls ##





## API class to call the facade class ##
class SportsAPI():
    def __init__(self):
        self.game_facade = GameFacade()

    def download_season_schedule(self):
        self.game_facade.download_season_schedule()

    def download_nba_teams(self):
        self.game_facade.download_nba_teams()

    def download_nba_roster(self):
        self.game_facade.download_nba_roster()
    
    def get_league_standings(self):
        return self.game_facade.get_league_standings()

    def get_current_schedule(self):
        return self.game_facade.get_current_schedule()

    def get_game_id(self, team_name, year, month, day):
        return self.game_facade.get_game_id(team_name, year, month, day)
       
    def get_team_id(self, team_name):  
        return self.game_facade.get_team_id(team_name)
    
    def get_team_roster_from_id(self, team_id):
<<<<<<< HEAD
        self.game_facade.get_team_roster_from_id(team_id)

    def download_nba_roster(self):
        self.game_facade.download_nba_roster()
    
=======
        return self.game_facade.get_team_roster_from_id(team_id)
        
>>>>>>> 52a7c4bed429d6d864d67399696161bd66325a45
    def get_live_game_stats(self, game_id):
        return self.game_facade.get_live_game_stats(game_id)

    def get_player_stats(self, player_name,year,month,day):
        return self.game_facade.get_player_stats(player_name,year,month,day)
    
    def get_live_team_stats(self, game_id):
        return self.game_facade.get_live_team_stats(game_id)
    
    def test(self, id):
        return self.game_facade.test(id)
## End of API class ##



### Main method to call the API class ###
'''
How to use the main method:
1. Create an instance of the API class
2. Look at methods within sportsAPI class to see what methods are available
3. Call the methods with the appropriate parameters
4. Some methods will require an api call to the API class to get the data i.e get_team_roster_from_id requires a team id that can be obtained from get_team_id
5. The methods will return the data in the form of a list or object that can be used to display the data on the website/console or the raspberry pi
6. Between each method call, there MUST be a time.sleep(1) to prevent the API from being overloaded and blocking a request
7. The main method is a template to show how to call the methods, it is not meant to be run as is
'''

api = SportsAPI()

<<<<<<< HEAD
stats = api.get_player_stats("LeBron James", "2024", "01", "29")

print(stats[0].points)
=======
id = api.get_team_roster_from_id(api.get_team_id("Chicago Bulls"))
>>>>>>> 52a7c4bed429d6d864d67399696161bd66325a45

for player in id:
    print(player)
### End of main method ###