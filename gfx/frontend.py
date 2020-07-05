import os
import io
from io import BytesIO
from functools import partial

from kivy.app import App
from kivy.clock import Clock

from kivy.uix.behaviors import ButtonBehavior, FocusBehavior

from kivy.uix.screenmanager import ScreenManager as __ScreenManager__
from kivy.uix.screenmanager import Screen, NoTransition

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.filechooser import FileChooserIconView

from kivy.core.window import Window

from PIL import ImageDraw, ImageFont, Image as PIL_Image

import meta.app_config
import py.match.match_config
from meta.app_config import *
from py.match.match_config import *
from meta.localization import *


class Application(App):

    def build(self):
        
        import DVA

        self.title = app_title + ' ' + app_version

        self.authorization_window = AuthorizationWindow()
        self.match_window_referee = MatchWindowReferee()
        self.end_match_window_referee = EndWindowReferee()

        # The following is list of frontend_references which should be used in various places around the code instead of directly acessing widgets in case of changes in frontend
        DVA.frontend_references = {'AuthorizationWindow': self.authorization_window,
                                   'AuthorizationWindowLoginTextInput': self.authorization_window.design.main_widget.text_input.input_form_1.children[1],
                                   'AuthorizationWindowPasswordTextInput': self.authorization_window.design.main_widget.text_input.input_form_2.children[1],
                                   'AuthorizationWindowRememberMeCheckBox': self.authorization_window.design.main_widget.confirm_and_send.remember_me.centre.children[1],
                                   'AuthorizationWindowSendButtonBINDABLE': self.authorization_window.design.main_widget.confirm_and_send.button.send_button,

                                   'MatchWindowReferee': self.match_window_referee,
                                   'MatchWindowRefereeTabPanel': self.match_window_referee.design.main_widget.tabs_m,
                                   'MatchWindowRefereeTabPanelCoinToss': self.match_window_referee.design.main_widget.tabs_m.coin_toss,
                                   'MatchWindowRefereeTabPanelTeamSetUp': self.match_window_referee.design.main_widget.tabs_m.team_set_up,
                                   'MatchWindowRefereeTabPanelLineUpSetUp': self.match_window_referee.design.main_widget.tabs_m.line_up_set_up,
                                   'MatchWindowRefereeTabPanelMatch': self.match_window_referee.design.main_widget.tabs_m.match,
                                   'MatchWindowRefereeTabPanelSubstitutions': self.match_window_referee.design.main_widget.tabs_m.substitutions,
                                   'MatchWindowRefereeTabPanelProtests': self.match_window_referee.design.main_widget.tabs_m.protests,
                                   'MatchWindowRefereeTabPanelSanctions': self.match_window_referee.design.main_widget.tabs_m.sanctions,

                                   'MatchWindowRefereeCoinTossTabContent': self.match_window_referee.design.main_widget.tabs_m.coin_toss.content,
                                   'MatchWindowRefereeCoinTossTabTeamAName': self.match_window_referee.design.main_widget.tabs_m.coin_toss.content.design.main_widget.team_names.team_A,
                                   'MatchWindowRefereeCoinTossTabTeamBName': self.match_window_referee.design.main_widget.tabs_m.coin_toss.content.design.main_widget.team_names.team_B,
                                   'MatchWindowRefereeCoinTossTabTeamAButtonA': self.match_window_referee.design.main_widget.tabs_m.coin_toss.content.design.main_widget.toss_result.team_A_A,
                                   'MatchWindowRefereeCoinTossTabTeamAButtonServe': self.match_window_referee.design.main_widget.tabs_m.coin_toss.content.design.main_widget.toss_result.team_A_serve,
                                   'MatchWindowRefereeCoinTossTabTeamBButtonA': self.match_window_referee.design.main_widget.tabs_m.coin_toss.content.design.main_widget.toss_result.team_B_A,
                                   'MatchWindowRefereeCoinTossTabTeamBButtonServe': self.match_window_referee.design.main_widget.tabs_m.coin_toss.content.design.main_widget.toss_result.team_B_serve,
                                   'MatchWindowRefereeCoinTossSendButtonBINDABLE': self.match_window_referee.design.main_widget.tabs_m.coin_toss.content.design.main_widget.save.button,

                                   'MatchWindowRefereeTeamSetUpTabContent': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content,
                                   'MatchWindowRefereeTeamSetUpTabHeader': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.referee_spot.content,
                                   'MatchWindowRefereeTeamSetUpTabTeamATab': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.referee_spot.content.team_A_button,
                                   'MatchWindowRefereeTeamSetUpTabTeamBTab': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.referee_spot.content.team_B_button,
                                   'MatchWindowRefereeTeamSetUpTabTeamAPLAYERSLIST': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.referee_spot.content.team_A_button.content.list_area.list,
                                   'MatchWindowRefereeTeamSetUpTabTeamBPLAYERSLIST': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.referee_spot.content.team_B_button.content.list_area.list,
                                   'MatchWindowRefereeTeamSetUpTeamASLIDER': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.referee_spot.content.team_A_button.content.list_area.scrollbar,
                                   'MatchWindowRefereeTeamSetUpTeamBSLIDER': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.referee_spot.content.team_B_button.content.list_area.scrollbar,
                                   'MatchWindowRefereeTeamSetUpCancelButton': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.buttons.cancel,
                                   'MatchWindowRefereeTeamSetUpSaveButton': self.match_window_referee.design.main_widget.tabs_m.team_set_up.content.design.main_widget.buttons.save,

                                   'MatchWindowRefereeLineUpSetUpTabContent': self.match_window_referee.design.main_widget.tabs_m.line_up_set_up.content,
                                   'MatchWindowRefereeLineUpSetUpTabHeader': self.match_window_referee.design.main_widget.tabs_m.line_up_set_up.content.design.main_widget.referee_spot.content,
                                   'MatchWindowRefereeLineUpSetUpTabTeamATab': self.match_window_referee.design.main_widget.tabs_m.line_up_set_up.content.design.main_widget.referee_spot.content.team_A_button,
                                   'MatchWindowRefereeLineUpSetUpTabTeamBTab': self.match_window_referee.design.main_widget.tabs_m.line_up_set_up.content.design.main_widget.referee_spot.content.team_B_button,
                                   'MatchWindowRefereeLineUpSetUpTabTeamAContent': self.match_window_referee.design.main_widget.tabs_m.line_up_set_up.content.design.main_widget.referee_spot.content.team_A_button.content.team.real_indexes,
                                   'MatchWindowRefereeLineUpSetUpTabTeamBContent': self.match_window_referee.design.main_widget.tabs_m.line_up_set_up.content.design.main_widget.referee_spot.content.team_B_button.content.team.real_indexes,
                                   'MatchWindowRefereeLineUpSetUpSaveButton': self.match_window_referee.design.main_widget.tabs_m.line_up_set_up.content.design.main_widget.buttons.save, 

                                   'MatchWindowRefereeMatchTabContent': self.match_window_referee.design.main_widget.tabs_m.match.content,
                                   'MatchWindowRefereeMatchTabTeamAName': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.score.children[8],
                                   'MatchWindowRefereeMatchTabTeamBName': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.score.children[6],
                                   'MatchWindowRefereeMatchTabTeamASetScore': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.score.set_scores_and_serve_balls.digits.children[2],
                                   'MatchWindowRefereeMatchTabTeamBSetScore': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.score.set_scores_and_serve_balls.digits.children[0],
                                   'MatchWindowRefereeMatchTabTeamAPointScore': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.score.children[3],
                                   'MatchWindowRefereeMatchTabTeamBPointScore': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.score.children[1],
                                   'MatchWindowRefereeMatchTabTeamAServeBall': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.score.set_scores_and_serve_balls.children[0].children[2],
                                   'MatchWindowRefereeMatchTabTeamBServeBall': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.score.set_scores_and_serve_balls.children[0].children[0],
                                   'MatchWindowRefereeMatchTabTeamACourtPlayers': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.teams.team_A.players.real_indexes,
                                   'MatchWindowRefereeMatchTabTeamBCourtPlayers': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.teams.team_B.players.real_indexes,
                                   'MatchWindowRefereeMatchTabTeamALiberos': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.teams.team_A.liberos.children,
                                   'MatchWindowRefereeMatchTabTeamBLiberos': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.teams.team_B.liberos.children,
                                   'MatchWindowRefereeMatchTabMistakeButton': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.teams.error.button,
                                   'MatchWindowRefereeMatchTabTeamATimeOuts': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.time_outs.team_A.children,
                                   'MatchWindowRefereeMatchTabTeamBTimeOuts': self.match_window_referee.design.main_widget.tabs_m.match.content.design.main_widget.time_outs.team_B.children,

                                   'MatchWindowRefereeSubstitutionsTabContent': self.match_window_referee.design.main_widget.tabs_m.substitutions.content,
                                   'MatchWindowRefereeSubstitutionsTabHeader': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content,
                                   'MatchWindowRefereeSubstitutionsTabTeamATab': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content.team_A,
                                   'MatchWindowRefereeSubstitutionsTabTeamBTab': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content.team_B,
                                   'MatchWindowRefereeSubstitutionsTabTeamAOnCourtPLAYERSLIST': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content.team_A.content.content.list_on_court,
                                   'MatchWindowRefereeSubstitutionsTabTeamAOnBenchPLAYERSLIST': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content.team_A.content.content.list_on_bench,
                                   'MatchWindowRefereeSubstitutionsTabTeamBOnCourtPLAYERSLIST': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content.team_B.content.content.list_on_court,
                                   'MatchWindowRefereeSubstitutionsTabTeamBOnBenchPLAYERSLIST': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content.team_B.content.content.list_on_bench,
                                   'MatchWindowRefereeSubstitutionsTabTeamASLIDER': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content.team_A.content.content.scrollbar,
                                   'MatchWindowRefereeSubstitutionsTabTeamBSLIDER': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.referee_or_shared_area_spot.content.team_B.content.content.scrollbar,
                                   'MatchWindowRefereeSubstitutionsSaveButton': self.match_window_referee.design.main_widget.tabs_m.substitutions.content.design.main_widget.buttons.next, 

                                   'MatchWindowRefereeProtestsTabContent': self.match_window_referee.design.main_widget.tabs_m.protests.content,
                                   'MatchWindowRefereeProtestsTabHeader': self.match_window_referee.design.main_widget.tabs_m.protests.content.design.main_widget.referee_or_text_input_spot.content,
                                   'MatchWindowRefereeProtestsTabTeamATab': self.match_window_referee.design.main_widget.tabs_m.protests.content.design.main_widget.referee_or_text_input_spot.content.team_A,
                                   'MatchWindowRefereeProtestsTabTeamBTab': self.match_window_referee.design.main_widget.tabs_m.protests.content.design.main_widget.referee_or_text_input_spot.content.team_B,
                                   'MatchWindowRefereeProtestsTabTeamALabel': self.match_window_referee.design.main_widget.tabs_m.protests.content.design.main_widget.referee_or_text_input_spot.content.team_A.content.content.team_name,
                                   'MatchWindowRefereeProtestsTabTeamBLabel': self.match_window_referee.design.main_widget.tabs_m.protests.content.design.main_widget.referee_or_text_input_spot.content.team_B.content.content.team_name,
                                   'MatchWindowRefereeProtestsTabTeamATextInput': self.match_window_referee.design.main_widget.tabs_m.protests.content.design.main_widget.referee_or_text_input_spot.content.team_A.content.content.text,
                                   'MatchWindowRefereeProtestsTabTeamBTextInput': self.match_window_referee.design.main_widget.tabs_m.protests.content.design.main_widget.referee_or_text_input_spot.content.team_B.content.content.text,

                                   'MatchWindowRefereeSanctionsTabContent': self.match_window_referee.design.main_widget.tabs_m.sanctions.content,
                                   'MatchWindowRefereeSanctionsTabHeader': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab,
                                   'MatchWindowRefereeSanctionsTeamATab': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_A,
                                   'MatchWindowRefereeSanctionsTeamBTab': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_B,
                                   'MatchWindowRefereeSanctionsTeamAPEOPLELIST': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_A.content.persons_list,
                                   'MatchWindowRefereeSanctionsTeamBPEOPLELIST': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_B.content.persons_list,
                                   'MatchWindowRefereeSanctionsTabTeamASanctionsLeft': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_A.content.sanctions_list_left, 
                                   'MatchWindowRefereeSanctionsTabTeamASanctionsRight': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_A.content.sanctions_list_right, 
                                   'MatchWindowRefereeSanctionsTabTeamBSanctionsLeft': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_B.content.sanctions_list_left, 
                                   'MatchWindowRefereeSanctionsTabTeamBSanctionsRight': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_B.content.sanctions_list_right,
                                   'MatchWindowRefereeSanctionsTabTeamASanctionsDelayWarning': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_A.content.sanctions_list_left.delay_warning,
                                   'MatchWindowRefereeSanctionsTabTeamBSanctionsDelayWarning': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_B.content.sanctions_list_left.delay_warning,
                                   'MatchWindowRefereeSanctionsTabTeamASanctionsDelayPenalty': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_A.content.sanctions_list_left.delay_penalty,
                                   'MatchWindowRefereeSanctionsTabTeamBSanctionsDelayPenalty': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_B.content.sanctions_list_left.delay_penalty,
                                   'MatchWindowRefereeSanctionsTabTeamASLIDER': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_A.content.scrollbar,
                                   'MatchWindowRefereeSanctionsTabTeamBSLIDER': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.teams_tab.team_B.content.scrollbar,
                                   'MatchWindowRefereeSanctionsTabSaveButton': self.match_window_referee.design.main_widget.tabs_m.sanctions.content.design.main_widget.buttons.next,

                                   'EndWindowReferee': self.end_match_window_referee,
                                   'EndWindowRefereeLabel': self.end_match_window_referee.design.main_widget.up,
                                   'EndWindowRefereeProtocolImage': self.end_match_window_referee.design.main_widget.middle.protocol_area.image,
                                   'EndWindowRefereeSendProtocolButton': self.end_match_window_referee.design.main_widget.middle.buttons.send_protocol,
                                   'EndWindowRefereeSaveProtocolButton': self.end_match_window_referee.design.main_widget.middle.buttons.save_protocol,
                                   'EndWindowRefereeWriteNoteButton': self.end_match_window_referee.design.main_widget.middle.buttons.write_note,
                                   'EndWindowRefereeWinnersProtestButton': self.end_match_window_referee.design.main_widget.middle.buttons.winners_protest,
                                   'EndWindowRefereeTeamABestPlayerButton': self.end_match_window_referee.design.main_widget.middle.buttons.best_player_A,
                                   'EndWindowRefereeTeamBBestPlayerButton': self.end_match_window_referee.design.main_widget.middle.buttons.best_player_B,
                                   'EndWindowRefereeBackButton': self.end_match_window_referee.design.main_widget.down.back,
                                   'EndWindowRefereeForwardButton': self.end_match_window_referee.design.main_widget.down.forward
                                   }

        DVA.sm.add_widget(self.authorization_window)
        DVA.sm.add_widget(self.match_window_referee)
        DVA.sm.add_widget(self.end_match_window_referee)

        for screen in DVA.sm.screens:
            screen.add_widget(BackgroundWindow(), 2)

        Clock.schedule_once(DVA.sm.screens[0].on_load)

        return DVA.sm


class ScreenManager(__ScreenManager__):

    def __init__(self):
        super().__init__()
        self.transition = NoTransition()


class AuthorizationWindow(Screen):

    def __init__(self):

        super().__init__()

        self.name = 'Authorization Window'
        self.design = GridLayout(cols=1)
        self.design.main_widget = GridLayout(rows=2, pos_hint={"x": 0, "y": -50}, size_hint=(1, 1))

        self.design.main_widget.text_input = GridLayout(rows=2, cols=3)
        self.design.main_widget.confirm_and_send = GridLayout(rows=3)

        self.design.main_widget.text_input.input_form_1 = GridLayout(rows=3, padding=[0, 0, 30, 0])
        self.design.main_widget.text_input.input_form_2 = GridLayout(rows=3, padding=[0, 0, 30, 0])

        self.design.main_widget.confirm_and_send.remember_me = GridLayout(cols=3)
        self.design.main_widget.confirm_and_send.remember_me.centre = GridLayout(cols=2)

        self.design.main_widget.confirm_and_send.button = GridLayout(cols=3, rows=3)

        self.design.main_widget.text_input.input_form_1.add_widget(Label())  # empty
        self.design.main_widget.text_input.input_form_1.add_widget(TextInput(multiline=False, size_hint=(1.5, 0.75)))
        self.design.main_widget.text_input.input_form_1.add_widget(Label())  # empty

        self.design.main_widget.text_input.input_form_2.add_widget(Label())  # empty
        self.design.main_widget.text_input.input_form_2.add_widget(TextInput(multiline=False, size_hint=(1.5, 0.75)))
        self.design.main_widget.text_input.input_form_2.add_widget(Label())  # empty

        self.design.main_widget.text_input.add_widget(Label(font_size=24, text=authorization_window[language_code][0]))
        self.design.main_widget.text_input.add_widget(Label())  # empty
        self.design.main_widget.text_input.add_widget(self.design.main_widget.text_input.input_form_1)
        self.design.main_widget.text_input.add_widget(Label(font_size=24, text=authorization_window[language_code][1]))
        self.design.main_widget.text_input.add_widget(Label())  # empty
        self.design.main_widget.text_input.add_widget(self.design.main_widget.text_input.input_form_2)

        self.design.main_widget.confirm_and_send.remember_me.centre.add_widget(CheckBox(active=True))
        self.design.main_widget.confirm_and_send.remember_me.centre.add_widget(Label(font_size=24, text=authorization_window[language_code][2]))

        self.design.main_widget.confirm_and_send.remember_me.add_widget(Label())  # empty
        self.design.main_widget.confirm_and_send.remember_me.add_widget(self.design.main_widget.confirm_and_send.remember_me.centre)
        self.design.main_widget.confirm_and_send.remember_me.add_widget(Label())  # empty

        self.design.main_widget.confirm_and_send.button.add_widget(Label())  # empty
        self.design.main_widget.confirm_and_send.button.add_widget(Label())  # empty
        self.design.main_widget.confirm_and_send.button.add_widget(Label())  # empty
        self.design.main_widget.confirm_and_send.button.add_widget(Label())  # empty
        self.design.main_widget.confirm_and_send.button.send_button = Button(text=buttons[language_code][0])
        self.design.main_widget.confirm_and_send.button.add_widget(self.design.main_widget.confirm_and_send.button.send_button)
        self.design.main_widget.confirm_and_send.button.add_widget(Label())  # empty
        self.design.main_widget.confirm_and_send.button.add_widget(Label())  # empty
        self.design.main_widget.confirm_and_send.button.add_widget(Label())  # empty
        self.design.main_widget.confirm_and_send.button.add_widget(Label())  # empty

        self.design.main_widget.confirm_and_send.add_widget(self.design.main_widget.confirm_and_send.remember_me)
        self.design.main_widget.confirm_and_send.add_widget(Label())
        self.design.main_widget.confirm_and_send.add_widget(self.design.main_widget.confirm_and_send.button)

        self.design.main_widget.add_widget(self.design.main_widget.text_input)
        self.design.main_widget.add_widget(self.design.main_widget.confirm_and_send)

        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

        self.design.main_widget.confirm_and_send.button.send_button.bind(on_release=self.send_button)

    def on_load(self, *args):

        import DVA
        from DVA import logs, sm, frontend_references as gui
        from py.core import authorization_successful
        from py.objects import Request

        Request(('VersionControl', None))

        if os.path.isfile(os.getcwd() + '/meta/remember.me'):
            if logs[1].get(2, 'Authorization', True).get('exists'):
                DVA.user_id = 0  # TODO change when internet is enabled
                DVA.user_status = [1]  # TODO change when internet is enabled
                authorization_successful()
            return None

        sm.switch_to(gui.get('AuthorizationWindow'))

    def send_button(self, button):

        from DVA import logs, Request, frontend_references as gui
        from py.core import authorization_successful

        Request(['Authorization', None, [gui.get('AuthorizationWindowLoginTextInput').text, gui.get('AuthorizationWindowPasswordTextInput').text]])

        if logs[1].get(2, 'Authorization', True).get('exists'): # TODO when internet is enabled, wait for execution of request?
            authorization_successful()
            if gui.get('AuthorizationWindowRememberMeCheckBox').active:
                with open(os.getcwd() + '/meta/remember.me', 'wb') as f:
                    f.close()


class CoinTossWindow(Screen):

    def __init__(self):

        super().__init__()

        self.design = GridLayout(cols=1)

        self.design.main_widget = GridLayout(rows=3, cols=3)

        self.design.main_widget.team_names = GridLayout(cols=3)
        self.design.main_widget.toss_result = GridLayout(cols=3, rows=3, spacing=[30, -35], padding=[0, 0, 0, 40])
        self.design.main_widget.save = GridLayout(rows=3, padding=[0, 60], pos_hint=(1.2, 1))

        self.design.main_widget.team_names.team_A = Label(font_size=34, text='Team A')
        self.design.main_widget.team_names.team_B = Label(font_size=34, text='Team B')

        self.design.main_widget.toss_result.team_A_A = ToggleButton(text=coin_toss_window[language_code][0], group='A', state='down')
        self.design.main_widget.toss_result.team_B_A = ToggleButton(text=coin_toss_window[language_code][1], group='A', state='normal')
        self.design.main_widget.toss_result.team_A_serve = ToggleButton(text=coin_toss_window[language_code][2], group='serve', state='down')
        self.design.main_widget.toss_result.team_B_serve = ToggleButton(text=coin_toss_window[language_code][3], group='serve', state='normal')

        self.design.main_widget.save.button = Button(text=buttons[language_code][1])

        self.design.main_widget.team_names.add_widget(self.design.main_widget.team_names.team_A)
        self.design.main_widget.team_names.add_widget(Label())
        self.design.main_widget.team_names.add_widget(self.design.main_widget.team_names.team_B)

        self.design.main_widget.toss_result.add_widget(self.design.main_widget.toss_result.team_A_A)
        self.design.main_widget.toss_result.add_widget(Label())
        self.design.main_widget.toss_result.add_widget(self.design.main_widget.toss_result.team_B_A)
        self.design.main_widget.toss_result.add_widget(Label())
        self.design.main_widget.toss_result.add_widget(Label())
        self.design.main_widget.toss_result.add_widget(Label())
        self.design.main_widget.toss_result.add_widget(self.design.main_widget.toss_result.team_A_serve)
        self.design.main_widget.toss_result.add_widget(Label())
        self.design.main_widget.toss_result.add_widget(self.design.main_widget.toss_result.team_B_serve)

        self.design.main_widget.save.add_widget(self.design.main_widget.save.button, 1)

        self.design.main_widget.add_widget(Label())
        self.design.main_widget.add_widget(self.design.main_widget.team_names)
        self.design.main_widget.add_widget(Label())
        self.design.main_widget.add_widget(Label())
        self.design.main_widget.add_widget(self.design.main_widget.toss_result)
        self.design.main_widget.add_widget(Label())
        self.design.main_widget.add_widget(Label())
        self.design.main_widget.add_widget(self.design.main_widget.save)
        self.design.main_widget.add_widget(Label())

        self.design.main_widget.toss_result.team_A_A.bind(on_press=self.radio_button_changed)
        self.design.main_widget.toss_result.team_B_A.bind(on_press=self.radio_button_changed)
        self.design.main_widget.toss_result.team_A_serve.bind(on_press=self.radio_button_changed)
        self.design.main_widget.toss_result.team_B_serve.bind(on_press=self.radio_button_changed)

        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

        self.design.main_widget.save.button.bind(on_release=self.save_button)

    def init_visual_elements(self):
        
        from DVA import match, frontend_references as gui
        from gfx.visual_elements import TeamName

        match.home_team.Name = TeamName(gui.get('MatchWindowRefereeCoinTossTabTeamAName'))
        match.away_team.Name = TeamName(gui.get('MatchWindowRefereeCoinTossTabTeamBName'))
        match.home_team.Name.load(match.home_team.long_name)
        match.away_team.Name.load(match.away_team.long_name)

    def on_load(self, *args):
        
        self.init_visual_elements()
    
    def radio_button_changed(self, instance):

        from DVA import frontend_references as gui

        if instance == gui.get('MatchWindowRefereeCoinTossTabTeamAButtonA'):
            if instance.state == 'down':
                instance.text = coin_toss_window[language_code][0]
                self.design.main_widget.toss_result.team_B_A.text = coin_toss_window[language_code][1]
        elif instance == gui.get('MatchWindowRefereeCoinTossTabTeamBButtonA'):
            if instance.state == 'down':
                instance.text = coin_toss_window[language_code][0]
                self.design.main_widget.toss_result.team_A_A.text = coin_toss_window[language_code][1]
        elif instance == gui.get('MatchWindowRefereeCoinTossTabTeamAButtonServe'):
            if instance.state == 'down':
                instance.text = coin_toss_window[language_code][2]
                self.design.main_widget.toss_result.team_B_serve.text = coin_toss_window[language_code][3]
        else:
            if instance.state == 'down':
                instance.text = coin_toss_window[language_code][2]
                self.design.main_widget.toss_result.team_A_serve.text = coin_toss_window[language_code][3]

        if (gui.get('MatchWindowRefereeCoinTossTabTeamAButtonA').state == 'down' or gui.get('MatchWindowRefereeCoinTossTabTeamBButtonA').state == 'down') and \
        (gui.get('MatchWindowRefereeCoinTossTabTeamAButtonServe').state == 'down' or gui.get('MatchWindowRefereeCoinTossTabTeamBButtonServe').state == 'down'):
            gui.get('MatchWindowRefereeCoinTossSendButtonBINDABLE').disabled = False
        else:
            gui.get('MatchWindowRefereeCoinTossSendButtonBINDABLE').disabled = True

    def save_button(self, button):

        from DVA import match

        match.officials[0].coin_toss()


class TeamSetUpBase(Screen):
    
    class SharedArea(GridLayout):

        def __init__(self):
            
            super().__init__()

            self.rows = 2

            self.header = TeamSetUpBase.Header()
            self.list_area = GridLayout(cols=2)
            self.list_area.list = GridLayout(rows=6)
            self.list_area.scrollbar = Slider(orientation='vertical', size_hint=(0.05, 1), opacity=0, value=10, step=1, range=[0, 10])

            for _ in range(0, 6):
                self.list_area.list.add_widget(TeamSetUpBase.PlayerWidget())

            self.list_area.add_widget(self.list_area.list)
            self.list_area.add_widget(self.list_area.scrollbar)

            self.list_area.scrollbar.bind(on_touch_up=scroll__init)

            self.add_widget(self.header)
            self.add_widget(self.list_area)

    class PlayerWidget(GridLayout):

        def __init__(self, **kwargs):
            super().__init__()
            self.cols = 5
            self.name = Label(font_size=18, text='Name of the Player', size_hint=(1.2, 1))
            self.is_present = CheckBox()
            self.is_captain = CheckBox(disabled=True)
            self.is_libero = CheckBox(disabled=True)
            self.number = TextInput(multiline=False, disabled=True)
            self.number.size_hint_max_y = 30
            self.number.size_hint_max_x = 30

            self.add_widget(self.name)
            self.add_widget(self.is_present)
            self.add_widget(self.is_captain)
            self.add_widget(self.is_libero)
            self.add_widget(self.number)

            self.is_present.bind(state=self.present_checkbox)

        def present_checkbox(self, *args):

            if args[0].active:
                for i in range(3):
                    args[0].parent.children[i].disabled = False
            else:
                for i in range(3):
                    args[0].parent.children[i].disabled = True

    class Header(BoxLayout):

        def __init__(self, **kwargs):

            super().__init__()

            self.widget = Label(font_size=24, text=str(team_set_up[language_code][0]
                                                       + '                         '
                                                       + team_set_up[language_code][1]
                                                       + '                     '
                                                       + team_set_up[language_code][2]
                                                       + '                      '
                                                       + team_set_up[language_code][3]
                                                       + '            '
                                                       + team_set_up[language_code][4]))
            self.add_widget(self.widget)
            self.size_hint = (1, 0.2)

    def __init__(self):

        super().__init__()

        self.design = GridLayout(cols=1, pos_hint={"x": 0, "y": 0}, size_hint=(1, 1))
        self.design.main_widget = GridLayout(rows=3, padding=[10], spacing=[10, 10])

        self.design.main_widget.referee_spot = BoxLayout()  # also, put content of other users' mode
        self.design.main_widget.buttons = GridLayout(cols=5, size_hint=(1, 0.1), padding=[5])

        self.design.main_widget.buttons.cancel = Button(text=buttons[language_code][2])
        self.design.main_widget.buttons.save = Button(text=buttons[language_code][1])

        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.cancel)
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.save)

        self.design.main_widget.add_widget(self.design.main_widget.referee_spot)
        self.design.main_widget.add_widget(self.design.main_widget.buttons)

        self.design.main_widget.buttons.cancel.bind(on_release=self.cancel_button)
        self.design.main_widget.buttons.save.bind(on_release=self.save_button)

    def get_players_list(self, team):
        
        from py.core import get_people_list

        return get_people_list(team, with_absent_players=True)

    def load_players_list(self, team, start_index, end_index):

        from DVA import match, frontend_references as gui
        from gfx.visual_elements import TeamPeopleList

        #if not hasattr(team.SetUp, 'window') or team.SetUp.window != 'TeamSetUp':
        team.PlayersList = TeamPeopleList(gui.get('MatchWindowRefereeTeamSetUpTabTeam' + ('A' if team == match.left_team else 'B') + 'PLAYERSLIST'))
        team.PlayersList.load('TeamSetUp', self.get_players_list(team), TeamSetUpBase.PlayerWidget, 4)
        team.PlayersList.scroll(start_index, end_index, TeamSetUpBase.PlayerWidget, 4)

    def get_team_set_up_children(self, index):
        
        from DVA import frontend_references as gui

        team_set_up_children = []
        
        for i in range(len(gui.get('MatchWindowRefereeTeamSetUpTabTeam' + ('A' if index == 0 else 'B') + 'PLAYERSLIST').children)):
            team_set_up_children.append([])
            for j in range(len(gui.get('MatchWindowRefereeTeamSetUpTabTeam' + ('A' if index == 0 else 'B') + 'PLAYERSLIST').children[i].children)):
                if j != 4:
                    team_set_up_children[i].append(gui.get('MatchWindowRefereeTeamSetUpTabTeam' + ('A' if index == 0 else 'B') + 'PLAYERSLIST').children[i].children[j])
        
        return team_set_up_children

    def init_visual_elements(self, team, children_index, start_index, end_index):

        from DVA import match, frontend_references as gui
        from gfx.visual_elements import TeamSetUp, TeamName
       
        if not hasattr(team.SetUp, 'map_values') or len(team.SetUp.map_values) == 0:
            team.SetUp = TeamSetUp(self.get_team_set_up_children(children_index))
            team.SetUp.create_map(team)
            self.load_players_list(team, start_index, end_index)

        team.SetUp.update()
        self.load_players_list(team, start_index, end_index)
        team.SetUp.load()

        team.Name = TeamName(gui.get('MatchWindowRefereeTeamSetUpTabTeam' + ('A' if team == match.left_team else 'B') + 'Tab'))
        team.Name.load(team.long_name)
        for opposite_team in (match.left_team, match.right_team):
            if opposite_team != team: 
                opposite_team.Name = TeamName(gui.get('MatchWindowRefereeTeamSetUpTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab'))
                opposite_team.Name.load(opposite_team.long_name)

    def on_load(self, team, start_index, end_index, *args):

        from DVA import match, frontend_references as gui

        if team == 'A':
            self.init_visual_elements(match.left_team, 0, start_index, end_index)

        else:
            self.init_visual_elements(match.right_team, 1, start_index, end_index)

    def cancel_button(self, button):  # TODO change for non-referee

        from DVA import match, frontend_references as gui

        if gui.get('MatchWindowRefereeTeamSetUpTabHeader').current_tab == gui.get('MatchWindowRefereeTeamSetUpTabTeamATab'):
            match.left_team.SetUp.clear(button)
        else:
            match.right_team.SetUp.clear(button)

    def save_button(self, button):  # TODO change for non-referee

        from DVA import match, frontend_references as gui
        from py.match.objects import HeadCoach

        if gui.get('MatchWindowRefereeTeamSetUpTabHeader').current_tab == gui.get('MatchWindowRefereeTeamSetUpTabTeamATab'):
            if match.left_team.head_coach != '':
                match.left_team.head_coach.team_set_up(match.left_team, button)
            else:
                HeadCoach.team_set_up('', match.left_team, button)
        else:
            if match.right_team.head_coach != '':
                match.right_team.head_coach.team_set_up(match.right_team, button)
            else:
                HeadCoach.team_set_up('', match.right_team, button)


class TeamSetUpWindowReferee(TeamSetUpBase):  # TODO either save button disabled or popup when not all conditions are met for ALL THE TABS

    def __init__(self):

        super().__init__()
        self.name = 'TeamSetUpWindowReferee'

        self.design.main_widget.referee_spot.content = TabbedPanel(do_default_tab=False, background_color=[1, 1, 1, 0.5])
        self.design.main_widget.referee_spot.content.team_A_button = TabbedPanelHeader(text='Team A')
        self.design.main_widget.referee_spot.content.team_A_button.content = self.SharedArea()
        self.design.main_widget.referee_spot.content.team_B_button = TabbedPanelHeader(text='Team B')
        self.design.main_widget.referee_spot.content.team_B_button.content = self.SharedArea()

        self.design.main_widget.referee_spot.content.add_widget(self.design.main_widget.referee_spot.content.team_A_button)
        self.design.main_widget.referee_spot.content.add_widget(self.design.main_widget.referee_spot.content.team_B_button)
        self.design.main_widget.referee_spot.add_widget(self.design.main_widget.referee_spot.content)

        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

        self.design.main_widget.referee_spot.content.team_A_button.bind(on_release=self.header_button)
        self.design.main_widget.referee_spot.content.team_B_button.bind(on_release=self.header_button)

    def header_button(self, button):

        from DVA import match, frontend_references as gui

        teams = [match.left_team, match.right_team]
        letters = ['A', 'B']

        if button.text == match.left_team.long_name:
            index = 0
        else:
            index = 1

        if indexes[index] + 6 <= len(teams[index].players) - (len(teams[index].disqualified_players) + len(teams[index].expulsed_players)):
            gui.get('MatchWindowRefereeTeamSetUpTabContent').on_load(letters[index], indexes[index], indexes[index] + 6)
        else:
            gui.get('MatchWindowRefereeTeamSetUpTabContent').on_load(letters[index], indexes[index], (len(teams[index].players) - (len(teams[index].disqualified_players) + len(teams[index].expulsed_players))))


class LineUpSetUpBase(Screen):

    class SharedArea(GridLayout):

        def __init__(self):

            super().__init__()

            self.cols = 1
            self.team = TeamWidget(Spinner)
            self.team.padding = [30, 80, 30, 80]
            self.team.spacing = [40, 100]

            self.add_widget(self.team)

            for spinner in self.team.real_indexes:
                spinner.bind(text=self.spinner_pressed)

        def spinner_pressed(self, *args):

            from kivy.clock import Clock
            from DVA import frontend_references as gui
            from functools import partial

            screen = gui.get('MatchWindowRefereeLineUpSetUpTabContent')

            if args[0] in gui.get('MatchWindowRefereeLineUpSetUpTabTeamAContent'):
                Clock.schedule_once(partial(screen.on_load, 'A', args[0]))
            else:
                Clock.schedule_once(partial(screen.on_load, 'B', args[0]))

    def __init__(self):

        super().__init__()

        self.design = GridLayout(cols=1)

        self.design.main_widget = GridLayout(rows=2)

        self.design.main_widget.referee_spot = BoxLayout(orientation='horizontal')
        self.design.main_widget.buttons = GridLayout(cols=5, size_hint=(1, 0.1), padding=[2])

        self.design.main_widget.buttons.cancel = Button(text=buttons[language_code][2])
        self.design.main_widget.buttons.save = Button(text=buttons[language_code][1])

        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.cancel)
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.save)

        self.design.main_widget.add_widget(self.design.main_widget.referee_spot)
        self.design.main_widget.add_widget(self.design.main_widget.buttons)

        self.design.main_widget.buttons.cancel.bind(on_release=self.cancel_button)
        self.design.main_widget.buttons.save.bind(on_release=self.save_button)
        self.design.main_widget.buttons.save.disabled = True

    def get_save_button_state(self, letter):
        
        from DVA import frontend_references as gui

        not_able_to_save = False

        for position in gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + letter + 'Content'):
            if position.text == '':
                not_able_to_save = True

        gui.get('MatchWindowRefereeLineUpSetUpSaveButton').disabled = not_able_to_save

    def init_visual_elements(self, team, spinner):

        from DVA import match, frontend_references as gui
        from gfx.visual_elements import TeamLineUpSetUp, TeamName

        team.LineUpSetUp = TeamLineUpSetUp(gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + ('A' if team == match.left_team else 'B') +'Content'))
        team.LineUpSetUp.load(spinner, team)

        team.Name = TeamName(gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + ('A' if team == match.left_team else 'B') + 'Tab'))
        team.Name.load(team.long_name)
        for opposite_team in (match.left_team, match.right_team):
            if opposite_team != team: 
                opposite_team.Name = TeamName(gui.get('MatchWindowRefereeLineUpSetUpTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab'))
                opposite_team.Name.load(opposite_team.long_name)

    def on_load(self, team, spinner=None, *args):

        from DVA import match, frontend_references as gui

        if team == 'A':

            self.get_save_button_state('A')
            self.init_visual_elements(match.left_team, spinner)

        elif team == 'B':

            self.get_save_button_state('B')
            self.init_visual_elements(match.right_team, spinner)       

    def cancel_button(self, *args):

        from DVA import match, frontend_references as gui

        if gui.get('MatchWindowRefereeLineUpSetUpTabHeader').current_tab == gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab'):
            match.left_team.LineUpSetUp.clear()
        else:
            match.right_team.LineUpSetUp.clear()

    def save_button(self, button):

        from DVA import match, frontend_references as gui
        from py.match.objects import HeadCoach

        if gui.get('MatchWindowRefereeLineUpSetUpTabHeader').current_tab == gui.get('MatchWindowRefereeLineUpSetUpTabTeamATab'):
            if match.left_team.head_coach != '':
                match.left_team.head_coach.line_up_set_up(match.left_team, 'A')
            else:
                HeadCoach.line_up_set_up('', match.left_team, 'A')
        else:
            if match.right_team.head_coach != '':
                match.right_team.head_coach.line_up_set_up(match.right_team, 'B')
            else:
                HeadCoach.line_up_set_up('', match.right_team, 'B')


class LineUpSetUpReferee(LineUpSetUpBase):

    def __init__(self):

        super().__init__()

        self.name = 'TeamSetUpWindowReferee'

        self.design.main_widget.referee_spot.content = TabbedPanel(do_default_tab=False, background_color=[1, 1, 1, 0.5])
        self.design.main_widget.referee_spot.content.team_A_button = TabbedPanelHeader(text='Team A')
        self.design.main_widget.referee_spot.content.team_A_button.content = self.SharedArea()
        self.design.main_widget.referee_spot.content.team_B_button = TabbedPanelHeader(text='Team B')
        self.design.main_widget.referee_spot.content.team_B_button.content = self.SharedArea()

        self.design.main_widget.referee_spot.content.add_widget(self.design.main_widget.referee_spot.content.team_A_button)
        self.design.main_widget.referee_spot.content.add_widget(self.design.main_widget.referee_spot.content.team_B_button)
        self.design.main_widget.referee_spot.add_widget(self.design.main_widget.referee_spot.content)

        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

        self.design.main_widget.referee_spot.content.team_A_button.bind(on_release=self.header_button)
        self.design.main_widget.referee_spot.content.team_B_button.bind(on_release=self.header_button)

    def header_button(self, button):

        from DVA import match

        if button.text == match.left_team.long_name:
            self.on_load('A')
        else:
            self.on_load('B')


class SanctionsWindowReferee(Screen):
    
    class SharedArea(GridLayout):

        def __init__(self, team):

            super().__init__()

            self.cols = 4
            self.spacing = [40]
            self.padding = [20, 10, -20, 0]
            
            self.sanctions_list_left = GridLayout(rows=6, size_hint=(0.4, 2), spacing=[0, 20])
            self.sanctions_list_right = GridLayout(rows=6, size_hint=(0.4, 2), spacing=[0, 20])
            self.persons_list = GridLayout(rows=6, size_hint=(1, 1), padding=[10, 0, 20, 20], spacing=[0, 30])
            self.scrollbar = Slider(orientation='vertical', size_hint=(0.01, 0.01), opacity=0, value=10, step=1, range=[0, 10])

            self.sanctions_list_left.delay_warning = ToggleButton(group='sanction'+team,
                                                             background_normal=os.getcwd() + '/gfx/match/sanctions/delay_warning.png', # Should be png.
                                                             background_down=os.getcwd() + '/gfx/match/sanctions/delay_warning_down.png',
                                                             border=[0, 0, 0, 0],
                                                             size_hint=(0.2, 1))
            self.sanctions_list_left.delay_penalty = ToggleButton(group='sanction'+team,
                                                             background_normal=os.getcwd() + '/gfx/match/sanctions/delay_penalty.png',
                                                             background_down=os.getcwd() + '/gfx/match/sanctions/delay_penalty_down.png',
                                                             border=[0, 0, 0, 0],
                                                             size_hint=(0.2, 1))
            self.sanctions_list_left.warning = ToggleButton(group='sanction'+team,
                                                       background_normal=os.getcwd() + '/gfx/match/sanctions/warning.png',
                                                       background_down=os.getcwd() + '/gfx/match/sanctions/warning_down.png',
                                                       border=[0, 0, 0, 0],
                                                       size_hint=(0.2, 1))
            self.sanctions_list_right.penalty = ToggleButton(group='sanction'+team,
                                                       background_normal=os.getcwd() + '/gfx/match/sanctions/penalty.png',
                                                       background_down=os.getcwd() + '/gfx/match/sanctions/penalty_down.png',
                                                       border=[0, 0, 0, 0],
                                                       size_hint=(0.2, 1))
            self.sanctions_list_right.expulsion = ToggleButton(group='sanction'+team,
                                                         background_normal=os.getcwd() + '/gfx/match/sanctions/expulsion.png',
                                                         background_down=os.getcwd() + '/gfx/match/sanctions/expulsion_down.png',
                                                         border=[0, 0, 0, 0],
                                                         size_hint=(0.2, 1))
            self.sanctions_list_right.disqualification = ToggleButton(group='sanction'+team,
                                                                background_normal=os.getcwd() + '/gfx/match/sanctions/disqualification.png',
                                                                background_down=os.getcwd() + '/gfx/match/sanctions/disqualification_down.png',
                                                                border=[0, 0, 0, 0],
                                                                size_hint=(0.2, 1))

            self.sanctions_list_left.add_widget(self.sanctions_list_left.delay_warning)
            self.sanctions_list_left.add_widget(self.sanctions_list_left.delay_penalty)
            self.sanctions_list_left.add_widget(self.sanctions_list_left.warning)
            self.sanctions_list_right.add_widget(self.sanctions_list_right.penalty)
            self.sanctions_list_right.add_widget(self.sanctions_list_right.expulsion)
            self.sanctions_list_right.add_widget(self.sanctions_list_right.disqualification)

            for i in range(0, 6):
                self.persons_list.add_widget(ToggleButton(group='person'+team, text='Player\'s name'))

            self.add_widget(self.sanctions_list_left)
            self.add_widget(self.persons_list)
            self.add_widget(self.sanctions_list_right)
            self.add_widget(self.scrollbar)

            self.scrollbar.bind(on_touch_up=scroll__init)          

    def header_button(self, *args):
        
        from DVA import frontend_references as gui

        if args[0] == gui.get('MatchWindowRefereeSanctionsTeamATab'):
            self.on_load('A', scroll_get_indexes('Sanctions', 'A')[0], scroll_get_indexes('Sanctions', 'A')[1], False)
        elif args[0] == gui.get('MatchWindowRefereeSanctionsTeamBTab'):
            self.on_load('B', scroll_get_indexes('Sanctions', 'B')[0], scroll_get_indexes('Sanctions', 'B')[1], False)

    def __init__(self):

        super().__init__()

        self.design = GridLayout(cols=1)

        self.design.main_widget = GridLayout(rows=2)

        self.design.main_widget.teams_tab = TabbedPanel(do_default_tab=False, background_color=[0, 0, 0, 0])
        self.design.main_widget.teams_tab.team_A = TabbedPanelHeader(text='Team A')
        self.design.main_widget.teams_tab.team_B = TabbedPanelHeader(text='Team B')

        self.design.main_widget.buttons = GridLayout(cols=5, size_hint=(1, 0.1), padding=5)
        self.design.main_widget.buttons.cancel = Button(text=buttons[language_code][2])
        self.design.main_widget.buttons.next = Button(text=buttons[language_code][1])

        self.design.main_widget.teams_tab.team_A.content = self.SharedArea('A')
        self.design.main_widget.teams_tab.team_B.content = self.SharedArea('B')

        self.design.main_widget.teams_tab.add_widget(self.design.main_widget.teams_tab.team_A)
        self.design.main_widget.teams_tab.add_widget(self.design.main_widget.teams_tab.team_B)

        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.cancel)
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.next)

        self.design.main_widget.add_widget(self.design.main_widget.teams_tab)
        self.design.main_widget.add_widget(self.design.main_widget.buttons)
        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

        self.design.main_widget.buttons.cancel.bind(on_release=self.cancel_button_pressed)
        self.design.main_widget.buttons.next.bind(on_release=self.save_button_pressed)

        self.design.main_widget.teams_tab.team_A.bind(on_release=self.header_button)
        self.design.main_widget.teams_tab.team_B.bind(on_release=self.header_button)

        for sanction in self.design.main_widget.teams_tab.team_A.content.sanctions_list_left.children:
            sanction.bind(state=self.sanction_button_pressed)
        for sanction in self.design.main_widget.teams_tab.team_B.content.sanctions_list_left.children:
            sanction.bind(state=self.sanction_button_pressed)
        for sanction in self.design.main_widget.teams_tab.team_A.content.sanctions_list_right.children:
            sanction.bind(state=self.sanction_button_pressed)
        for sanction in self.design.main_widget.teams_tab.team_B.content.sanctions_list_right.children:
            sanction.bind(state=self.sanction_button_pressed)

        for persons_list in (self.design.main_widget.teams_tab.team_A.content.persons_list.children, self.design.main_widget.teams_tab.team_B.content.persons_list.children):
            for person_button in persons_list:
                person_button.bind(on_release=self.person_button_pressed)

        self.person_chosen_A = ''
        self.sanction_chosen_A = ''
        self.person_chosen_B = ''
        self.sanction_chosen_B = ''

    def get_save_button_state(self, team):
        
        from DVA import match, frontend_references as gui
          
        gui.get('MatchWindowRefereeSanctionsTabSaveButton').disabled = True
       
        sanction_chosen = ''
        person_chosen = ''

        for direction in ('Right', 'Left'):
            for sanction in gui.get('MatchWindowRefereeSanctionsTabTeam' + ("A" if team == match.left_team else 'B') + 'Sanctions' + direction).children:
                if sanction.state == 'down':
                    sanction_chosen = sanction.background_normal.split('/')[-1].split('.')[0]

        for person in gui.get('MatchWindowRefereeSanctionsTeam' + ("A" if team == match.left_team else 'B') + 'PEOPLELIST').children:
            if person.state == 'down':
                person_chosen = person.text

        if (sanction_chosen != '' and person_chosen != '') or sanction_chosen.startswith('delay'):
            gui.get('MatchWindowRefereeSanctionsTabSaveButton').disabled = False

    def calculate_popup(self, team):

        from DVA import match

        if expulsions_instead_of_penalties_on_set_point:
            
            if len(match.sets) < sets_to_win * 2 - 1:
                if match.sets[-1].score[(0 if team == match.left_team else 1)] - match.sets[-1].score[(1 if team == match.left_team else 0)] >= min_difference_to_end_regular_set - 1:
                    if match.sets[-1].score[(0 if team == match.left_team else 1)] >= min_points_to_win_regular_set -1:
                        PopUpWindow().show_pop_up(sanctions_errors[language_code][0])

            else:
                if match.sets[-1].score[(0 if team == match.left_team else 1)] - match.sets[-1].score[(1 if team == match.left_team else 0)] >= min_difference_to_end_final_set - 1:
                    if match.sets[-1].score[(0 if team == match.left_team else 1)] >= min_points_to_win_final_set -1:
                        PopUpWindow().show_pop_up(sanctions_errors[language_code][0])

    def enable_every_sanction(self, team):

        from DVA import match, frontend_references as gui

        for direction in ('Left', 'Right'):
            for sanction in gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') + 'Sanctions' + direction).children:
                sanction.disabled = False

    def get_people_list(self, team):

        from py.core import get_people_list

        return get_people_list(team, True, True)

    def hide_people_list(self, team, button):

        from DVA import match, frontend_references as gui
        
        for sanction in ('Warning', 'Penalty'):

            if button == gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') + 'SanctionsDelay' + sanction):

                if gui.get('MatchWindowRefereeSanctionsTeam' + ('A' if team == match.left_team else 'B') + 'PEOPLELIST').opacity:
                    gui.get('MatchWindowRefereeSanctionsTeam' + ('A' if team == match.left_team else 'B') + 'PEOPLELIST').opacity = 0

                    self.clear_chosen_person((match.left_team if ('A' if team == match.left_team else 'B') == 'A' else match.right_team))

                elif not gui.get('MatchWindowRefereeSanctionsTeam' + ('A' if team == match.left_team else 'B') + 'PEOPLELIST').opacity:
                    gui.get('MatchWindowRefereeSanctionsTeam' + ('A' if team == match.left_team else 'B') + 'PEOPLELIST').opacity = 1       

    def init_visual_elements(self, team, start_index, end_index, custom_people_list=False):

        from DVA import match, frontend_references as gui
        from gfx.visual_elements import TeamPeopleList, TeamName
       
        team.PlayersList = TeamPeopleList(gui.get('MatchWindowRefereeSanctionsTeam' + ('A' if team == match.left_team else 'B') + 'PEOPLELIST'))
        team.PlayersList.load('Sanctions', (self.get_people_list(team) if not custom_people_list else self.apply_sanction_limitations(team)), ToggleButton, with_numbers=True)
        team.PlayersList.scroll(start_index, end_index, ToggleButton, with_numbers=True, choice_data=getattr(self, 'person_chosen_' + ('A' if team == match.left_team else 'B')))

        team.Name = TeamName(gui.get('MatchWindowRefereeSanctionsTeam' + ('A' if team == match.left_team else 'B') + 'Tab'))
        team.Name.load(team.long_name)
        for opposite_team in (match.left_team, match.right_team):
            if opposite_team != team: 
                opposite_team.Name = TeamName(gui.get('MatchWindowRefereeSanctionsTeam' + ('B' if team == match.left_team else 'A') + 'Tab'))
                opposite_team.Name.load(opposite_team.long_name)

    def clear_chosen_person(self, team):

        from DVA import match, frontend_references as gui
        
        for button in gui.get('MatchWindowRefereeSanctionsTeam' + ('A' if team == match.left_team else 'B') + 'PEOPLELIST').children:
            if button.text == getattr(self, 'person_chosen_' + ('A' if team == match.left_team else 'B')):
                button.state = 'normal'     
        setattr(self, 'person_chosen_' + ('A' if team == match.left_team else 'B'), '')

    def clear_chosen_sanction(self, team):
        
        from DVA import match, frontend_references as gui
        
        for direction in ('Right', 'Left'):
            for button in gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') + 'Sanctions' + direction).children:
                if button.background_normal.split('/')[-1].split('.')[0] == getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B')):
                    button.state = 'normal'
            setattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B'), '')

    def get_person_sanction_level(self, team, person_name_string):

        from DVA import match

        person = ''

        if person_name_string[:1].isdigit() or person_name_string.split()[0] in statuses[language_code]: person_name_string = person_name_string.split(maxsplit=1)[1]

        if team.head_coach != '' and team.head_coach.name_string == person_name_string:
            person = team.head_coach
        for _staff_ in team.staff:
            if _staff_.name_string == person_name_string:
                person = _staff_
        for player in team.players:
            if player.name_string == person_name_string:
                person = player

        if person != '': return person.get_sanction_level()

    def apply_team_limitations(self, team):

        from DVA import match, frontend_references as gui

        sanctions_requests = [0, 0, 0, 0, 0, 0]
        sanctions_allowed = [getattr(py.match.match_config, SANCTIONS_LEVELS[i] + '_amount_limitations_team') for i in range(1, 7)]   

        for direction in ('Left', 'Right'):
            for button in gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') + 'Sanctions' + direction).children:
                button.disabled = False
                if not button.background_normal.split('/')[-1].split('.')[0] == getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B')):
                    button.state = 'normal'   

        for i in range(len(SANCTIONS_LEVELS[1:])):
            for _set_ in match.sets:
                for sanction in _set_.sanctions:
                    if sanction.type == SANCTIONS_LEVELS[1:][i] and sanction.team == team.long_name:
                        sanctions_requests[i] += 1
        
        for i in range(len(sanctions_allowed)):
            if sanctions_allowed[i] is not None and sanctions_requests[i] >= sanctions_allowed[i]:
                for direction in ('Left', 'Right'):
                    for button in gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') + 'Sanctions' + direction).children:
                        if button.background_normal.split('/')[-1].split('.')[0] == SANCTIONS_LEVELS[i + 1]:
                            button.disabled = True

        if sanctions_requests[0] < sanctions_allowed[0]:
            gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') +'SanctionsDelayPenalty').disabled = True
        else:
            gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') +'SanctionsDelayPenalty').disabled = False

        for i in range(len(sanctions_requests)):
            if sanctions_allowed[i] is not None and sanctions_requests[i] >= sanctions_allowed[i] and getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B')) == SANCTIONS_LEVELS[i + 1]:
                self.clear_chosen_sanction(team)
        
    def apply_person_limitations(self, team, person_name_string):
        
        from DVA import match, frontend_references as gui
       
        if getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B')) != '':
            if SANCTIONS_LEVELS.index(getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B'))) < SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person_name_string)[0]):
                self.clear_chosen_sanction(team)
            elif SANCTIONS_LEVELS.index(getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B'))) == SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person_name_string)[0]):
                if self.get_person_sanction_level(team, person_name_string)[1] >= getattr(py.match.match_config, getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B')) + '_amount_limitations_person'):
                    self.clear_chosen_sanction(team)

        for i in range(1, SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person_name_string)[0]) + 1):

            for direction in ('Right', 'Left'):
                for sanction_button in gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') + 'Sanctions' + direction).children:
                    
                    if i < 3:
                        sanction_button.disabled = True
                        continue

                    if sanction_button.background_normal.split('/')[-1].split('.')[0] == SANCTIONS_LEVELS[i]:
                        
                        if i < SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person_name_string)[0]):
                            sanction_button.disabled = True
                        elif i == SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person_name_string)[0]):
                            if self.get_person_sanction_level(team, person_name_string)[1] >= getattr(py.match.match_config, sanction_button.background_normal.split('/')[-1].split(".")[0] + '_amount_limitations_person'):
                                sanction_button.disabled = True      

        for i in range(SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person_name_string)[0]), 7):

            for direction in ('Right', 'Left'):
                for sanction_button in gui.get('MatchWindowRefereeSanctionsTabTeam' + ('A' if team == match.left_team else 'B') + 'Sanctions' + direction).children:

                    if i < 3:
                        sanction_button.disabled = True
                        continue

                    if sanction_button.background_normal.split('/')[-1].split('.')[0] == SANCTIONS_LEVELS[i]:
                        
                        if i > SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person_name_string)[0]):
                            sanction_button.disabled = False
                        elif i == SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person_name_string)[0]):
                            if self.get_person_sanction_level(team, person_name_string)[1] < getattr(py.match.match_config, sanction_button.background_normal.split('/')[-1].split(".")[0] + '_amount_limitations_person'):
                                sanction_button.disabled = False      

    def apply_sanction_limitations(self, team):
        
        from DVA import match, frontend_references as gui
        
        if getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B')) != '':

            people_list = []

            if team.head_coach != '' and team.head_coach not in team.disqualified_staff:
                people_list.append(team.head_coach)
            for _staff_ in team.staff:
                if _staff_ not in team.disqualified_staff: people_list.append(_staff_)

            for person in team.players:
               
                if SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person.name_string)[0]) < SANCTIONS_LEVELS.index(getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B'))):
                    people_list.append(person)
                
                elif SANCTIONS_LEVELS.index(self.get_person_sanction_level(team, person.name_string)[0]) == SANCTIONS_LEVELS.index(getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B'))):
                    
                    if self.get_person_sanction_level(team, person.name_string)[1] < getattr(py.match.match_config, getattr(self, 'sanction_chosen_' + ('A' if team == match.left_team else 'B')) + '_amount_limitations_person'):
                        people_list.append(person)
                    
                    else:
                        if getattr(self, 'person_chosen_' + ('A' if team == match.left_team else 'B')) == person.name_string:
                            self.clear_chosen_person(team)

                else:
                    if getattr(self, 'person_chosen_' + ('A' if team == match.left_team else 'B')) == person.name_string:
                        self.clear_chosen_person(team)

        else:
            people_list = self.get_people_list(team)

        return people_list
    
    def on_load(self, team, start_index, end_index, is_scrolling=False, *args):

        from DVA import match, frontend_references as gui
     
        if team == 'A':

            self.get_save_button_state(match.left_team)
            self.apply_team_limitations(match.left_team)
            if self.person_chosen_A != '':
                self.apply_person_limitations(match.left_team, self.person_chosen_A)
            self.apply_sanction_limitations(match.left_team)
            if not is_scrolling:
                self.calculate_popup(match.left_team)
            self.init_visual_elements(match.left_team, start_index, end_index, is_scrolling)

        elif team == 'B':  
          
            self.get_save_button_state(match.right_team)
            self.apply_team_limitations(match.right_team)
            if self.person_chosen_B != '':
                self.apply_person_limitations(match.right_team, self.person_chosen_B)
            self.apply_sanction_limitations(match.right_team)
            if not is_scrolling:
                self.calculate_popup(match.right_team)            
            self.init_visual_elements(match.right_team, start_index, end_index, is_scrolling)  

    def sanction_button_pressed(self, *args):

        from DVA import match, frontend_references as gui 

        if gui.get('MatchWindowRefereeSanctionsTabHeader').current_tab == gui.get('MatchWindowRefereeSanctionsTeamATab'):
            
            if args[0].state == 'down':
                self.sanction_chosen_A = args[0].background_normal.split('/')[-1].split('.')[0]
            else:
                self.sanction_chosen_A = ''
            self.hide_people_list(match.left_team, args[0])

            match.left_team.PlayersList.load('Sanctions', self.apply_sanction_limitations(match.left_team), ToggleButton, with_numbers=True)
            match.left_team.PlayersList.scroll(0,6, ToggleButton, with_numbers=True, choice_data=self.person_chosen_A)
            indexes[4] = 0

            self.get_save_button_state(match.left_team)

        elif gui.get('MatchWindowRefereeSanctionsTabHeader').current_tab == gui.get('MatchWindowRefereeSanctionsTeamBTab'):

            if args[0].state == 'down':
                self.sanction_chosen_B = args[0].background_normal.split('/')[-1].split('.')[0]
            else:
                self.sanction_chosen_B = ''
            self.hide_people_list(match.right_team, args[0])

            match.right_team.PlayersList.load('Sanctions', self.apply_sanction_limitations(match.right_team), ToggleButton, with_numbers=True)
            match.right_team.PlayersList.scroll(0,6, ToggleButton, with_numbers=True, choice_data=self.person_chosen_B)
            indexes[5] = 0

            self.get_save_button_state(match.right_team)

    def person_button_pressed(self, *args):

        from DVA import match, frontend_references as gui

        if gui.get('MatchWindowRefereeSanctionsTabHeader').current_tab == gui.get('MatchWindowRefereeSanctionsTeamATab'):

            if args[0].state == 'down':
                self.person_chosen_A = args[0].text
                self.apply_person_limitations(match.left_team, args[0].text)
            else:
                self.person_chosen_A = ''
                self.enable_every_sanction(match.left_team)
                self.apply_team_limitations(match.left_team)

            self.get_save_button_state(match.left_team)

        elif gui.get('MatchWindowRefereeSanctionsTabHeader').current_tab == gui.get('MatchWindowRefereeSanctionsTeamBTab'):

            if args[0].state == 'down':
                self.person_chosen_B = args[0].text
                self.apply_person_limitations(match.right_team, args[0].text)
            else:
                self.person_chosen_B = ''
                self.enable_every_sanction(match.right_team)
                self.apply_team_limitations(match.right_team)

            self.get_save_button_state(match.right_team)

    def cancel_button_pressed(self, *args):
        
        from DVA import match, frontend_references as gui
        
        if gui.get('MatchWindowRefereeSanctionsTabHeader').current_tab == gui.get('MatchWindowRefereeSanctionsTeamATab'):

            self.clear_chosen_sanction(match.left_team)
            self.clear_chosen_person(match.left_team)

            for direction in ('Left', 'Right'):
                for sanction_button in gui.get('MatchWindowRefereeSanctionsTabTeamASanctions' + direction).children:
                    sanction_button.state = 'normal'

            for player_button in gui.get('MatchWindowRefereeSanctionsTeamAPEOPLELIST').children:
                player_button.state = 'normal'

        elif gui.get('MatchWindowRefereeSanctionsTabHeader').current_tab == gui.get('MatchWindowRefereeSanctionsTeamBTab'):

            self.clear_chosen_sanction(match.right_team)
            self.clear_chosen_person(match.right_team)

            for direction in ('Left', 'Right'):
                for sanction_button in gui.get('MatchWindowRefereeSanctionsTabTeamBSanctions' + direction).children:
                    sanction_button.state = 'normal'

            for player_button in gui.get('MatchWindowRefereeSanctionsTeamBPEOPLELIST').children:
                player_button.state = 'normal'

    def save_button_pressed(self, *args):
        
        from DVA import match, frontend_references as gui

        if gui.get('MatchWindowRefereeSanctionsTabHeader').current_tab == gui.get('MatchWindowRefereeSanctionsTeamATab'):

            sanction_chosen = self.sanction_chosen_A
            person_chosen = self.person_chosen_A

            self.sanction_chosen_A = ''
            self.person_chosen_A = ''

            match.officials[0].sanction(sanction_chosen, person_chosen, match.left_team)

            if self.sanction_chosen_A != 'expulsion' and self.sanction_chosen_A != 'disqualification':
                self.cancel_button_pressed(None)

        elif gui.get('MatchWindowRefereeSanctionsTabHeader').current_tab == gui.get('MatchWindowRefereeSanctionsTeamBTab'):

            sanction_chosen = self.sanction_chosen_B
            person_chosen = self.person_chosen_B

            self.sanction_chosen_B = ''
            self.person_chosen_B = ''

            match.officials[0].sanction(sanction_chosen, person_chosen, match.right_team)

            if self.sanction_chosen_B != 'expulsion' and self.sanction_chosen_B != 'disqualification':
                self.cancel_button_pressed(None)


class SubstitutionsWindowBase(Screen):
    
    class SharedArea(GridLayout):

        def __init__(self, team, **kwargs):
            
            super().__init__()
            
            self.rows = 1
            self.size_hint = (1, 1)
            self.padding = [20, 40]

            self.content = GridLayout(cols=3, padding=[20, 0, -20, 0], spacing=[40])

            self.content.list_on_court = GridLayout(rows=6, spacing=[20])
            self.content.list_on_bench = GridLayout(rows=6, spacing=[20])
            self.content.scrollbar = Slider(orientation='vertical', size_hint=(0.01, 1), opacity=0, value=10, step=1, range=[0, 10])
            
            for _ in range(0, 6):
                self.content.list_on_court.add_widget(ToggleButton(group='court'+team, text='Player on court'))
                self.content.list_on_bench.add_widget(ToggleButton(group='bench'+team, text='Player on the bench'))

            self.content.add_widget(self.content.list_on_court)
            self.content.add_widget(self.content.list_on_bench)
            self.content.add_widget(self.content.scrollbar)
            self.add_widget(self.content)

            self.content.scrollbar.bind(on_touch_up=scroll__init)

    def __init__(self):
        
        super().__init__()

        self.design = GridLayout(rows=1)
        self.design.main_widget = GridLayout(rows=2)

        self.design.main_widget.referee_or_shared_area_spot = GridLayout(rows=1)

        self.design.main_widget.buttons = GridLayout(cols=5, size_hint=(1, 0.1), padding=[5])
        self.design.main_widget.buttons.cancel = Button(text=buttons[language_code][2])
        self.design.main_widget.buttons.next = Button(text=buttons[language_code][1])

        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.cancel)
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.next)

        self.design.main_widget.buttons.cancel.bind(on_release=self.cancel_button)
        self.design.main_widget.buttons.next.bind(on_release=self.next_button)
        self.design.main_widget.buttons.next.disabled = True

        self.requests_counter = 0
        
        self.player_out_A = ''
        self.player_in_A = ''
        self.player_out_B = ''
        self.player_in_B = ''

        self.forced_A = False
        self.forced_B = False

    def get_save_button_state(self, team):
        
        from DVA import match, frontend_references as gui

        gui.get('MatchWindowRefereeSubstitutionsSaveButton').disabled = True

        for button in gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('A' if team == match.left_team else 'B') + 'OnCourtPLAYERSLIST').children:
            if button.state == 'down':
                for __button__ in gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('A' if team == match.left_team else 'B') + 'OnBenchPLAYERSLIST').children:
                    if __button__.state == 'down':
                        gui.get('MatchWindowRefereeSubstitutionsSaveButton').disabled = False

    def get_subs_requests(self, team):

        from DVA import match

        team_subs = 0
        team_subs_requests = 0
        opposite_team_subs = 0
        opposite_team_subs_requests = 0

        for substitution in match.sets[-1].substitutions:
            
            if substitution.team == team.long_name:
                team_subs += 1
                if substitution.then_score == match.sets[-1].score or (substitution.then_score[0] == match.sets[-1].score[1] and substitution.then_score[1] == match.sets[-1].score[0]): 
                    if substitution.request_counter != self.requests_counter:
                        team_subs_requests += 1

            else:
                opposite_team_subs += 1
                if substitution.then_score == match.sets[-1].score or (substitution.then_score[0] == match.sets[-1].score[1] and substitution.then_score[1] == match.sets[-1].score[0]):
                    if substitution.request_counter != self.requests_counter:
                        opposite_team_subs_requests += 1
        
        return team_subs, team_subs_requests, opposite_team_subs, opposite_team_subs_requests

    def calculate_pop_ups(self, team, reverse_sub_check='', list_to_check=''):
            
        from DVA import match, frontend_references as gui

        if reverse_sub_check == '':
            
            if not match.sets[-1].is_tie_break:
                
                if self.get_subs_requests(team)[0] >= max_substitutions_regular_set:

                    if self.get_subs_requests(team)[2] < max_substitutions_regular_set and (not hasattr(match.sets[-1], 'wrong_sub_warned_' + ('A' if team == match.left_team else 'B'))):
                        setattr(match.sets[-1], 'wrong_sub_warned_' + ('A' if team == match.left_team else 'B'), True)
                        gui.get('MatchWindowRefereeSubstitutionsTabHeader').switch_to(gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab'))
                        gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab').trigger_action()
                    else:
                        PopUpWindow().show_pop_up(substitution_errors[language_code][0])

            else:

                if self.get_subs_requests(team)[0] >= max_substitutions_final_set:
                    
                    if self.get_subs_requests(team)[2] < max_substitutions_final_set and (not hasattr(match.sets[-1], 'wrong_sub_warned_' + ('A' if team == match.left_team else 'B'))):
                        setattr(match.sets[-1], 'wrong_sub_warned_' + ('A' if team == match.left_team else 'B'), True)
                        gui.get('MatchWindowRefereeSubstitutionsTabHeader').switch_to(gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab'))
                        gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab').trigger_action()
                    else:
                        PopUpWindow().show_pop_up(substitution_errors[language_code][0])

            if self.get_subs_requests(team)[1] >= substitutions_requests_from_a_team_during_one_play:
                
                if self.get_subs_requests(team)[3] < substitutions_requests_from_a_team_during_one_play and (not hasattr(match.sets[-1], 'extra_sub_warned_' + ('A' if team == match.left_team else 'B'))):
                    setattr(match.sets[-1], 'extra_sub_warned_' + ('A' if team == match.left_team else 'B'), True)
                    gui.get('MatchWindowRefereeSubstitutionsTabHeader').switch_to(gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab'))
                    gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab').trigger_action()
                else:
                    PopUpWindow().show_pop_up(substitution_errors[language_code][1])

        elif reverse_sub_check != '':
            
            flag = True
            reverse_sub_partner = ''
            reverse_subs_count = 0

            for button in gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ("A" if team == match.left_team else 'B') + 'On' + list_to_check + 'PLAYERSLIST').children:
                if button.state == 'down':
                    flag = False

            if flag:

                if only_reverse_substitutions:
                    for substitution in match.sets[-1].substitutions:    
                        if substitution.player_in == reverse_sub_check.split(maxsplit=1)[1] or substitution.player_out == reverse_sub_check.split(maxsplit=1)[1]:
                            
                            if substitution.player_in == reverse_sub_check.split(maxsplit=1)[1]:
                                reverse_sub_partner = substitution.player_out
                            else:
                                reverse_sub_partner = substitution.player_in
                            
                            for another_substitution in match.sets[-1].substitutions:
                                
                                if another_substitution != substitution and (another_substitution.player_in == reverse_sub_check.split(maxsplit=1)[1] or another_substitution.player_out == reverse_sub_check.split(maxsplit=1)[1]):
                                    reverse_subs_count += 1
                                    if another_substitution.player_in == reverse_sub_check.split(maxsplit=1)[1]:
                                        reverse_sub_partner = another_substitution.player_out
                                    else:
                                        reverse_sub_partner = another_substitution.player_in

                if (not match.sets[-1].is_tie_break) and reverse_subs_count >= reverse_substitutions_amount_regular_set:
                    PopUpWindow().show_pop_up(substitution_errors[language_code][2])
                elif  match.sets[-1].is_tie_break and reverse_subs_count >= reverse_substitutions_amount_final_set:
                    PopUpWindow().show_pop_up(substitution_errors[language_code][2])
                
                if reverse_sub_partner != '':
                    PopUpWindow().show_pop_up(substitution_errors[language_code][3] + '\n' + reverse_sub_partner)

    def get_players_list(self, team, forced=False):

        from py.core import get_people_list

        return get_people_list(team, with_expulsed_players=forced, with_disqualified_players=forced, end_index=players_in_team)

    def get_subs_list(self, team):

        from py.core import get_people_list
        
        return get_people_list(team, start_index=players_in_team, with_liberos=libero_allowed_to_substitute)

    def forced_disable_enable(self, team, boolean):
        
        from DVA import match, frontend_references as gui
        
        gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelSubstitutions'))
        gui.get('MatchWindowRefereeSubstitutionsTabHeader').switch_to(gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('A' if team == match.left_team else 'B') + 'Tab'))
        gui.get('MatchWindowRefereeTabPanelMatch').disabled = boolean
        gui.get('MatchWindowRefereeTabPanelSanctions').disabled = boolean
        gui.get('MatchWindowRefereeTabPanelProtests').disabled = boolean
        gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab').disabled = boolean

    def init_visual_elements(self, team, start_index, end_index, forced):
        
        from DVA import match, frontend_references as gui
        from gfx.visual_elements import TeamPeopleList, TeamName

        team.Name = TeamName(gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('A' if team == match.left_team else 'B') + 'Tab'))
        team.Name.load(team.long_name)
        for opposite_team in (match.left_team, match.right_team):
            if opposite_team != team: 
                opposite_team.Name = TeamName(gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab'))
                opposite_team.Name.load(opposite_team.long_name)

        team.PlayersList = TeamPeopleList(gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('A' if team == match.left_team else 'B') + 'OnCourtPLAYERSLIST'))
        team.PlayersList.load('Substitutions', self.get_players_list(team, forced), ToggleButton, with_numbers=True)          

        if not forced:
            if getattr(self, 'player_out_' + ('A' if team == match.left_team else 'B')) != '':
                team.PlayersList.scroll(start_index, end_index, ToggleButton, with_numbers=True, choice_data=str(getattr(self, 'player_out_' + ('A' if team == match.left_team else 'B')).number) + ' ' + getattr(self, 'player_out_' + ('A' if team == match.left_team else 'B')).name_string)
            else:
                team.PlayersList.scroll(start_index, end_index, ToggleButton, with_numbers=True, choice_data='')

        else:
            team.PlayersList.scroll(start_index, end_index, ToggleButton, with_numbers=True, choice_data=match.sets[-1].sanctions[-1].person, disabled_data=True)
            for player in team.players:
                if player.name_string == match.sets[-1].sanctions[-1].person:
                    setattr(self, 'player_out_' + ('A' if team == match.left_team else 'B'), player)

        team.PlayersList = TeamPeopleList(gui.get('MatchWindowRefereeSubstitutionsTabTeam' + ('A' if team == match.left_team else 'B') + 'OnBenchPLAYERSLIST'))
        team.PlayersList.load('Substitutions', self.get_subs_list(team), ToggleButton, with_numbers=True)
        
        if not forced:
            if getattr(self, 'player_in_' + ('A' if team == match.left_team else 'B')) != '':
                team.PlayersList.scroll(start_index, end_index, ToggleButton, with_numbers=True, choice_data=str(getattr(self, 'player_in_' + ('A' if team == match.left_team else 'B')).number) + ' ' + getattr(self, 'player_in_' + ('A' if team == match.left_team else 'B')).name_string)
            else:
                team.PlayersList.scroll(start_index, end_index, ToggleButton, with_numbers=True, choice_data='')
        
    def on_load(self, team, start_index, end_index, forced=False, *args):

        from DVA import match, frontend_references as gui
        
        if team == 'A':

            self.forced_A = forced
           
            self.get_save_button_state(match.left_team)
            self.calculate_pop_ups(match.left_team)
            self.init_visual_elements(match.left_team, start_index, end_index, self.forced_A)
            self.forced_disable_enable(match.left_team, self.forced_A)

        elif team == 'B':
           
            self.forced_B = forced

            self.get_save_button_state(match.right_team)
            self.calculate_pop_ups(match.right_team)
            self.init_visual_elements(match.right_team, start_index, end_index, self.forced_B)
            self.forced_disable_enable(match.right_team, self.forced_B)

    def on_court_player_button_pressed(self, *args):
        
        from DVA import match, frontend_references as gui

        if gui.get('MatchWindowRefereeSubstitutionsTabHeader').current_tab == gui.get('MatchWindowRefereeSubstitutionsTabTeamATab'):

            self.player_out_A = ''

            self.get_save_button_state(match.left_team)
            if args[0].state == 'down':
                self.calculate_pop_ups(match.left_team, args[0].text, 'Bench')

            for player in match.left_team.players:
                if args[0].text == str(player.number) + ' ' + player.name_string and args[0].state == 'down':
                    self.player_out_A = player                               
           
        elif gui.get('MatchWindowRefereeSubstitutionsTabHeader').current_tab == gui.get('MatchWindowRefereeSubstitutionsTabTeamBTab'):

            self.player_out_B = ''

            self.get_save_button_state(match.right_team)
            if args[0].state == 'down':
                self.calculate_pop_ups(match.right_team, args[0].text, 'Bench')

            for player in match.right_team.players:
                if args[0].text == str(player.number) + ' ' + player.name_string and args[0].state == 'down':
                    self.player_out_B = player                               

    def on_bench_player_button_pressed(self, *args):
        
        from DVA import match, frontend_references as gui

        if gui.get('MatchWindowRefereeSubstitutionsTabHeader').current_tab == gui.get('MatchWindowRefereeSubstitutionsTabTeamATab'):
            
            self.player_in_A = ''

            self.get_save_button_state(match.left_team)
            if args[0].state == 'down':
                self.calculate_pop_ups(match.left_team, args[0].text, 'Court')

            for player in match.left_team.players:
                if args[0].text == str(player.number) + ' ' + player.name_string and args[0].state == 'down':
                    self.player_in_A = player

        elif gui.get('MatchWindowRefereeSubstitutionsTabHeader').current_tab == gui.get('MatchWindowRefereeSubstitutionsTabTeamBTab'):

            self.player_in_B = ''

            self.get_save_button_state(match.right_team)
            if args[0].state == 'down':
                self.calculate_pop_ups(match.right_team, args[0].text, 'Court')

            for player in match.right_team.players:
                if args[0].text == str(player.number) + ' ' + player.name_string and args[0].state == 'down':
                    self.player_in_B = player                               

    def next_button(self, *args):
        
        from DVA import match, frontend_references as gui
        from py.match.objects import HeadCoach

        if gui.get('MatchWindowRefereeSubstitutionsTabHeader').current_tab == gui.get('MatchWindowRefereeSubstitutionsTabTeamATab'):

            if not match.left_team.head_coach == '':
                match.left_team.head_coach.substitution(match.left_team, self.player_in_A, self.player_out_A, self.requests_counter, self.forced_A)
            else:
                HeadCoach.substitution(None, match.left_team, self.player_in_A, self.player_out_A, self.requests_counter, self.forced_A)
        
        else:
            
            if not match.right_team.head_coach == '':
                match.right_team.head_coach.substitution(match.right_team, self.player_in_B, self.player_out_B, self.requests_counter, self.forced_B)
            else:
                HeadCoach.substitution(None, match.right_team, self.player_in_B, self.player_out_B, self.requests_counter, self.forced_B)

        self.cancel_button(args)

    def cancel_button(self, *args):
        
        from DVA import frontend_references as gui

        if gui.get('MatchWindowRefereeSubstitutionsTabHeader').current_tab == gui.get('MatchWindowRefereeSubstitutionsTabTeamATab'):
            
            for button in gui.get('MatchWindowRefereeSubstitutionsTabTeamAOnCourtPLAYERSLIST').children:
                if button.state == 'down':
                    button.state = 'normal'
                
            for button in gui.get('MatchWindowRefereeSubstitutionsTabTeamAOnBenchPLAYERSLIST').children:
                if button.state == 'down':
                    button.state = 'normal'
        
            self.player_in_A = ''
            self.player_out_A = ''

        elif gui.get('MatchWindowRefereeSubstitutionsTabHeader').current_tab == gui.get('MatchWindowRefereeSubstitutionsTabTeamBTab'):
            
            for button in gui.get('MatchWindowRefereeSubstitutionsTabTeamBOnCourtPLAYERSLIST').children:
                if button.state == 'down':
                    button.state = 'normal'
                
            for button in gui.get('MatchWindowRefereeSubstitutionsTabTeamBOnBenchPLAYERSLIST').children:
                if button.state == 'down':
                    button.state = 'normal'
        
            self.player_in_B = ''
            self.player_out_B = ''


class SubstitutionsWindowReferee(SubstitutionsWindowBase):

    def __init__(self):
        
        super().__init__()

        self.design.main_widget.referee_or_shared_area_spot.cols = 1
        self.design.main_widget.referee_or_shared_area_spot.content = TabbedPanel(do_default_tab=False, background_color=[0, 0, 0, 0])
        self.design.main_widget.referee_or_shared_area_spot.content.team_A = TabbedPanelHeader(text='Team A')
        self.design.main_widget.referee_or_shared_area_spot.content.team_B = TabbedPanelHeader(text='Team B')

        content_A = self.SharedArea('A')
        content_B = self.SharedArea('B')

        self.design.main_widget.referee_or_shared_area_spot.content.team_A.content = content_A
        self.design.main_widget.referee_or_shared_area_spot.content.team_B.content = content_B

        self.design.main_widget.referee_or_shared_area_spot.content.add_widget(self.design.main_widget.referee_or_shared_area_spot.content.team_A)
        self.design.main_widget.referee_or_shared_area_spot.content.add_widget(self.design.main_widget.referee_or_shared_area_spot.content.team_B)

        self.design.main_widget.referee_or_shared_area_spot.add_widget(self.design.main_widget.referee_or_shared_area_spot.content)
        self.design.main_widget.add_widget(self.design.main_widget.referee_or_shared_area_spot)
        self.design.main_widget.add_widget(self.design.main_widget.buttons)

        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

        for button in self.design.main_widget.referee_or_shared_area_spot.content.team_A.content.content.list_on_court.children:
            button.bind(on_release=self.on_court_player_button_pressed)
        for button in self.design.main_widget.referee_or_shared_area_spot.content.team_B.content.content.list_on_court.children:
            button.bind(on_release=self.on_court_player_button_pressed)
        for button in self.design.main_widget.referee_or_shared_area_spot.content.team_A.content.content.list_on_bench.children:
            button.bind(on_release=self.on_bench_player_button_pressed)
        for button in self.design.main_widget.referee_or_shared_area_spot.content.team_B.content.content.list_on_bench.children:
            button.bind(on_release=self.on_bench_player_button_pressed)

        self.design.main_widget.referee_or_shared_area_spot.content.team_A.bind(on_release=self.header_button)
        self.design.main_widget.referee_or_shared_area_spot.content.team_B.bind(on_release=self.header_button)       

    def header_button(self, *args):

        from DVA import frontend_references as gui

        if args[0] == gui.get('MatchWindowRefereeSubstitutionsTabTeamATab'):
            self.on_load('A', scroll_get_indexes('Substitutions', 'A')[0], scroll_get_indexes('Substitutions', 'A')[1], False)
        elif args[0] == gui.get('MatchWindowRefereeSubstitutionsTabTeamBTab'):
            self.on_load('B', scroll_get_indexes('Substitutions', 'B')[0], scroll_get_indexes('Substitutions', 'B')[1], False)


class ProtestWindowBase(Screen):

    class SharedPart(GridLayout):

        def __init__(self):
            
            super().__init__()

            self.rows = 1
            self.content = GridLayout(rows=2, padding=[10])
            self.content.team_name = Label(font_size=40, text=protest_window[language_code][0] + ' ' + 'TeamName', size_hint=(1, 0.2))
            self.content.text = TextInput(focus=False)
            self.content.add_widget(self.content.team_name)
            self.content.add_widget(self.content.text)
            self.add_widget(self.content)

    def __init__(self):

        super().__init__()

        self.design = GridLayout(cols=1)
        self.design.main_widget = GridLayout(rows=2)

        self.design.main_widget.referee_or_text_input_spot = GridLayout(rows=1)
        self.design.main_widget.buttons = GridLayout(cols=5, size_hint=(0, 0.1), padding=[5])
        self.design.main_widget.buttons.cancel = Button(text=buttons[language_code][2])
        self.design.main_widget.buttons.next = Button(text=buttons[language_code][1])

        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(Label())
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.cancel)
        self.design.main_widget.buttons.add_widget(self.design.main_widget.buttons.next)

        self.design.main_widget.buttons.cancel.bind(on_release=self.cancel_button_pressed)
        self.design.main_widget.buttons.next.bind(on_release=self.save_button_pressed)
        self.design.main_widget.buttons.disabled = True

    def calculate_pop_ups(self, team):
        
        from DVA import match
        
        if team.protest == '' and match.status != 'Finished':
            PopUpWindow().show_protest_creation_window(team)

    def init_visual_elements(self, team):
        
        from DVA import match, frontend_references as gui
        from gfx.visual_elements import TeamName

        team.Name = TeamName([gui.get('MatchWindowRefereeProtestsTabTeam' + ('A' if team == match.left_team else 'B') + 'Tab')])
        team.Name.load(team.long_name)

        team.Name = TeamName([gui.get('MatchWindowRefereeProtestsTabTeam' + ('A' if team == match.left_team else 'B') + 'Label')])
        team.Name.load(protest_window[language_code][0] + team.long_name + protest_window[language_code][1]) # before and after the team's name for differeny languages
    
        for opposite_team in (match.left_team, match.right_team):
            if opposite_team != team: 
                opposite_team.Name = TeamName(gui.get('MatchWindowRefereeProtestsTabTeam' + ('B' if team == match.left_team else 'A') + 'Tab'))
                opposite_team.Name.load(opposite_team.long_name)

    def on_load(self, team, mode='declare', team_object=''):
        
        from DVA import match, frontend_references as gui

        self.mode = mode
        self.team = team_object

        if team == 'A':
            self.init_visual_elements(match.left_team)
            gui.get('MatchWindowRefereeProtestsTabTeamATextInput').focus = False
        else:
            self.init_visual_elements(match.right_team)
            gui.get('MatchWindowRefereeProtestsTabTeamBTextInput').focus = False
        
        if self.mode == 'write':
            self.design.main_widget.buttons.disabled = False

    def on_text_input_click(self, *args):
        
        from DVA import match, frontend_references as gui
         
        if args[0].focus and self.mode == 'declare':

            if args[0] == gui.get('MatchWindowRefereeProtestsTabTeamATextInput'):
                self.calculate_pop_ups(match.left_team)
                gui.get('MatchWindowRefereeProtestsTabTeamATextInput').focus = False
            elif args[0] == gui.get('MatchWindowRefereeProtestsTabTeamBTextInput'):
                self.calculate_pop_ups(match.right_team)
                gui.get('MatchWindowRefereeProtestsTabTeamBTextInput').focus = False

    def cancel_button_pressed(self, *args):
        
        from DVA import sm, frontend_references as gui
        
        self.team.protest = ''
        
        sm.switch_to(gui.get('EndWindowReferee'))
        gui.get('EndWindowReferee').on_load()

    def save_button_pressed(self, *args):
        
        from py.match.objects import HeadCoach
        from DVA import sm, frontend_references as gui

        if self.team.head_coach != '':
            self.team.head_coach.write_protest(self.team)
        else:
            HeadCoach.write_protest('', self.team)
        
        sm.switch_to(gui.get('EndWindowReferee'))
        gui.get('EndWindowReferee').on_load()


class ProtestWindowReferee(ProtestWindowBase):

    def __init__(self):
        super().__init__()

        self.design.main_widget.referee_or_text_input_spot.rows = 1
        self.design.main_widget.referee_or_text_input_spot.content = TabbedPanel(do_default_tab=False, background_color=[0, 0, 0, 0])
        self.design.main_widget.referee_or_text_input_spot.content.team_A = TabbedPanelHeader(text='Team A')
        self.design.main_widget.referee_or_text_input_spot.content.team_B = TabbedPanelHeader(text='Team B')

        team_A = self.SharedPart()
        team_B = self.SharedPart()

        self.design.main_widget.referee_or_text_input_spot.content.team_A.content = team_A
        self.design.main_widget.referee_or_text_input_spot.content.team_B.content = team_B

        self.design.main_widget.referee_or_text_input_spot.content.add_widget(self.design.main_widget.referee_or_text_input_spot.content.team_A)
        self.design.main_widget.referee_or_text_input_spot.content.add_widget(self.design.main_widget.referee_or_text_input_spot.content.team_B)

        self.design.main_widget.referee_or_text_input_spot.add_widget(self.design.main_widget.referee_or_text_input_spot.content)
        self.design.main_widget.add_widget(self.design.main_widget.referee_or_text_input_spot)
        self.design.main_widget.add_widget(self.design.main_widget.buttons)

        self.design.main_widget.referee_or_text_input_spot.content.team_A.bind(on_release=self.header_button)
        self.design.main_widget.referee_or_text_input_spot.content.team_B.bind(on_release=self.header_button)

        self.design.main_widget.referee_or_text_input_spot.content.team_A.content.content.text.bind(focus=self.on_text_input_click)
        self.design.main_widget.referee_or_text_input_spot.content.team_B.content.content.text.bind(focus=self.on_text_input_click)

        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

    def header_button(self, *args):
        
        from DVA import frontend_references as gui

        if args[0] == gui.get('MatchWindowRefereeProtestsTabTeamATab'):
            self.on_load('A')
        elif args[0] == gui.get('MatchWindowRefereeProtestsTabTeamBTab'):
            self.on_load('B')


class MatchWindowBase(Screen):

    class Scores(GridLayout):

        class ServeBalls(GridLayout):

            def __init__(self):
                
                super().__init__(cols=3)

                self.add_widget(Image(source=os.getcwd() + '/gfx/match/serve_ball.png', opacity=1))
                self.add_widget(Label())
                self.add_widget(Image(source=os.getcwd() + '/gfx/match/serve_ball.png', opacity=0))

        def __init__(self, **kwargs):
            
            super().__init__()
            
            self.rows = 2
            self.cols = 5
            self.spacing = [100, -100]

            self.set_scores_and_serve_balls = GridLayout(rows=3, padding=[-20], size_hint=(2, 0.1))

            self.set_scores_and_serve_balls.digits = GridLayout(cols=3, spacing=[-50])

            self.set_scores_and_serve_balls.digits.add_widget(Label(font_size=48, text='0'))
            self.set_scores_and_serve_balls.digits.add_widget(Label(font_size=48, text=':'))
            self.set_scores_and_serve_balls.digits.add_widget(Label(font_size=48, text='0'))

            self.set_scores_and_serve_balls.add_widget(Label())
            self.set_scores_and_serve_balls.add_widget(self.set_scores_and_serve_balls.digits)
            self.set_scores_and_serve_balls.add_widget(self.ServeBalls())

            self.add_widget(ButtonImage(source=os.getcwd() + '/gfx/match/arrows/arrow_back.png', size_hint=(1, 1)))
            self.add_widget(Label(font_size=48, text='Team A'))
            self.add_widget(Label())
            self.add_widget(Label(font_size=48, text='Team B'))
            self.add_widget(ButtonImage(source=os.getcwd() + '/gfx/match/arrows/arrow_forward.png', size_hint=(1, 1)))

            self.add_widget(Label())
            self.add_widget(Label(font_size=96, text='0'))
            self.add_widget(self.set_scores_and_serve_balls)
            self.add_widget(Label(font_size=96, text='0'))
            self.add_widget(Label())

            self.children[5].bind(on_release=MatchWindowReferee.MatchWindowReferee.forward_button_pressed)
            self.children[9].bind(on_release=MatchWindowReferee.MatchWindowReferee.back_button_pressed)

    class Team(GridLayout):

        def __init__(self, **kwargs):

            super().__init__()

            self.rows = 3
            self.padding = [10]

            self.players = TeamWidget(ButtonLabel)
            for number in self.players.real_indexes:
                number.font_size = 48
                number.bind(on_release=MatchWindowReferee.MatchWindowReferee.player_button_pressed)

            self.separators = BoxLayout(orientation='horizontal', size_hint_y=0.2)
            self.liberos = BoxLayout(orientation='horizontal', size_hint_y=0.3)

            self.liberos.cols = max(self.players.cols, max_amount_liberos)

            for i in range(0, self.players.cols):
                self.separators.add_widget(Label(text='-------------------------'))

            for i in range(0, max_amount_liberos):
                i = ButtonLabel(font_size=48, text=str(i + players_in_team), opacity=0)
                self.liberos.add_widget(i)
                i.bind(on_release=MatchWindowReferee.MatchWindowReferee.player_button_pressed)

            self.add_widget(self.players)
            self.add_widget(self.separators)
            self.add_widget(self.liberos)

    def __init__(self):

        super().__init__()

        self.design = GridLayout(cols=1)

        self.design.main_widget = GridLayout(rows=2)
        self.design.main_widget.tabs_m = TabbedPanel(do_default_tab=False, background_color=[0, 0, 0, 0])

        self.design.main_widget.tabs_m.coin_toss = TabbedPanelHeader(text=tabs[language_code][0])
        self.design.main_widget.tabs_m.team_set_up = TabbedPanelHeader(text=tabs[language_code][1])
        self.design.main_widget.tabs_m.line_up_set_up = TabbedPanelHeader(text=tabs[language_code][2])
        self.design.main_widget.tabs_m.match = TabbedPanelHeader(text=tabs[language_code][3])
        self.design.main_widget.tabs_m.substitutions = TabbedPanelHeader(text=tabs[language_code][4])

        self.design.main_widget.tabs_m.coin_toss.content = CoinTossWindow()
        self.design.main_widget.tabs_m.team_set_up.content = TeamSetUpWindowReferee()
        self.design.main_widget.tabs_m.line_up_set_up.content = LineUpSetUpReferee()
        self.design.main_widget.tabs_m.match.content = self.MatchWindowReferee()  # TODO change according to status
        self.design.main_widget.tabs_m.substitutions.content = SubstitutionsWindowReferee() # TODO remember about protest for coach's mode

        self.design.main_widget.tabs_m.add_widget(self.design.main_widget.tabs_m.coin_toss)
        self.design.main_widget.tabs_m.add_widget(self.design.main_widget.tabs_m.team_set_up)
        self.design.main_widget.tabs_m.add_widget(self.design.main_widget.tabs_m.line_up_set_up)
        self.design.main_widget.tabs_m.add_widget(self.design.main_widget.tabs_m.match)
        self.design.main_widget.tabs_m.add_widget(self.design.main_widget.tabs_m.substitutions)

        self.design.main_widget.tabs_m.substitutions.bind(on_release=self.substitutions_button_pressed)
        self.design.main_widget.tabs_m.match.bind(on_release=self.match_button_pressed)

    def substitutions_button_pressed(self, *args):

        from DVA import frontend_references as gui
        gui.get('MatchWindowRefereeSubstitutionsTabContent').requests_counter += 1
        gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load('A', scroll_get_indexes('Substitutions', 'A')[0], scroll_get_indexes('Substitutions', 'A')[1], False)

    def match_button_pressed(self, *args):

        from DVA import frontend_references as gui

        gui.get('MatchWindowRefereeMatchTabContent').on_load()

    def protest_button_pressed(self, *args):

        from DVA import frontend_references as gui

        gui.get('MatchWindowRefereeProtestsTabContent').on_load('A')
        gui.get('MatchWindowRefereeProtestsTabContent').on_load('B') # This was added because of some mistake with opposite team Name label not loading on re-entering the tab after issuing the protest that I coldn't catch.


class MatchWindowReferee(MatchWindowBase):

    class MatchWindowReferee(GridLayout):

        def __init__(self):

            super().__init__(cols=1)

            self.design = GridLayout(cols=1)
            self.design.main_widget = GridLayout()

            self.design.main_widget.rows = 3
            self.design.main_widget.padding = [0, -50, 0, 0]
            self.design.main_widget.spacing = [10]

            self.design.main_widget.score = MatchWindowBase.Scores()
            self.design.main_widget.teams = GridLayout(cols=3)
            self.design.main_widget.time_outs = GridLayout(cols=6, size_hint=(1, 0.15))

            self.design.main_widget.teams.team_A = MatchWindowBase.Team()
            self.design.main_widget.teams.error = GridLayout(rows=3, size_hint=(1, 0.5), padding=[50])
            self.design.main_widget.teams.error.button = ToggleButton(text=match_window[language_code][0])
            self.design.main_widget.teams.team_B = MatchWindowBase.Team()

            self.design.main_widget.teams.error.add_widget(Label())
            self.design.main_widget.teams.error.add_widget(self.design.main_widget.teams.error.button)
            self.design.main_widget.teams.error.add_widget(Label())

            self.design.main_widget.teams.add_widget(self.design.main_widget.teams.team_A)
            self.design.main_widget.teams.add_widget(self.design.main_widget.teams.error)
            self.design.main_widget.teams.add_widget(self.design.main_widget.teams.team_B)

            self.design.main_widget.time_outs.team_A = BoxLayout(orientation='horizontal')
            self.design.main_widget.time_outs.team_B = BoxLayout(orientation='horizontal')

            self.design.main_widget.add_widget(self.design.main_widget.score)
            self.design.main_widget.add_widget(self.design.main_widget.teams)
            self.design.main_widget.add_widget(self.design.main_widget.time_outs)

            self.design.add_widget(self.design.main_widget)
            self.add_widget(self.design)

        def calculate_pop_ups(self, mode):
            
            from py.match.events import SetStart
            from DVA import match_events_dispatch, match
            import time
            from py.match.core import get_time_instructions
            
            if len(match.sets) == 0 and match.status == 'Awaiting' and get_time_instructions(match.data, 'match_start')[0] == 'match_interval':
                PopUpWindow().show_interval_window([2, 3, get_time_instructions(match.data, 'match_start')[1], [mode]])  # TODO change according to status
            elif len(match.sets) == 0 and match.status == 'Awaiting' and get_time_instructions(match.data, 'match_start') == 'match_window':
                match.status = 'Ongoing'
                match.start_time = str(time.localtime()[3]) + ':' + str(time.localtime()[4])
                match_events_dispatch.run(SetStart, None, mode)

            if match.status == 'Ongoing' and get_time_instructions(match.data, 'set_start')[0] == 'set_interval' and match.sets[-1].status == 'Finished':
                PopUpWindow().show_interval_window([4, 4, get_time_instructions(match.data, 'set_start')[1], [mode]])
            elif match.status == 'Ongoing' and get_time_instructions(match.data, 'set_start') == 'set_window' and match.sets[-1].status == 'Finished':
                match_events_dispatch.run(SetStart, None, mode)

        def init_visual_elements(self):

            from DVA import match, frontend_references as gui
            from gfx.visual_elements import TeamName, TeamLineUp

            match.left_team.Name = TeamName(gui.get('MatchWindowRefereeMatchTabTeamAName'))
            match.left_team.Name.load(match.left_team.long_name)
            match.right_team.Name = TeamName(gui.get('MatchWindowRefereeMatchTabTeamBName'))
            match.right_team.Name.load(match.right_team.long_name)

            if match.left_team.LineUp == '':
                match.left_team.LineUp = TeamLineUp([gui.get('MatchWindowRefereeMatchTabTeamACourtPlayers'), gui.get('MatchWindowRefereeMatchTabTeamALiberos')])
                match.right_team.LineUp = TeamLineUp([gui.get('MatchWindowRefereeMatchTabTeamBCourtPlayers'), gui.get('MatchWindowRefereeMatchTabTeamBLiberos')])
            else:
                match.left_team.LineUp._switch_(match.right_team.LineUp)
        
            match.left_team.LineUp.load()
            match.right_team.LineUp.load()

        def on_load(self, mode='NEW', *args):

            self.enable_everything()
            self.calculate_pop_ups(mode)
            self.init_visual_elements()

        def enable_everything(self):

            from DVA import frontend_references as gui

            gui.get('MatchWindowRefereeTabPanelLineUpSetUp').disabled = True
            gui.get('MatchWindowRefereeTabPanel').disabled = False
            gui.get('MatchWindowRefereeTabPanelMatch').disabled = False
            gui.get('MatchWindowRefereeMatchTabContent').disabled = False
            gui.get('MatchWindowRefereeTabPanelSubstitutions').disabled = False
            if not (gui.get('MatchWindowRefereeProtestsTabTeamATab').disabled and not gui.get('MatchWindowRefereeProtestsTabTeamBTab').disabled):
                gui.get('MatchWindowRefereeTabPanelProtests').disabled = False
            gui.get('MatchWindowRefereeTabPanelSanctions').disabled = False
            gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelMatch'))

        def load_time_out_buttons(self):

            from DVA import match

            self.design.main_widget.time_outs.team_A.clear_widgets()
            self.design.main_widget.time_outs.team_B.clear_widgets()

            self.design.main_widget.time_outs.clear_widgets()

            if len(match.sets) < sets_to_win * 2 - 1:

                for i in range(0, time_outs_regular_set):
                    j = Button(text=match_window[language_code][1])
                    self.design.main_widget.time_outs.team_A.add_widget(j)
                    j.bind(on_release=self.time_out_button_pressed)

                for i in range(0, time_outs_regular_set):
                    j = Button(text=match_window[language_code][1])
                    self.design.main_widget.time_outs.team_B.add_widget(j)
                    j.bind(on_release=self.time_out_button_pressed)

            else:
                for i in range(0, time_outs_final_set):
                    j = Button(text=match_window[language_code][1])
                    self.design.main_widget.time_outs.team_A.add_widget(j)
                    j.bind(on_release=self.time_out_button_pressed)

                for i in range(0, time_outs_final_set):
                    j = Button(text=match_window[language_code][1])
                    self.design.main_widget.time_outs.team_B.add_widget(j)
                    j.bind(on_release=self.time_out_button_pressed)

            self.design.main_widget.time_outs.add_widget(self.design.main_widget.time_outs.team_A)

            for i in range(0, 2):
                self.design.main_widget.time_outs.add_widget(Label())

            self.design.main_widget.time_outs.add_widget(self.design.main_widget.time_outs.team_B)

        def time_out_button_pressed(self, *args):

            from DVA import match, frontend_references as gui
            from py.match.objects import HeadCoach

            if args[0] in gui.get('MatchWindowRefereeMatchTabTeamATimeOuts'):

                if match.left_team.head_coach != '':
                    match.left_team.head_coach.time_out(args[0], match.left_team)
                else:
                    HeadCoach.time_out('', args[0], match.left_team)

            else:

                if match.right_team.head_coach != '':
                    match.right_team.head_coach.time_out(args[0], match.right_team)
                else:
                    HeadCoach.time_out('', args[0], match.right_team)

        def player_button_pressed(*args):

            from DVA import match, frontend_references as gui

            if gui.get('MatchWindowRefereeMatchTabMistakeButton').state == 'down':
                event = 'mistake'
                gui.get('MatchWindowRefereeMatchTabMistakeButton').state = 'normal'
            else:
                event = 'point'

            if args[0] in match.left_team.LineUp.elements[0] or args[0] in match.left_team.LineUp.elements[1]:
                team = match.left_team
            else:
                team = match.right_team

            for player in team.players:
                if player.number == args[0].text:
                    if event == 'point':
                        player.point()
                        break
                    else:
                        player.mistake()
                        break

        def back_button_pressed(*args):
            
            from DVA import match_events_dispatch

            match_events_dispatch.back()

        def forward_button_pressed(*args):
            
            from DVA import match_events_dispatch

            match_events_dispatch.forward()

    def __init__(self):

        super().__init__()

        self.name = 'MatchWindowReferee'

        self.design.main_widget.tabs_m.sanctions = TabbedPanelHeader(text=tabs[language_code][6])
        self.design.main_widget.tabs_m.sanctions.content = SanctionsWindowReferee()
        self.design.main_widget.tabs_m.add_widget(self.design.main_widget.tabs_m.sanctions)

        self.design.main_widget.tabs_m.protests = TabbedPanelHeader(text=tabs[language_code][5])
        self.design.main_widget.tabs_m.protests.content = ProtestWindowReferee()
        self.design.main_widget.tabs_m.add_widget(self.design.main_widget.tabs_m.protests)

        self.design.main_widget.add_widget(self.design.main_widget.tabs_m)
        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

        self.design.main_widget.tabs_m.sanctions.bind(on_release=self.sanctions_button_pressed)
        self.design.main_widget.tabs_m.protests.bind(on_release=self.protest_button_pressed)

    def sanctions_button_pressed(self, *args):

        from DVA import frontend_references as gui

        gui.get('MatchWindowRefereeSanctionsTabContent').on_load('A', scroll_get_indexes('Sanctions', 'A')[0], scroll_get_indexes('Sanctions', 'A')[1])


class EndWindowBase(Screen):
    
    #def on_pre_enter(self, *args):

        #from DVA import match

        #match.loading_gif = PopUpWindow()
        #match.loading_gif.show_loading_gif()


    def __init__(self):

        super().__init__()

        self.design = GridLayout(rows=1)
        self.design.main_widget = GridLayout(rows=3, padding=[0, 15, 0, 0])

        self.design.main_widget.up = Label(font_size=30, size_hint=(1, 0.2))
        self.design.main_widget.middle = GridLayout(cols=2, spacing=[10], padding=[5, 50, 0, 50])
        self.design.main_widget.down = GridLayout(cols=3, size_hint=(1, 0.07))
        
        self.design.main_widget.middle.protocol_area = GridLayout(rows=2)
        self.design.main_widget.middle.buttons = GridLayout(rows=8)

        self.design.main_widget.down.back = Button(text=buttons[language_code][4], size_hint=(0.5, 0.5))
        self.design.main_widget.down.forward = Button(text=buttons[language_code][5], size_hint=(0.5, 0.5), disabled=True)

        self.design.main_widget.middle.protocol_area.image = ButtonImage()
        self.design.main_widget.middle.protocol_area.annotation = Label(text=match_end[language_code][0], size_hint=(1, 0.1))

        self.design.main_widget.middle.buttons.send_protocol = Button(text=match_end[language_code][3], disabled=True, opacity=0)
        self.design.main_widget.middle.buttons.save_protocol = Button(text=match_end[language_code][4])
        self.design.main_widget.middle.buttons.write_note = Button(text=match_end[language_code][5])
        self.design.main_widget.middle.buttons.winners_protest = Button(disabled=True)
        self.design.main_widget.middle.buttons.best_player_A = Spinner(disabled=True, opacity=0)
        self.design.main_widget.middle.buttons.best_player_B = Spinner(disabled=True, opacity=0)

        self.design.main_widget.middle.protocol_area.add_widget(self.design.main_widget.middle.protocol_area.image)
        self.design.main_widget.middle.protocol_area.add_widget(self.design.main_widget.middle.protocol_area.annotation)

        self.design.main_widget.middle.buttons.add_widget(self.design.main_widget.middle.buttons.send_protocol)
        self.design.main_widget.middle.buttons.add_widget(self.design.main_widget.middle.buttons.save_protocol)
        self.design.main_widget.middle.buttons.add_widget(Label())
        self.design.main_widget.middle.buttons.add_widget(self.design.main_widget.middle.buttons.write_note)
        self.design.main_widget.middle.buttons.add_widget(self.design.main_widget.middle.buttons.winners_protest)    
        self.design.main_widget.middle.buttons.add_widget(Label())
        self.design.main_widget.middle.buttons.add_widget(self.design.main_widget.middle.buttons.best_player_A)
        self.design.main_widget.middle.buttons.add_widget(self.design.main_widget.middle.buttons.best_player_B)

        self.design.main_widget.middle.add_widget(self.design.main_widget.middle.protocol_area)
        self.design.main_widget.middle.add_widget(self.design.main_widget.middle.buttons)

        self.design.main_widget.down.add_widget(self.design.main_widget.down.back)
        self.design.main_widget.down.add_widget(Label())
        self.design.main_widget.down.add_widget(self.design.main_widget.down.forward)

        self.design.main_widget.add_widget(self.design.main_widget.up)
        self.design.main_widget.add_widget(self.design.main_widget.middle)
        self.design.main_widget.add_widget(self.design.main_widget.down)

        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

        self.design.main_widget.middle.protocol_area.image.bind(on_release=self.protocol_image_pressed)
        
        self.design.main_widget.middle.buttons.winners_protest.bind(on_release=self.protest_button_pressed)
        self.design.main_widget.middle.buttons.write_note.bind(on_release=self.notes_button_pressed)
        self.design.main_widget.middle.buttons.save_protocol.bind(on_release=self.save_protocol_button_pressed)
        self.design.main_widget.middle.buttons.send_protocol.bind(on_release=self.send_protocol_button_pressed)

        self.design.main_widget.down.back.bind(on_release=self.back_button_pressed)
        self.design.main_widget.down.forward.bind(on_release=self.forward_button_pressed)

        self.protocol_image = BytesIO()

    def load_protocol(self):
        
        from DVA import match
        from py.match.protocol import borders

        def get_group_size_borders(sign, total_border, pieces_amount, division_offset=0):

            rv = []

            if sign == 0:
                indexes = [0, 2]
                opposite_indexes = [1, 3]
            elif sign == 1:
                indexes = [1, 3]
                opposite_indexes = [0, 2]

            step = int((total_border[indexes[1]] - total_border[indexes[0]]) / pieces_amount)               
        
            for i in range(pieces_amount):
                rv.append([[], [], [], []])

                rv[i][indexes[0]] = total_border[indexes[0]] + (i * step) + division_offset
                rv[i][opposite_indexes[0]] = total_border[opposite_indexes[0]]
                rv[i][indexes[1]] = total_border[indexes[0]] + (i + 1) * step - division_offset
                rv[i][opposite_indexes[1]] = total_border[opposite_indexes[1]]

            return rv            

        def fix_oversize(new_image_draw, new_image_size, text, size, font_name='times', font_size=40, font_fill=(0, 0, 0, 255)):
            
            text_to_insert_size = new_image_draw.textsize(text, font=ImageFont.truetype(font=font_name, size=font_size))        

            if text_to_insert_size[0] > new_image_size[0] or text_to_insert_size[1] > new_image_size[1]:
                original_font_size = font_size
                assured_text_size = new_image_draw.textsize(text, font=ImageFont.truetype(font=font_name, size=font_size))
                
                while assured_text_size[0] > new_image_size[0] or assured_text_size[1] > new_image_size[1]:

                    font_size -= 1
                    assured_text_size = new_image_draw.textsize(text, font=ImageFont.truetype(font=font_name, size=font_size))
                    if font_size <= int(original_font_size / 2) and text_to_insert_size[1] <= new_image_size[1]:
                        text_middle = int(len(text) / 2)
                        text = text[:text_middle] + '\n' + text[text_middle + 2:]
                        font_size = original_font_size

            return font_size

        def insert_text(text, size, font_name='times', font_size=40, font_fill=(0, 0, 0, 255), circle=False, circle_outline=(0, 0, 0, 255), circle_offset=(10, 5, 10, -5)):

            new_image_size = (size[2]-size[0], size[3]-size[1])
            new_image = PIL_Image.new('RGBA', new_image_size, 'white')
            new_image_draw = ImageDraw.ImageDraw(new_image)

            font_size = fix_oversize(new_image_draw, new_image_size, text, size, font_name, font_size, font_fill)

            new_image_draw.text((0, 0), text, font=ImageFont.truetype(font=font_name, size=font_size), fill=font_fill)          

            protocol_image.paste(new_image, size)

            if circle:
                image_draw.ellipse([i - j for i, j in zip(size, circle_offset)], outline=circle_outline)

        def sort_by_alphabet(list_to_sort):
            list_to_sort.sort()
            return list_to_sort

        def load_header():

            def load_competition_name():

                if hasattr(borders, 'HeaderCompetitionName'):
                    border = borders.HeaderCompetitionName
                    insert_text(match.competition_name, border, font_size=80)

            def load_match_city():
                
                match_city = match.city

                if len(match_city) != 0:
                    if not hasattr(borders, 'HeaderMatchCity_0') and not hasattr(borders, 'HeaderMatchCity_1'):
                        for i in range(len(match_city)):
                            border = getattr(borders, 'HeaderMatchCityChar' + str(i))
                            insert_text(str(match_city[i]), border)
                    elif hasattr(borders, 'HeaderMatchCity_0'):
                        border = get_group_size_borders(0, borders.HeaderMatchCity_0, len(match_city), 7)
                        for i in range(len(match_city)):
                            insert_text(match_city[i], border[i])
                    elif hasattr(borders, 'HeaderMatchCity_1'):
                        border = get_group_size_borders(1, borders.HeaderMatchCity_1, len(match_city), 7)
                        for i in range(len(match_city)):
                            insert_text(match_city[i], border[i])

            def load_match_court_address():

                match_court_address = match.street_address
                
                if len(match_court_address) != 0:
                    if not hasattr(borders, 'HeaderMatchCourtAddress_0') and not hasattr(borders, 'HeaderMatchCourtAddress_1'):
                        for i in range(len(match_court_address)):
                            border = getattr(borders, 'HeaderMatchCourtAddressChar' + str(i))
                            insert_text(str(match_court_address[i]), border)
                    elif hasattr(borders, 'HeaderMatchCourtAddress_0'):
                        border = get_group_size_borders(0, borders.HeaderMatchCourtAddress_0, len(match_court_address), 4)
                        for i in range(len(match_court_address)):
                            insert_text(match_court_address[i], border[i])
                    elif hasattr(borders, 'HeaderMatchCourtAddress_1'):
                        border = get_group_size_borders(1, borders.HeaderMatchCourtAddress_1, len(match_court_address), 4)
                        for i in range(len(match_court_address)):
                            insert_text(match_court_address[i], border[i])

            def load_competition_stage():
                
                if hasattr(borders, 'HeaderCompetitionStage'):
                    border = borders.HeaderCompetitionStage
                    insert_text(match.competition_stage, border, font_size=80)

            def load_match_country_code():

                if match.match_country_code == '': match.match_country_code = ' '  

                if not hasattr(borders, 'HeaderMatchCountryCode_0') and not hasattr(borders, 'HeaderMatchCountryCode_1'):
                    for i in range(len(match.match_country_code)):
                        border = getattr(borders, 'HeaderMatchCountryCodeChar' + str(i))
                        insert_text(match.match_country_code[i], border)
                elif hasattr(borders, 'HeaderMatchCountryCode_0'):
                    border = get_group_size_borders(0, borders.HeaderMatchCountryCode_0, len(match.match_country_code), 7)
                    for i in range(len(match.match_country_code)):
                        insert_text(match.match_country_code[i], border[i])
                elif hasattr(borders, 'HeaderMatchCountryCode_1'):
                    border = get_group_size_borders(1, borders.HeaderMatchCountryCode_1, len(match.match_country_code), 7)
                    for i in range(len(match.match_country_code)):
                        insert_text(match.match_country_code[i], border[i])

            def load_match_number():

                if match.match_number == '': match.match_number = ' '  

                if not hasattr(borders, 'HeaderMatchNumber_0') and not hasattr(borders, 'HeaderMatchNumber_1'):
                    for i in range(len(match.match_number)):
                        border = getattr(borders, 'HeaderMatchNumberChar' + str(i))
                        insert_text(match.match_number[i], border)
                elif hasattr(borders, 'HeaderMatchNumber_0'):
                    border = get_group_size_borders(0, borders.HeaderMatchNumber_0, len(match.match_number), 7)
                    for i in range(len(match.match_number)):
                        insert_text(match.match_number[i], border[i])
                elif hasattr(borders, 'HeaderMatchNumber_1'):
                    border = get_group_size_borders(1, borders.HeaderMatchNumber_1, len(match.match_number), 7)
                    for i in range(len(match.match_number)):
                        insert_text(match.match_number[i], border[i])

            def load_match_sex():
                
                if match.match_sex == 'M':
                    if hasattr(borders, 'HeaderMatchSexMales'):
                        border = borders.HeaderMatchSexMales
                        insert_text('X', border)
                elif match.match_sex == 'F':
                    if hasattr(borders, 'HeaderMatchSexFemales'):
                        border = borders.HeaderMatchSexFemales
                        insert_text('X', border)

            def load_competition_age():
                if match.competition_age == 'S':
                    if hasattr(borders, 'HeaderCompetitionAgeSenior'):
                        border = borders.HeaderCompetitionAgeSenior
                        insert_text('X', border)
                elif match.competition_age == 'J':
                    if hasattr(borders, 'HeaderCompetitionAgeJunior'):
                        border = borders.HeaderCompetitionAgeJunior
                        insert_text('X', border)
                elif match.competition_age == 'Y':
                    if hasattr(borders, 'HeaderCompetitionAgeYouth'):
                        border = borders.HeaderCompetitionAgeYouth
                        insert_text('X', border)

            def load_match_date():
                
                match_start_date = match.scheduled_date.split('-')
                match_start_date.reverse()
                match_start_date = match_start_date[0] + match_start_date[1] + match_start_date[2][2:]

                if not hasattr(borders, 'HeaderMatchStartDate_0') and not hasattr(borders, 'HeaderMatchStartDate_1'):
                    for i in range(6):
                        border = getattr(borders, 'MatchStartDateChar' + str(i))
                        insert_text(str(match_start_date[i]), border)
                elif hasattr(borders, 'HeaderMatchStartDate_0'):
                    border = get_group_size_borders(0, borders.HeaderMatchStartDate_0, 6, 7)
                    for i in range(6):
                        insert_text(match_start_date[i], border[i])
                elif hasattr(borders, 'HeaderMatchStartDate_1'):
                    border = get_group_size_borders(1, borders.HeaderMatchStartDate_1, 6, 7)
                    for i in range(6):
                        insert_text(match_start_date[i], border[i])

            def load_match_time():

                match_start_time = match.scheduled_time[:2] + match.scheduled_time[3:]
                
                if not hasattr(borders, 'HeaderMatchStartTime_0') and not hasattr(borders, 'HeaderMatchStartTime_1'):
                    for i in range(4):
                        border = getattr(borders, 'MatchStartTimeChar' + str(i))
                        insert_text(str(match_start_time[i]), border)
                elif hasattr(borders, 'HeaderMatchStartTime_0'):
                    border = get_group_size_borders(0, borders.HeaderMatchStartTime_0, 4, 7)
                    for i in range(4):
                        insert_text(match_start_time[i], border[i])
                elif hasattr(borders, 'HeaderMatchStartTime_1'):
                    border = get_group_size_borders(1, borders.HeaderMatchStartTime_1, 4, 7)
                    for i in range(4):
                        insert_text(match_start_time[i], border[i])

            def load_team_names():
                
                for team_direction in ("Left", "Right"):
                    if hasattr(borders, 'HeaderTeamName' + team_direction):
                        team = getattr(match, team_direction.lower()+'_team')
                        border = getattr(borders, 'HeaderTeamName' + team_direction)
                        insert_text(team.long_name, border)
                
            def load_team_letters():
                
                for team_direction in ("Left", "Right"):
                    if hasattr(borders, 'HeaderTeamLetter' + team_direction):
                        team = getattr(match, team_direction.lower()+'_team')
                        border = getattr(borders, 'HeaderTeamLetter' + team_direction)
                        if team == match.team_A:
                            insert_text(coin_toss_window[language_code][0], border)
                        else:
                            insert_text(coin_toss_window[language_code][1], border)

            load_competition_name()
            load_match_city()
            load_match_court_address()
            load_competition_stage()
            load_match_country_code()
            load_match_number()
            load_competition_age()
            load_match_sex()
            load_match_date()
            load_match_time()
            load_team_names()
            load_team_letters()

        def load_teams():
            
            def get_liberos(team):

                rv = []

                for player in team.players:
                    if player.libero:
                        rv.append(player)
                
                return rv

            def load_team_letters():
                
                for team_direction in ("Left", "Right"):
                    if hasattr(borders, 'TeamsLetter' + team_direction):
                        team = getattr(match, team_direction.lower()+'_team')
                        border = getattr(borders, 'TeamsLetter' + team_direction)
                        if team == match.team_A:
                            insert_text(coin_toss_window[language_code][0], border)
                        else:
                            insert_text(coin_toss_window[language_code][1], border)

            def load_team_names():

                for team_direction in ("Left", "Right"):
                    if hasattr(borders, 'TeamsNames' + team_direction):
                        team = getattr(match, team_direction.lower()+'_team')
                        border = getattr(borders, 'TeamsNames' + team_direction)
                        insert_text(team.long_name, border)

            def load_players_numbers():
            
                for team_direction in ('Left', 'Right'):
                     
                    if not hasattr(borders, 'TeamsPlayerNumbers' + team_direction + '_0') and not hasattr(borders, 'TeamsPlayerNumbers' + team_direction + '_1'):
                        team = getattr(match, team_direction.lower()+'_team')
                        for i in range(len(team.players)):
                            border = getattr(borders, 'TeamsPlayerNumbers' + team_direction + 'Char' + str(i))
                            insert_text(str(team.players[i].number), border, circle=team.players[i].captain)
                    
                    elif hasattr(borders, 'TeamsPlayerNumbers' + team_direction + '_0'):
                        border = get_group_size_borders(0, getattr(borders, 'TeamsPlayerNumbers' + team_direction + '_0'), 14, 6)
                        team = getattr(match, team_direction.lower()+'_team')
                        for i in range(len(team.players)):
                            insert_text(str(team.players[i].number), border[i], circle=team.players[i].captain)
                    
                    elif hasattr(borders, 'TeamsPlayerNumbers' + team_direction + '_1'):
                        border = get_group_size_borders(1, getattr(borders, 'TeamsPlayerNumbers' + team_direction + '_1'), 14, 6)
                        team = getattr(match, team_direction.lower()+'_team')
                        for i in range(len(team.players)):
                            insert_text(str(team.players[i].number), border[i], circle=team.players[i].captain)

            def load_players_names():
                
                for team_direction in ('Left', 'Right'):
                     
                    team = getattr(match, team_direction.lower()+'_team')
                    team_players = team.players
                    sort_by_alphabet(team_players)

                    if not hasattr(borders, 'TeamsPlayerNames' + team_direction + '_0') and not hasattr(borders, 'TeamsPlayerNames' + team_direction + '_1'):                        
                        for i in range(len(team_players)):
                            border = getattr(borders, 'TeamsPlayerNames' + team_direction + 'Char' + str(i))
                            insert_text(team_players[i].name_string, border)
                    
                    elif hasattr(borders, 'TeamsPlayerNames' + team_direction + '_0'):
                        border = get_group_size_borders(0, getattr(borders, 'TeamsPlayerNames' + team_direction + '_0'), 14, 5)
                        team = getattr(match, team_direction.lower()+'_team')
                        for i in range(len(team_players)):
                            insert_text(team_players[i].name_string, border[i])
                    
                    elif hasattr(borders, 'TeamsPlayerNames' + team_direction + '_1'):
                        border = get_group_size_borders(1, getattr(borders, 'TeamsPlayerNames' + team_direction + '_1'), 14, 5)
                        team = getattr(match, team_direction.lower()+'_team')
                        for i in range(len(team_players)):
                            insert_text(team_players[i].name_string, border[i])

            def cross_abstent_players():
                
                for team_direction in ('Left', 'Right'):
                    
                    if not hasattr(borders, 'TeamsPlayerNames' + team_direction + '_0') and not hasattr(borders, 'TeamsPlayerNames' + team_direction + '_1'):
        
                        team = getattr(match, team_direction.lower() + '_team')
                        if len(team.players) < 13:
                            last_player = getattr(borders, 'TeamsPlayerNames' + team_direction + 'Char' + len(team.players))
                            last_entry_field = getattr(borders, 'TeamsPlayerNumbers' + team_direction + 'Char13')
                            image_draw.line((last_player[0], last_player[1], last_entry_field[0], last_entry_field[1]), fill=(0, 0, 0, 255), width=3)
                        elif len(team.players) == 13:
                            border = getattr(borders, 'TeamsPlayerNames' + team_direction + 'Char13')
                            number_border = getattr(borders, 'TeamsPlayerNumbers' + team_direction + 'Char13')
                            y_middle = int((border[1] + border[3]) / 2)
                            image_draw.line((number_border[0], y_middle, box[2], y_middle), fill=(0, 0, 0, 255), width=3)

                    elif hasattr(borders, 'TeamsPlayerNames' + team_direction + '_0'):
                        
                        team = getattr(match, team_direction.lower() + '_team')
                        if len(team.players) < 13:
                            border = getattr(borders, 'TeamsPlayerNames' + team_direction + '_0')
                            last_player = get_group_size_borders(0, border, 14, 5)[len(team.players)]
                            last_entry_field = getattr(borders, 'TeamsPlayerNumbers' + team_direction + '_0')
                            image_draw.line((last_player[0], last_player[1], last_entry_field[0], last_entry_field[1]), fill=(0, 0, 0, 255), width=3)
                        elif len(team.players) == 13:
                            border = getattr(borders, 'TeamsPlayerNames' + team_direction + '_0')
                            number_border = get_group_size_borders(0, getattr(borders, 'TeamsPlayerNumbers' + team_direction +'_0'), 14, 6)[13]
                            box = get_group_size_borders(0, border, 14, 5)[13]
                            y_middle = int((box[1] + box[3]) / 2)
                            image_draw.line((number_border[0], y_middle, box[2], y_middle), fill=(0, 0, 0, 255), width=3)

                    elif hasattr(borders, 'TeamsPlayerNames' + team_direction + '_1'):
                        
                        team = getattr(match, team_direction.lower() + '_team')
                        if len(team.players) < 13:
                            border = getattr(borders, 'TeamsPlayerNames' + team_direction + '_1')
                            last_player = get_group_size_borders(1, border, 14, 5)[len(team.players)]
                            last_entry_field = getattr(borders, 'TeamsPlayerNumbers' + team_direction + '_1')
                            image_draw.line((last_player[2], last_player[1], last_entry_field[0], last_entry_field[3]), fill=(0, 0, 0, 255), width=3)
                        elif len(team.players) == 13:
                            border = getattr(borders, 'TeamsPlayerNames' + team_direction + '_1')
                            number_border = get_group_size_borders(1, getattr(borders, 'TeamsPlayerNumbers' + team_direction +'_1'), 14, 6)[13]
                            box = get_group_size_borders(1, border, 14, 5)[13]
                            y_middle = int((box[1] + box[3]) / 2)
                            image_draw.line((number_border[0], y_middle, box[2], y_middle), fill=(0, 0, 0, 255), width=3)

            def load_liberos_numbers():
                
                for team_direction in ('Left', 'Right'):
                     
                    if not hasattr(borders, 'TeamsLiberosNumbers' + team_direction + '_0') and not hasattr(borders, 'TeamsLiberosNumbers' + team_direction + '_1'):
                        team = getattr(match, team_direction.lower()+'_team')
                        liberos = get_liberos(team)
                        for i in range(len(liberos)):
                            border = getattr(borders, 'TeamsLiberosNumbers' + team_direction + 'Char' + str(i))
                            insert_text(str(liberos[i].number), border, circle=liberos[i].captain)
                    
                    elif hasattr(borders, 'TeamsLiberosNumbers' + team_direction + '_0'):
                        border = get_group_size_borders(0, getattr(borders, 'TeamsLiberosNumbers' + team_direction + '_0'), 2, 6)
                        team = getattr(match, team_direction.lower()+'_team')
                        liberos = get_liberos(team)
                        for i in range(len(liberos)):
                            insert_text(str(liberos[i].number), border[i], circle=liberos[i].captain)
                    
                    elif hasattr(borders, 'TeamsLiberosNumbers' + team_direction + '_1'):
                        border = get_group_size_borders(1, getattr(borders, 'TeamsLiberosNumbers' + team_direction + '_1'), 2, 6)
                        team = getattr(match, team_direction.lower()+'_team')
                        liberos = get_liberos(team)
                        for i in range(len(liberos)):
                            insert_text(str(liberos[i].number), border[i], circle=liberos[i].captain)

            def load_liberos_names():
                
                for team_direction in ('Left', 'Right'):
                     
                    team = getattr(match, team_direction.lower()+'_team')
                    team_liberos = get_liberos(team)
                    sort_by_alphabet(team_liberos)

                    if not hasattr(borders, 'TeamsLiberosNames' + team_direction + '_0') and not hasattr(borders, 'TeamsLiberosNames' + team_direction + '_1'):
                        for i in range(len(team_liberos)):
                            border = getattr(borders, 'TeamsLiberosNames' + team_direction + 'Char' + str(i))
                            insert_text(team_liberos[i].name_string, border)
                    
                    elif hasattr(borders, 'TeamsLiberosNames' + team_direction + '_0'):
                        border = get_group_size_borders(0, getattr(borders, 'TeamsLiberosNames' + team_direction + '_0'), 2, 5)
                        for i in range(len(liberos)):
                            insert_text(team_liberos[i].name_string, border[i])
                    
                    elif hasattr(borders, 'TeamsLiberosNames' + team_direction + '_1'):
                        border = get_group_size_borders(1, getattr(borders, 'TeamsLiberosNames' + team_direction + '_1'), 2, 5)
                        for i in range(len(liberos)):
                            insert_text(team_liberos[i].name_string, border[i])
                
            def cross_abstent_liberos():
                
                for team_direction in ('Left', 'Right'):
                    
                    if not hasattr(borders, 'TeamsLiberosNames' + team_direction + '_0') and not hasattr(borders, 'TeamsLiberosNames' + team_direction + '_1'):
        
                        team = getattr(match, team_direction.lower() + '_team')
                        liberos = get_liberos(team)
                        if len(liberos) == 0:
                            last_player = getattr(borders, 'TeamsLiberosNames' + team_direction + 'Char0')
                            last_entry_field = getattr(borders, 'TeamsLiberosNumbers' + team_direction + 'Char1')
                            image_draw.line((last_player[2], last_player[1], last_entry_field[0], last_entry_field[3]), fill=(0, 0, 0, 255), width=3)
                        elif len(liberos) == 1:
                            border = getattr(borders, 'TeamsLiberosNames' + team_direction + 'Char1')
                            number_border = getattr(borders, 'TeamsLiberosNumbers' + team_direction + 'Char1')
                            y_middle = int((border[1] + border[3]) / 2)
                            image_draw.line((number_border[0], y_middle, box[2], y_middle), fill=(0, 0, 0, 255), width=3)

                    elif hasattr(borders, 'TeamsLiberosNames' + team_direction + '_0'):
                        
                        team = getattr(match, team_direction.lower() + '_team')
                        liberos = get_liberos(team)
                        if len(liberos) == 0:
                            border = getattr(borders, 'TeamsLiberosNames' + team_direction + '_0')
                            last_player = get_group_size_borders(0, border, 2, 5)[len(liberos)]
                            last_entry_field = getattr(borders, 'TeamsLiberosNumbers' + team_direction + '_0')
                            image_draw.line((last_player[2], last_player[1], last_entry_field[0], last_entry_field[3]), fill=(0, 0, 0, 255), width=3)
                        elif len(liberos) == 1:
                            border = getattr(borders, 'TeamsLiberosNames' + team_direction + '_0')
                            number_border = get_group_size_borders(0, getattr(borders, 'TeamsLiberosNumbers' + team_direction +'_0'), 2, 6)[1]
                            box = get_group_size_borders(0, border, 2, 5)[1]
                            y_middle = int((box[1] + box[3]) / 2)
                            image_draw.line((number_border[0], y_middle, box[2], y_middle), fill=(0, 0, 0, 255), width=3)

                    elif hasattr(borders, 'TeamsLiberosNames' + team_direction + '_1'):
                        
                        team = getattr(match, team_direction.lower() + '_team')
                        liberos = get_liberos(team)
                        if len(liberos) == 0:
                            border = getattr(borders, 'TeamsLiberosNames' + team_direction + '_1')
                            last_player = get_group_size_borders(1, border, 2, 5)[len(liberos)]
                            last_entry_field = getattr(borders, 'TeamsLiberosNumbers' + team_direction + '_1')
                            image_draw.line((last_player[2], last_player[1], last_entry_field[0], last_entry_field[3]), fill=(0, 0, 0, 255), width=3)
                        elif len(liberos) == 1:
                            border = getattr(borders, 'TeamsLiberosNames' + team_direction + '_1')
                            number_border = get_group_size_borders(1, getattr(borders, 'TeamsLiberosNumbers' + team_direction +'_1'), 2, 6)[1]
                            box = get_group_size_borders(1, border, 2, 5)[1]
                            y_middle = int((box[1] + box[3]) / 2)
                            image_draw.line((number_border[0], y_middle, box[2], y_middle), fill=(0, 0, 0, 255), width=3)

            def load_head_coach_names():
                
                for team_direction in ("Left", "Right"):
                    if hasattr(borders, 'TeamsHeadCoach' + team_direction):
                        team = getattr(match, team_direction.lower()+'_team')
                        border = getattr(borders, 'TeamsHeadCoach' + team_direction)
                        if team.head_coach != '': insert_text(team.head_coach.name_string, border)

            def load_staff_names():
                
                for team_direction in ("Left", "Right"):
                    
                    team = getattr(match, team_direction.lower()+'_team')
                        
                    team_staff = []
                    for staff in team.staff:
                        if staff != team.head_coach: team_staff.append(staff)

                    if not hasattr(borders, 'TeamStaff' + team_direction + '_0') and not hasattr(borders, 'TeamStaff' + team_direction + '_1'):
                       
                        for i in range(len(team_staff)):

                            border = getattr(borders, 'TeamStaff' + team_direction + 'Char' + str(i))

                            if len(team_staff) > 3 and i == 0:
                                insert_text(team_staff[0].name_string + ' | ' + team_staff[1].name_string, border[i])
                            elif len(team_staff) > 3 and i == 1:
                                pass
                            elif len(team_staff) > 3 and i > 1:
                                insert_text(team_staff[i].name_string, border[i-1])
                            elif len(team_staff) <= 3:
                                insert_text(team_staff[i].name_string, border[i])

                    elif hasattr(borders, 'TeamStaff' + team_direction + '_0'):

                        for i in range(len(team_staff)):

                            border = get_group_size_borders(0, getattr(borders, 'TeamStaff' + team_direction + '_0'), 3, 4)

                            if len(team_staff) > 3 and i == 0:
                                insert_text(team_staff[0].name_string + ' | ' + team_staff[1].name_string, border[i])
                            elif len(team_staff) > 3 and i == 1:
                                pass
                            elif len(team_staff) > 3 and i > 1:
                                insert_text(team_staff[i].name_string, border[i-1])
                            elif len(team_staff) <= 3:
                                insert_text(team_staff[i].name_string, border[i])

                    elif hasattr(borders, 'TeamStaff' + team_direction + '_1'):

                        for i in range(len(team_staff)):

                            border = get_group_size_borders(1, getattr(borders, 'TeamStaff' + team_direction + '_1'), 3, 4)

                            if len(team_staff) > 3 and i == 0:
                                insert_text(team_staff[0].name_string + ' | ' + team_staff[1].name_string, border[i])
                            elif len(team_staff) > 3 and i == 1:
                                pass
                            elif len(team_staff) > 3 and i > 1:
                                insert_text(team_staff[i].name_string, border[i-1])
                            elif len(team_staff) <= 3:
                                insert_text(team_staff[i].name_string, border[i])


            load_team_letters()
            load_team_names()
            load_players_numbers() 
            load_players_names()
            cross_abstent_players()
            load_liberos_numbers()
            load_liberos_names()
            cross_abstent_liberos()
            load_head_coach_names()
            load_staff_names()

        protocol_image = PIL_Image.open(os.getcwd()+'/py/match/protocol/image.png').convert('RGBA')
        image_draw = ImageDraw.ImageDraw(protocol_image)
        
        load_header()
        load_teams()

        protocol_image.save(self.protocol_image, 'png')

    def init_visual_elements(self):

        from DVA import match, frontend_references as gui
      
        self.protocol_image.seek(0)
        gui.get('EndWindowRefereeProtocolImage').texture = CoreImage(self.protocol_image, ext="png").texture
        
        gui.get('EndWindowRefereeLabel').text = match_end[language_code][1] + match.sets[-1].winner + match_end[language_code][2]
        gui.get('EndWindowRefereeTeamABestPlayerButton').text = match_end[language_code][8] + match.left_team.long_name + match_end[language_code][9]
        gui.get('EndWindowRefereeTeamBBestPlayerButton').text = match_end[language_code][8] + match.right_team.long_name + match_end[language_code][9]
        
        for team in (match.left_team, match.right_team): # TODO change according to status
            if team.long_name != match.sets[-1].winner:
                gui.get('EndWindowRefereeWinnersProtestButton').text = match_end[language_code][6] + team.long_name + match_end[language_code][7]
                if team.protest == '':
                    gui.get('EndWindowRefereeWinnersProtestButton').disabled = False

    def load_teams_squads(self):
        
        from DVA import match, frontend_references as gui

        for player in match.left_team.players:
            gui.get('EndWindowRefereeTeamABestPlayerButton').values.append(player.name_string)

        for player in match.right_team.players:
            gui.get('EndWindowRefereeTeamBBestPlayerButton').values.append(player.name_string)     

    def on_load(self, *args):
        
        from DVA import match

        self.load_protocol()

        #match.loading_gif.popupWindow.dismiss()

        self.init_visual_elements()
        self.load_teams_squads()

    def protocol_image_pressed(self, *args):
        PopUpWindow().show_protocol_image(args[0])

    def protest_button_pressed(self, *args):

        from DVA import match_events_dispatch, match
        from py.match.events import ProtestAfterMatchEnded

        for _team_ in (match.left_team, match.right_team):
            if _team_.long_name != match.sets[-1].winner:
                team = _team_

        PopUpWindow().show_text_input('protest', team)

    def notes_button_pressed(self, *args):

        PopUpWindow().show_text_input('notes')

    def save_protocol_button_pressed(self, *args):

        PopUpWindow().show_file_chooser()

    def send_protocol_button_pressed(self, *args):
        
        from DVA import frontend_references as gui

        gui.get('EndWindowRefereeForwardButton').disabled = False

    def back_button_pressed(self, *args):
        
        from DVA import match_events_dispatch

        match_events_dispatch.back()

    def forward_button_pressed(self, *args):
        
        import sys

        sys.exit()


class EndWindowReferee(EndWindowBase):
    
    def __init__(self):

        super().__init__()

        self.design.main_widget.middle.buttons.send_protocol.disabled = False
        self.design.main_widget.middle.buttons.send_protocol.opacity = 1

        self.design.main_widget.middle.buttons.best_player_A.disabled = False
        self.design.main_widget.middle.buttons.best_player_A.opacity = 1
        self.design.main_widget.middle.buttons.best_player_B.disabled = False
        self.design.main_widget.middle.buttons.best_player_B.opacity = 1


class IntervalWindowBase(GridLayout):

    def __init__(self):

        super().__init__(cols=1)

        self.design = GridLayout(cols=1)

        self.design.main_widget = GridLayout(rows=3)

        self.design.main_widget.text = Label(font_size=24)
        self.design.main_widget.timer = Label(font_size=48)
        self.design.main_widget.skip_button_area = GridLayout(rows=1, padding=[20])

        self.design.main_widget.skip_button_area.button = Button(text=buttons[language_code][3], opacity=0)

        self.design.main_widget.skip_button_area.add_widget(self.design.main_widget.skip_button_area.button)

        self.design.main_widget.add_widget(self.design.main_widget.text)
        self.design.main_widget.add_widget(self.design.main_widget.timer)
        self.design.main_widget.add_widget(self.design.main_widget.skip_button_area)

        self.design.add_widget(self.design.main_widget)
        self.add_widget(self.design)

    def format_zeroes(self, time_till_action):
        
        if len(time_till_action.split(':')[0]) == 1:
            time_till_action = '0' + time_till_action
        if len(time_till_action.split(':')[1]) == 1:
            time_till_action = time_till_action.split(':')[0] + ':0' + time_till_action.split(':')[1]

    def on_load(self, window, action_instruction_id, event_id, time_till_action, *args): # It was decided to leave action_instruction_id and event_id as separate parameters instead 
        #of making them into one and moving 'in' string in localication to the end as amount of events may grow in the future

        from DVA import frontend_references as gui

        self.format_zeroes(time_till_action)

        self.design.main_widget.text.text = interval_window[language_code][event_id] + ' ' + interval_window[language_code][0]
        self.design.main_widget.timer.text = time_till_action
        self.action_instructions_id = action_instruction_id
        self.clock = Clock.schedule_interval(self.timer, 1)
        self.window = window
        self.arguments = args

    def timer(self, dt):

        from DVA import frontend_references as gui

        time = self.design.main_widget.timer.text.split(':')

        time = map(int, time)
        time = list(time)

        if time[1] > 0:
            time[1] -= 1
        elif time[1] == 0:
            if time[0] == 0:
                self.action('')
            elif time[0] > 0:
                time[0] -= 1
            time[1] = 59

        for i in range(2):
            if time[i] < 10:
                time[i] = '0' + str(time[i])

        time = map(str, time)
        time = list(time)

        self.design.main_widget.timer.text = ':'.join(time)

    def action(self, button):

        import DVA
        from DVA import match, match_events_dispatch, logs, frontend_references as gui
        from gfx.interval_instructons import instructions
        from py.match.events import SetStart

        self.clock.cancel()
        self.window.dismiss()
        exec(instructions[self.action_instructions_id])


class IntervalWindowReferee(IntervalWindowBase):

    def __init__(self):
        
        from DVA import frontend_references as gui
        
        super().__init__()

        self.design.main_widget.skip_button_area.button.opacity = 1
        self.design.main_widget.skip_button_area.button.bind(on_release=self.action)


class CaptainChooser(GridLayout):

    def __init__(self):

        super().__init__()

        self.rows = 4

        self.text = Label(text_size=(300, None))
        self.spinner = Spinner(size_hint=(1, 0.3))
        self.buttons = GridLayout(cols=3, size_hint=(1, 0.2))

        self.buttons.back = Button(text=buttons[language_code][4])
        self.buttons.save = Button(text=buttons[language_code][1])

        self.buttons.add_widget(self.buttons.back)
        self.buttons.add_widget(Label())
        self.buttons.add_widget(self.buttons.save)

        self.add_widget(self.text)
        self.add_widget(self.spinner)
        self.add_widget(Label(size_hint_y=0.5))
        self.add_widget(self.buttons)

        self.buttons.back.bind(on_release=self.back_button_pressed)
        self.buttons.save.bind(on_release=self.save_button_pressed)

    def on_load(self, team_name, window):
        
        from DVA import match
        from py.core import get_people_list

        self.team_name = team_name
        self.window = window

        self.text.text = match_window[language_code][3] + team_name + match_window[language_code][4]

        for team in (match.left_team, match.right_team):
            if team.long_name == team_name:
                self.spinner.values = get_people_list(team, with_numbers=True, end_index=players_in_team, rv_format='str')
        
        self.spinner.text = self.spinner.values[0]

    def save_button_pressed(self, *args):
        
        from DVA import match_events_dispatch
        from py.match.events import CaptainNotPresent

        match_events_dispatch.run(CaptainNotPresent, [self.team_name, self.spinner.text.split(maxsplit=1)[1]], 'NEW')
        self.window.dismiss()

    def back_button_pressed(self, *args):
        
        from DVA import match_events_dispatch

        match_events_dispatch.back()
        self.window.dismiss()


class ProtestCreationWindow(GridLayout):
    
    def __init__(self):
        
        super().__init__()
        
        self.rows = 4
        self.spacing = [50, 15]
        self.padding = [20, -100, 20, 0]

        self.message = Label(text=protest_window[language_code][2])
        self.message.text_size = (300, 300)

        self.confirm = Button(text=buttons[language_code][0], size_hint=(0.275, 0.275))
        self.cancel = Button(text=buttons[language_code][2], size_hint=(0.275, 0.275))

        self.add_widget(self.message)
        self.add_widget(Label())
        self.add_widget(self.confirm)
        self.add_widget(self.cancel)

        self.confirm.bind(on_release=self.confirm_button_pressed)
        self.cancel.bind(on_release=self.cancel_button_pressed)

        self.team = ''

    def on_load(self, window, team):
        self.window = window
        self.team = team

    def confirm_button_pressed(self, *args):
        
        from DVA import match, frontend_references as gui
        from py.match.objects import HeadCoach

        if gui.get('MatchWindowRefereeProtestsTabHeader').current_tab == gui.get('MatchWindowRefereeProtestsTabTeamATab'):
            if match.left_team.head_coach != '':
                match.left_team.head_coach.declare_protest(self.team)
            else:
                HeadCoach.declare_protest('', self.team)
        elif gui.get('MatchWindowRefereeProtestsTabHeader').current_tab == gui.get('MatchWindowRefereeProtestsTabTeamBTab'):
            if match.left_team.head_coach != '':
                match.left_team.head_coach.declare_protest(self.team)
            else:
                HeadCoach.declare_protest('', self.team)

        self.window.dismiss()

    def cancel_button_pressed(self, *args):
        
        from DVA import frontend_references as gui

        gui.get('MatchWindowRefereeTabPanel').switch_to(gui.get('MatchWindowRefereeTabPanelMatch'))
        self.window.dismiss()


class ProtocolViewWindow(ScrollView):

    def __init__(self, image):

        super().__init__()

        self.size_hint_min = (None, None)
        self.size_hint = (0, 0)
        self.size = Window.width, Window.height
        self.add_widget(Image(texture=image.texture, size=image.texture_size, size_hint=(None, None)))


class MatchEndTextInput(GridLayout):

    def __init__(self):

        super().__init__()

        self.rows=2

        self.field = TextInput(size_hint=(1, 0.9))
        self.buttons = GridLayout(cols=3, size_hint=(1, 0.1))

        self.buttons.cancel = Button(text=buttons[language_code][4])
        self.buttons.send = Button(text=buttons[language_code][0])

        self.buttons.add_widget(self.buttons.cancel)
        self.buttons.add_widget(Label())
        self.buttons.add_widget(self.buttons.send)

        self.add_widget(self.field)
        self.add_widget(self.buttons)
    
        self.buttons.cancel.bind(on_release=self.cancel_button_pressed)
        self.buttons.send.bind(on_release=self.send_button_pressed)

    def on_load(self, window, mode, team):
        
        from DVA import match

        self.window = window
        self.mode = mode
        self.team = team

        if self.mode == 'notes':
            self.field.text = match.referee_notes
            self.buttons.send.text = buttons[language_code][1]

    def cancel_button_pressed(self, *args):
        
        self.window.dismiss()

    def send_button_pressed(self, *args): 
        
        from DVA import match_events_dispatch
        from py.match.events import ProtestAfterMatchEnded, RefereeNotesWritten
        if self.mode == 'protest':
            match_events_dispatch.run(ProtestAfterMatchEnded, [self.team, self.field.text], 'NEW')
            self.cancel_button_pressed()
        elif self.mode == 'notes':
            match_events_dispatch.run(RefereeNotesWritten, self.field.text, 'NEW')
            self.cancel_button_pressed()


class SaveProtocolFileChooser(GridLayout):

    def __init__(self):

        super().__init__()
        self.rows=3

        self.file_chooser = FileChooserIconView()
        self.file_chooser.dirselect = True
        self.file_chooser.path = os.getcwd()[:3]
        self.file_chooser.filters = ['*.']

        self.buttons = GridLayout(cols=3, size_hint=(1, 0.1))
        self.buttons.cancel = Button(text=buttons[language_code][2])
        self.buttons.save = Button(text=buttons[language_code][1])

        self.buttons.add_widget(self.buttons.cancel)
        self.buttons.add_widget(Label())
        self.buttons.add_widget(self.buttons.save)

        self.add_widget(self.file_chooser)
        self.add_widget(self.buttons)

        self.buttons.cancel.bind(on_release=self.cancel_button_pressed)
        self.buttons.save.bind(on_release=self.save_button_pressed)

    def on_load(self, window):

        self.window = window
        self.address = os.getcwd()

    def cancel_button_pressed(self, *args):

        self.window.dismiss()

    def save_button_pressed(self, *args):
        
        from DVA import match, frontend_references as gui 

        image_to_save = PIL_Image.open(gui.get('EndWindowReferee').protocol_image)
        image_to_save.save(self.file_chooser.path + '\\' + match.home_team.long_name + '_' + match.away_team.long_name + '_' + str(match.scheduled_date) + '_' + str(match.scheduled_time)[0:2] + '_' + match.scheduled_time[3:] + '.png', 'PNG')

        gui.get('EndWindowRefereeForwardButton').disabled = False

        self.window.dismiss()


class PopUpWindow(Popup):

    def show_pop_up(self, popup_text):
        popupWindow = PopUpWindow(title='', content=Label(text=str(popup_text), text_size=(200, None)), size_hint=(0.5, 0.5))
        popupWindow.open()

    def show_interval_window(self, args):
        popupWindow = PopUpWindow(title='', content=IntervalWindowReferee(), size_hint=(0.5, 0.5), auto_dismiss=False)  # TODO change according to status
        popupWindow.open()
        popupWindow.content.on_load(popupWindow, *args)

    def show_text_input(self, mode, team=None, *args):
        if mode == 'protest':
            popupWindow = PopUpWindow(title=protest_window[language_code][0] + team.long_name + protest_window[language_code][1], title_size=20, content=MatchEndTextInput(), size_hint=(0.5, 0.5), auto_dismiss=False)  # TODO change according to status
        elif mode == 'notes':
            popupWindow = PopUpWindow(title=match_end[language_code][10], title_size=20, content=MatchEndTextInput(), size_hint=(0.5, 0.5), auto_dismiss=False)  # TODO change according to status

        popupWindow.open()
        popupWindow.content.on_load(popupWindow, mode, team)

    def show_captain_chooser(self, team_name):
        popupWindow = PopUpWindow(title='', content=CaptainChooser(), size_hint=(0.5, 0.5), auto_dismiss=False)
        popupWindow.open()
        popupWindow.content.on_load(team_name, popupWindow)

    def show_protest_creation_window(self, team):
        popupWindow = PopUpWindow(title='', content=ProtestCreationWindow(), size_hint=(0.5, 0.5), auto_dismiss=False)
        popupWindow.open()
        popupWindow.content.on_load(popupWindow, team)

    def show_protocol_image(self, image):
        popupWindow = PopUpWindow(title='', content=ProtocolViewWindow(image))
        popupWindow.open()

    def show_file_chooser(self):
        
        popupWindow = PopUpWindow(title='', content=SaveProtocolFileChooser(), size_hint=(0.5, 0.5), auto_dismiss=False)        
        popupWindow.open()
        popupWindow.content.on_load(popupWindow)

    def show_loading_gif(self, *args):
        self.background_color = [0, 0, 0, 1]
        self.popupWindow = PopUpWindow(title='', content=Image(source=os.getcwd()+'\gfx\loading.gif'), size_hint=(1, 1), auto_dismiss=False)
        self.popupWindow.open()


class BackgroundWindow(FloatLayout):
    
    class BackgroundPicture(FloatLayout):

        def __init__(self, **kwargs):
            
            super().__init__(**kwargs)

            image = Image()
            image.source = os.getcwd() + r'\gfx\background_pictures\background_' + app_background_picture + '.jpg'
            image.pos_hint = {"x": 0, "y": 0}
            image.pos_size = 1, 1
            image.allow_stretch = True
            image.keep_ratio = False

            self.add_widget(image)

    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        
        self.add_widget(self.BackgroundPicture(pos_hint={"x": 0, "y": 0}, size_hint=(1, 1)))


class TeamWidget(GridLayout):

    def get_line_up_parameters(self):

        if players_in_team % 2 == 0:
            rows = 2
            cols = players_in_team / 2
        else:
            cols = 3
            rows = (players_in_team - 1) / 2

        rows = int(rows)
        cols = int(cols)
        return rows, cols

    def get_index(self, current_positioning_cords, positioning_rotation_direction): # TODO This function
        # does not work for one-line lineups (also, probably some others non-standard as well). Temporarily,
        # hotfix was written for one-line lineups but fixing the original function so that it works with 
        # any lineup is more desirable. Also, update table below and see it for non-border, non-angle cases.

        # if we're at one_of the extremes:
        #   if we're also at other_extreme:
        #       change direction according to direction
        #   else:
        #       move next according to direction
        # else:
        #   pass # TODO make a research for non-standard line ups

        if min(self.rows, self.cols) > 1:

            if positioning_rotation_direction == 'Clockwise':

                if current_positioning_cords == [0, 0]:
                    return 1
                elif current_positioning_cords == [0, self.cols - 1]:
                    return (self.cols * 2) - 1
                elif current_positioning_cords == [self.rows - 1, self.cols - 1]:
                    return (self.rows - 1) * (self.cols + (self.cols - 2))
                elif current_positioning_cords == [self.rows - 1, 0]:
                    return (self.rows - 2) * self.cols

                if current_positioning_cords[0] == 0 and 0 < current_positioning_cords[1] < self.cols - 1:
                    return current_positioning_cords[1] + 1
                elif 0 < current_positioning_cords[0] < self.rows - 1 and current_positioning_cords[1] == self.cols - 1:
                    return (current_positioning_cords[0] + 2) * (self.rows - 1)
                elif current_positioning_cords[0] == self.rows - 1 and 0 < current_positioning_cords[1] < self.cols - 1:
                    return ((self.rows - 1) * self.cols) + (current_positioning_cords[1] - 1)
                elif 0 < current_positioning_cords[0] < self.rows - 1 and current_positioning_cords[1] == 0:
                    return (current_positioning_cords[0] - 1) * self.cols

                else:
                    pass

            else:

                if current_positioning_cords == [0, 0]:
                    return self.cols
                elif current_positioning_cords == [self.rows - 1, 0]:
                    return (self.rows - 1) * (self.cols + 1)
                elif current_positioning_cords == [self.rows - 1, self.cols - 1]:
                    return (self.rows - 1) * (self.cols - 1)
                elif current_positioning_cords == [0, self.cols - 1]:
                    return self.cols - 2

                if 0 < current_positioning_cords[0] < self.rows - 1 and current_positioning_cords[1] == 0:
                    return (current_positioning_cords[0] + 1) * self.cols
                elif current_positioning_cords[0] == self.rows - 1 and 0 < current_positioning_cords[1] < self.cols - 1:
                    return ((self.rows - 1) * self.cols) + (current_positioning_cords[1] + 1)
                elif 0 < current_positioning_cords[0] < self.rows - 1 and current_positioning_cords[1] == self.cols - 1:
                    return current_positioning_cords[0] * (self.rows - 1)
                elif current_positioning_cords[0] == 0 and 0 < current_positioning_cords[1] < self.cols - 1:
                    return current_positioning_cords[1] - 1

                else:
                    pass

        else:

            if positioning_rotation_direction == 'Clockwise':
                
                if self.rows == 1:
                    if current_positioning_cords[1] < self.cols - 1:
                        return current_positioning_cords[1] + 1
                    else:
                        return 0
                
                elif self.cols == 1:
                    if current_positioning_cords[0] < self.rows - 1:
                        return current_positioning_cords[0] + 1
                    else:
                        return 0                  
            
            else:

                if self.rows == 1:
                    if current_positioning_cords[1] > 0:
                        return current_positioning_cords[1] - 1
                    else:
                        return self.cols - 1
                
                elif self.cols == 1:
                    if current_positioning_cords[0] > 0:
                        return current_positioning_cords[0] - 1
                    else:
                        return self.rows - 1

    def __init__(self, widget, *args):

        from py.match.match_config import position_direction as positioning_rotation_direction, \
            position_starting_point as current_positioning_cords

        super().__init__()

        self.rows, self.cols = self.get_line_up_parameters()
        self.indexes = [[] for _ in range(self.rows * self.cols)]
        self.real_indexes = []

        for i in range(players_in_team):
            current_index = self.get_index(current_positioning_cords, positioning_rotation_direction)
            current_positioning_cords = [int(current_index / self.cols), current_index % self.cols]
            w = widget()
            self.indexes[current_index] = w
            self.real_indexes.append(w)

        for i in range(len(self.indexes)):
            if self.indexes[i]:
                self.add_widget(self.indexes[i])
            else:
                self.add_widget(Label())


class ButtonImage(ButtonBehavior, Image):
    pass


class ButtonLabel(ButtonBehavior, Label):
    pass


indexes = [0, 0, 0, 0, 0, 0]


def scroll__init(slider, movement):
    
    from DVA import match, frontend_references as gui

    global indexes

    proceed = False

    if slider == gui.get('MatchWindowRefereeTeamSetUpTeamASLIDER'):
        index = 0
        team = match.left_team
    elif slider == gui.get('MatchWindowRefereeTeamSetUpTeamBSLIDER'):
        index = 1
        team = match.right_team
    elif slider == gui.get('MatchWindowRefereeSubstitutionsTabTeamASLIDER'):
        index = 2
        team = match.left_team
    elif slider == gui.get('MatchWindowRefereeSubstitutionsTabTeamBSLIDER'):
        index = 3
        team = match.right_team
    elif slider == gui.get('MatchWindowRefereeSanctionsTabTeamASLIDER'):
        index = 4
        team = match.left_team
    elif slider == gui.get('MatchWindowRefereeSanctionsTabTeamBSLIDER'):
        index = 5
        team = match.right_team

    if movement.is_mouse_scrolling:

        if movement.button == 'scrollup':

            if indexes[index] < slider.max:
                indexes[index] += 1
            
            proceed = True

        elif movement.button == 'scrolldown':

            if indexes[index] > slider.min:
                indexes[index] -= 1

            proceed = True

    if proceed:
           
        if index < 4 and indexes[index] + 6 <= len(team.players) - (len(team.disqualified_players) + len(team.expulsed_players)):
    
            if index == 0:
                gui.get('MatchWindowRefereeTeamSetUpTabContent').on_load('A', indexes[index], indexes[index] + 6)

            elif index == 1:
                gui.get('MatchWindowRefereeTeamSetUpTabContent').on_load('B', indexes[index], indexes[index] + 6)
            
            elif index == 2:
                gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load('A', indexes[index], indexes[index] + 6, gui.get('MatchWindowRefereeSubstitutionsTabContent').forced_A)

            elif index == 3:
                gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load('B', indexes[index], indexes[index] + 6, gui.get('MatchWindowRefereeSubstitutionsTabContent').forced_B)

        elif index < 4 and indexes[index] + 6 > len(team.players) - (len(team.disqualified_players) + len(team.expulsed_players)):

            if index == 0:
                gui.get('MatchWindowRefereeTeamSetUpTabContent').on_load('A', indexes[index], (len(match.left_team.players) - (len(match.left_team.disqualified_players) + len(match.left_team.expulsed_players))))

            elif index == 1:
                gui.get('MatchWindowRefereeTeamSetUpTabContent').on_load('B', indexes[index], (len(match.right_team.players) - (len(match.right_team.disqualified_players) + len(match.right_team.expulsed_players))))
        
            elif index == 2:
                gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load('A', indexes[index], (len(match.left_team.players) - (len(match.left_team.disqualified_players) + len(match.left_team.expulsed_players))))
    
            elif index == 3:
                gui.get('MatchWindowRefereeSubstitutionsTabContent').on_load('B', indexes[index], (len(match.right_team.players) - (len(match.right_team.disqualified_players) + len(match.right_team.expulsed_players))))

        elif index == 4 and indexes[index] + 6 <= len(team.players) + len(team.staff) + (1 if team.head_coach != '' else 0):
            gui.get('MatchWindowRefereeSanctionsTabContent').on_load('A', indexes[index], indexes[index] + 6, is_scrolling=True)
        
        elif index == 4 and indexes[index] + 6 > len(team.players) + len(team.staff) + (1 if team.head_coach != '' else 0):
            gui.get('MatchWindowRefereeSanctionsTabContent').on_load('A', indexes[index], len(team.players) - len(team.disqualified_players) + len(team.staff) + (1 if team.head_coach != '' else 0), is_scrolling=True)
        
        elif index == 5 and indexes[index] + 6 <= len(team.players) + len(team.staff) + (1 if team.head_coach != '' else 0):
            gui.get('MatchWindowRefereeSanctionsTabContent').on_load('B', indexes[index], indexes[index] + 6, is_scrolling=True)
        
        elif index == 5 and indexes[index] + 6 > len(team.players) + len(team.staff) + (1 if team.head_coach != '' else 0):
            gui.get('MatchWindowRefereeSanctionsTabContent').on_load('B', indexes[index], len(team.players) - len(team.disqualified_players) + len(team.staff) + (1 if team.head_coach != '' else 0), is_scrolling=True)


def scroll_get_indexes(window, team):

   
    from DVA import match
    from py.core import set_range_to_sliders

    set_range_to_sliders()

    if window == 'TeamSetUp':
        
        if team == 'A':
            index = 0
            team = match.left_team
        else:
            index = 1
            team = match.right_team

        if indexes[index] + 6 <= len(team.players) - (len(team.disqualified_players) + len(team.expulsed_players)):
            rv = indexes[index], indexes[index] + 6
        else:
            rv = indexes[indexes], (len(team.players) - (len(team.disqualified_players) + len(team.expulsed_players)))

    elif window == 'Substitutions':
        
        if team == 'A':
            index = 2
            team = match.left_team
        else:
            index = 3
            team = match.right_team
        
        if indexes[index] + 6 <= len(team.players) - (len(team.disqualified_players) + len(team.expulsed_players)):
            rv = indexes[index], indexes[index] + 6
        else:
            rv = indexes[indexes], (len(team.players) - (len(team.disqualified_players) + len(team.expulsed_players)))       

    elif window == 'Sanctions':

        if team == 'A':
            index = 4
            team = match.left_team
        else:
            index = 5
            team = match.right_team
        
        if indexes[index] + 6 <= len(team.players) + len(team.staff) + (1 if team.head_coach != '' else 0):
            rv = indexes[index], indexes[index] + 6
        else:
            rv = indexes[index], len(team.players) - len(team.disqualified_players) + len(team.staff) + (1 if team.head_coach != '' else 0)
    
    return rv