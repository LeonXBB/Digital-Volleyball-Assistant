import os

def is_empty(log_address):
    import re

    if os.stat(log_address).st_size == 0:
        return True

    content = open(log_address, 'r').read()
    if re.search(r'^\s*$', content):
        return True

    return False


def load_log(log_name, save_to_file):

    from DVA import logs
    from py.objects import Log, Request
    import py.match.events

    LOADING_INSTRUCTIONS = [
        'index 0 does not mean anything',
        'pass',
        "Request(data, 'RESTORED')"
    ]

    if os.path.isfile(os.getcwd() + '/logs/' + log_name + '.txt'):
        with open(os.getcwd() + '/logs/' + log_name + '.txt', 'r', encoding='utf-8') as f:
            if not is_empty(os.getcwd() + '/logs/' + log_name + '.txt'):
                logs.append(Log(log_name, 'RESTORED', save_to_file))
                for line in f:
                    if not line.isspace():
                        data = line.split('#')
                        exec(LOADING_INSTRUCTIONS[len(logs)])
            else:
                logs.append(Log(log_name, 'NEW', save_to_file))
    
    else:
        logs.append(Log(log_name, 'NEW', save_to_file))


def set_range_to_sliders():

    from DVA import match, frontend_references as gui

    RANGE = [
        (len(match.team_A.players) - len(match.team_A.disqualified_players) - len(match.team_A.expulsed_players)),
        (len(match.team_B.players) - len(match.team_B.disqualified_players) - len(match.team_B.expulsed_players)),
        (len(match.team_A.staff) - len(match.team_A.disqualified_staff)),
        (len(match.team_B.staff) - len(match.team_B.disqualified_staff)),
        (len(match.team_A.players) - len(match.team_A.disqualified_players) - len(match.team_A.expulsed_players)) / 2,
        (len(match.team_B.players) - len(match.team_B.disqualified_players) - len(match.team_B.expulsed_players)) / 2,
        (len(match.team_A.players) - len(match.team_A.disqualified_players) + len(match.team_A.staff) + (1 if match.team_A.head_coach != '' else 0)),
        (len(match.team_B.players) - len(match.team_B.disqualified_players) + len(match.team_B.staff) + (1 if match.team_B.head_coach != '' else 0)),
            ] # according to the order in dictionary

    SCROLLBARS = [gui.get('MatchWindowRefereeTeamSetUpTeamAPLAYERSSLIDER'), 
                    gui.get('MatchWindowRefereeTeamSetUpTeamBPLAYERSSLIDER'),
                    gui.get('MatchWindowRefereeTeamSetUpTeamASTAFFSLIDER'),
                    gui.get('MatchWindowRefereeTeamSetUpTeamBSTAFFSLIDER'),
                    gui.get('MatchWindowRefereeSubstitutionsTabTeamASLIDER'), 
                    gui.get('MatchWindowRefereeSubstitutionsTabTeamBSLIDER'), 
                    gui.get('MatchWindowRefereeSanctionsTabTeamASLIDER'), 
                    gui.get('MatchWindowRefereeSanctionsTabTeamBSLIDER')]

    for i in range(len(SCROLLBARS)):
        SCROLLBARS[i].range = (0, RANGE[i] - 1)
        SCROLLBARS[i].value_normalized = 1


def authorization_successful():  # TODO This function should deal with calculating what to load depending on user's status, if they have a match assigned to them, what is theirs status in it, and if it's starting

        import DVA
        from DVA import logs
        from gfx.frontend import PopUpWindow
        from py.match.core import try_loading_closest_match, load_events_from_log, get_time_instructions
        from py.match.events import EventDispatcher, MatchStart

        if try_loading_closest_match():
            
            DVA.match_events_dispatch = EventDispatcher()

            match_data = eval(logs[1].get(2, 'MatchData', True).get('record').split('#')[5])

            DVA.match_events_dispatch.run(MatchStart, match_data, 'NEW')  # TODO change according to status
            load_events_from_log()

            if get_time_instructions(match_data)[0] == 'court_entry_interval' and DVA.match.status == 'Awaiting':  # TODO change according to status
                PopUpWindow().show_interval_window([0, 1, get_time_instructions(match_data)[1]])
            elif get_time_instructions(match_data)[0] == 'coin_toss_interval' and DVA.match.status == 'Awaiting': # TODO change according to status
                PopUpWindow().show_interval_window([1, 2, get_time_instructions(match_data)[1]])
        
        else:  # TODO else load profile
            pass


def get_people_list(team, with_players=True, with_staff=False, with_expulsed_players=False, with_disqualified_staff=False, with_disqualified_players=False, with_liberos=True, with_absent_players=False, with_numbers=False, start_index=None, end_index=None, rv_format='bin'):

    from meta.localization import statuses
    from meta.app_config import language_code

    people_list = []

    if with_staff:
            
        if team.head_coach != '' and (team.head_coach not in team.disqualified_staff or with_disqualified_staff):
            people_list.append(team.head_coach)
        for _staff_ in team.staff:
            if _staff_ not in team.disqualified_staff or with_disqualified_staff: people_list.append(_staff_)

    
    if with_players:
        for i in range((start_index if start_index is not None else 0), (end_index if (end_index is not None and end_index < len(team.players)) else len(team.players))):
            if team.players[i] not in team.disqualified_players or with_disqualified_players: 
                if team.players[i] not in team.expulsed_players or with_expulsed_players:
                    if not team.players[i].libero or with_liberos:
                        if team.players[i].present or with_absent_players:
                            people_list.append(team.players[i])

    if rv_format == 'bin':
        return people_list

    elif rv_format == 'str':
        
        prefixes = ['' for _ in range(len(people_list))]
        if with_numbers:
            for i in range(len(people_list)):
                if people_list[i] in team.players:
                    prefixes[i] = (str(people_list[i].number) + ' ')
                else:
                    prefixes[i] = people_list[i].Status.join(' / ')

        rv = [prefixes[i] + people_list[i].name_string for i in range(len(people_list))]
        return rv
