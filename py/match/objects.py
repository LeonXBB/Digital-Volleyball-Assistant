from py.match.match_config import *

class Match:

    match_id = 0
    match_sex = '' # 'M' \ 'F'
    match_country_code = ''
    competition_name = ''
    competition_stage = ''
    competition_age = '' # 'S' / 'J' / 'Y'
    scheduled_date = 0
    scheduled_time = 0
    city = ''
    street_address = ''
    start_time = 0
    end_time = 0
    home_team = ''
    team_A = ''
    serving_team = ''
    left_team = ''
    away_team = ''
    team_B = ''
    receiving_team = ''
    right_team = ''
    set_score = [0, 0]
    referee_notes = ''
    officials = []
    sets = []
    status = '' # scheduled, awaiting, ongoing, finished

    SetScoreA = ''
    SetScoreB = ''

    def __init__(self, match_data):

        self.match_id = match_data[0]
        self.match_sex = ''
        self.match_country_code = ''
        self.match_number = ''
        self.competition_name = match_data[2]
        self.competition_stage = ''
        self.competition_age = ''
        self.scheduled_date = match_data[1].split(' ')[0]
        self.scheduled_time = match_data[1].split(' ')[1]
        self.city = ''
        self.street_address = match_data[3]

    def load_match_data(self, match_data):

        import DVA
        from py.match.core import calculate_name_string

        DVA.match.home_team = Team(match_data[2])
        DVA.match.away_team = Team(match_data[3])
        for i in range(0, len(match_data[6]), 3):
            DVA.match.home_team.head_coach = HeadCoach(match_data[6][i:i + 3])
        for i in range(0, len(match_data[7]), 3):
            DVA.match.away_team.head_coach = HeadCoach(match_data[7][i:i + 3])
        for i in range(0, len(match_data[8]), 3):
            DVA.match.home_team.staff.append(Staff(match_data[8][i:i + 3]))
        for i in range(0, len(match_data[9]), 3):
            DVA.match.away_team.staff.append(Staff(match_data[9][i:i + 3]))
        for i in range(0, len(match_data[4]), 3):
            DVA.match.home_team.players.append(Player(match_data[4][i:i + 3]))
        for i in range(0, len(match_data[5]), 3):
            DVA.match.away_team.players.append(Player(match_data[5][i:i + 3]))
        for i in range(0, len(match_data[1]), 3):
            DVA.match.officials.append(Official(match_data[1][i:i + 3]))

        calculate_name_string()

    def start_match_as_referee(self, match_data):

        from DVA import sm, match_events_dispatch, frontend_references as gui

        sm.current = gui.get('MatchWindowReferee').name

        self.status = 'Awaiting'

        self.load_match_data(match_data)

        for tab in gui.get('MatchWindowRefereeTabPanel').tab_list:
            tab.disabled = True
        gui.get('MatchWindowRefereeTabPanelCoinToss').disabled = False

        gui.get('MatchWindowRefereeCoinTossTabContent').on_load()

    def end_match_as_referee(self):
        
        from DVA import match
        import time

        match.end_time = str(time.localtime()[3]) + ':' + str(time.localtime()[4])
        match.status = 'Finished'


class Set:

    status = ''
    is_tie_break = False
    start_time = 0
    end_time = 0
    end_time_epoch = 0

    winner = ''

    PointScoreA = ''
    PointScoreB = ''
    '''time_outs = []
    substitutions = []
    score = [0, 0]
    set_formatted_players = [[], []]''' # all moved to self.start()

    def start(self):

        from DVA import match, frontend_references as gui
        import time

        self.time_outs = []
        self.substitutions = []
        self.sanctions = []
        self.score = [0, 0]
        self.points = []
        self.set_formatted_players = [[], []]
        self.technical_time_outs_used = []

        match.status = 'Ongoing'
        self.status = 'Ongoing'

        if len(match.sets) == 0:
            self.start_time = match.start_time
        else:
            self.start_time = str(time.localtime(match.sets[-1].end_time_epoch + time_between_sets * 60)[3]) + ':' + str(time.localtime(match.sets[-1].end_time_epoch + time_between_sets * 60)[4])

        if len(match.sets) == sets_to_win * 2 - 2:
            self.is_tie_break = True
            for _ in range(len(score_for_technical_time_outs_final_set)):
                self.technical_time_outs_used.append(False)
        else:
            for _ in range(len(score_for_technical_time_outs_regular_set)):
                self.technical_time_outs_used.append(False)

        self.set_formatted_players[0].extend(match.left_team.players)
        self.set_formatted_players[1].extend(match.right_team.players)

        match.sets.append(self)

    def end(self):

        from DVA import match
        import time

        self.status = 'Finished'
        self.end_time = str(time.localtime()[3]) + ':' + str(time.localtime()[4])
        self.end_time_epoch = time.time()

        if match.sets[-1].score[0] > match.sets[-1].score[1]:
            self.winner = match.left_team.long_name
        else:
            self.winner = match.right_team.long_name

        match.team_A.expulsed_players, match.team_B.expulsed_players = [], []


class Team:
    team_server_id = 0
    long_name = ''
    short_name = ''

    head_coach = ''
    captain = ''

    protest = ''

    Name = ''
    PlayersList = ''
    StaffList = ''
    SetUp = ''
    SetUpStaff = ''
    LineUpSetUp = ''
    LineUp = ''
    Serve = ''

    # players = [] # Moved to self.__init__
    # expulsed_players = []
    # disqualified_players = []
    # staff = []

    def __init__(self, match_data):

        from DVA import match
        from gfx.visual_elements import TeamName

        self.team_server_id = match_data[0]
        self.long_name = match_data[1]
        self.short_name = match_data[2]

        self.players = []
        self.expulsed_players = []
        self.disqualified_players = []
        self.disqualified_staff = []
        self.staff = []

    def rotate(self):

        self.LineUp.rotate()

    def rotate_backwards(self):
        
        self.LineUp.rotate_backwards()

    def get_sanction_level(self):

        from DVA import match

        team_sanction_level = 'nothing'
        sanction_count = 0

        for _set_ in match.sets:
            for sanction in _set_.sanctions:
                if sanction.team == self.long_name and sanction.type.startswith('delay'):
                        team_sanction_level = sanction.type
        
        for _set_ in match.sets:
            for sanction in _set_.sanctions:
                if sanction.team == self.long_name and sanction.type == team_sanction_level:
                        sanction_count += 1

        return team_sanction_level, sanction_count


class Person:

    server_id = 0
    first_name = ''
    last_name = ''
    status = ''

    name_string = ''

    def __init__(self, match_data):
        self.server_id = match_data[0]
        self.last_name = match_data[1]
        self.first_name = match_data[2]
        self.status = match_data[3]

    def get_sanction_level(self):
        
        from DVA import match
        
        person_sanction_level = 'nothing'
        sanction_count = 0

        for _set_ in match.sets:
            for sanction in _set_.sanctions:
                if sanction.person == self.name_string:
                    person_sanction_level = sanction.type

        for _set_ in match.sets:
            for sanction in _set_.sanctions:
                if sanction.person == self.name_string and sanction.type == person_sanction_level:
                    sanction_count += 1

        return person_sanction_level, sanction_count


class HeadCoach(Person):

    # sanctions = []  # list of events # Moved to self.__init__ TODO finish every function
    Name = ''

    def __init__(self, data):

        data.append('Head Coach')
        super().__init__(data)

    def team_set_up(self, team, button):

        team.SetUp.save(team, button)

    def team_set_up_staff(self, team, button):

        team.SetUpStaff.save(team, button)

    def line_up_set_up(self, team, letter):
        
        team.LineUpSetUp.save(letter)
    
    def substitution(self, team, player_in, player_out, request_counter, is_forced):
        
        from DVA import match_events_dispatch
        from py.match.events import SubstitutionMade

        match_events_dispatch.run(SubstitutionMade, [team, player_in, player_out, request_counter, is_forced], 'NEW')

    def time_out(self, button, team):

        from DVA import match, match_events_dispatch, frontend_references as gui
        from py.match.events import TimeOutTaken

        match_events_dispatch.run(TimeOutTaken, [team.long_name, len(match.sets), match.sets[-1].score, button, False], 'NEW')

    def declare_protest(self, team):
        
        from DVA import match_events_dispatch
        from py.match.events import ProtestDeclared

        match_events_dispatch.run(ProtestDeclared, [team], 'NEW')

    def write_protest(self, team):
        
        from DVA import match_events_dispatch, match, frontend_references as gui
        from py.match.events import ProtestWritten

        match_events_dispatch.run(ProtestWritten, [team, gui.get('MatchWindowRefereeProtestsTabTeam' + ('A' if team == match.left_team else 'B') + 'TextInput').text], 'NEW')


class Staff(Person):

    # sanctions = [] Moved to self.__init__
    Name = ''
    Status = ''

    def __init__(self, data):
        data.append('Staff')
        super().__init__(data)


class Player(Person):

    present = False
    number = 0
    position = 0
    captain = False
    temp_captain = False
    libero = False

    Name = ''
    Number = ''

    def __init__(self, data):

        data.append('Player')
        self.statistics = []
        super().__init__(data)

    def point(self):

        from py.match.events import Point_sReceived
        from DVA import match_events_dispatch, match

        match_events_dispatch.run(Point_sReceived, ['score', self], 'NEW')

    def mistake(self):

        from py.match.events import Point_sReceived
        from DVA import match_events_dispatch, match

        match_events_dispatch.run(Point_sReceived, ['mistake', self], 'NEW')


class Official(Person):

    def __init__(self, data):
        data.append('Official')
        super().__init__(data)
    
    def coin_toss(self):
        
        from DVA import match_events_dispatch, frontend_references as gui
        from py.match.events import CoinTossResultsConfirmed

        match_events_dispatch.run(CoinTossResultsConfirmed, [gui.get('MatchWindowRefereeCoinTossTabTeamAButtonA').state,
                                                             gui.get('MatchWindowRefereeCoinTossTabTeamBButtonA').state,
                                                             gui.get('MatchWindowRefereeCoinTossTabTeamAButtonServe').state,
                                                             gui.get('MatchWindowRefereeCoinTossTabTeamBButtonServe').state],
                                  'NEW')

    def sanction(self, sanction_type, person, team):
        
        from py.match.events import SanctionIssued
        from DVA import match_events_dispatch

        match_events_dispatch.run(SanctionIssued, [sanction_type, person, team], 'NEW')


class Point:
    
    def __init__(self, point_create_data, team_index):
        
        from DVA import match

        self.type = point_create_data[0]
        self.team = point_create_data[1]
        self.player = point_create_data[2]
        self.then_score = match.sets[-1].score.copy()
        self.set = len(match.sets)

        self.is_serve_end_point = True
        self.is_team_set_end_point = True

        for i in range(len(match.sets[-1].points) - 1, -1, -1):
            if match.sets[-1].points[i].team == self.team:
                if i == len(match.sets[-1].points) - 1:
                    match.sets[-1].points[i].is_serve_end_point = False
                match.sets[-1].points[i].is_team_set_end_point = False
                break

        match.sets[-1].points.append(self)


class TimeOut:
    
    def __init__(self, time_out_creation_data):

        from DVA import match

        self.is_technical = time_out_creation_data[4]
        self.team = time_out_creation_data[0]
        self.then_score = time_out_creation_data[2]
        self.set = time_out_creation_data[1]
        self.related_button_index = time_out_creation_data[3]

        if time_out_creation_data[2] == match.right_team.long_name:
            self.then_score.reverse()

        match.sets[-1].time_outs.append(self)


class Sanction:
    
    def __init__(self, data):

        from DVA import match

        self.type = data[0]
        self.person = data[1]
        self.team = data[2]

        self.set = len(match.sets)
        self.then_score = match.sets[-1].score.copy()
        if data[0] == match.right_team.long_name:
            self.then_score.reverse()

        match.sets[-1].sanctions.append(self)


class Substitution:
    
    def __init__(self, data):
        
        from DVA import match
       
        self.team = data[0]
        self.then_score = match.sets[-1].score.copy()
        self.player_in = data[1]
        self.player_out = data[2]
        self.set = len(match.sets)

        self.request_counter = data[3]

        if data[0] == match.right_team.long_name:
            self.then_score.reverse()

        match.sets[-1].substitutions.append(self)


class Protest:
    
    def __init__(self, team_name_string):

        from DVA import match

        self.team = team_name_string
        self.set = len(match.sets)
        self.then_score = match.sets[-1].score.copy()

        self.text = ''