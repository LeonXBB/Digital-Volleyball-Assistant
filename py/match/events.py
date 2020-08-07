import py.match
import py.match.match_config, meta.app_config

from py.match.match_config import *
from meta.app_config import *
from gfx.frontend import PopUpWindow

class EventDispatcher:

    def __init__(self):
        
        self.return_command = ''
        self.cancelled_events_ids = []
        self.created_events_ids = []

    def run(self, event, event_data, mode, is_quite=False, is_last=False):

        import DVA
        from DVA import logs, frontend_references as gui

        if not (event == MatchStart and mode == 'RESTORED'):
            event(create_data=event_data, mode=mode, is_quite=is_quite)

        if self.return_command != '':

            if ((mode == 'RESTORED' and is_last) or mode == 'NEW'):

                if mode == 'RESTORED' and is_last and self.return_command == 'gui.get("MatchWindowRefereeMatchTabContent").on_load(mode)':
                    self.return_command = 'gui.get("MatchWindowRefereeMatchTabContent").on_load("NEW")'
                
                elif ((mode == 'RESTORED' and is_last) or mode == 'NEW') and self.return_command.startswith('self.run(SetEnd,'):
                    
                    SetEnd(eval(self.return_command.split(maxsplit=1)[1].split(']')[0] + ']'), is_quite=is_quite)
                    
                    if self.return_command.startswith('self.run(MatchEnd'):   
                        MatchEnd(None, is_quite=is_quite) 
                    
                    self.return_command = 'pass'
                
                elif ((mode == 'RESTORED' and is_last) or mode == 'NEW') and self.return_command.startswith('self.run(MatchEnd'):   

                    if self.return_command.startswith('self.run(MatchEnd'):   
                        MatchEnd(None, is_quite=is_quite) 
                    
                    self.return_command = 'pass'

                elif ((mode == 'RESTORED' and is_last) or mode == 'NEW') and self.return_command.startswith('self.run(TieBreakRotation, None, "'):

                    TieBreakRotation(None, is_quite=is_quite)
                    self.return_command = 'pass'

                elif ((mode == 'RESTORED' and is_last) or mode == 'NEW') and self.return_command.startswith('self.run(TimeOutTaken'):
                    
                    from DVA import match

                    TimeOutTaken([None, len(match.sets), match.sets[-1].score, None, True], is_quite=is_quite)
                    self.return_command = 'pass'
            
                elif ((mode == 'RESTORED' and is_last) or mode == 'NEW') and '?@?' in self.return_command:
                    
                    from DVA import match

                    command_type = self.return_command.split('?@?')[1]
                    command_team = self.return_command.split('?@?')[2]
                    command_person = self.return_command.split('?@?')[3]

                    check_flag = False

                    for team in (match.team_A, match.team_B):
                        if team.long_name == command_team:
                            command_team = team
                    
                    for player in command_team.players:
                        if player.name_string == command_person:
                            command_person = player
                            check_flag = True

                    if self.return_command.split('?@?')[0] != '': exec(self.return_command.split('?@?')[0])
                    if check_flag: Point_sReceived([command_type, command_person, command_team])
                    if self.return_command != '' and '?@?' not in self.return_command: exec(self.return_command)
                    self.return_command = 'pass'

            elif mode == 'RESTORED' and not is_last:

                if isinstance(event, MatchEnd):   
                        MatchEnd(None, is_quite=is_quite) 
                
                else:
                    self.return_command = 'pass'
            
            exec(self.return_command)
            self.return_command = ''

    def back(self):
        
        from DVA import logs

        for i in range(len(logs[0].deep_log) - 1, -1, -1): 

            if logs[0].deep_log[i].is_active and logs[0].deep_log[i].id == self.created_events_ids[-1]:
                                
                logs[0].deep_log[i].__delete__()

                for j in range(len(logs[0].deep_log) - 1, -1, -1): # TieBreakRotation, Technical Timeout, Match/Set Start/End

                    if logs[0].deep_log[j].is_active and len(self.created_events_ids) > 1 and logs[0].deep_log[j].id == self.created_events_ids[-1]:
                                                
                        if logs[0].deep_log[i].type == 'MatchEnd' and logs[0].deep_log[j].type == 'SetEnd': # We technically only need to know the i event, but just to be save 
                            logs[0].deep_log[j].__delete__()
                            logs[0].deep_log[j - 1].__delete__()
                        elif logs[0].deep_log[i].type == 'SetEnd' and logs[0].deep_log[j].type == 'Point_sReceived':
                            logs[0].deep_log[j].__delete__()
                        elif logs[0].deep_log[i].type == 'SetStart' and logs[0].deep_log[j].type == 'LineUpConfirmed':
                            logs[0].deep_log[j].__delete__()
                        elif logs[0].deep_log[i].type == 'TieBreakRotation' and logs[0].deep_log[j].type == 'Point_sReceived':
                            logs[0].deep_log[j].__delete__()
                        elif logs[0].deep_log[i].type == 'TimeOutTaken' and logs[0].deep_log[i].create_data[4] and logs[0].deep_log[j].type == 'Point_sReceived':
                            logs[0].deep_log[j].__delete__()
                        elif logs[0].deep_log[i].type == 'CoinTossResultsConfirmed' and logs[0].deep_log[j].type == 'MatchStart':
                            logs[0].deep_log[j].__delete__()
                        elif logs[0].deep_log[i].type == 'Point_sReceived' and logs[0].deep_log[j].type == 'SanctionIssued' and logs[0].deep_log[i].create_data[0] == logs[0].deep_log[j].create_data[0]:
                            logs[0].deep_log[j].__delete__()

                        break
                break

    def forward(self):
        
        from DVA import match, logs

        for i in range(len(logs[0].deep_log) - 1, -1, -1): 
            
            if (not logs[0].deep_log[i].is_active) and logs[0].deep_log[i].id == self.cancelled_events_ids[-1]:
                logs[0].deep_log[i].restore()
                for j in range(len(logs[0].deep_log) - 1, -1, -1): # TieBreakRotation, Technical Timeout, Match/Set Start/End
                    
                    if (not logs[0].deep_log[j].is_active) and len(self.cancelled_events_ids) > 0 and logs[0].deep_log[j].id == self.cancelled_events_ids[-1]:

                        #if logs[0].deep_log[i].type == 'SetEnd' and logs[0].deep_log[j].type == 'MatchEnd': # We technically only need to know the i event, but just to be save 
                        #    logs[0].deep_log[j].restore()
                        if logs[0].deep_log[i].type == 'Point_sReceived' and logs[0].deep_log[j].type == 'SetEnd':
                            logs[0].deep_log[j].restore()
                            if logs[0].deep_log[j + 1].type == 'MatchEnd':
                                logs[0].deep_log[j + 1].restore()
                        elif logs[0].deep_log[i].type == 'LineUpConfirmed' and logs[0].deep_log[j].type == 'SetStart':
                            logs[0].deep_log[j].restore()
                        elif logs[0].deep_log[i].type == 'Point_sReceived' and logs[0].deep_log[j].type == 'TieBreakRotation':
                            logs[0].deep_log[j].restore()
                        elif logs[0].deep_log[i].type == 'Point_sReceived'and logs[0].deep_log[j].type == 'TimeOutTaken' and logs[0].deep_log[j].create_data[4] :
                            logs[0].deep_log[j].restore()
                        elif logs[0].deep_log[i].type == 'MatchStart' and logs[0].deep_log[j].type == 'CoinTossResultsConfirmed':
                            logs[0].deep_log[j].restore()
                        elif logs[0].deep_log[i].type == 'SanctionIssued' and logs[0].deep_log[j].type == 'Point_sReceived' and logs[0].deep_log[i].create_data[0] == logs[0].deep_log[j].create_data[0]:
                            logs[0].deep_log[j].restore()

                    #break #TODO fix this???

                break


class Event():
      
    type = ''
    
    def __init__(self, create_data, mode='NEW', is_quite=False, *args):

        from DVA import logs, match_events_dispatch
        from py.objects import Request

        self.id = len(logs[0].deep_log)

        self.create_data = create_data

        self.type = type(self).__name__

        if not is_quite:

            self.is_active = True
            self.mode = mode

            match_events_dispatch.created_events_ids.append(self.id)

            self.create()

            if self.mode == 'NEW':
                Request(('MatchPoolSend', self.id, (self.type, self.create_data, self.is_active)))
        
        else:

            self.is_active = False
            self.mode = 'RESTORED'

            match_events_dispatch.cancelled_events_ids.insert(0, self.id)

        logs[0].add(self.__dir__(), self, self.mode)
        logs[0].deep_add(self)

    def __delete__(self):

        from DVA import logs, match_events_dispatch
        from py.objects import Request

        match_events_dispatch.cancelled_events_ids.append(self.id)
        match_events_dispatch.created_events_ids = match_events_dispatch.created_events_ids[:-1]

        self.is_active = False

        self.delete()

        Request(('MatchPoolSend', self.id, (self.type, self.create_data, self.is_active)))

    def restore(self):
        
        from DVA import match_events_dispatch
        from py.objects import Request

        self.mode = 'RESTORED'
        self.is_active = True

        self.create()

        Request(('MatchPoolSend', self.id, (self.type, self.create_data, self.is_active)))

        match_events_dispatch.created_events_ids.append(self.id)
        match_events_dispatch.cancelled_events_ids = match_events_dispatch.cancelled_events_ids[:-1]

    def __dir__(self):
        return '#' + str(self.id) + '#' + self.type + '#' + str(self.create_data) + '#' + str(self.is_active)


class MatchStart(Event):

    def create(self):

        import DVA
        from DVA import logs, frontend_references as gui
        from py.match.objects import Match
        from gfx.visual_elements import MatchSetScore

        if self.mode == 'NEW':

            DVA.match = Match(self.create_data[0])
            DVA.match.data = self.create_data
            DVA.match.start_match_as_referee(self.create_data) # TODO change according on status

            self.create_data = ''

        if logs[1].get(4, "('MatchStart', '', True)", False).get('exists'):
            self.mode = 'RESTORED'

    def delete(self): 
       
        import os

        self.match = ''
        os.close()


class MatchEnd(Event):
    
    def create(self):
        
        from DVA import sm, match, frontend_references as gui
        from gfx.frontend import PopUpWindow

        match.end_match_as_referee() # TODO change according to status
        flag = False

        for team in (match.team_A, match.team_B):
            if team.long_name != match.sets[-1].winner and team.protest != '':
                gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelProtests'))                
                gui.get('MatchWindowRefereeProtestsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab').disabled = True
                gui.get('MatchWindowRefereeProtestsTabTeam' + ('A' if team == match.left_team else 'B') + 'Tab').disabled = False

                gui.get('MatchWindowRefereeProtestsTabHeader').switch_to(gui.get('MatchWindowRefereeProtestsTabTeam' + ('A' if team == match.left_team else 'B') + 'Tab'))
                gui.get('MatchWindowRefereeProtestsTabContent').on_load(('A' if team == match.left_team else 'B'), 'write', team)
                
                gui.get('MatchWindowRefereeTabPanelSanctions').disabled = True
                gui.get('MatchWindowRefereeTabPanelSubstitutions').disabled = True
                gui.get('MatchWindowRefereeTabPanelMatch').disabled = True
                
                flag = True
        
        if not flag or self.mode == 'RESTORED':
            sm.switch_to(gui.get('EndWindowReferee'))
            gui.get('EndWindowReferee').on_load()

    def delete(self):

        from DVA import sm, match, frontend_references as gui

        match.status = 'Ongoing'
        match.end_time = ''

        sm.switch_to(gui.get('MatchWindowReferee'))


class SetStart(Event):

    def create(self):

        from DVA import match_events_dispatch, match, frontend_references as gui
        from py.match.objects import Set
        from gfx.visual_elements import TeamServe, TeamLineUp, SetPointScore, MatchSetScore

        if len(match.sets) == 0 or match.sets[-1].status == 'Finished':
            Set().start()
            gui.get('MatchWindowRefereeMatchTabContent').load_time_out_buttons()

        if self.mode == 'NEW':
            self.create_data = [len(match.sets), match.sets[-1].start_time]

        elif self.mode == 'RESTORED':
            if self.create_data is not None:
                match.sets[-1].status = 'Ongoing'
                match.sets[-1].start_time = self.create_data[1]
                
                gui.get("MatchWindowRefereeMatchTabContent").on_load('RESTORED')

        '''if match.left_team.Serve == '':'''
        match.left_team.Serve = TeamServe([gui.get('MatchWindowRefereeMatchTabTeamAServeBall')])
        match.right_team.Serve = TeamServe([gui.get('MatchWindowRefereeMatchTabTeamBServeBall')])

        if match.serving_team == match.left_team:
            match.left_team.Serve.params[0] = 1
            match.right_team.Serve.params[0] = 0
            match.left_team.Serve.elements[0].opacity = 1
            match.right_team.Serve.elements[0].opacity = 0
        else:
            match.left_team.Serve.params[0] = 0
            match.right_team.Serve.params[0] = 1
            match.left_team.Serve.elements[0].opacity = 0
            match.right_team.Serve.elements[0].opacity = 1
        
        '''else:
            match.left_team.Serve._switch_(match.right_team.Serve, switch_params=False)'''

        match.sets[-1].PointScoreA = SetPointScore([gui.get('MatchWindowRefereeMatchTabTeamAPointScore')])
        match.sets[-1].PointScoreB = SetPointScore([gui.get('MatchWindowRefereeMatchTabTeamBPointScore')])
        match.sets[-1].PointScoreA.zero()
        match.sets[-1].PointScoreB.zero()

        match.SetScoreA = MatchSetScore(gui.get('MatchWindowRefereeMatchTabTeamBSetScore'))
        match.SetScoreB = MatchSetScore(gui.get('MatchWindowRefereeMatchTabTeamASetScore'))
        match.SetScoreA.params[2] = str(match.set_score[0])
        match.SetScoreB.params[2] = str(match.set_score[1])
        match.SetScoreA.__load__()
        match.SetScoreB.__load__()

        for team in (match.left_team, match.right_team):
            if team.captain not in team.players[:players_in_team]:
                match_events_dispatch.return_command = f'PopUpWindow().show_captain_chooser("{team.long_name}")'

    def delete(self):

        from DVA import match, frontend_references as gui
        from gfx.visual_elements import TeamServe, TeamLineUp, SetPointScore

        gui.get('MatchWindowRefereeMatchTabContent').load_time_out_buttons()        
        for i in range(len(match.sets[-1].time_outs)):
            if match.sets[-1].time_outs[i].team == match.left_team.long_name:
                gui.get('MatchWindowRefereeMatchTabTeamATimeOuts')[match.sets[-1].time_outs[i].related_button_index].disabled == True
            else:
                gui.get('MatchWindowRefereeMatchTabTeamBTimeOuts')[match.sets[-1].time_outs[i].related_button_index].disabled == True

        match.left_team.Serve = TeamServe([gui.get('MatchWindowRefereeMatchTabTeamAServeBall')])
        match.right_team.Serve = TeamServe([gui.get('MatchWindowRefereeMatchTabTeamBServeBall')])

        if len(match.sets) > 1:
            if match.sets[-2].points[-1].team == match.left_team.long_name:
                match.left_team.Serve.params[0] = 1
                match.right_team.Serve.params[0] = 0
                match.left_team.Serve.elements[0].opacity = 1
                match.right_team.Serve.elements[0].opacity = 0
            else:
                match.left_team.Serve.params[0] = 0
                match.right_team.Serve.params[0] = 1
                match.left_team.Serve.elements[0].opacity = 0
                match.right_team.Serve.elements[0].opacity = 1

        '''match.left_team.LineUp = TeamLineUp([gui.get('MatchWindowRefereeMatchTabTeamACourtPlayers'), gui.get('MatchWindowRefereeMatchTabTeamALiberos')])
        match.right_team.LineUp = TeamLineUp([gui.get('MatchWindowRefereeMatchTabTeamBCourtPlayers'), gui.get('MatchWindowRefereeMatchTabTeamBLiberos')])
        match.left_team.LineUp.load()
        match.right_team.LineUp.load()'''
        
        match.sets[-1].PointScoreA = SetPointScore([gui.get('MatchWindowRefereeMatchTabTeamAPointScore')])
        match.sets[-1].PointScoreB = SetPointScore([gui.get('MatchWindowRefereeMatchTabTeamBPointScore')])
        match.sets[-1].PointScoreA.elements[0].text = str(match.sets[-1].score[0])
        match.sets[-1].PointScoreB.elements[0].text = str(match.sets[-1].score[1])

        del match.sets[-1]

        if len(match.sets) == 0:
            match.status = 'Awaiting'


class SetEnd(Event):

    def create(self):

        from DVA import match, match_events_dispatch, frontend_references as gui
       
        match.sets[-1].end()
        
        if self.mode == 'NEW':
            self.create_data = [len(match.sets), match.sets[-1].end_time, match.sets[-1].end_time_epoch, (match.left_team.long_name if match.sets[-1].score[0] > match.sets[-1].score[1] else match.right_team.long_name)]
        else:
            match.sets[-1].end_time = self.create_data[1]
            match.sets[-1].end_time_epoch = self.create_data[2]

        match.left_team, match.right_team = match.right_team, match.left_team
        match.serving_team, match.receiving_team = match.receiving_team, match.serving_team
              
        match.sets[-1].PointScoreA.zero()
        match.sets[-1].PointScoreB.zero()

        if match.sets[-1].score[0] > match.sets[-1].score[1]:
            match.set_score[0] += 1
        else:
            match.set_score[1] += 1

        match.set_score.reverse()

        if len(match.sets) == sets_to_win * 2 - 2:
            for tab in gui.get('MatchWindowRefereeTabPanel').tab_list:
                tab.disabled = True
            gui.get('MatchWindowRefereeTabPanelCoinToss').disabled = False
            gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelCoinToss'))
            gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab').disabled = False
            gui.get('MatchWindowRefereeLineUpSetUpTabTeamBTab').disabled = False
            gui.get('MatchWindowRefereeLineUpSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab'))
 
        elif max(match.set_score) == sets_to_win:
            match_events_dispatch.return_command = 'self.run(MatchEnd, None, "' + self.mode + '")'

        else:
            for tab in gui.get('MatchWindowRefereeTabPanel').tab_list:
                tab.disabled = True
            gui.get('MatchWindowRefereeTabPanelLineUpSetUp').disabled = False
            gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelLineUpSetUp'))
            gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab').disabled = False
            gui.get('MatchWindowRefereeLineUpSetUpTabTeamBTab').disabled = False
            gui.get('MatchWindowRefereeLineUpSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab'))
            gui.get('MatchWindowRefereeLineUpSetUpTabContent').on_load('A')

    def delete(self):
        
        from DVA import match

        match.sets[-1].status = 'Ongoing'
        match.sets[-1].end_time, match.sets[-1].end_time_epoch = 0, 0

        for sanction in match.sets[-1].sanctions:
            if sanction.type == 'Expulsion':
                if sanction.team == match.left_team.long_name:
                    for player in match.left_team.players:
                        if player.name_string == sanction.person:
                            match.left_team.expulsed_players.append(player)
                else:
                    for player in match.right_team.players:
                        if player.name_string == sanction.person:
                            match.right_team.expulsed_players.append(player)

        match.set_score.reverse()
 
        if match.sets[-1].score[0] > match.sets[-1].score[1]:
            match.set_score[0] -= 1
        else:
            match.set_score[1] -= 1

        match.sets[-1].PointScoreA.elements[0].text = str(match.sets[-1].score[0])
        match.sets[-1].PointScoreB.elements[0].text = str(match.sets[-1].score[1])

        match.left_team, match.right_team = match.right_team, match.left_team    
        match.serving_team, match.receiving_team = match.receiving_team, match.serving_team

        if match.serving_team == match.left_team:
            match.left_team.Serve.params[0] = 1
            match.right_team.Serve.params[0] = 0
            match.left_team.Serve.elements[0].opacity = 1
            match.right_team.Serve.elements[0].opacity = 0
        else:
            match.left_team.Serve.params[0] = 0
            match.right_team.Serve.params[0] = 1
            match.left_team.Serve.elements[0].opacity = 0
            match.right_team.Serve.elements[0].opacity = 1


class CoinTossResultsConfirmed(Event):

    def create(self):

        from DVA import match, frontend_references as gui
        from py.match.objects import Team
        from gfx.visual_elements import TeamName
       
        if self.mode == 'RESTORED':
            if self.create_data[0] == match.home_team.long_name:
                self.create_data[0] = 'down'
                self.create_data[1] = 'normal'
            else:
                self.create_data[0] = 'normal'
                self.create_data[1] = 'down'
            if self.create_data[2] == match.home_team.long_name:
                self.create_data[2] = 'down'
                self.create_data[3] = 'normal'
            else:
                self.create_data[2] = 'normal'
                self.create_data[3] = 'down'

        if self.create_data[0] == 'down':
            match.team_A = match.home_team
            match.team_B = match.away_team
        elif self.create_data[0] == 'normal':
            match.team_A = match.away_team
            match.team_B = match.home_team
        if self.create_data[2] == 'down':
            match.serving_team = match.home_team
            match.receiving_team = match.away_team
        elif self.create_data[2] == 'normal':
            match.serving_team = match.away_team
            match.receiving_team = match.home_team

        match.left_team = match.team_A
        match.right_team = match.team_B

        self.create_data = [match.team_A.long_name, match.team_B.long_name, match.serving_team.long_name, match.receiving_team.long_name]

        gui.get('MatchWindowRefereeTabPanelCoinToss').disabled = True

        if len(match.sets) < sets_to_win * 2 - 2:
            gui.get('MatchWindowRefereeTabPanelTeamSetUp').disabled = False
            gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelTeamSetUp'))
            gui.get('MatchWindowRefereeTeamSetUpTabContent').on_load('A', 0, 6)
        else:
            gui.get('MatchWindowRefereeTabPanelLineUpSetUp').disabled = False
            gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelLineUpSetUp'))
            gui.get('MatchWindowRefereeLineUpSetUpTabContent').on_load('A')
  
    def delete(self):

        from DVA import logs, match, frontend_references as gui
        from gfx.visual_elements import TeamName

        if len(match.sets) == sets_to_win * 2 - 2:
            for event in logs[0].deep_log:
                if event.type == 'CoinTossResultsConfirmed' and event != self:
                    event.mode = 'Restored'
                    event.create()
                    gui.get('MatchWindowRefereeTabPanelLineUpSetUp').disabled = True
                    gui.get('MatchWindowRefereeTabPanelMatch').disabled = False
                    gui.get('MatchWindowRefereeTabPanel').switch_to('MatchWindowRefereeTabPanelMatch')
                    break
        else:
            match.team_A = ''
            match.team_B = ''
            match.serving_team = ''
            match.receiving_team = ''
            match.left_team = ''
            match.right_team = ''


class SetUpConfirmed(Event):

    def create(self):

        from DVA import match, frontend_references as gui

        if self.mode == 'RESTORED':
            if self.create_data[1] == match.left_team.long_name:
                self.create_data[1] = match.left_team
            else:
                self.create_data[1] = match.right_team

        for i in range(0, len(self.create_data[0]), 5):
            self.create_data[1].players[int(i / 5)].number = self.create_data[0][i + 1]
            self.create_data[1].players[int(i / 5)].libero = self.create_data[0][i + 2]
            self.create_data[1].players[int(i / 5)].captain = self.create_data[0][i + 3]
            if self.create_data[1].players[int(i / 5)].captain: self.create_data[1].captain = self.create_data[1].players[int(i / 5)]
            self.create_data[1].players[int(i / 5)].present = self.create_data[0][i + 4]

        self.create_data[1] = self.create_data[1].long_name

        if gui.get('MatchWindowRefereeTeamSetUpTabHeader').current_tab == gui.get('MatchWindowRefereeTeamSetUpTabTeamATab'):

            gui.get('MatchWindowRefereeTeamSetUpTabTeamATab').disabled = True

            if gui.get('MatchWindowRefereeTeamSetUpTabTeamBTab').disabled:

                gui.get('MatchWindowRefereeTabPanelLineUpSetUp').disabled = False
                gui.get('MatchWindowRefereeTabPanelTeamSetUp').disabled = True
                gui.get('MatchWindowRefereeLineUpSetUpTabContent').on_load('A')
                gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelLineUpSetUp'))


            else:
                gui.get('MatchWindowRefereeTeamSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeTeamSetUpTabTeamBTab'))
                gui.get('MatchWindowRefereeTeamSetUpTabTeamBTab').trigger_action()

        else:

            gui.get('MatchWindowRefereeTeamSetUpTabTeamBTab').disabled = True

            if gui.get('MatchWindowRefereeTeamSetUpTabTeamATab').disabled:

                gui.get('MatchWindowRefereeTabPanelLineUpSetUp').disabled = False
                gui.get('MatchWindowRefereeTabPanelTeamSetUp').disabled = True
                gui.get('MatchWindowRefereeLineUpSetUpTabContent').on_load('A')
                gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelLineUpSetUp'))


            else:
                gui.get('MatchWindowRefereeTeamSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeTeamSetUpTabTeamATab'))
                gui.get('MatchWindowRefereeTeamSetUpTabTeamATab').trigger_action()

    def delete(self):

        from DVA import match, frontend_references as gui

        self.create_data[1].captain = ''

        for player in self.create_data[1].players:
            player.present, player.captain, player.libero, player.number = False, False, False, ''

        for tab in gui.get('MatchWindowRefereeTabPanel').tab_list:
            tab.disabled = True
            
        if self.create_data == match.left_team.long_name:
            
            if gui.get('MatchWindowRefereeTeamSetUpTabTeamBTab').disabled:
                gui.get('MatchWindowRefereeTabPanelCoinToss').disabled = False
                gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelCoinToss'))
            else:
                gui.get('MatchWindowRefereeTabPanelTeamSetUp').disabled = False
                gui.get('MatchWindowRefereeTeamSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeTeamSetUpTabTeamBTab'))
                gui.get('MatchWindowRefereeTeamSetUpTabTeamBTab').trigger_action()
        else:

            if gui.get('MatchWindowRefereeTeamSetUpTabTeamATab').disabled:
                gui.get('MatchWindowRefereeTabPanelCoinToss').disabled = False
                gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelCoinToss'))
            else:
                gui.get('MatchWindowRefereeTabPanelTeamSetUp').disabled = False
                gui.get('MatchWindowRefereeTeamSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeTeamSetUpTabTeamATab'))
                gui.get('MatchWindowRefereeTeamSetUpTabTeamATab').trigger_action()


class LineUpConfirmed(Event):

    def create(self):

        from DVA import match, match_events_dispatch, frontend_references as gui
        from py.match.core import get_time_instructions
        from gfx.frontend import PopUpWindow
        from kivy.clock import Clock

        players_list = []
            
        if self.create_data[1] == 'A':

            for player_name in self.create_data[0]:
                for player in match.left_team.players:
                    if player.name_string == player_name:
                        players_list.append(player)
                        match.left_team.players.remove(player)
                        break

            match.left_team.players = players_list + match.left_team.players

            for i in range(players_in_team):
                match.left_team.players[i].position = i

            gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab').disabled = True

            if gui.get('MatchWindowRefereeLineUpSetUpTabTeamBTab').disabled:
                match_events_dispatch.return_command = 'gui.get("MatchWindowRefereeMatchTabContent").on_load(mode)'

            else:
                gui.get('MatchWindowRefereeLineUpSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeLineUpSetUpTabTeamBTab'))
                gui.get('MatchWindowRefereeLineUpSetUpTabTeamBTab').trigger_action()

        else:

            for player_name in self.create_data[0]:
                for player in match.right_team.players:
                    if player.name_string == player_name:
                        players_list.append(player)
                        match.right_team.players.remove(player)
                        break

            match.right_team.players = players_list + match.right_team.players

            for i in range(players_in_team):
                match.right_team.players[i].position = i

            gui.get('MatchWindowRefereeLineUpSetUpTabTeamBTab').disabled = True

            if gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab').disabled:
                match_events_dispatch.return_command = 'gui.get("MatchWindowRefereeMatchTabContent").on_load(mode)'

            else:
                gui.get('MatchWindowRefereeLineUpSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab'))
                gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab').trigger_action()

    def delete(self):

        from DVA import match, frontend_references as gui
        from gfx.frontend import scroll_get_indexes

        if len(match.sets) > 0:

            if self.create_data[1] == 'A':
                team = match.left_team
                original_line_up = match.sets[-1].set_formatted_players[0]

            else:
                original_line_up = match.sets[-1].set_formatted_players[1]
                team = match.right_team
            
            team.players[:players_in_team] = original_line_up[:players_in_team]
            for i in range(players_in_team):
                team[i].players.position = i #TODO if this is not the first set, does it include changes
                #from other sets, or does it restore everyone's position into default order by SetUpConfirmed
                #event?

        for tab in gui.get('MatchWindowRefereeTabPanel').tab_list:
            tab.disabled = True

        # we're going backwards when cancelling. If the other tab is NOT disabled, means this is the first one and we need to switch to another window. Else, to the opposite tab.

        #TODO in here, there are some logical mistakes and since we do not allow for going back everywhere in this version, this part was skipped.
 
        if gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + ('A' if self.create_data[1] == 'B' else 'B') + 'Tab').disabled:
            
            gui.get('MatchWindowRefereeTabPanelLineUpSetUp').disabled = False
            gui.get('MatchWindowRefereeLineUpSetUpTabContent').disabled = False
            gui.get('MatchWindowRefereeLineUpSetUpTabHeader').disabled = False
            gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + self.create_data[1] + 'Tab').disabled = False
            for widget in gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + self.create_data[1] + 'Content'): widget.disabled = False
            gui.get('MatchWindowRefereeLineUpSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + self.create_data[1] + 'Tab'))
            gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelLineUpSetUp'))

            gui.get('MatchWindowRefereeLineUpSetUpTabContent').on_load(self.create_data[1])

        '''if not gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + ('A' if self.create_data[1] == 'B' else 'B') + 'Tab').disabled:

             gui.get('MatchWindowRefereeTabPanelLineUpSetUp').disabled = False 

            if len(match.sets) == 0:
   
                gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + self.create_data[1] + 'Tab').disabled = False
                gui.get('MatchWindowRefereeLineUpSetUpTabContent').disabled = False
                gui.get('MatchWindowRefereeLineUpSetUpTabHeader').disabled = False
                for element in gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + self.create_data[1] + 'Content'): element.disabled = True
                
                gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelLineUpSetUp'))
                gui.get('MatchWindowRefereeLineUpSetUpTabContent').on_load(self.create_data[1])
            
            elif 0 < len(match.sets) < sets_to_win * 2 - 2:
                gui.get('MatchWindowRefereeTabPanelMatch').disabled = False
                gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelMatch'))
                gui.get('MatchWindowRefereeTabPanelMatch').on_load()
            
            elif len(match.sets) == sets_to_win * 2 - 2:
                gui.get('MatchWindowRefereeTabPanelCoinToss').disabled = False
                gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelCoinToss'))
        
        else:
            
            for tab in gui.get('MatchWindowRefereeLineUpSetUpTabHeader').tab_list:
                tab.disabled = False
                #tab.content.disabled = False
                for spinner in 


            gui.get('MatchWindowRefereeLineUpSetUpTabHeader').switch_to(gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + ('A' if self.create_data[1] == 'B' else 'B') + 'Tab'))
            gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + ('A' if self.create_data[1] == 'B' else 'B') + 'Tab').trigger_action()
            gui.get('MatchWindowRefereeLineUpSetUpTabContent').on_load(self.create_data[1])'''
            

class TimeOutTaken(Event):

    def create(self):

        from gfx.frontend import PopUpWindow
        from DVA import logs, match, frontend_references as gui
        from kivy.clock import Clock
        from py.match.objects import TimeOut
     
        if self.mode == 'NEW' or (logs[0].deep_log[-1] == self):
            if len(match.sets) != sets_to_win * 2 - 1 and not self.create_data[4]:
                PopUpWindow().show_interval_window([3, 5, '0:' + str(length_of_time_outs_regular_set)])
            elif len(match.sets) != sets_to_win * 2 - 1 and self.create_data[4]:
                PopUpWindow().show_interval_window([3, 5, '0:' + str(length_of_technical_time_outs_regular_set)])
            elif len(match.sets) == sets_to_win * 2 - 1 and not self.create_data[4]:
                PopUpWindow().show_interval_window([3, 5, '0:' + str(length_of_time_outs_final_set)])
            elif len(match.sets) == sets_to_win * 2 - 1 and self.create_data[4]:
                PopUpWindow().show_interval_window([3, 5, '0:' + str(length_of_technical_time_outs_final_set)])

        if not self.create_data[4]:

            if self.mode == 'NEW':
            
                self.create_data[3].disabled = True

                if self.create_data[3] in gui.get('MatchWindowRefereeMatchTabTeamATimeOuts'):
                    self.create_data[3] = gui.get('MatchWindowRefereeMatchTabTeamATimeOuts').index(self.create_data[3])
                else:
                    self.create_data[3] = gui.get('MatchWindowRefereeMatchTabTeamBTimeOuts').index(self.create_data[3])

            else:
                if self.create_data[0] == match.left_team.long_name:
                    letter = 'A'
                else:
                    letter = 'B'

                gui.get('MatchWindowRefereeMatchTabTeam' + letter + 'TimeOuts')[self.create_data[3]].disabled = True

        TimeOut(self.create_data)

    def delete(self):

        from DVA import match, frontend_references as gui

        if not self.create_data[4]:
            if match.sets[-1].time_outs[-1].team == match.left_team.long_name:
                gui.get('MatchWindowRefereeMatchTabTeamATimeOuts')[self.create_data[3]].disabled = False
            else:
                gui.get('MatchWindowRefereeMatchTabTeamBTimeOuts')[self.create_data[3]].disabled = False
        
        else:
            for i in range(len(match.sets[-1].technical_time_outs_used) - 1, -1, -1):
                if match.sets[-1].technical_time_outs_used[i]:
                    match.sets[-1].technical_time_outs_used[i] = False
                    break
        
        match.sets[-1].time_outs = match.sets[-1].time_outs[:-1]


class Point_sReceived(Event):

    def create(self): 

        import DVA
        from DVA import match, match_events_dispatch, frontend_references as gui

        from py.match.objects import Point

        if self.mode == 'NEW':
            player = self.create_data[1]
        else:
            for _player_ in match.left_team.players:
                if _player_.name_string == self.create_data[2]:
                    player = _player_
                    break
            for _player_ in match.right_team.players:
                if _player_.name_string == self.create_data[2]:
                    player = _player_
                    break

        points = [getattr(py.match.match_config, 'points_for_' + self.create_data[0]+'_same_team'), getattr(py.match.match_config, 'points_for_' + self.create_data[0]+'_another_team')]

        if player in match.left_team.players:               

            teams = (match.left_team, match.right_team)
            scores = (match.sets[-1].PointScoreA, match.sets[-1].PointScoreB)

        elif player in match.right_team.players:

            teams = (match.right_team, match.left_team)
            scores = (match.sets[-1].PointScoreB, match.sets[-1].PointScoreA)

        match.sets[-1].score[0] += points[teams.index(match.left_team)]
        match.sets[-1].score[1] += points[teams.index(match.right_team)]

        for i in range(2):

            scores[i].increase(points[i])

            if points[i] == 0 and teams[i].Serve.params[0] == 1:

                change_serve = True

                teams[(0 if i == 1 else 1)].rotate()
                teams[i].Serve._switch_(teams[(0 if i == 1 else 1)].Serve, switch_elements=False)
                '''teams[i].Serve.switch()
                teams[(0 if i == 1 else 1)].Serve.switch()'''
                break

            else:

                change_serve = False

        if self.mode == 'NEW':
            self.create_data = [self.create_data[0], teams[0].long_name, self.create_data[1].name_string, change_serve]

        for i in range(2):
            for _ in range(points[i]):
                Point(self.create_data, i)

        if not match.sets[-1].is_tie_break and max(match.sets[-1].score) - min(match.sets[-1].score) >= min_difference_to_end_regular_set and max(match.sets[-1].score) >= min_points_to_win_regular_set:
            match_events_dispatch.return_command = 'self.run(SetEnd, ' + str(self.create_data) + ", '"  + self.mode + "')"
        elif match.sets[-1].is_tie_break and max(match.sets[-1].score) - min(match.sets[-1].score) >= min_difference_to_end_final_set and max(match.sets[-1].score) >= min_points_to_win_final_set:
            match_events_dispatch.return_command = 'self.run(SetEnd, ' + str(self.create_data) + ", '"  + self.mode + "')"
        
        if match.sets[-1].is_tie_break and tie_break_mid_set_rotation and max(match.sets[-1].score) == tie_break_mid_set_rotation_score and not hasattr(DVA, 'tie_break_mid_set_rotation_happened'):
            match_events_dispatch.return_command = 'self.run(TieBreakRotation, None, "' + self.mode + '")'
  
        if technical_time_outs_enabled:
            
            if not match.sets[-1].is_tie_break:
                
                for i in range(len(score_for_technical_time_outs_regular_set)):
                    if max(match.sets[-1].score) == score_for_technical_time_outs_regular_set[i] and not match.sets[-1].technical_time_outs_used[i]:
                        match.sets[-1].technical_time_outs_used[i] = True
                        match_events_dispatch.return_command = 'self.run(TimeOutTaken, [None, len(match.sets), match.sets[-1].score, None, True], "' + self.mode + '")'

            else:

                for i in range(len(score_for_technical_time_outs_final_set)):
                    if max(match.sets[-1].score) == score_for_technical_time_outs_final_set[i] and not match.sets[-1].technical_time_outs_used[i]:
                        match.sets[-1].technical_time_outs_used[i] = True
                        match_events_dispatch.return_command = 'self.run(TimeOutTaken, [None, len(match.sets), match.sets[-1].score, None, True], "' + self.mode + '")'

    def delete(self):

        from DVA import match

        for _player_ in match.left_team.players:
            if _player_.name_string == self.create_data[2]:
                player = _player_
                break

        for _player_ in match.right_team.players:
            if _player_.name_string == self.create_data[2]:
                player = _player_
                break

        points = [getattr(py.match.match_config, 'points_for_' + self.create_data[0]+'_same_team'), getattr(py.match.match_config, 'points_for_' + self.create_data[0]+'_another_team')]

        if player in match.left_team.players:               

            teams = (match.left_team, match.right_team)
            scores = (match.sets[-1].PointScoreA, match.sets[-1].PointScoreB)

        elif player in match.right_team.players:

            teams = (match.right_team, match.left_team)
            scores = (match.sets[-1].PointScoreB, match.sets[-1].PointScoreA)
        
        match.sets[-1].score[0] -= points[teams.index(match.left_team)]
        match.sets[-1].score[1] -= points[teams.index(match.right_team)]

        for i in range(2):
            
            scores[i].decrease(points[i])

            '''if points[i] != 0 and teams[i].Serve.params[0] == 0:
                teams[i].Serve._switch_(teams[(0 if i == 1 else 1)].Serve, switch_elements=False)
                teams[(0 if i == 1 else 1)].rotate_backwards()
                teams[i].Serve.switch()
                teams[(0 if i == 1 else 1)].Serve.switch()
                break'''

            if self.create_data[3]:
                teams[i].rotate_backwards()
                teams[i].Serve._switch_(teams[(0 if i == 1 else 1)].Serve, switch_elements=False)
                '''teams[i].Serve.switch()
                teams[(0 if i == 1 else 1)].Serve.switch()'''
                break

        match.sets[-1].points = match.sets[-1].points[:-sum(points)]


class TieBreakRotation(Event):

    def create(self):
        
            import DVA
            from DVA import match, frontend_references as gui
            from meta.localization import match_window
            from gfx.frontend import PopUpWindow
            
            match.left_team, match.right_team = match.right_team, match.left_team

            setattr(DVA, 'tie_break_mid_set_rotation_happened', True)

            match.set_score.reverse()
            match.sets[-1].score.reverse()

            match.left_team.Name._switch_(match.right_team, deep_load=True, deep_load_data=(match.left_team.long_name, match.right_team.long_name))

            '''match.left_team.Name.elements, match.right_team.Name.elements = match.right_team.Name.elements, match.left_team.Name.elements
                        
            match.left_team.Name.load(match.left_team.long_name)
            match.right_team.Name.load(match.right_team.long_name)'''

            match.SetScoreA._switch_(match.SetScoreB)

            '''match.SetScoreA.elements, match.SetScoreB.elements = match.SetScoreB.elements, match.SetScoreA.elements
            match.SetScoreA.elements[0].text, match.SetScoreB.elements[0].text = match.SetScoreB.elements[0].text, match.SetScoreA.elements[0].text'''

            match.sets[-1].PointScoreA._switch_(match.sets[-1].PointScoreB)

            '''match.sets[-1].PointScoreA, match.sets[-1].PointScoreB = match.sets[-1].PointScoreB, match.sets[-1].PointScoreA
            match.sets[-1].PointScoreA.elements[0].text, match.sets[-1].PointScoreB.elements[0].text = match.sets[-1].PointScoreB.elements[0].text, match.sets[-1].PointScoreA.elements[0].text'''

            match.left_team.Serve._switch_(match.right_team.Serve, deep_load_func_name='switch')

            '''match.left_team.Serve, match.right_team.Serve = match.right_team.Serve, match.left_team.Serve
            match.left_team.Serve.elements, match.right_team.Serve.elements = match.right_team.Serve.elements, match.left_team.Serve.elements 
            match.left_team.Serve.params, match.right_team.Serve.params = match.right_team.Serve.params, match.left_team.Serve.params
            
            match.left_team.Serve.switch()
            match.right_team.Serve.switch()'''

            match.left_team.LineUp.load()
            match.right_team.LineUp.load()

            for i in range(len(gui.get('MatchWindowRefereeMatchTabTeamATimeOuts'))):
                gui.get('MatchWindowRefereeMatchTabTeamATimeOuts')[i].disabled, gui.get('MatchWindowRefereeMatchTabTeamBTimeOuts')[i].disabled = gui.get('MatchWindowRefereeMatchTabTeamBTimeOuts')[i].disabled, gui.get('MatchWindowRefereeMatchTabTeamATimeOuts')[i].disabled

            PopUpWindow().show_pop_up(match_window[language_code][2])
    
    def delete(self):
                  
            from DVA import match 

            match.left_team, match.right_team = match.right_team, match.left_team

            setattr(DVA, 'tie_break_mid_set_rotation_happened', False)

            match.set_score.reverse()
            match.sets[-1].score.reverse()

            match.left_team.Name._switch_(match.right_team, deep_load=True, deep_load_data=(mathc.left_team.long_name, match.right_team.long_name))

            '''match.left_team.Name.elements, match.right_team.Name.elements = match.right_team.Name.elements, match.left_team.Name.elements
            
            match.left_team.Name.load(match.left_team.long_name)
            match.right_team.Name.load(match.right_team.long_name)'''

            match.SetScoreA._switch_(match.SetScoreB)

            '''match.SetScoreA.elements, match.SetScoreB.elements = match.SetScoreB.elements, match.SetScoreA.elements
            match.SetScoreA.elements[0].text, match.SetScoreB.elements[0].text = match.SetScoreB.elements[0].text, match.SetScoreA.elements[0].text'''

            match.sets[-1].PointScoreA._switch_(match.sets[-1].PointScoreB)

            '''match.sets[-1].PointScoreA, match.sets[-1].PointScoreB = match.sets[-1].PointScoreB, match.sets[-1].PointScoreA
            match.sets[-1].PointScoreA.elements[0].text, match.sets[-1].PointScoreB.elements[0].text = match.sets[-1].PointScoreB.elements[0].text, match.sets[-1].PointScoreA.elements[0].text'''

            match.left_team.Serve._switch_(match.right_team.Serve, deep_load_func_name='switch')

            '''match.left_team.Serve, match.right_team.Serve = match.right_team.Serve, match.left_team.Serve
            match.left_team.Serve.elements, match.right_team.Serve.elements = match.right_team.Serve.elements, match.left_team.Serve.elements 
            match.left_team.Serve.params, match.right_team.Serve.params = match.right_team.Serve.params, match.left_team.Serve.params
            
            match.left_team.Serve.switch()
            match.right_team.Serve.switch()'''

            match.left_team.LineUp.load()
            match.right_team.LineUp.load()

            for i in range(len(gui.get('MatchWindowRefereeMatchTabTeamATimeOuts'))):
                gui.get('MatchWindowRefereeMatchTabTeamATimeOuts')[i].disabled, gui.get('MatchWindowRefereeMatchTabTeamBTimeOuts')[i].disabled = gui.get('MatchWindowRefereeMatchTabTeamBTimeOuts')[i].disabled, gui.get('MatchWindowRefereeMatchTabTeamATimeOuts')[i].disabled


class SanctionIssued(Event):
    
    def create(self):
        
        from py.match.objects import Sanction
        from DVA import match_events_dispatch, match, frontend_references as gui

        if self.mode == 'NEW':
            self.create_data = [self.create_data[0], (self.create_data[1].split(maxsplit=1)[1] if self.create_data[1] != '' else ''), self.create_data[2].long_name]

        Sanction(self.create_data)
        
        for team in (match.left_team, match.right_team):
            if self.create_data[2] == team.long_name:
                
                if self.create_data[0].startswith('delay'):
                    team.Name.load(team.long_name)
                else:
                    if team.head_coach != '' and team.head_coach.name_string == self.create_data[1]:
                        if team.head_coach.Name != '': team.head_coach.Name.load(team.head_coach.name_string)
                    for _staff_ in team.staff:
                        if _staff_.name_string == self.create_data[1]:
                            if _staff_.Name != '': _staff_.Name.load(_staff_.name_string)
                            if self.create_data[0] == 'disqualification':
                                team.disqualified_staff.append(_staff_) 
                    for player in team.players:
                        if player.name_string == self.create_data[1]:
                            if player.Name != '': player.Name.load(player.name_string, any((player.captain, player.temp_captain)))
                            if player.Number != '': player.Number.load(player.number, player.name_string, any((player.captain, player.temp_captain)))
                            if self.create_data[0] == 'expulsion' and player in team.players[:players_in_team]:
                                match_events_dispatch.return_command = "gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load(" + ("'A'" if team == match.left_team else "'B'") + ", 0, 6, True)"
                                team.expulsed_players.append(player) 
                            elif self.create_data[0] == 'disqualification' and player in team.players[:players_in_team]:
                                match_events_dispatch.return_command = "gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load(" + ("'A'" if team == match.left_team else "'B'") + ", 0, 6, True)"
                                team.disqualified_players.append(player) 

        if not (getattr(py.match.match_config, 'points_for_' + self.create_data[0] + '_same_team') == 0 and getattr(py.match.match_config, 'points_for_' + self.create_data[0] + '_another_team') == 0):
            match_events_dispatch.return_command = match_events_dispatch.return_command + '?@?' + self.create_data[0] + '?@?' + self.create_data[2] + '?@?' + self.create_data[1]  
        
        gui.get('MatchWindowRefereeSanctionsTabContent').on_load(('A' if self.create_data[2]==match.left_team.long_name else 'B'), 0, 6)

    def delete(self):
        
        from DVA import match, frontend_references as gui
        
        match.sets[-1].sanctions = match.sets[-1].sanctions[:-1]

        for team in (match.left_team, match.right_team):
            if self.create_data[2] == team.long_name:
                if self.create_data[0].startswith('delay'):
                    team.Name.load(team.long_name)
                else:
                    if team.head_coach != '' and team.head_coach.name_string == self.create_data[1]:
                        if team.head.coach.Name != '': team.head_coach.Name.load(team.head_coach.name_string)
                        if self.create_data[0] == 'disqualification' and team.head_coach in team.disqualified_staff:
                            team.disqualified_staff.remove(team.head_coach)                     
                    for _staff_ in team.staff:
                        if _staff_.name_string == self.create_data[1]:
                            if _staff_.Name != '': _staff_.Name.load(_staff_.name_string)
                            if self.create_data[0] == 'disqualification' and _staff_ in team.disqualified_staff:
                                team.disqualified_staff.remove(_staff_)                     
                    for player in team.players:
                        if player.name_string == self.create_data[1]:
                            if player.Name != '': player.Name.load(player.name_string, any((player.captain, player.temp_captain)))
                            if player.Number != '': player.Number.load(player.number, player.name_string, any((player.captain, player.temp_captain)))
                            if self.create_data[0] == 'expulsion' and player in team.expulsed_players:
                                team.expulsed_players.remove(player) 
                            elif self.create_data[0] == 'disqualification' and player in team.disqualified_players:
                                team.disqualified_players.remove(player) 


class SubstitutionMade(Event):
    
    def create(self):
        
        from DVA import match_events_dispatch, match, frontend_references as gui
        from py.match.objects import Substitution

        if self.mode == "RESTORED":
            
            if self.create_data[0] == match.left_team.long_name:
                self.create_data[0] = match.left_team
            else:
                self.create_data[0] = match.right_team
            
            for player in self.create_data[0].players:
                if player.name_string == self.create_data[1]:
                    self.create_data[1] = player
                elif player.name_string == self.create_data[2]:
                    self.create_data[2] = player

            gui.get('MatchWindowRefereeSubstitutionsTabContent').requests_counter = self.create_data[3]

        player_in_index = self.create_data[0].players.index(self.create_data[1])
        player_out_index = self.create_data[0].players.index(self.create_data[2])

        if player_in_index == player_out_index + players_in_team:
            self.create_data[0].players[player_in_index], self.create_data[0].players[player_out_index] = self.create_data[0].players[player_out_index], self.create_data[0].players[player_in_index]
        else:
            if len(self.create_data[0].players) > player_out_index + players_in_team:
                self.create_data[0].players[player_in_index], self.create_data[0].players[player_out_index + players_in_team] = self.create_data[0].players[player_out_index + players_in_team], self.create_data[0].players[player_in_index]
                self.create_data[0].players[player_out_index + players_in_team], self.create_data[0].players[player_out_index] = self.create_data[0].players[player_out_index], self.create_data[0].players[player_out_index + players_in_team]
            else:
                self.create_data[0].players[player_in_index], self.create_data[0].players[player_out_index] = self.create_data[0].players[player_out_index], self.create_data[0].players[player_in_index]

        if self.create_data[1].libero:
            was_libero = True
            self.create_data[1].libero = False
        else:
            was_libero = False

        gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelMatch'))
        gui.get("MatchWindowRefereeMatchTabContent").on_load()

        '''if self.create_data[4]:
            gui.get('MatchWindowRefereeTabPanelMatch').content.enable_everything()'''

        if self.create_data[2].captain or self.create_data[2].temp_captain:
            match_events_dispatch.return_command = f'PopUpWindow().show_captain_chooser("{self.create_data[0].long_name}")'

        self.create_data = [self.create_data[0].long_name, self.create_data[1].name_string, self.create_data[2].name_string, self.create_data[3], self.create_data[4], player_in_index, player_out_index, was_libero]

        Substitution(self.create_data)

    def delete(self):
        
        from DVA import match, frontend_references as gui

        if self.create_data[0] == match.left_team.long_name:
            self.create_data[0] = match.left_team
        else:
            self.create_data[0] = match.right_team
            
        for player in self.create_data[0].players:
            if player.name_string == self.create_data[1]:
                self.create_data[1] = player
            elif player.name_string == self.create_data[2]:
                self.create_data[2] = player

        match.sets[-1].substitutions = match.sets[-1].substitutions[:-1]
        if len(match.sets[-1].substitutions) > 0:
            gui.get('MatchWindowRefereeSubstitutionsTabContent').requests_counter = self.create_data[3]

        player_in_index = self.create_data[5] # as of original substitution
        player_out_index = self.create_data[6]
       
        if player_in_index == player_out_index + players_in_team:
            self.create_data[0].players[player_in_index], self.create_data[0].players[player_out_index] = self.create_data[0].players[player_out_index], self.create_data[0].players[player_in_index]
        else:
            if len(self.create_data[0].players) > player_out_index + players_in_team:
                self.create_data[0].players[player_out_index + players_in_team], self.create_data[0].players[player_out_index] = self.create_data[0].players[player_out_index], self.create_data[0].players[player_out_index + players_in_team]
                self.create_data[0].players[player_in_index], self.create_data[0].players[player_out_index + players_in_team] = self.create_data[0].players[player_out_index + players_in_team], self.create_data[0].players[player_in_index]
            else:
                self.create_data[0].players[player_in_index], self.create_data[0].players[player_out_index] = self.create_data[0].players[player_out_index], self.create_data[0].players[player_in_index]

        if self.create_data[7]:
            self.create_data[1].libero = True

        if self.create_data[0] == match.left_team:
            gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load('A', 0, 6, self.create_data[4])
        elif self.create_data[0] == match.right_team:
            gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load('B', 0, 6, self.create_data[4])

        gui.get("MatchWindowRefereeMatchTabContent").on_load()

        self.create_data[0:5] = [self.create_data[0].long_name, self.create_data[1].name_string, self.create_data[2].name_string, self.create_data[3], self.create_data[4]]


class CaptainNotPresent(Event):

    def create(self):
        
        from DVA import match, frontend_references as gui

        if self.mode == 'NEW': self.create_data.append('')

        for team in match.left_team, match.right_team:
            if team.long_name == self.create_data[0]:
                for player in team.players:
                    if player.temp_captain: 
                        self.create_data[2] == player.name_string
                        player.temp_captain = False
                for player in team.players:
                    if player.name_string == self.create_data[1]: player.temp_captain = True

        gui.get("MatchWindowRefereeMatchTabContent").on_load()

    def delete(self):
        
        from DVA import match, frontend_references as gui
        from gfx.frontend import PopUpWindow

        PopUpWindow().show_captain_chooser(self.create_data[0])

        for team in match.left_team, match.right_team:
            if team.long_name == self.create_data[0]:
                for player in team.players:
                    if player.name_string == self.create_data[2]:
                        player.temp_captain = True
                    if player.name_string == self.create_data[1]:
                        player.temp_captain = False

        gui.get("MatchWindowRefereeMatchTabContent").on_load()


class ProtestDeclared(Event):
    
    def create(self):
        
        from DVA import match, frontend_references as gui
        from py.match.objects import Protest

        if self.mode == 'RESTORED':
            for team in (match.left_team, match.right_team):
                if team.long_name == self.create_data:
                    self.create_data = [team]
        
        gui.get('MatchWindowRefereeProtestsTabTeam' + ("A" if self.create_data[0] == match.left_team else 'B') + 'Tab').disabled = True
        gui.get('MatchWindowRefereeProtestsTabHeader').switch_to(gui.get('MatchWindowRefereeProtestsTabTeam' + ("B" if self.create_data[0] == match.left_team else 'A') + 'Tab'))
        gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelMatch'))
        if gui.get('MatchWindowRefereeProtestsTabTeam' + ("B" if self.create_data[0] == match.left_team else 'A') + 'Tab').disabled:
            gui.get('MatchWindowRefereeTabPanelProtests').disabled = True

        self.create_data[0].protest = Protest(self.create_data[0].long_name)

        self.create_data = self.create_data[0].long_name

    def delete(self):
        
        from DVA import match, frontend_references as gui

        for team in (match.left_team, match.right_team):
            if team.long_name == self.create_data:
                self.create_data = [team]

        gui.get('MatchWindowRefereeProtestsTabTeam' + ("A" if self.create_data[0] == match.left_team else 'B') + 'Tab').disabled = False
        gui.get('MatchWindowRefereeProtestsTabHeader').switch_to(gui.get('MatchWindowRefereeProtestsTabTeam' + ("A" if self.create_data[0] == match.left_team else 'B') + 'Tab'))
        gui.get('MatchWindowRefereeTabPanelProtests').disabled = False
        gui.get('MatchWindowRefereeProtestsTabContent').on_load(self.create_data[0])

        self.create_data[0].protest = ''

        self.create_data = self.create_data[0].long_name


class ProtestWritten(Event):
    
    def create(self):
        
        from DVA import match

        if self.mode == "RESTORED":
            for team in (match.left_team, match.right_team):
                if team.long_name == self.create_data[0]:
                    self.create_data[0] = team

        self.create_data[0].protest.text = self.create_data[1]

        self.create_data[0] = self.create_data[0].long_name

    def delete(self):
        
        from DVA import match

        if self.mode == "RESTORED":
            for team in (match.left_team, match.right_team):
                if team.long_name == self.create_data[0]:
                    self.create_data[0] = team

        self.create_data[0].protest.text = ''

        self.create_data[0] = self.create_data[0].long_name


class ProtestAfterMatchEnded(Event):

    def create(self):
        
        from DVA import match, frontend_references as gui
        from py.match.objects import Protest

        if self.mode == 'RESTORED':
            for team in (match.left_team, match.right_team):
                if team.long_name == self.create_data[0]:
                    self.create_data[0] = team

        gui.get('EndWindowRefereeWinnersProtestButton').disabled = True

        self.create_data[0].protest = Protest(self.create_data[0].long_name)
        self.create_data[0].protest.text = self.create_data[1]

        self.create_data[0] = self.create_data[0].long_name
        
        gui.get('EndWindowReferee').on_load()

    def delete(self):
        
        from DVA import match, frontend_references as gui

        gui.get('EndWindowRefereeWinnersProtestButton').disabled = False
        
        for team in (match.left_team, match.right_team):
            if team.long_name == self.create_data[0]:
                self.create_data[0] = team

        self.create_data[0].protest = 0

        self.create_data[0] = self.create_data[0].long_name
        gui.get('EndWindowReferee').on_load()
        

class RefereeNotesWritten(Event):

    def create(self):
        
        from DVA import match, frontend_references as gui

        match.referee_notes = self.create_data
        gui.get('EndWindowReferee').on_load()

    def delete(self):
        
        from DVA import match, frontend_references as gui

        match.referee_notes = ''
        gui.get('EndWindowReferee').on_load()
