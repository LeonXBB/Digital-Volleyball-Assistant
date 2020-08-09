from py.match.match_config import *
from meta.app_config import *
from meta.localization import *

class VisualElement:
    
    def __init__(self, elements):
        self.elements = elements
        self.params = [1, [1, 1, 1, 1], '', False, False]  # opacity, color, text, is_checked, underline

        if type(self.elements) != list:
            self.elements = [self.elements]

    def __load__(self, load_parameters=True):

        for element in self.elements:
            if hasattr(element, 'opacity'):
                element.opacity = self.params[0]
            if hasattr(element, 'color'):
                element.color = self.params[1]
            if hasattr(element, 'text'):
                element.text = self.params[2]
            if hasattr(element, 'active'):
                element.active = self.params[3]
            if hasattr(element, 'underline'):
                element.underline = self.params[4]

    def add_element(self, element, reload=True):
        
        self.elements.extend(element)
        
        if reload:
            self.__load__()

    def delete_element(self, element, reload=True):
        
        del self.elements[element]

        if reload:
            self.__load__()

    def clear_elements(self):
        
        self.elements = []

    def _switch_(self, switch_with, switch_elements=True, switch_params=True, deep_load=False, deep_load_func_name='load', deep_load_data=None):
        
        if switch_elements: self.elements, switch_with.elements = switch_with.elements, self.elements
        if switch_params: self.params, switch_with.params = switch_with.params, self.params

        if hasattr(self, deep_load_func_name) and deep_load:
            if deep_load_data is not None:
                getattr(self, deep_load_func_name)(deep_load_data[0])
                getattr(switch_with, deep_load_func_name)(deep_load_data[1])
            else:
                getattr(self, deep_load_func_name)()
                getattr(switch_with, deep_load_func_name)()

        self.__load__()
        switch_with.__load__()


class HeadCoachName(VisualElement):

    def load(self, name_string):

        from DVA import match

        self.params[2] = name_string

        head_coaches = []
        for team in (match.team_A, match.team_B):
            if team.head_coach != '':
                head_coaches.append(team.head_coach)

        for head_coach in head_coaches:
            if head_coach.name_string == name_string or head_coach.name_string == name_string.split(maxsplit=1)[1]:
                if head_coach.get_sanction_level()[0] == 'nothing':
                    self.clear_sanctions()
                if head_coach.get_sanction_level()[0] == 'warning':
                    self.warning()
                elif head_coach.get_sanction_level()[0] == 'penalty':
                    self.penalty()
                elif head_coach.get_sanction_level()[0] == 'expulsion':
                    self.expulsion()

        self.__load__()

    def clear_sanctions(self):
        self.params[1] = [1, 1, 1, 1]

    def warning(self):
        self.params[1] = [240/255, 250/255, 0, 1]

    def penalty(self):
        self.params[1] = [207/255, 0, 15/255, 1]

    def expulsion(self): # used in sanctions windows, as expulsed head coach is still subject to sanctions and thus must be highlighted accordinely.
        self.params[1] = [252/255, 15/255, 192/255, 1] 


class StaffName(VisualElement):

    def load(self, name_string):
        
        from DVA import match

        self.params[2] = name_string
        
        staff = []
        staff.extend(match.team_A.staff)
        staff.extend(match.team_B.staff)

        for _staff_ in staff:
            if _staff_.name_string == name_string or _staff_.name_string == name_string.split(maxsplit=1)[1]:
                if _staff_.get_sanction_level()[0] == 'nothing':
                    self.clear_sanctions()
                if _staff_.get_sanction_level()[0] == 'warning':
                    self.warning()
                elif _staff_.get_sanction_level()[0] == 'penalty':
                    self.penalty()
                elif _staff_.get_sanction_level()[0] == 'expulsion':
                    self.expulsion()

        self.__load__()

    def clear_sanctions(self):
        self.params[1] = [1, 1, 1, 1]

    def warning(self):
        self.params[1] = [240/255, 250/255, 0, 1]

    def penalty(self):
        self.params[1] = [207/255, 0, 15/255, 1]

    def expulsion(self): # used in sanctions windows, as expulsed staff is still subject to sanctions and thus must be highlighted accordinely.
        self.params[1] = [252/255, 15/255, 192/255, 1] 


class PlayerName(VisualElement):

    def load(self, name_string, is_captain=False):

        from DVA import match

        self.params[2] = name_string
        self.params[4] = is_captain

        players = []
        players.extend(match.team_A.players)
        players.extend(match.team_B.players)

        for player in players:
            if player.name_string == name_string or player.name_string == name_string.split(maxsplit=1)[1]:
                if player.get_sanction_level()[0] == 'nothing':
                    self.clear_sanctions()
                elif player.get_sanction_level()[0] == 'warning':
                    self.warning()
                elif player.get_sanction_level()[0] == 'penalty':
                    self.penalty()
                elif player.get_sanction_level()[0] == 'expulsion':
                    self.expulsion()
                elif player.get_sanction_level()[0] == 'disqualification':
                    self.disqualification()
        
        self.__load__()

    def clear_sanctions(self):
        self.params[1] = [1, 1, 1, 1]

    def warning(self):
        self.params[1] = [240/255, 250/255, 0, 1]

    def penalty(self):
        self.params[1] = [207/255, 0, 15/255, 1]

    def expulsion(self): # used in sanctions windows, as expulsed players are still subject to sanctions and thus must be highlighted accordinely.
        self.params[1] = [252/255, 15/255, 192/255, 1] 

    def disqualification(self): # used in substitutions windows
        self.params[1] = [205/255, 127/255, 50/255, 1] 


class PlayerNumber(VisualElement):

    def load(self, number, name_string, is_captain=False):
        
        from DVA import match

        self.params[2] = str(number)
        self.params[4] = is_captain
        
        players = []
        players.extend(match.team_A.players)
        players.extend(match.team_B.players)

        for player in players:
            if player.number == number and player.name_string == name_string:
                if player.get_sanction_level()[0] == 'nothing':
                    self.clear_sanctions()
                elif player.get_sanction_level()[0] == 'warning':
                    self.warning()
                elif player.get_sanction_level()[0] == 'penalty':
                    self.penalty()

        self.__load__()

    def clear_sanctions(self):
        self.params[1] = [1, 1, 1, 1]

    def warning(self):
        self.params[1] = [240/255, 250/255, 0, 1]

    def penalty(self):
        self.params[1] = [207/255, 0, 15/255, 1]


class TeamName(VisualElement):

    def load(self, team_name):

        from DVA import match

        self.params[2] = team_name
        
        for team in (match.team_A, match.team_B):
            if team != '' and team.long_name == team_name:
                if team.get_sanction_level()[0] == 'nothing':
                    self.clear_sanctions()
                elif team.get_sanction_level()[0] == 'delay_warning':
                    self.delay_warning()
                elif team.get_sanction_level()[0] == 'delay_penalty':
                    self.delay_penalty()
        
        self.__load__()

    def clear_sanctions(self):
        self.params[1] = [1, 1, 1, 1]

    def delay_warning(self):
        self.params[1] = [240/255, 250/255, 0, 1]

    def delay_penalty(self):
        self.params[1] = [207/255, 0, 15/255, 1]


class TeamPeopleList(VisualElement):

    def get_labels_list(self, widget_type, specific_child_index): #TODO rename to get_widgets_list?
        
        labels_list = []

        for element in self.elements:
            for widget in element.children:
                if type(widget) == widget_type:
                    if specific_child_index is None:
                        labels_list.append(widget)
                    else:
                        labels_list.append(widget.children[specific_child_index])

        labels_list.reverse()

        return labels_list

    def init_sub_visual_elements(self, widget_type, specific_child_index, with_numbers):

        for i in range(len(self.get_labels_list(widget_type, specific_child_index))):

            self.get_labels_list(widget_type, specific_child_index)[i].underline = False
            self.get_labels_list(widget_type, specific_child_index)[i].color = [1, 1, 1, 1]

            if i < len(self.people_list) and self.people_list[i].status == 'Player':
                self.people_list[i].Name = PlayerName([self.get_labels_list(widget_type, specific_child_index)[i]])
                if not with_numbers: 
                    self.people_list[i].Name.load(self.people_list[i].name_string, any([self.people_list[i].captain, self.people_list[i].temp_captain]))
                else:
                    self.people_list[i].Name.load(str(self.people_list[i].number) + ' ' + self.people_list[i].name_string, any([self.people_list[i].captain, self.people_list[i].temp_captain]))

            elif i < len(self.people_list) and self.people_list[i].status == 'Head Coach':
                self.people_list[i].Name = HeadCoachName([self.get_labels_list(widget_type, specific_child_index)[i]])
                if not with_numbers:
                    self.people_list[i].Name.load(self.people_list[i].name_string)
                else:
                    self.people_list[i].Name.load(statuses[language_code][0] + ' ' + self.people_list[i].name_string)

            elif i < len(self.people_list) and self.people_list[i].status == 'Staff':
                self.people_list[i].Name = StaffName([self.get_labels_list(widget_type, specific_child_index)[i]])
                if not with_numbers:
                    self.people_list[i].Name.load(self.people_list[i].name_string)
                else:
                    self.people_list[i].Name.load(statuses[language_code][1] + ' ' + self.people_list[i].name_string)

    def unfull_list_format(self, widget_type, specific_child_index):
        
        if len(self.get_labels_list(widget_type, specific_child_index)) > len(self.people_list):
            for i in range(len(self.people_list), len(self.get_labels_list(widget_type, specific_child_index))):
                self.get_labels_list(widget_type, specific_child_index)[i].opacity = 0
                self.get_labels_list(widget_type, specific_child_index)[i].disabled = True

        if self.window == 'TeamSetUp':
            
            for i in range(len(self.get_labels_list(widget_type, specific_child_index))):

                if self.get_labels_list(widget_type, specific_child_index)[i].opacity == 0:
                    for child in self.get_labels_list(widget_type, specific_child_index)[i].parent.children:
                        child.opacity = 0
                        child.disabled = True
                else:
                    for child in self.get_labels_list(widget_type, specific_child_index)[i].parent.children:
                        child.opacity = 1
                        child.disabled = False
        
                self.get_labels_list(widget_type, specific_child_index)[i].parent.present_checkbox(self.get_labels_list(widget_type, specific_child_index)[i].parent.children[3])

        elif self.window == 'Substitutions' or self.window == 'Sanctions':
           
            for i in range(len(self.get_labels_list(widget_type, specific_child_index))):

                if self.get_labels_list(widget_type, specific_child_index)[i].opacity == 0:
                    self.get_labels_list(widget_type, specific_child_index)[i].opacity = 0
                    self.get_labels_list(widget_type, specific_child_index)[i].disabled = True
                else:
                    self.get_labels_list(widget_type, specific_child_index)[i].opacity = 1
                    self.get_labels_list(widget_type, specific_child_index)[i].disabled = False

    def load(self, window, people_list, widget_type, specific_child_index=None, with_numbers=False):

        self.window = window       
        self.people_list = people_list

        self.init_sub_visual_elements(widget_type, specific_child_index, with_numbers)
        self.unfull_list_format(widget_type, specific_child_index)

    def scroll(self, start_index, end_index, widget_type, specific_child_index=None, with_numbers=False, **kwargs):
        
        from py.core import set_range_to_sliders

        set_range_to_sliders()

        self.original_peoples_list = self.people_list
        people_list = self.people_list[min(start_index, len(self.people_list)):min(end_index, len(self.people_list))]
        self.load(self.window, people_list, widget_type, specific_child_index, with_numbers)
        self.people_list = self.original_peoples_list

        if self.window == 'Substitutions' or self.window == 'Sanctions':
            
            choice_data = kwargs.get('choice_data')
            disabled_data = kwargs.get('disabled_data')

            for button in self.elements[0].children:
                if choice_data != '' and choice_data in button.text:
                    button.state = 'down'
                    if disabled_data:
                        button.disabled = False
                else:
                    button.state = 'normal'
                    if disabled_data:
                        button.disabled = True


class TeamSetUp(VisualElement):

    def create_map(self, team):

        self.map_values = []

        for player in team.players:
            
            if player not in team.disqualified_players and player not in team.expulsed_players:
                self.map_values.append(player.name_string)
                self.map_values.append('')
                self.map_values.append(False)
                self.map_values.append(False)
                self.map_values.append(False)

    def load(self): #TODO fix so it's not specific to our current window design (4th index)

        self.elements.reverse()

        for i in range(6):

            if self.elements[i][0].opacity > 0:

                index = self.elements[i][0].parent.children[4].text
                for j in range(4):

                    if j == 0:
                        self.elements[i][j].text = self.map_values[self.map_values.index(index) + 1]
                    else:
                        self.elements[i][j].active = self.map_values[self.map_values.index(index) + j + 1]

        self.elements.reverse()

    def update(self):
        
        for i in range(6):

            if self.elements[i][0].opacity > 0:

                index = self.elements[i][0].parent.children[4].text

                for j in range(4):

                    if j == 0:
                        self.map_values[self.map_values.index(index) + 1] = self.elements[i][j].text
                    else:
                        self.map_values[self.map_values.index(index) + j + 1] = self.elements[i][j].active

    def clear(self, button):

        for i in range(0, len(self.map_values), 5):
            self.map_values[i + 1] = ''

            for j in range(2, 5):
                self.map_values[i + j] = False

        self.load()

    def save(self, team, button):

        from py.match.events import SetUpConfirmed
        from DVA import match_events_dispatch
        from gfx.frontend import PopUpWindow

        self.update()

        players_present = 0
        players_liberos = 0
        players_captains = 0

        errors = []

        for i in range(0, len(self.map_values), 5):

            if not self.map_values[i + 4]:
                pass

            else:

                players_present += 1

                if self.map_values[i + 3]:

                    players_captains += 1

                    if self.map_values[i + 2]:
                        if not libero_can_be_captain:
                            errors.append(team_set_up_errors[language_code][4])

                if self.map_values[i + 2]:
                    players_liberos += 1

                if self.map_values[i + 1].isdigit() and 0 < int(self.map_values[i + 1]) < max_shirt_number:
                    for j in range(0, len(self.map_values), 5):
                        if self.map_values[j + 1] == self.map_values[i + 1] and j != i and team_set_up_errors[language_code][6] not in errors:
                            errors.append(team_set_up_errors[language_code][6])
                else:
                    errors.append(team_set_up_errors[language_code][5])

        if players_present - players_liberos < players_in_team:
            errors.append(team_set_up_errors[language_code][0])
        if players_captains != 1:
            errors.append(team_set_up_errors[language_code][1])
        if (players_in_team + players_liberos) > players_present or players_liberos > max_amount_liberos:
            errors.append(team_set_up_errors[language_code][2])
        if players_present >= players_more_or_equal_to_x_liberos_at_least_y[0] and players_liberos < players_more_or_equal_to_x_liberos_at_least_y[1]:
            errors.append(team_set_up_errors[language_code][3])

        if len(errors) == 0:
            match_events_dispatch.run(SetUpConfirmed, [self.map_values, team], 'NEW')
        else:
            PopUpWindow().show_pop_up('\n'.join(errors))


class TeamLineUpSetUp(VisualElement): # TODO try doing Players' names VE in values

    def load(self, spinner, team):

        from py.core import get_people_list

        for name in self.elements:

            name.values = get_people_list(team, with_numbers=True, with_liberos=False, rv_format='str')

            if spinner:
                if spinner.text == name.text and spinner != name:
                    name.text = ''

    def clear(self):

        for name in self.elements:
            name.text = ''

    def save(self, team):

        from DVA import match_events_dispatch
        from py.match.events import LineUpConfirmed
    
        data = []
        
        for name in self.elements:
            data.append(name.text.split(maxsplit=1)[1])

        self.clear()

        if team == 'A':
            match_events_dispatch.run(LineUpConfirmed, [data, 'A'], 'NEW')
        else:
            match_events_dispatch.run(LineUpConfirmed, [data, 'B'], 'NEW')


class TeamLineUp(VisualElement):

    def load(self):

        from DVA import match, frontend_references as gui

        liberos = []

        if self.elements[0] == gui.get('MatchWindowRefereeMatchTabTeamACourtPlayers'):

            for i in range(2):
                for j in range(max(len(self.elements[0]), len(self.elements[1]))):
                    if j < len(self.elements[i]):
                        self.elements[i][j].underline = False
                        self.elements[i][j].color = [1, 1, 1, 1]
                        self.elements[i][j].opacity = 0
                        self.elements[i][j].text = ''
    
            for i in range(players_in_team):
                match.left_team.players[i].Number = PlayerNumber(self.elements[0][i])
                match.left_team.players[i].Number.load(match.left_team.players[i].number, match.left_team.players[i].name_string, any((match.left_team.players[i].captain, match.left_team.players[i].temp_captain)))

            for i in range(len(match.left_team.players)):
                if match.left_team.players[i].libero and match.left_team.players[i].present:
                    liberos.append(match.left_team.players[i])

            for i in range(len(liberos)):
                liberos[i].Number = PlayerNumber(self.elements[1][i])
                liberos[i].Number.load(liberos[i].number, liberos[i].name_string, any((liberos[i].captain, liberos[i].temp_captain)))

        else:

            for i in range(2):
                for j in range(max(len(self.elements[0]), len(self.elements[1]))):
                    if j < len(self.elements[i]):
                        self.elements[i][j].underline = False
                        self.elements[i][j].color = [1, 1, 1, 1]
                        self.elements[i][j].opacity = 0
                        self.elements[i][j].text = ''
    
            for i in range(players_in_team):
                match.right_team.players[i].Number = PlayerNumber(self.elements[0][i])
                match.right_team.players[i].Number.load(match.right_team.players[i].number, match.right_team.players[i].name_string, any((match.right_team.players[i].captain, match.right_team.players[i].temp_captain)))

            for i in range(len(match.right_team.players)):
                if match.right_team.players[i].libero and match.right_team.players[i].present:
                    liberos.append(match.right_team.players[i])

            for i in range(len(liberos)):
                liberos[i].Number = PlayerNumber(self.elements[1][i])
                liberos[i].Number.load(liberos[i].number, liberos[i].name_string, any((liberos[i].captain, liberos[i].temp_captain)))

    def rotate(self, *args):

        from DVA import match, frontend_references as gui

        if rotation_enabled:

            if self.elements[0] == gui.get('MatchWindowRefereeMatchTabTeamACourtPlayers'):
                team = match.left_team
            else:
                team = match.right_team

            players_on_court = team.players[:players_in_team]
            team.players = team.players[players_in_team:]

            if rotation_direction == 'Clockwise':
                players_on_court = players_on_court[1:] + players_on_court[:1]
            else:
                players_on_court = players_on_court[-1:] + players_on_court[:-1]

            team.players = players_on_court + team.players
            self.load()

    def rotate_backwards(self, *args):

        from DVA import match, frontend_references as gui

        if rotation_enabled:

            if self.elements[0] == gui.get('MatchWindowRefereeMatchTabTeamACourtPlayers'):
                team = match.left_team
            else:
                team = match.right_team

            players_on_court = team.players[:players_in_team]
            team.players = team.players[players_in_team:]

            if rotation_direction == 'Clockwise':
                players_on_court = players_on_court[-1:] + players_on_court[:-1]
            else:
                players_on_court = players_on_court[1:] + players_on_court[:1]

            team.players = players_on_court + team.players
            self.load()


class TeamServe(VisualElement):

    def switch(self):

        if self.params[0] == 1:
            self.params[0] = 0
            self.__load__()
        elif self.params[0] == 0:
            self.params[0] = 1
            self.__load__()


class SetPointScore(VisualElement):

    def increase(self, i):
        self.params[2] = self.elements[0].text
        self.params[2] = str(int(self.params[2]) + i)
        self.__load__()

    def decrease(self, i):
        self.params[2] = self.elements[0].text
        self.params[2] = str(int(self.params[2]) - i)
        self.__load__()

    def zero(self):
        self.params[2] = '0'
        self.__load__()


class MatchSetScore(VisualElement):

    def increase(self, i):
        self.params[2] = self.elements[0].text
        self.params[2] = str(int(self.params[2]) + i)
        self.__load__()

    def decrease(self, i):
        self.params[2] = self.elements[0].text
        self.params[2] = str(int(self.params[2]) - i)
        self.__load__()

    def zero(self):
        self.params[2] = '0'
        self.__load__()