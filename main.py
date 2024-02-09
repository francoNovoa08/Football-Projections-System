def new_run():
    print("Function list: ")
    print("Program_info - 1\n"
          "Display_stats - 2\n"
          "simple_regular_season - 3\n")
    user_input = get_input("Enter run ID: ")
    if user_input == 1:
        program_info()
    if user_input == 2:
        display_stats()
    if user_input == 3:
        simple_regular_season()


def program_info():
    info_index = int(input("Enter function to receive information: "))
    if info_index == 1:
        print("Display_stats - Access the following NSL team data: city, state, conference, timezone_UTC, name\n")
    elif info_index == 2:
        print(
            "simple_regular_season - Access simple data of the regular season (only accounting for win (3 points)/loss (0 points)/draw (1 point). Ranking and stat. available\n"
            "ranking - Display a ranking of teams based on wins, losses, and draws\n"
            "Head-to-head stats - Compare two teams based on wins, losses, and draws\n"
            "team match finder - Find match ids of games between 2 teams")


def display_stats():
    team_id = str(input("Enter team ID: "))
    team_id = team_id.upper()
    stat = get_input("Enter index (city = 0, state = 1, conference = 2, timezone = 3, name = 4: ")
    if team_id in Team_IDs:
        team_index = Team_IDs.index(team_id)
        print(Team_data[team_index][stat])


def simple_regular_season():
    match_ids = read_match_ids("Game_ids.txt")
    home_ids = read_team_ids("Home.txt")
    away_ids = read_team_ids("Away.txt")
    home_scores = read_scores("home_scores.txt")
    away_scores = read_scores("away_scores.txt")
    team_stats = build_team_stats(match_ids, home_ids, away_ids, home_scores, away_scores)
    index = get_input("Enter index (ranking = 0, head-to-head stats = 1, team_match_finder = 2): ")
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


# ------------------------------------------------------
def read_match_ids(file_path):
    with open(file_path, "r") as file:
        return [line.strip().replace("game_2023_", "") for line in file]


def read_team_ids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def read_scores(file_path):
    with open(file_path, 'r') as file:
        return [int(line.strip()) for line in file]


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
        print(f"{rank}. Team ID: {team_id}, Points: {stats['points']}, Wins: {stats['wins']}, Draws: {stats['draws']}, Losses: {stats['losses']}")
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
    team_1_points = 3*team_1_wins + team_1_draws
    team_2_points = 3*team_2_wins + team_2_draws
    print(f"Team {team_id_1}: Points - "+str(team_1_points)+f", Wins - {team_1_wins}, Draws - {team_1_draws}, Losses - {team_1_losses}")
    print(f"Team {team_id_2}: Points - "+str(team_2_points)+f", Wins - {team_2_wins}, Draws - {team_2_draws}, Losses - {team_2_losses}")
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

        if (home_team_id == team_id_1 and away_team_id == team_id_2) or (home_team_id == team_id_2 and away_team_id == team_id_1):
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
#------------------------------------------------------


def get_input(prompt, input_type=int):
    while True:
        try:
            user_input = input_type(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"An error has occurred: {e}")
#------------------------------------------------------
#Team_id = [city, state, conference, timezone_UTC, name]
#city[0], state[1], conference[2], timezone_UTC[3, name[4]


Team_IDs = ["ALB", "ANC", "AUG", "BAK", "BOI", "CHM", "DES", "DOV", "EUG", "FAR", "FOR", "JAC",
            "LAR", "LEX", "LRO", "MAN", "MOB", "OAK", "PRO", "REN", "SAS", "SFS", "SJU", "SPOR",
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
#------------------------------------------------------
new_run()
