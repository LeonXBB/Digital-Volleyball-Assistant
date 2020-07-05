import time
from py.match.match_config import *

def try_loading_closest_match():

    import DVA
    from DVA import Request, logs, user_id, frontend_references as gui

    if not logs[1].get(2, 'MatchData', True).get('exists'):
        Request(['MatchData', None, [user_id]])

    if logs[1].get(2, 'MatchData', True).get('record').split('#')[5] != 'No Matches!':
        return True
    else:
        return False


def get_time_instructions(match_data, mode='launch'):

    # check if it's court enrty time yet. If no, return 'court_entry_interval'
    # If yes, check if it's coin toss results entry time. if no, return 'coin_toss_interval'. If yes, return 'coin_toss_window'

    match_start_time = []
    match_start_time.extend(match_data[0][1].split()[0].split('-'))
    match_start_time.extend(match_data[0][1].split()[1].split(':'))
    match_start_time.extend([0, 0, 1, -1])
    match_start_time = [int(x) for x in match_start_time]
    match_start_time = time.mktime(tuple(match_start_time))

    minutes = str((match_start_time - time.time()) / 60).split('.')[0]
    seconds = str(int(match_start_time - time.time() - int(minutes) * 60))

    if mode == 'launch':
    
        if match_start_time - time.time() <= (time_between_court_entry_and_coin_tossing + time_between_coin_tossing_and_set_start) * 60:
    
            if match_start_time - time.time() <= time_between_coin_tossing_and_set_start * 60:
    
                return 'coin_toss_window', ':'.join([minutes, seconds])

            minutes = str((match_start_time - time.time() - time_between_court_entry_and_coin_tossing * 60) / 60).split('.')[0]
            seconds = str(int(match_start_time - time.time() - time_between_court_entry_and_coin_tossing * 60 - int(minutes) * 60))

            return 'coin_toss_interval', ':'.join([minutes, seconds])

        minutes = str((match_start_time - time.time() - (time_between_court_entry_and_coin_tossing + time_between_coin_tossing_and_set_start) * 60) / 60).split('.')[0]
        seconds = str(int(match_start_time - time.time() - (time_between_court_entry_and_coin_tossing + time_between_coin_tossing_and_set_start) * 60 - int(minutes) * 60))

        return 'court_entry_interval', ':'.join([minutes, seconds])

    elif mode == 'match_start':

        if match_start_time - time.time() <= 0:
            return 'match_window'
        else:
            return 'match_interval', ':'.join([minutes, seconds])

    elif mode == 'set_start':

        from DVA import match

        if match.sets[-1].end_time_epoch + time_between_sets * 60 - time.time() <= 0:
            return 'set_window'
        else:
            minutes = str((match.sets[-1].end_time_epoch + time_between_sets * 60 - time.time()) / 60).split('.')[0]
            seconds = str(int(match.sets[-1].end_time_epoch + time_between_sets * 60 - time.time() - int(minutes) * 60))
            return 'set_interval', ':'.join([minutes, seconds])


def calculate_name_string():

    from DVA import match

    people = []

    for team in [match.home_team, match.away_team]:
        people.extend(team.players)
        people.extend(team.staff)
        if team.head_coach != '':
            people.append(team.head_coach)
    people.extend(match.officials)

    for person in people:
        person.name_string = str(person.last_name) + ' ' + str(person.first_name)


def load_events_from_log():
        
        def sort_event_array(elem):
            return elem[3]
        
        import py.match.events
        from DVA import logs, match_events_dispatch

        events = []
        for event in logs[1].get_all(2, ['MatchPoolSend', 'MatchPoolReceive']):
          
            event_id = eval(event[1].split('#')[6])
            event_is_active = eval(event[1].split('#')[4])[2]

            for same_event in logs[1].get_all(2, ['MatchPoolSend', 'MatchPoolReceive']):
                if eval(same_event[1].split('#')[6]) == event_id:
                    event_is_active = eval(same_event[1].split('#')[4])[2]

            event_type = eval(event[1].split('#')[4])[0]
            event_restoration_data = eval(event[1].split('#')[4])[1]

            for __event__ in events:
                if __event__[3] == event_id:
                    events.remove(__event__)
                    break
            events.append([getattr(py.match.events, event_type), event_type, event_restoration_data, event_id, event_is_active])

        events.sort(key=sort_event_array)

        last_active_event_id = 0
        for event in events:
            if event[4]:
                last_active_event_id = event[3]

        for event in events:
            if event[4]:
                match_events_dispatch.run(event[0], event[2], 'RESTORED', is_last=event[3] == last_active_event_id, is_quite=False)

            else:
                match_events_dispatch.run(event[0], event[2], 'RESTORED', is_last=event[3] == last_active_event_id, is_quite=True)

# statistics?
