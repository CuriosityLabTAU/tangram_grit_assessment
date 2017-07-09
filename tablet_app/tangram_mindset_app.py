from tangram_selection_not_using import *
from tangram_game import *

from zero_screen_room import *
from first_screen_room import *
from selection_screen_room import *
from solve_tangram_room import *
from party_screen_room import *
from game_facilitator import *

from text_handling import *

from interaction_control import *
from game import *
from tablet import *

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import Layout
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

from random import choice

GAME_WITH_ROBOT = False  # False
STUDY_SITE = 'TAU'      #'TAU'      # MIT

class MyScreenManager (ScreenManager):
    the_tablet = None

# MyScreenManager:
#    ZeroScreenRoom:
#    FirstScreenRoom:
#    SelectionScreenRoom:
#    SolveTangramRoom:r

root_widget = Builder.load_string('''

<ZeroScreenRoom>:
    start_button: start_button
    subject_id: subject_id
    name: 'zero_screen_room'
    Widget:
        canvas.before:
            Color:
                rgba: 0.2,0.3,0.4,1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "Subject ID:"
            font_size:16
            size: root.width * 0.05, root.height * 0.07
            pos: root.width * 0.1, root.height * 0.8 - self.height * 0.5

        LoggedTextInput:
            id: subject_id
            name: 'subject_id'
            text: ''
            multiline: False
            font_size: 16
            size: root.width * 0.4, root.height * 0.07
            pos: root.width * 0.18, root.height * 0.8 - self.height * 0.5

        LoggedSpinner:
            id: condition_spinner
            text: 'condition'
            font_size: 16
            background_color: 0.2,0.2,0.2,1
            values: ('c-g-','c+g-')
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.62, root.height * 0.8 - self.height * 0.5
            on_text: app.condition_selected()

        LoggedButton:
            id: start_button
            name: 'start_button'
            background_color: 0.1,0.5,0.2,1
            background_normal: ''
            text: 'Start'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.8, root.height * 0.8 - self.height * 0.5
            on_press: app.press_start_button()

        LoggedSpinner:
            id: difficulty_spinner
            text: 'difficulty'
            font_size: 16
            background_color: 0.2,0.2,0.2,1
            values: ('dif1','dif2','dif3')
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.62, root.height * 0.7 - self.height * 0.5
            on_text: app.difficulty_selected()

        LoggedButton:
            id: tega_sleep_button
            name: 'tega_sleep_button'
            background_color: 0.5,0.5,0.5,1
            background_normal: ''
            text: '- -'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.08, root.height * 0.5 - self.height * 0.5
            on_press: app.press_tega_sleep()

        LoggedButton:
            id: goto_game2_button
            name: 'goto_game2_button'
            background_color: 0.5,0.5,0.5,1
            background_normal: ''
            text: 'game2'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.08, root.height * 0.4 - self.height * 0.5
            on_press: app.press_load_transition('game2')

        LoggedButton:
            id: goto_game4_button
            name: 'goto_game4_button'
            background_color: 0.5,0.5,0.5,1
            background_normal: ''
            text: 'game4'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.25, root.height * 0.4 - self.height * 0.5
            on_press: app.press_load_transition('game4')

        LoggedButton:
            id: goto_game6_button
            name: 'goto_game6_button'
            background_color: 0.5,0.5,0.5,1
            background_normal: ''
            text: 'game6'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.42, root.height * 0.4 - self.height * 0.5
            on_press: app.press_load_transition('game6')

        LoggedButton:
            id: goto_game8_button
            name: 'goto_game8_button'
            background_color: 0.5,0.5,0.5,1
            background_normal: ''
            text: 'game8'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.59, root.height * 0.4 - self.height * 0.5
            on_press: app.press_load_transition('game8')

        LoggedButton:
            id: goto_game10_button
            name: 'goto_game10_button'
            background_color: 0.5,0.5,0.5,1
            background_normal: ''
            text: 'game10'
            font_size: 16
            size: root.width * 0.15, root.height * 0.07
            pos: root.width * 0.76, root.height * 0.4 - self.height * 0.5
            on_press: app.press_load_transition('game10')


<FirstScreenRoom>:
    name: 'first_screen_room'
    Widget:
        FirstScreenBackground:
            size: root.size
            pos: root.pos
        LoggedButton:
            id: yes_button
            name: 'yes_button'
            borders: 2, 'solid', (1,1,0,1)
            background_normal: './tablet_app/images/BalloonBtn.gif'
            background_down: './tablet_app/images/BalloonBtn_on.gif'
            size: root.width * 0.2, root.height * 0.5
            pos: root.width * 0.5 - self.width * 0.5, root.height * 0.7 - self.height * 0.5
            on_press: app.press_yes_button()
            opacity: 0

<FirstScreenBackground>:
    Image:
        size: root.size
        pos: root.pos
        source: './tablet_app/images/TangramGame_Open.jpg'
        allow_stretch: True
        keep_ratio: False


<SelectionScreenRoom>:
    name: 'selection_screen_room'
    Widget:
        Image:
            id: background_image
            size: root.size
            pos: root.pos
            source: './tablet_app/images/TangramGame_Selection.jpg'
            allow_stretch: True
            keep_ratio: False
        TangramSelectionWidget:
            id: tangram_selection_widget
        QuestionMarkWidget:
            id: question_mark_widget
            size: root.size
            pos: root.pos
        BalloonsWonWidget:
            id: balloons_won_widget
            size: (root.size[0] * 0.7,root.size[1])
            pos: root.pos
        LoggedButton:
            id: stop_button
            name: 'stop_button'
            background_normal:  './tablet_app/images/reset_button.jpg'
            background_down:  './tablet_app/images/reset_button_down.jpg'
            border: (0,0,0,0)
            size: root.width * 0.03, root.width * 0.03
            pos: root.width * 0.98 - self.width * 0.5, root.height * 0.975 - self.height * 0.5
            on_press: app.press_stop_button()


<TangramSelectionWidget>
    name: 'tangram_selection_widget'

<BalloonsWonWidget>
    Image:
        id: balloon1
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.1, root.height * 0.90
        source: './tablet_app/images/Balloon_Price1.gif'
        opacity: 0

    Image:
        id: balloon2
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.2, root.height * 0.90
        source: './tablet_app/images/Balloon_Price2.gif'
        opacity: 0

    Image:
        id: balloon3
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.3, root.height * 0.90
        source: './tablet_app/images/Balloon_Price3.gif'
        opacity: 0

    Image:
        id: balloon4
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.4, root.height * 0.90
        source: './tablet_app/images/Balloon_Price1.gif'
        opacity: 0

    Image:
        id: balloon5
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.5, root.height * 0.90
        source: './tablet_app/images/Balloon_Price2.gif'
        opacity: 0

    Image:
        id: balloon6
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.6, root.height * 0.90
        source: './tablet_app/images/Balloon_Price3.gif'
        opacity: 0

    Image:
        id: balloon7
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.7, root.height * 0.90
        source: './tablet_app/images/Balloon_Price1.gif'
        opacity: 0

    Image:
        id: balloon8
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.8, root.height * 0.90
        source: './tablet_app/images/Balloon_Price2.gif'
        opacity: 0

    Image:
        id: balloon9
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.9, root.height * 0.90
        source: './tablet_app/images/Balloon_Price3.gif'
        opacity: 0

    Image:
        id: balloon10
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 1, root.height * 0.90
        source: './tablet_app/images/Balloon_Price1.gif'
        opacity: 0

    Image:
        id: balloon11
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 1.1, root.height * 0.90
        source: './tablet_app/images/Balloon_Price2.gif'
        opacity: 0

    Image:
        id: balloon12
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 1.2, root.height * 0.90
        source: './tablet_app/images/Balloon_Price3.gif'
        opacity: 0

<QuestionMarkWidget>
    Image:
        id: question_mark
        size: (root.size[0] * 0.17375, root.size[1] * 0.18833)
        pos: root.width * 0.7375, root.height * 0.22
        source: './tablet_app/images/question_mark.gif'
        opacity: 1

<SolveTangramRoom>:
    name: 'solve_tangram_room'
    Widget:
        Background:
            size: root.size
            pos: root.pos
        TreasureBox:
            id: treasure_box
            size: root.size
            pos: root.pos
        HourGlassWidget:
            id: hourglass_widget
        TangramGameWidget:
            id: tangram_game_widget
        LoggedButton:
            id: stop_button
            name: 'stop_button'
            background_normal:  './tablet_app/images/reset_button.jpg'
            background_down:  './tablet_app/images/reset_button_down.jpg'
            border: (0,0,0,0)
            size: root.width * 0.04, root.width * 0.04
            pos: root.width * 0.975 - self.width * 0.5, root.height * 0.970 - self.height * 0.5
            on_press: app.press_stop_button()


<Background>:
    Image:
        size: root.size
        pos: root.pos
        source: './tablet_app/images/tangram_background.jpg'
        allow_stretch: True
        keep_ratio: False

<TreasureBox>:
    Image:
        name: 'treasure_box'
        id: box
        source: './tablet_app/images/TreasureBoxLayers_B.gif'
        allow_stretch: True
        keep_ratio: False
    Image:
        name: 'balloon'
        id: balloon
        allow_stretch: True
        keep_ratio: False
        opacity: 0

<HourGlassWidget>:
    name: 'hour_glass_widget'
    Image:
        id:topSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id:middleSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id:bottomSand
        source: './tablet_app/images/sand.jpg'
        allow_stretch: True
        keep_ratio: False
    Image:
        id: hourglass
        source: './tablet_app/images/hour_glass.gif'
        allow_stretch: True
        keep_ratio: False
        pos: self.pos
        size: self.size

<TangramGameWidget>:
    name: 'tangram_game_widget'

<PartyScreenRoom>:
    name: 'party_screen_room'
    Widget:
        PartyScreenBackground:
            size: root.size
            pos: root.pos
        PartyScreenBalloonsWidget:
            id: party_screen_balloons_widget
            size: root.size
            pos: root.pos

<PartyScreenBackground>:
    Image:
        size: root.size
        pos: root.pos
        source: './tablet_app/images/TangramGame_Open.jpg'
        allow_stretch: True
        keep_ratio: False

<PartyScreenBalloonsWidget>
    Image:
        id: balloon1
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.15, root.height * 0.56
        source: './tablet_app/images/Balloon_Price1.gif'
        opacity: 1

    Image:
        id: balloon5
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.2, root.height * 0.54
        source: './tablet_app/images/Balloon_Price2.gif'
        opacity: 1

    Image:
        id: balloon12
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.25, root.height * 0.53
        source: './tablet_app/images/Balloon_Price3.gif'
        opacity: 1

    Image:
        id: balloon7
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.30, root.height * 0.52
        source: './tablet_app/images/Balloon_Price1.gif'
        opacity: 1

    Image:
        id: balloon2
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.35, root.height * 0.52
        source: './tablet_app/images/Balloon_Price2.gif'
        opacity: 1

    Image:
        id: balloon9
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.40, root.height * 0.52
        source: './tablet_app/images/Balloon_Price3.gif'
        opacity: 1

    Image:
        id: balloon4
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.45, root.height * 0.52
        source: './tablet_app/images/Balloon_Price1.gif'
        opacity: 1

    Image:
        id: balloon11
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.50, root.height * 0.52
        source: './tablet_app/images/Balloon_Price2.gif'
        opacity: 1

    Image:
        id: balloon6
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.55, root.height * 0.53
        source: './tablet_app/images/Balloon_Price3.gif'
        opacity: 1

    Image:
        id: balloon10
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.60, root.height * 0.53
        source: './tablet_app/images/Balloon_Price1.gif'
        opacity: 1

    Image:
        id: balloon8
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.65, root.height * 0.54
        source: './tablet_app/images/Balloon_Price2.gif'
        opacity: 1

    Image:
        id: balloon3
        size: root.width * 0.10, root.width * 0.10
        pos: root.width * 0.7, root.height * 0.55
        source: './tablet_app/images/Balloon_Price3.gif'
        opacity: 1


''')

# functions connecting to button pressed


class TangramMindsetApp(App):
    tangrams_solved = 0
    interaction = None
    sounds = None
    current_sound = None
    screen_manager = None
    current = None
    game = None
    selection = None
    text_handler = None
    tablet_disabled = False
    yes_clicked_flag = False

    def build(self):
        self.interaction = Interaction(
            [('robot', 'RobotComponent'),
             ('child', 'ChildComponent'),
             ('internal_clock', 'ClockComponent'),
             ('hourglass', 'HourglassComponent')
             ]
        )
        self.interaction.components['tablet'] = TabletComponent(self.interaction, 'tablet')
        self.interaction.components['game'] = GameComponent(self.interaction, 'game')
        self.interaction.components['game'].game_facilitator = GameFacilitator()

        s = SolveTangramRoom(self.interaction.components['tablet'])

        self.interaction.components['tablet'].hourglass_widget = s.ids['hourglass_widget']
        #self.interaction.components['hourglass'].widget = s.ids['hourglass_widget']
        self.interaction.components['tablet'].app = self
        if not GAME_WITH_ROBOT:
            self.interaction.components['robot'].app = self
            self.interaction.components['robot'].load_text(filename='./tablet_app/robot_text_grit_assess.json') #added in order to play sound files
        else:
            if STUDY_SITE == 'MIT':
                self.interaction.components['robot'].load_text(filename='./tablet_app/robot_text_revised3.json')
                self.interaction.components['robot'].robot_name = 'tega'
            elif STUDY_SITE == 'TAU':
                self.interaction.components['robot'].load_text(filename='./tablet_app/robot_text_revised4_tau.json')
                self.interaction.components['robot'].robot_name = 'nao'
        self.interaction.load(filename='./tablet_app/transitions.json')
        self.interaction.next_interaction()

        self.load_sounds()
        self.init_communication()

        self.screen_manager = MyScreenManager()
        zero_screen = ZeroScreenRoom(self)
        zero_screen.ids['subject_id'].bind(text=zero_screen.ids['subject_id'].on_text_change)
        self.screen_manager.add_widget(zero_screen)
        self.screen_manager.add_widget(FirstScreenRoom(self.interaction.components['tablet']))
        self.screen_manager.add_widget(SelectionScreenRoom(self.interaction.components['tablet']))
        self.screen_manager.add_widget(PartyScreenRoom(self.interaction.components['tablet']))
        self.screen_manager.add_widget(s)


        return self.screen_manager

    def on_start(self):
        print ('app: on_start')
        TangramGame.SCALE = round(self.root_window.size[0] / 60)
        TangramGame.window_size = self.root_window.size

    def init_communication(self):
        local_ip = '192.168.1.254'
        if STUDY_SITE == 'TAU':
            local_ip = '192.168.0.103'
        elif STUDY_SITE == 'MIT':
            local_ip = '192.168.1.254'
        KC.start(the_parents=[self, self.interaction.components['robot']], the_ip=local_ip)  # 127.0.0.1
        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir, the_ip=local_ip)

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='TangramMindsetApp', comment='start')


    def load_sounds(self):
        # load all the wav files into a dictionary whose keys are the expressions from the transition.json
        sound_list = ['introduction', 'click_balloon', 'introduction_c-g-_0', 'ask_again_0', \
                      'ask_again_1', 'let_play_0', 'selection_tutorial_c-g-_0', \
                      'tangram_tutorial_all_0_faster', 'move_explanation_c-g-_0',\
                      'move_explanation_c-g-_0', 'move_explanation_c-g-_1', 'move_explanation_c-g-_2',\
                      'move_explanation_c-g-_3', 'move_explanation_c-g-_4',\
                      'child_win_c-g-_0', 'child_win_c-g-_1', 'child_win_c-g-_2', 'child_win_c-g-_3', 'child_win_c-g-_4',\
                      'child_win_c-g-_5', 'child_win_c-g-_6', 'child_win_c-g-_7', \
                      'robot_win_c-g-_0', 'robot_win_c-g-_1',\
                      'robot_win_c-g-_2', 'robot_win_c-g-_3', 'robot_win_c-g-_4', 'robot_win_c-g-_5', 'robot_win_c-g-_6',\
                      'robot_win_c-g-_7',\
                      'robot_lose_c-g-_0', 'robot_lose_c-g-_1', 'robot_lose_c-g-_2', 'robot_lose_c-g-_3', 'robot_lose_c-g-_4',
                      'child_lose_c-g-_0', 'child_lose_c-g-_1', 'child_lose_c-g-_3', 'child_lose_c-g-_4', 'child_lose_c-g-_5',\
                      'your_turn_all_0', 'your_turn_all_1', 'your_turn_all_2', 'your_turn_all_3', 'your_turn_all_4','your_turn_all_0',\
                      'your_turn_c-g-_0', 'your_turn_c-g-_1', 'your_turn_c-g-_2', 'your_turn_c-g-_3', 'your_turn_c-g-_4',\
                      'your_turn_c-g-_5', 'your_turn_c-g-_6', 'comment_move_c-g-_0', 'comment_move_c-g-_1', 'comment_move_c-g-_2',\
                      'comment_move_c-g-_3', 'comment_move_c-g-_4', 'comment_move_c-g-_5', 'conclusion_all_0', 'party_all_0']
        self.sounds = {}
        for s in sound_list:
            self.sounds[s] = SoundLoader.load("./tablet_app/sounds/" + s + ".m4a")
        self.current_sound = None

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Messages from robot to tablet to interaction
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def change_pieces(self, x):
        print('app changes pieces to ', x)
        # first, start to move the pieces on the tablet

        self.screen_manager.get_screen('solve_tangram_room').change_pieces(x)
        # put dynamic here!
        # XXXXXX RINAT XXX
        # ONLY WHEN THE PIECES FINISHED MOVING, then call the interaction with the line below.
        # time.sleep(1)
        # self.interaction.components['child'].on_action(['tangram_change', x])


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Messages from tablet to interaction
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def changed_pieces(self, x):
        # the robot finished changing the pieces
        print("tangram_mindset_app:changed_pieces",x)
        self.interaction.components['child'].on_action(['tangram_change', x])
        print("finished changed_pieces")

    def press_start_button (self):
        # child pressed the start button
        self.interaction.components['child'].on_action(["press_start_button"])

    def press_tega_sleep (self):
        # put tega to sleep
        action_script = ["tega_init"]
        self.interaction.components['robot'].express(action_script)

    def press_load_transition(self, stage):
        print("loading new transition file")

        games_played = int(stage.replace('game',''))-1

        # increase challenge_counter
        if games_played > 6:
            self.interaction.components['game'].game_facilitator.selection_gen.challenge_counter += 1
            self.interaction.components['game'].game_facilitator.selection_gen.challenge_index += 1

        for i in range(games_played):
            self.interaction.components['game'].game_facilitator.update_game_result('S')
            print(self.interaction.components['game'].game_facilitator.selection_gen.current_level)
            self.tangrams_solved += choice([1,0])

        if games_played < 4:
            games_played += 1

        self.tangrams_solved = max(games_played/2, self.tangrams_solved)

        filename = './tablet_app/transitions_'+stage+'.json'
        self.interaction.load(filename)
        self.interaction.next_interaction()

    def press_yes_button(self):
        # child pressed the yes button
        if not self.yes_clicked_flag:
            self.interaction.components['child'].on_action(["press_yes_button"])
            self.yes_clicked_flag = True

    def press_treasure(self, treasure, dt=0):
        # child selected treasure (1/2/3)
        # print("press_treasure", treasure)
        #self.screen_manager.current_screen.show_selection(treasure)
        self.interaction.components['child'].on_action(['press_treasure', treasure])

    def tangram_move(self, x):
        # child moved a tangram piece (json of all the pieces)
        print(self.name, 'tangram_mindset_app: tangram_move', x)
        self.interaction.components['child'].on_action(['tangram_change', x])

    def tangram_turn (self, x):
        # child turned a tangram piece (json of all the pieces)
        print(self.name, 'tangram_mindset_app: tangram_turn', x)
        self.interaction.components['child'].on_action(['tangram_change', x])

    def check_solution(self, solution_json):
        # this function should not really be here
        print("tangram_mindset_app: check_solution", solution_json)
        return self.interaction.components['game'].game_facilitator.check_solution(solution_json)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Messages from interaction to tablet
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def first_screen(self):
        self.screen_manager.current = 'first_screen_room'


    def party_screen(self):
        self.screen_manager.get_screen('party_screen_room').init_balloons(self.tangrams_solved)
        self.screen_manager.current = 'party_screen_room'


    def selection_screen(self, x):
        # Rinat: x is a list of tangrams from maor
        # you need to present all options with the tangram pieces
        print('x=',x)
        TangramGame.SCALE = round(Window.size[0] / 75)
        self.screen_manager.get_screen('selection_screen_room').init_selection_options(x=x,the_app=self)
        self.screen_manager.current = 'selection_screen_room'

    def select_treasure(self,treasure):
        # robot selected treasure
        print ("select_treasure",treasure)
        print()
        self.screen_manager.current_screen.show_selection(treasure)
        Clock.schedule_once(lambda dt: self.press_treasure(treasure),1)

    def tangram_screen(self, x):
        # Rinat: x is a single tangram from maor
        # you need to present it and allow game
        print("tangram_screen",x)
        TangramGame.SCALE = round(Window.size[0] / 30)
        self.screen_manager.get_screen('solve_tangram_room').init_task(x, the_app=self)
        self.screen_manager.current = 'solve_tangram_room'

    def robot_express(self, action, expression):
        # robot is saying action
        print ('robot_express action',action, ' expression ', expression)
        self.current_sound = action

        sound_filename = ''
        for name in expression[1:]:
            if name.lower() == name:
                print('filename: ',name)
                sound_filename = name

        # attempt tts
        #if self.text_handler.say(self.current_sound):
        if 1==0:
            self.finish_robot_express(0)
        else:   # attempt recorded speech
            try:
                print('current_sound: ',sound_filename)
                sound = self.sounds[sound_filename]
                print(sound)
                sound.bind(on_stop=self.finish_robot_express)
                sound.play()
            except: # there is no sound for
                print('no sound for: ', sound_filename)
                self.finish_robot_express(0)

    def finish_robot_express (self, dt):
        #robot finished to talk
        print ('finish_robot_express', self, self.current_sound)
        self.interaction.components['robot'].finished_expression(self.current_sound)

    def yes(self):
        # yes balloon appear on the screen
        print ('yes in app')
        self.screen_manager.current_screen.ids['yes_button'].opacity = 1


    def solved(self):
        print ("trangram_mindset_app: solved")
        self.tangrams_solved += 1
        self.screen_manager.get_screen('solve_tangram_room').solved()

    def robot_solve(self, x):
        # robot is providing a solution sequence x, and solve_tangram_room animates this solution
        print ("tangram_mindset_app: robot_solve")

    def finish(self):
        # when time is up
        self.screen_manager.get_screen('solve_tangram_room').finish()

    # ~~~~~~ child-proofing ~~~~~~

    def disable_tablet(self):
        self.tablet_disabled = True
        self.screen_manager.current_screen.disable_widgets()

    def enable_tablet(self):
        self.tablet_disabled = False
        self.screen_manager.current_screen.enable_widgets()

    def update_condition(self, condition):
        self.text_handler = TextHandler(condition)
        if STUDY_SITE == 'MIT':
            self.text_handler.load_text(filename='./tablet_app/robot_text_revised3.json')
        elif STUDY_SITE == 'TAU':
            self.text_handler.load_text(filename='./tablet_app/robot_text_revised4_tau.json')
        self.interaction.components['robot'].agent.update_condition(condition)

    def press_stop_button(self):
        print('stop button pressed')
        self.interaction.components['hourglass'].stop()
        self.interaction.end_interaction()

    def difficulty_selected(self):
        difficulty = self.screen_manager.get_screen('zero_screen_room').ids['difficulty_spinner'].text
        self.interaction.components['game'].game_facilitator.selection_gen.load_dif_levels(difficulty)


    def condition_selected(self):
        #NOW MOVED TO ADD AND NAMED condition_selection
        print("spinner_selected")
        condition = self.screen_manager.get_screen('zero_screen_room').ids['condition_spinner'].text
        #self.the_app.update_condition(condition)
        self.update_condition(condition)
        print(condition)

if __name__ == "__main__":
    TangramMindsetApp().run()