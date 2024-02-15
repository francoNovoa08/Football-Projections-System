def new_run():
    print("Function list: ")
    print("Program_info - 1\n"
          "Display_stats - 2\n"
          "simple_regular_season - 3\n"
          "complex_regular_season - 4\n")
    user_input = get_input("Enter run ID: ")
    if user_input == 1:
        program_info()
    if user_input == 2:
        display_stats()
    if user_input == 3:
        simple_regular_season()
    if user_input == 4:
        complex_regular_season()


def program_info():
    info = get_input("Enter function to receive information: ", )
    if info == 2:
        print("Display_stats - Access the following NSL team data: city, state, conference, timezone_UTC, name\n")
    elif info == 3:
        print(
            "simple_regular_season - Access simple data of the regular season (only accounting for win (3 points)/loss"
            "(0 points)/draw (1 point). Ranking and stat. available\n"
            "ranking - Display a ranking of teams based on wins, losses, and draws\n"
            "Head-to-head stats - Compare two teams based on wins, losses, and draws\n"
            "team match finder - Find match ids of games between 2 teams\n"
            "conference_ranking - Ranking separated by conference (west and east)")
    elif info == 4:
        print(
            "complex_regular_season - Access data of the regular season accounting for all variables")


def display_stats():
    team_id = str(input("Enter team ID: "))
    team_id = team_id.upper()
    stat = get_input("Enter index (city = 0, state = 1, conference = 2, timezone = 3, name = 4: ")
    if team_id in Team_IDs:
        team_index = Team_IDs.index(team_id)
        print(Team_data[team_index][stat])


def simple_regular_season():
    team_stats = build_team_stats(match_ids, home_ids, away_ids, home_scores, away_scores)
    index = get_input("Enter index (ranking = 0, head-to-head stats = 1, team_match_finder = 2\n"
                      "conference_ranking = 3): ")
    if index == 0:
        print_ranking(team_stats)
    elif index == 1:
        team1 = str(input("Enter first team ID: "))
        team2 = str(input("Enter second team ID: "))
        display_team_head_to_head_stats(team_stats, team1, team2)
    elif index == 2:
        team1 = str(input("Enter first team ID: "))
        team2 = str(input("Enter second team ID: "))
        display_exclusive_team_head_to_head_stats(match_ids, home_ids, away_ids, team_stats, team1, team2)
    elif index == 3:
        west_teams, east_teams = conference_ranking()
        west_stats = {team: team_stats[team] for team in west_teams}
        east_stats = {team: team_stats[team] for team in east_teams}
        print("West stats: ")
        print_ranking(west_stats)
        print("\nEast Stats:")
        print_ranking(east_stats)

# ------------------------------------------------------


def conference_ranking():
    west_teams = []
    east_teams = []
    for items in range(len(Team_IDs)):
        if Team_data[items][2] == "W":
            west_teams.append(Team_IDs[items])
        elif Team_data[items][2] == "E":
            east_teams.append(Team_IDs[items])
    return west_teams, east_teams


# ------------------------------------------------------
def read_match_ids(file_path):
    with open(file_path, "r") as file:
        return [line.strip().replace("game_2023_", "") for line in file]


def read_str(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def read_int(file_path):
    with open(file_path, 'r') as file:
        return [int(line.strip()) for line in file]


def read_float(file_path):
    with open(file_path, 'r') as file:
        return [float(line.strip()) for line in file]


def calculate_points(home_score, away_score):
    if home_score > away_score:
        return 3, 0  # Home team wins
    elif home_score < away_score:
        return 0, 3  # Away team wins
    else:
        return 1, 1  # Match is a draw


def build_team_stats(match_ids, home_ids, away_ids, home_scores, away_scores):
    team_stats = {}

    for i in range(len(match_ids)):
        home_id = home_ids[i]
        away_id = away_ids[i]
        home_score = home_scores[i]
        away_score = away_scores[i]

        home_points, away_points = calculate_points(home_score, away_score)

        # Update home team stats
        if home_id not in team_stats:
            team_stats[home_id] = {'wins': 0, 'draws': 0, 'losses': 0, 'points': 0}
        team_stats[home_id]['wins'] += home_points == 3
        team_stats[home_id]['draws'] += home_points == 1
        team_stats[home_id]['losses'] += home_points == 0
        team_stats[home_id]['points'] += home_points

        # Update away team stats
        if away_id not in team_stats:
            team_stats[away_id] = {'wins': 0, 'draws': 0, 'losses': 0, 'points': 0}
        team_stats[away_id]['wins'] += away_points == 3
        team_stats[away_id]['draws'] += away_points == 1
        team_stats[away_id]['losses'] += away_points == 0
        team_stats[away_id]['points'] += away_points
    return team_stats


def print_ranking(team_stats):
    sorted_teams = sorted(team_stats.items(), key=lambda x: x[1]['points'], reverse=True)

    print("Ranking:")
    for rank, (team_id, stats) in enumerate(sorted_teams, start=1):
        print(
            f"{rank}. Team ID: {team_id}, Points: {stats['points']}, Wins: {stats['wins']}, "
            f"Draws: {stats['draws']}, Losses: {stats['losses']}")


# ------------------------------------------------------


def display_team_head_to_head_stats(team_stats, team_id_1, team_id_2):
    # Initialize counters for team 1 and team 2
    team_1_wins = team_2_wins = team_1_draws = team_2_draws = team_1_losses = team_2_losses = 0
    team_id_1 = team_id_1.upper()
    team_id_2 = team_id_2.upper()

    for team_id, stats in team_stats.items():
        if team_id == team_id_1:
            team_1_wins = stats["wins"]
            team_1_draws = stats["draws"]
            team_1_losses = stats["losses"]
        elif team_id == team_id_2:
            team_2_wins = stats["wins"]
            team_2_draws = stats["draws"]
            team_2_losses = stats["losses"]

    print(f"Head-to-head stats between Team {team_id_1} and Team {team_id_2}:")
    team_1_points = 3 * team_1_wins + team_1_draws
    team_2_points = 3 * team_2_wins + team_2_draws
    print(f"Team {team_id_1}: Points - " + str(
        team_1_points) + f", Wins - {team_1_wins}, Draws - {team_1_draws}, Losses - {team_1_losses}")
    print(f"Team {team_id_2}: Points - " + str(
        team_2_points) + f", Wins - {team_2_wins}, Draws - {team_2_draws}, Losses - {team_2_losses}")


# ------------------------------------------------------


def display_exclusive_team_head_to_head_stats(match_ids, home_ids, away_ids, team_stats, team_id_1, team_id_2):
    # Initialize counters for team 1 and team 2
    team_1_wins = team_2_wins = team_1_draws = team_2_draws = team_1_losses = team_2_losses = 0
    team_id_1 = team_id_1.upper()
    team_id_2 = team_id_2.upper()
    # List to store match IDs for head-to-head matches
    head_to_head_match_ids = []

    for i in range(len(match_ids)):
        match_id = match_ids[i]
        home_team_id = home_ids[i]
        away_team_id = away_ids[i]

        if (home_team_id == team_id_1 and away_team_id == team_id_2) or (
                home_team_id == team_id_2 and away_team_id == team_id_1):
            result = determine_result(team_stats, home_team_id, away_team_id)

            head_to_head_match_ids.append(match_id)

            if home_team_id == team_id_1:
                update_counters(result, team_1_wins, team_1_draws, team_1_losses)
            else:
                update_counters(result, team_2_wins, team_2_draws, team_2_losses)
    print("Match IDs for head-to-head matches:", ', '.join(head_to_head_match_ids))


def determine_result(team_stats, home_team_id, away_team_id):
    if team_stats[home_team_id]['points'] > team_stats[away_team_id]['points']:
        return 'win'
    elif team_stats[home_team_id]['points'] < team_stats[away_team_id]['points']:
        return 'loss'
    else:
        return 'draw'


def update_counters(result, wins_counter, draws_counter, losses_counter):
    if result == 'win':
        wins_counter += 1
    elif result == 'draw':
        draws_counter += 1
    else:
        losses_counter += 1


# ------------------------------------------------------


def get_input(prompt, input_type=int):
    while True:
        try:
            user_input = input_type(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"An error has occurred: {e}")


# ------------------------------------------------------


def complex_regular_season():
    team_stats = build_complex_team_stats(match_ids, home_ids, away_ids, home_scores, away_scores, home_xGs,
                                          away_xGs, home_shots, away_shots, home_corners, away_corners, home_pk_goals,
                                          away_pk_goals,
                                          home_pk_shots, away_pk_shots, home_ToPs)


def build_complex_team_stats(match_ids, home_ids, away_ids, home_scores, away_scores, home_xGs,
                             away_xGs, home_shots, away_shots, home_corners, away_corners, home_pk_goals, away_pk_goals,
                             home_pk_shots, away_pk_shots, home_ToPs):
    team_stats = {}

    for i in range(len(match_ids)):
        home_id = home_ids[i]
        away_id = away_ids[i]
        home_score = home_scores[i]
        away_score = away_scores[i]
        home_xG = home_xGs[i]
        away_xG = away_xGs[i]
        home_shot = home_shots[i]
        away_shot = away_shots[i]
        home_corner = home_corners[i]
        away_corner = away_corners[i]
        home_pk_goal = home_pk_goals[i]
        away_pk_goal = away_pk_goals[i]
        home_pk_shot = home_pk_shots[i]
        away_pk_shot = away_pk_shots[i]
        home_ToP = home_ToPs[i]
        calculations =[complex_calculate_points(home_score, away_score, home_xG, away_xG,
                                 home_shot, away_shot, home_corner, away_corner,
                                 home_pk_goal, away_pk_goal, home_pk_shot, away_pk_shot,
                                 home_ToP)]

        home_points, away_points = calculations[0][0][0], calculations[0][0][1]
        home_xG_points, away_xG_points = calculations[0][1][0], calculations[0][1][1]
        home_shots_points, away_shots_points = calculations[0][2][0], calculations[0][2][1]
        home_corners_points, away_corners_points = calculations[0][3][0], calculations[0][3][1]
        home_pk_goals_points, away_pk_goals_points = calculations[0][4][0], calculations[0][4][1]
        home_pk_shots_points, away_pk_shots_points = calculations[0][5][0], calculations[0][5][1]
        home_ToP_points, away_ToP_points = calculations[0][6][0], calculations[0][6][1]
        # Update home team stats
        if home_id not in team_stats:
            team_stats[home_id] = {'wins': 0, 'draws': 0, 'losses': 0, 'xg': 0, "shots": 0,
                                   "corners": 0, "pk_goals": 0, "pk_shots": 0, "top": 0, 'points': 0}
        if 'xg' not in team_stats[home_id]:
            team_stats[away_id]['xg'] = 0
        team_stats[home_id]['wins'] += home_points == 3
        team_stats[home_id]['draws'] += home_points == 1
        team_stats[home_id]['xg'] += home_xG_points
        team_stats[home_id]['losses'] += home_points == 0
        team_stats[home_id]['shots'] += home_shots_points
        team_stats[home_id]['corners'] += home_corners_points
        team_stats[home_id]['pk_goals'] += home_pk_goals_points
        team_stats[home_id]['pk_shots'] += home_pk_shots_points
        team_stats[home_id]['points'] += home_points
        team_stats[home_id]['points'] += home_xG_points
        team_stats[home_id]['points'] += home_corners_points
        team_stats[home_id]['points'] += home_shots_points
        team_stats[home_id]['points'] += home_pk_goals_points
        team_stats[home_id]['points'] += home_pk_shots_points

        # Update away team stats
        if away_id not in team_stats:
            team_stats[away_id] = {'wins': 0, 'draws': 0, 'losses': 0, 'xg': 0, "shots": 0,
                                   "corners": 0, "pk_goals": 0, "pk_shots": 0, "top": 0, 'points': 0}
        if 'xg' not in team_stats[away_id]:
            team_stats[away_id]['xg'] = 0
        team_stats[away_id]['wins'] += away_points == 3
        team_stats[away_id]['draws'] += away_points == 1
        team_stats[away_id]['losses'] += away_points == 0
        team_stats[away_id]['xg'] += away_xG_points
        team_stats[away_id]['shots'] += away_shots_points
        team_stats[away_id]['corners'] += away_corners_points
        team_stats[away_id]['pk_goals'] += away_pk_goals_points
        team_stats[away_id]['pk_shots'] += away_pk_shots_points
        team_stats[away_id]['points'] += away_points
        team_stats[away_id]['points'] += away_xG_points
        team_stats[away_id]['points'] += away_corners_points
        team_stats[away_id]['points'] += away_shots_points
        team_stats[away_id]['points'] += away_pk_goals_points
        team_stats[away_id]['points'] += away_pk_shots_points
        sorted_teams = sorted(team_stats.items(), key=lambda x: x[1]['points'], reverse=True)

    print("Ranking:")
    for rank, (team_id, stats) in enumerate(sorted_teams, start=1):
        print(
            f"{rank}. Team ID: {team_id}, Points: {stats['points']}, Wins: {stats['wins']}, Draws: {stats['draws']}, Losses: {stats['losses']}")


def complex_calculate_points(home_score, away_score, home_xG, away_xG,
                             home_shot, away_shot, home_corner, away_corner,
                             home_pk_goal, away_pk_goal, home_pk_shot,
                             away_pk_shot, home_ToP):
    calculations = []
    calculations.append(calculate_points(home_score, away_score))
    calculations.append(calculate_xG(home_xG, away_xG))
    calculations.append(calculate_shot(home_shot, away_shot))
    calculations.append(calculate_corner(home_corner, away_corner))
    calculations.append(calculate_pk(home_pk_goal,away_pk_goal))
    calculations.append(calculate_pk_shot(home_pk_shot,away_pk_shot))
    calculations.append(calculate_ToP(home_ToP))
    return calculations
def calculate_xG(home_xG, away_xG):
    return (home_xG*0.01),(away_xG*0.01)
def calculate_shot(home_shots, away_shots):
    return (home_shots*0.1), (away_shots*0.1)
def calculate_corner(home_corner, away_corner):
    return(home_corner*0.1), (away_corner*0.1)
def calculate_pk(home_pk,away_pk):
    return(home_pk*0.25,away_pk*0.25)
def calculate_pk_shot(home_pk,away_pk):
    return(home_pk*0.05, away_pk*0.05)
def calculate_ToP(home_ToP):
    return (home_ToP), (1-home_ToP)
#------------------------------------------------------
# Team_id = [city, state, conference, timezone_UTC, name]
# city[0], state[1], conference[2], timezone_UTC[3, name[4]


Team_IDs = ["ALB", "ANC", "AUG", "BAK", "BOI", "CHM", "DES", "DOV", "EUG", "FAR", "FOR", "JAC",
            "LAR", "LEX", "LRO", "MAN", "MOB", "OAK", "PRO", "REN", "SAS", "SFS", "SJU", "SPR",
            "TAC", "TOL", "TUC", "WIC"]
Team_data = [["Albuquerque", "New Mexico", "W", "-6"],
             ["Anchorage", "Alaska", "W", "-8"],
             ["Augusta", "Georgia", "E", "-4"],
             ["Bakersfield", "California", "W", "-7"],
             ["Boise", "Idaho", "W", "-6"],
             ["Charleston", "South Carolina", "E", "-4"],
             ["Des Moines", "Iowa", "E", "-5"],
             ["Dover", "Delaware", "E", "-4"],
             ["Eugene", "Oregon", "W", "-7"],
             ["Fargo", "North Dakota", "W", "-5"],
             ["Fort Collins", "Colorado", "W", "-5"],
             ["Jackson", "Mississippi", "E", "-5"],
             ["Laredo", "Texas", "E", "-5"],
             ["Lexington", "Kentucky", "E", "-4"],
             ["Little Rock", "Arkansas", "E", "-5"],
             ["Manchester", "New Hampshire", "E", "-4"],
             ["Mobile", "Alabama", "E", "-5"],
             ["Oakland", "California", "W", "-7"],
             ["Providence", "Rhode Island", "E", "-4"],
             ["Reno", "Nevada", "W", "-7"],
             ["Saskatoon", "Saskatchewan", "W", "-6"],
             ["Sioux Falls", "South Dakota", "W", "-5"],
             ["San Juan", "Puerto Rico", "E", "-4"],
             ["Springfield", "Missouri", "E", "-5"],
             ["Tacoma", "Washington", "W", "-7"],
             ["Toledo", "Ohio", "E", "-4"],
             ["Tucson", "Arizona", "W", "-6"],
             ["Wichita", "Arkansas", "W", "-5"]]
match_ids = read_match_ids("Game_ids.txt")
home_ids = read_str("Home.txt")
away_ids = read_str("Away.txt")
home_scores = read_int("home_scores.txt")
away_scores = read_int("away_scores.txt")
home_xGs = read_float("home_xG.txt")
away_xGs = read_float("away_xG.txt")
home_shots = read_int("home_shots.txt")
away_shots = read_int("away_shots.txt")
home_corners = read_int("home_corner.txt")
away_corners = read_int("away_corner.txt")
home_pk_goals = read_int("home_pk_goals.txt")
away_pk_goals = read_int("away_pk_goals.txt")
home_pk_shots = read_int("home_pk_shots.txt")
away_pk_shots = read_int("away_pk_shots.txt")
home_ToPs = read_float("home_ToP.txt")
# ------------------------------------------------------

while True:
    new_run()
