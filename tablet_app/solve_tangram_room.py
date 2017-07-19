from interaction_control import *
from interaction_control import *
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import Layout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from tangram_game import *


class SolveTangramRoom(Screen):

    the_tablet = None
    tangram_game_widget = None
    time_is_up = False

    def __init__(self, the_tablet):
        self.the_tablet = the_tablet
        super(Screen, self).__init__()

    def on_enter(self, *args):
        print("on_enter solve_tangram_room")
        self.the_tablet.change_state('tangram_screen')
        if self.the_app.tablet_disabled:
            self.disable_widgets()
        # self.load_sounds()
        # self.play_sound("TangramOpen_myFriend")


    def init_task(self,x,the_app):
        self.time_is_up = False
        self.task_json = x
        self.shade_task_json = x[0]
        self.pieces_task_json = x[1]
        self.the_app = the_app

        print("Solve Tangram Room init_task ", self.task_json)

        #Hourglass
        hourglass_widget = self.ids['hourglass_widget']
        hourglass_widget.do_layout()

        tangram_game_widget = self.ids['tangram_game_widget']
        tangram_game_widget.reset(the_app=the_app)  # clear the pieces from previous run

        dX = 9 #Window.width/40.0  #20
        dY = 9 #Window.height/40.0 #15

        #Treasure Box:
        self.ids['treasure_box'].ids['box'].source = './tablet_app/images/TreasureBoxLayers_B.gif'
        self.ids['treasure_box'].ids['box'].size = (TangramGame.SCALE * 27, TangramGame.SCALE * 19)
        self.ids['treasure_box'].ids['box'].pos = [TangramGame.SCALE * 1, int(TangramGame.SCALE * 0.2)]
        self.ids['treasure_box'].ids['balloon'].opacity = 0
        self.ids['treasure_box'].ids['balloon'].size = [TangramGame.SCALE * 6, TangramGame.SCALE * 6]
        self.ids['treasure_box'].ids['balloon'].pos = [TangramGame.SCALE * 15, TangramGame.SCALE * 11]

        #shade:
        game_task_layout = GameTaskLayout()
        game_task_layout.dX = dX
        game_task_layout.dY = dY

        game_task_layout.reset(str(0))
        game_task_layout.import_json_task(self.shade_task_json)
        game_task_layout.update_selection_task_shade()
        tangram_game_widget.add_widget(game_task_layout)
        tangram_game_widget.current_game_task_layout = game_task_layout

        #pieces:
        tangram_game_widget.dX = dX
        tangram_game_widget.dY = dY
        tangram_game_widget.update_task_pieces(self.pieces_task_json)
        #tangram_game_widget.update_task_pieces(self.shade_task_json)

        # button
        button_rotate = Rotate(tangram_game_widget)
        button_rotate.border = (0,0,0,0)
        button_rotate.size =  [Window.width * 0.07, Window.width * 0.07] #[60,60] #
        button_rotate.pos = [TangramGame.SCALE * 20, TangramGame.SCALE * 9]
        button_rotate.background_normal = './tablet_app/images/Tangram_rotate_btn.gif'
        button_rotate.background_down =  './tablet_app/images/Tangram_rotate_btn_down.gif'
        button_rotate.background_disabled_normal = './tablet_app/images/Tangram_rotate_btn.gif'
        button_rotate.background_disabled_down = './tablet_app/images/Tangram_rotate_btn.gif'
        tangram_game_widget.add_widget(button_rotate)
        self.tangram_game_widget = tangram_game_widget


    def change_pieces(self, x):
        print ("solve_tangram_room: change_pieces", x)
        tangram_game_widget = self.ids['tangram_game_widget']
        tangram_game_widget.robot_change_pieces(x)
        #tangram_game_widget.update_task_pieces(x)

    def disable_widgets(self):
        for c in self.ids['tangram_game_widget'].children:
            if isinstance(c, TangramPiece):
                c.do_rotation = False
                c.do_translation = False
                c.do_scale = False
            else:
                c.disabled = True

    def enable(self):
        for c in self.ids['tangram_game_widget'].children:
            if isinstance(c, TangramPiece):
                c.do_rotation = False
                c.do_translation = True
                c.do_scale = False
            else:
                c.disabled = False

    def solved(self):
        print("solve_tangram_room: solved")
        i = self.the_app.tangrams_solved
        i = (i-1)%3 + 1
        self.ids['treasure_box'].ids['box'].source = './tablet_app/images/TreasureOpenBoxLayers_B.gif'
        self.ids['treasure_box'].ids['balloon'].source = './tablet_app/images/Balloon_Price'+str(i)+'.gif'
        self.ids['treasure_box'].ids['balloon'].opacity = 1
        anim = Animation(x=self.ids['treasure_box'].ids['balloon'].pos[0],
                         y=self.ids['treasure_box'].ids['balloon'].pos[1]*1.1,
                         duration=0.5)
        anim.start(self.ids['treasure_box'].ids['balloon'])


        for c in self.ids['tangram_game_widget'].children:
            if isinstance(c, TangramPiece):
                if (c.pos[1] > self.size[1] * 0.65): #if the pieces is still on top make it invisible
                    c.opacity = 0

    def finish(self):
        print("solve, finish, the time is up!")
        self.time_is_up = True
        self.ids['hourglass_widget'].middleSand.opacity = 0


class Rotate(LoggedButton):

    press_rotate_sound = None
    def __init__(self, game_widget):
        super(Rotate,self).__init__()
        self.tangram_game_widget = game_widget
        self.name = "rotate_btn"
        self.background_normal = 'buttons/arrow_rotate.png'
        self.size = (TangramGame.SCALE * 4, TangramGame.SCALE * 4)
        self.press_rotate_sound = SoundLoader.load('./tablet_app/sounds/tongue-click.m4a')

    def on_press(self):
    # press the rotate button
        if self.tangram_game_widget.current is not None:
            self.press_rotate_sound.play()
            self.tangram_game_widget.current.rot = str(int(self.tangram_game_widget.current.rot) + 90)
            if self.tangram_game_widget.current.rot == '360':
                self.tangram_game_widget.current.rot = '0'
            self.tangram_game_widget.current.set_shape()
        self.tangram_game_widget.tangram_turn()

class GameTaskLayout(LoggedButton, TaskLayout):
    # inherits from TaskLayout which is in tangram_game.py

    def __init__(self):
        super(GameTaskLayout, self).__init__()
        print("GameTaskLayout __init__")
        self.name = 'GameTaskLayout'
        self.size = [300,300]
        self.update_position()
        with self.canvas.before:
            print ("self.canvas.before")
            Color(234/255.0,226/255.0,139/255.0,1)
            self.rect = Rectangle()
            self.rect.pos = self.pos
            self.rect.size = self.size
            print (self.rect.size)

    def update_position(self, *args):
        print('GameTaskLayout update_position')
        #self.size = [Window.width * 0.26, Window.height * 0.26]
        self.size = [TangramGame.SCALE * 10, TangramGame.SCALE * 10]
        self.pos = [TangramGame.SCALE * 8, TangramGame.SCALE * 2]
        print("Window.width",Window.width,"Window.height", Window.height)
        #self.update_selection_task_pos()

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        print('GameTaskLayout self.size ',self.size, 'self.pos ', self.pos)
        self.rect.size = self.size

    def update_selection_task_shade(self):
        #print ('update_selection_task_shade ')
        #print('TangramGame.SCALE ', TangramGame.SCALE)
        #print('update_selection_task_pos ', self.pos, self.size)
        for p in self.pieces:
            p['pos'][0] +=  self.dX * TangramGame.SCALE
            p['pos'][1] +=  self.dY * TangramGame.SCALE
            #print("update_selection_task_shade", p['pos'])
        self.update_task()


    def get_color(self, index):
        modulo = index % 3
        if (modulo == 0):
            my_color = Color(1,0,0,1)
        elif (modulo == 1):
            my_color = Color(0,1,0,1)
        elif (modulo == 2):
            my_color = Color(0,0,1,1)
        return my_color


class Background(Widget):
    pass


class TreasureBox(Widget):
    def rotate_shape(self, *kwargs):
        print("rotate shape")

class TangramGameWidget(Widget):
    task_json = None
    the_app = None
    current = None  #current selected piece
    current_down = False
    current_game_task_layout = None
    pieces = {}
    dX = None
    dY = None
    anim = False
    pieces_target_json = None
    robot_press_rotate_sound = None

    def __init__(self, **kwargs):
        print("TangramGameWidget __init__")
        super(TangramGameWidget, self).__init__(**kwargs)
        self.canvas.clear()
        self.clear_widgets()
        self.robot_press_rotate_sound = SoundLoader.load('./tablet_app/sounds/tongue-click.m4a')

    def reset(self, the_app):
        self.the_app = the_app
        self.clear_widgets()

    def update_task_pieces(self, pieces_task_json):
        # updated the pieces that the child can play with (not the shade)
        self.current_down = False
        self.current = None
        print("update_task_pieces",pieces_task_json)
        self.pieces = {}
        pieces_dict = json.loads(pieces_task_json)

        for p in pieces_dict['pieces']:
            print(p)
            name = p[0]
            rot = p[1]
            self.pieces[name] = TangramPiece(self)
            self.pieces[name].name = name
            self.pieces[name].rot = p[1]
            x = float(p[2].split()[0])
            y = float(p[2].split()[1])
            converted_pos = self.convert_piece_pos(name,[x,y], rot)
            self.pieces[name].pos = converted_pos

        for key, value in self.pieces.items():
            print ("key,value",key,value)
            x = value.pos[0] + self.dX * TangramGame.SCALE
            y = value.pos[1] + self.dY * TangramGame.SCALE

            x -= TangramPiece.piece_size[name][0] * TangramGame.SCALE / 2
            y -= TangramPiece.piece_size[name][1] * TangramGame.SCALE / 2

            value.pos = [x, y]
            # value.init_position()
            value.set_shape()
            self.add_widget(value)

    def robot_change_pieces(self, pieces_target_json):
        if not self.anim:
            self.pieces_target_json = pieces_target_json
            print ("robot_change_pieces", pieces_target_json)
            pieces_dict = json.loads(pieces_target_json)
            i=0
            self.anim=False
            for p in pieces_dict['pieces']:
                self.robot_change_piece(p)
            if not self.anim:
                print("not anim")
                #self.robot_finished_change_piece(pieces_target_json)
                self.the_app.changed_pieces(pieces_target_json)
        else:
            print("already anim")

    def robot_change_piece (self, piece_dict):
        print("robot_change_piece", piece_dict)
        name = piece_dict[0]
        rot = piece_dict[1]
        x = float(piece_dict[2].split()[0])
        y = float(piece_dict[2].split()[1])
        initial_rot = self.pieces[name].rot
        self.pieces[name].rot = rot
        new_pos = self.convert_piece_pos(name,[x,y],rot)
        x = new_pos[0] + self.dX * TangramGame.SCALE
        y = new_pos[1] + self.dY * TangramGame.SCALE

        x -= TangramPiece.piece_size[name][0] * TangramGame.SCALE /2
        y -= TangramPiece.piece_size[name][1] * TangramGame.SCALE /2

        #self.pieces[name].pos = [x,y]
        self.pieces[name].set_shape()
        print("?", self.pieces[name].name, "pos=", self.pieces[name].pos, "target=", (x, y))

        if (initial_rot != rot):
            self.robot_press_rotate_sound.play()

        if (((round(self.pieces[name].pos[0]),round(self.pieces[name].pos[1])) != (x,y)) | (initial_rot != rot)):
            print("!=",self.pieces[name].name,"pos=",self.pieces[name].pos,"target=",(x,y))
            self.anim = True
            animPiece = Animation(x=x,y=y,
                                   duration=1,
                                   transition='in_quad')
            animPiece.start(self.pieces[name])
            # Clock.schedule_once(lambda dt: self.robot_finished_change_piece, 1)
            Clock.schedule_once(self.robot_finished_change_piece, 2)
            # animPiece.bind(on_complete=self.robot_finished_change_piece(self.pieces_target_json)) #the bind caused problems
            # self.robot_finished_change_piece(self.pieces_target_json)
            # self.the_app.changed_pieces(self.pieces_target_json)

    def robot_finished_change_piece(self, dt):
        print("robot_finished_change_piece", self.pieces_target_json)
        print ("time_is_up",self.parent.parent.time_is_up)
        self.anim = False
        if (not self.parent.parent.time_is_up):
            self.the_app.changed_pieces(self.pieces_target_json)
        return False

    @staticmethod
    def convert_piece_pos(name,pos,rot):
        #print("convert_piece", piece)
        #print("convert_piece: ",piece.name[0])
        #print("convert_dict_piece before",pos)
        #converted_piece = {'name': piece.name, 'rot': piece.rot}
        converted_pos = None
        if 'small triangle' in name:
            converted_pos = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                      (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
        if 'medium triangle' in name:
            if rot == '0':
                converted_pos = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                          (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
            if rot == '90':
                converted_pos = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                          (-2 * int(pos[0])) * TangramGame.SCALE]
            if rot == '180':
                converted_pos = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                          (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
            if rot == '270':
                converted_pos = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                          (-2 * int(pos[0])) * TangramGame.SCALE]
        if 'large triangle' in name:
            converted_pos = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                      (-2 * int(pos[0])) * TangramGame.SCALE]
        if 'square' in name:
            converted_pos = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                      (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
        if 'parrallelogram' in name:
            if rot == '0':
                converted_pos = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                          (-2 * int(pos[0])) * TangramGame.SCALE]
            if rot == '90':
                converted_pos = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                          (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
            if rot == '180':
                converted_pos = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                          (-2 * int(pos[0])) * TangramGame.SCALE]
            if rot == '270':
                converted_pos = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                          (-2 * int(pos[0]) + 1) * TangramGame.SCALE]

        #print("convert_piece_pos after", converted_pos)
        return converted_pos

    def is_selected(self):
        for k, p in self.pieces.items():
            if p.selected:
                return True
        return False

    def reset_sizes(self):
        for k, p in self.pieces.items():
            p.size = [TangramPiece.piece_size[p.name][0] * TangramGame.SCALE,
                      TangramPiece.piece_size[p.name][1] * TangramGame.SCALE]

    def tangram_turn (self):
        solution_json = self.export_task()
        print ("solve_tangram_room: tangram_turn", solution_json)
        self.the_app.tangram_turn(solution_json)

    def check_solution (self):
        # this function is called from tangram_game: TangramPiece class after touch_up on piece
        solution_json = self.export_task()
        self.the_app.tangram_move(solution_json)
        print ("check_solution:", self.the_app.check_solution(solution_json))

    def export_task(self):
        # export current pieces to json string in Task format
        task_dict = {}
        task_dict['size'] = '5 5'
        task_dict['pieces'] = []

        for p in self.pieces:
            name = self.pieces[p].name
            rot = self.pieces[p].rot
            pos = [self.pieces[p].pos[0], self.pieces[p].pos[1]]

            # print 'pieces:'
            # print  [self.pieces[p].name, self.pieces[p].rot,self.pieces[p].pos[0], self.pieces[p].pos[1] ]

            pos[0] += -self.dX * TangramGame.SCALE
            pos[1] += -self.dY * TangramGame.SCALE

            if 'small triangle' in name:
                pos = [(-0.5 * (pos[1] / TangramGame.SCALE - 1)) - 0.5, (0.5 * (pos[0] / TangramGame.SCALE - 1)) + 0.5]
            elif 'medium triangle' in name:
                if rot == '0':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
                elif rot == '90':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 1]
                elif rot == '180':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
                elif rot == '270':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 1]
            elif 'large triangle' in name:
                pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
            elif 'square' in name:
                pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 0.5, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 0.5]
            elif 'parrallelogram' in name:
                if rot == '0':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 1]
                elif rot == '90':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
                elif rot == '180':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 1]
                elif rot == '270':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
                    # print 'new pos:'
            # print [name, rot, pos]
            task_dict['pieces'].append((name, rot, str(pos[0]) + ' ' + str(pos[1])))
        json_str = json.dumps(task_dict)
        # print json_str
        return json_str


class HourGlassWidget (Widget):
    time_over_sound = None
    def __init__(self, **kwargs):
        super(HourGlassWidget, self).__init__(**kwargs)
        self.delta=0
        #self.animate_sand()
        Clock.schedule_interval(self.after_init,0.01)  #only after init is done ids can be accessed

    def after_init(self, *args):
        print ('HourGlassWidget: after init')
        self.time_over_sound = SoundLoader.load('./tablet_app/sounds/time_over.m4a')
        self.hourglass = self.ids['hourglass']
        self.topSand = self.ids['topSand']
        self.middleSand = self.ids['middleSand']
        self.bottomSand = self.ids['bottomSand']
        self.init = False
        self.do_layout()
        # self.start_hourglass(120)
        return False

    def do_layout(self, *args):
        print ("do_layout")
        print (self)
        #if (not self.init):
        self.size = Window.width * 0.08, Window.height * 0.2
        self.pos = [TangramGame.SCALE * 27, TangramGame.SCALE * 2]
        sandWidth = self.width
        sandHeight = self.height * 0.25
        self.sandHeight = sandHeight
        self.hourglass.size = self.width, self.height
        self.hourglass.pos = self.x, self.y
        self.topSand.size = sandWidth, sandHeight
        self.topSand.pos = self.x, self.y+self.height * 0.5
        self.middleSand.opacity = 1
        self.middleSand.size = sandWidth * 0.05, sandHeight * 2
        self.middleSand.pos = self.x + sandWidth/2.0 - sandWidth*0.02, self.y+0
        self.bottomSand.size = sandWidth, 0
        self.bottomSand.pos = self.x, self.y+0 + self.height * 0.041
        self.init = True

    def start_hourglass(self):
        print('start hourglass')
        pass

    def stop_hourglass(self, *args):
        #self.middleSand.height = 0
        print("time is up")

    def update_hourglass (self, percent):
        current_time = float(percent[0])
        total_time = float(percent[1])
        current_percent = current_time / total_time
        self.topSand.height =  self.sandHeight * current_percent
        self.bottomSand.height = self.sandHeight* (1 - current_percent)
        if (current_percent < 0.02):
            #self.middleSand.height = 0
            self.middleSand.opacity = 0
            self.time_over_sound.play()
            # self.time_is_up = True

