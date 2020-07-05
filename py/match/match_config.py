# Time
time_between_court_entry_and_coin_tossing = 15  # in minutes
time_between_coin_tossing_and_set_start = 15
time_between_sets = 3

# People
players_in_team = 6
max_amount_players = 14
max_amount_staff = 4  # excluding head coach
max_amount_liberos = 2
players_more_or_equal_to_x_liberos_at_least_y = [13, 2]  # if there is list[0] players, there should be at least list[1] liberos
max_shirt_number = 20
libero_can_be_captain = False

# Sets
sets_to_win = 3
min_points_to_win_regular_set = 25
min_points_to_win_final_set = 15
min_difference_to_end_regular_set = 2
min_difference_to_end_final_set = 2

# Rotation
rotation_enabled = True  # True or False
rotation_direction = 'Clockwise'  # 'Clockwise' or 'Anti-clockwise'
tie_break_mid_set_rotation = True
tie_break_mid_set_rotation_score = 8

# Positioning
position_starting_point = [1, 1] # one step ahead
position_direction = 'Anti-Clockwise' # same as rotation_direction

# Time Outs
time_outs_regular_set = 2
time_outs_final_set = 2
length_of_time_outs_regular_set = 30  # in seconds
length_of_time_outs_final_set = 30
technical_time_outs_enabled = False
score_for_technical_time_outs_regular_set = [8, 16]
length_of_technical_time_outs_regular_set = 30
score_for_technical_time_outs_final_set = []
length_of_technical_time_outs_final_set = 30

# Substitutions
max_substitutions_regular_set = 6
max_substitutions_final_set = 6
only_reverse_substitutions = True  # if the player has left the court, they can only substitute back their substitutё
reverse_substitutions_amount_regular_set = 1
reverse_substitutions_amount_final_set = 1
libero_allowed_to_substitute = False
substitutions_requests_from_a_team_during_one_play = 1

# Warnings and sanctions
expulsions_instead_of_penalties_on_set_point = True
warning_amount_limitations_person = 1
warning_amount_limitations_team = 1
penalty_amount_limitations_person = 1
penalty_amount_limitations_team = None
expulsion_amount_limitations_person = 1
expulsion_amount_limitations_team = None
disqualification_amount_limitations_person = 1
disqualification_amount_limitations_team = None
delay_warning_amount_limitations_team = 1
delay_penalty_amount_limitations_team = None
SANCTIONS_LEVELS = [
    'nothing',
    'delay_warning',
    'delay_penalty',
    'warning',
    'penalty',
    'expulsion',
    'disqualification'
    ]

# Scoring
points_for_score_same_team = 1
points_for_score_another_team = 0
points_for_mistake_same_team = 0
points_for_mistake_another_team = 1
points_for_warning_same_team = 0
points_for_warning_another_team = 0
points_for_penalty_same_team = 0
points_for_penalty_another_team = 1
points_for_expulsion_same_team = 0
points_for_expulsion_another_team = 0
points_for_disqualification_same_team = 0
points_for_disqualification_another_team = 0
points_for_delay_warning_same_team = 0
points_for_delay_warning_another_team = 0
points_for_delay_penalty_same_team = 0
points_for_delay_penalty_another_team = 1
