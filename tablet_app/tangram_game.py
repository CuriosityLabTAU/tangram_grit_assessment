import kivy
kivy.require('1.8.0')  # replace with your current kivy_tests version !
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
import copy
import json
from tangrams import Task
from kivy.core.window import Window
from kivy_communication import LoggedButton, WidgetLogger


class TangramPiece(Scatter, WidgetLogger):
    tangram_list = ['small triangle1','small triangle2',
                    'large triangle1','large triangle2',
                    'medium triangle',
                    'square', 'parrallelogram'
                    ]
    piece_color = {
        #'small triangle1':  Color(0.5, 0.0, 0.0, 0.9),
        #'small triangle2':  Color(0.0, 0.5, 0.0, 0.9),
        #'medium triangle':  Color(0.5, 0.5, 0.0, 0.9),
        #'large triangle1':  Color(0.0, 0.0, 0.5, 0.9),
        #'large triangle2':  Color(0.5, 0.0, 0.5, 0.9),
        #'square':           Color(0.0, 0.5, 0.5, 0.9),
        #'parrallelogram':   Color(0.5, 0.5, 0.0, 0.9)
        'small triangle1': Color(1.0, 0.0, 0.0, 0.9),
        'small triangle2': Color(0.0, 1.0, 0.0, 0.9),
        'medium triangle': Color(0, 0, 1.0, 0.9),
        'large triangle1': Color(1.0, 1.0, 0, 0.9),
        'large triangle2': Color(0.8, 0.18, 1, 0.9),
        'square': Color(1.0, 0.5, 0.0, 0.9),
        'parrallelogram': Color(1.0, 0.0, 1.0, 0.9)
    }
    piece_initial_pos = {
        'small triangle1':  [5, 5],
        'small triangle2':  [5, 10],
        'large triangle1':  [5, 15],
        'large triangle2':  [5, 20],
        'medium triangle':  [25, 5],
        'square':           [25, 12],
        'parrallelogram':   [25, 20]
    }
    piece_size = {
        'small triangle1':  [2, 2],
        'small triangle2':  [2, 2],
        'large triangle1':  [4, 4],
        'large triangle2':  [4, 4],
        'medium triangle':  [4, 4],
        'square':           [2, 2],
        'parrallelogram':   [4, 4]
    }

    @staticmethod
    def only_shape(name):
        if name[-1].isdigit():
            return name[:-1]
        else:
            return name

    def __init__(self, the_app):
        super(TangramPiece, self).__init__()
        self.the_app = the_app
        self.name = ''
        self.piece_pos = [0, 0]
        self.rot = '0'
        self.selected = False

        self.group = None

        self.do_rotation = False
        self.do_scale = False

        self.tangram_color = Color(0.5, 0.5, 0.5, 0.5)
        self.auto_bring_to_front = True

    def init_position(self):
        # self.pos = [TangramPiece.piece_initial_pos[self.name][0] * TangramGame.SCALE,
        #              TangramPiece.piece_initial_pos[self.name][1] * TangramGame.SCALE]
        #self.pos = [self.pos[0] * TangramGame.SCALE,
        #            self.pos[1] * TangramGame.SCALE]
        #n=self.pos[0]
        #x = self.pos[0] + 12 * TangramGame.SCALE
        #y = self.pos[1] + 13 * TangramGame.SCALE

        x = self.pos[0] + 13 * TangramGame.SCALE
        y = self.pos[1] + 20 * TangramGame.SCALE

        self.pos = [x,y]
        print("init_position",self.pos)
        #self.size = [self.piece_size[self.name][0] * TangramGame.SCALE,
        #             self.piece_size[self.name][1] * TangramGame.SCALE]

    def on_touch_down(self, touch):
        print ("tangram_game, on_touch_down", self.name)
        self.size = [TangramPiece.piece_size[self.name][0] * TangramGame.SCALE,
                     TangramPiece.piece_size[self.name][1] * TangramGame.SCALE]
        #print ("is collide point", self.name, touch.pos[0], touch.pos[1])
        if self.collide_point(touch.pos[0], touch.pos[1]):
            print ("down collide point", self,touch.pos[0],touch.pos[1])
            #if not self.parent.is_selected(): #rinat implemented the line below to try and make it more efficient
            if not self.parent.current_down:  #check if currently there is no other piece down
                super(TangramPiece, self).on_touch_down(touch)
                self.parent.current = self
                self.parent.current_down = True
                self.selected = True


    def on_touch_up(self, touch):
        print ("tangram_game, on_touch_up", self.name,touch.pos[0], touch.pos[1])
        super(TangramPiece, self).on_touch_up(touch)
        self.parent.current_down = False #rinat: I moved it here because sometimes on up the mouse is not on the piece that was pressed. We still want it to be false otherwise other pieces will not be able to move.
        try:
            if self.collide_point(touch.pos[0], touch.pos[1]):
                print ("self.collide_point",self.name, self.collide_point(touch.pos[0], touch.pos[1]))
                self.selected = False
                if self.name == self.parent.current.name:
                    self.parent.current_down = False
                    self.pos = (round(self.pos[0] / TangramGame.SCALE) * TangramGame.SCALE, round(self.pos[1]/TangramGame.SCALE) * TangramGame.SCALE)
                    self.parent.check_solution()
            self.size = [TangramPiece.piece_size[self.name][0] * TangramGame.SCALE,
                         TangramPiece.piece_size[self.name][1] * TangramGame.SCALE]
        except:
            print("failed on_touch_up")

#rinat

    def set_shape(self):#rinat
        self.size = [TangramPiece.piece_size[self.name][0] * TangramGame.SCALE,
                     TangramPiece.piece_size[self.name][1] * TangramGame.SCALE]
        if self.group is not None:
            self.canvas.remove(self.group)

        piece = {
            'name': self.name,
            'rot':  self.rot,
            'pos':  [self.size[0]/2, self.size[1]/2]
        }
#[self.size[0]/2, self.size[1]/2]
        self.group = TangramPiece.get_shape(piece, TangramPiece.piece_color[piece['name']])

        if self.group is not None:
            self.canvas.add(self.group)
            #self.canvas.ask_update()

    @staticmethod
    def get_shape(piece, color=None):
        x = None
        if piece['name'] == 'square':
            x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                 piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                 piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                 piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE)
            piece_shape = Quad(points=x)

        if piece['name'] == 'parrallelogram':
            if piece['rot'] == '0':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] - TangramGame.SCALE, piece['pos'][1],
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1])
            if piece['rot'] == '90':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0], piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0], piece['pos'][1] - TangramGame.SCALE)
            if piece['rot'] == '180':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1],
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] - TangramGame.SCALE, piece['pos'][1])
            if piece['rot'] == '270':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0], piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0], piece['pos'][1] - TangramGame.SCALE)
            piece_shape = Quad(points=x)

        if piece['name'] == 'small triangle1':
            if piece['rot'] == '0':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE)
            if piece['rot'] == '90':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE)
            if piece['rot'] == '180':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE)
            if piece['rot'] == '270':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE)
            piece_shape = Triangle(points=x)

        if piece['name'] == 'small triangle2':
            if piece['rot'] == '0':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE)
            if piece['rot'] == '90':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE)
            if piece['rot'] == '180':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE)
            if piece['rot'] == '270':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE)
            piece_shape = Triangle(points=x)

        if piece['name'] == 'medium triangle':
            if piece['rot'] == '0':
                x = (piece['pos'][0], piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] + TangramGame.SCALE)
            if piece['rot'] == '90':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] - TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1])
            if piece['rot'] == '180':
                x = (piece['pos'][0], piece['pos'][1] + TangramGame.SCALE,
                     piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] - TangramGame.SCALE)
            if piece['rot'] == '270':
                x = (piece['pos'][0] - TangramGame.SCALE, piece['pos'][1],
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] + TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE)
            piece_shape = Triangle(points=x)

        if piece['name'] == 'large triangle1':
            if piece['rot'] == '90':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE)
            if piece['rot'] == '180':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE)
            if piece['rot'] == '270':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE)
            if piece['rot'] == '0':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE)
            piece_shape = Triangle(points=x)

        if piece['name'] == 'large triangle2':
            if piece['rot'] == '90':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE)
            if piece['rot'] == '180':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE)
            if piece['rot'] == '270':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE)
            if piece['rot'] == '0':
                x = (piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] + 2*TangramGame.SCALE, piece['pos'][1] + 2*TangramGame.SCALE,
                     piece['pos'][0] - 2*TangramGame.SCALE, piece['pos'][1] - 2*TangramGame.SCALE)
            piece_shape = Triangle(points=x)

        if x is not None:
            group = InstructionGroup()
            group.add(color)
            group.add(piece_shape)
            return group
        return None


class Rotate(LoggedButton):

    def __init__(self, the_app):
        super(Rotate,self).__init__()
        self.name = 'rotate'
        #self.the_app = the_app
        #self.parent is TangramGameWidget which is the same value as the_app

        self.background_normal = 'buttons/arrow_rotate.png'
        self.size = (TangramGame.SCALE * 4, TangramGame.SCALE * 4)

    def on_press(self):
        if self.the_app.current is not None:
            self.the_app.current.rot = str(int(self.the_app.current.rot) + 90)
            if self.the_app.current.rot == '360':
                self.the_app.current.rot = '0'
            self.the_app.current.set_shape()
        self.the_app.check_solution()


class TaskLayout(FloatLayout):
    name = ''
    pieces = []
    groups = []

    def __init__(self):
        print('__init__ TaskLayout')
        super(TaskLayout, self).__init__()
        self.pieces = []
        self.groups = []

    def reset(self, name):
        print('reset TaskLayout')
        self.name = name
        self.pieces = []
        self.groups = []
        self.canvas.clear()

    def set_background(self):
        print ('set_background TaskLayout')
        g = InstructionGroup()
        g.add(Color(0.1, 0.1, 0.1, 0.9))
        g.add(Rectangle(pos=[10*TangramGame.SCALE, 10*TangramGame.SCALE], size=[13*TangramGame.SCALE, 13*TangramGame.SCALE]))
        self.canvas.add(g)

    def game_task(self, task):
        print('game_task TaskLayout')
        self.pieces = task.pieces
        for p in self.pieces:
            p['pos'][0] += 13 * TangramGame.SCALE
            p['pos'][1] += 20 * TangramGame.SCALE


    def update_task(self):
        #rinat
        print ('update_task TaskLayout')
        for g in self.groups:
            self.canvas.remove(g)

        self.groups = []
        for p in self.pieces:
            self.groups.append(TangramPiece.get_shape(p, Color(0, 0, 0, 1)))
            self.canvas.add(self.groups[-1])


    def import_task(self, task):
        print(task.get_difficulty())
        for p in task.solution:
            self.pieces.append(TaskLayout.convert_piece(p))

    def import_json_task(self, json_str):
        # create a task from a json string and import it
        print("import_json_task", json_str)
        task = Task()
        task.create_from_json(json_str)
        self.import_task(task)


    @staticmethod
    def convert_piece(piece):
        pos = piece.name[2].split()
        #print("convert_piece before: ", pos)
        converted_piece = {'name': piece.name[0], 'rot': piece.name[1]}
        if 'small triangle' in converted_piece['name']:
            converted_piece['pos'] = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                      (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
        if 'medium triangle' in converted_piece['name']:
            if converted_piece['rot'] == '0':
                converted_piece['pos'] = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                          (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
            if converted_piece['rot'] == '90':
                converted_piece['pos'] = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                          (-2 * int(pos[0])) * TangramGame.SCALE]
            if converted_piece['rot'] == '180':
                converted_piece['pos'] = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                          (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
            if converted_piece['rot'] == '270':
                converted_piece['pos'] = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                          (-2 * int(pos[0])) * TangramGame.SCALE]
        if 'large triangle' in converted_piece['name']:
            converted_piece['pos'] = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                      (-2 * int(pos[0])) * TangramGame.SCALE]
        if 'square' in converted_piece['name']:
            converted_piece['pos'] = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                      (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
        if 'parrallelogram' in converted_piece['name']:
            if converted_piece['rot'] == '0':
                converted_piece['pos'] = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                          (-2 * int(pos[0])) * TangramGame.SCALE]
            if converted_piece['rot'] == '90':
                converted_piece['pos'] = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                          (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
            if converted_piece['rot'] == '180':
                converted_piece['pos'] = [(2 * int(pos[1]) + 1) * TangramGame.SCALE,
                                          (-2 * int(pos[0])) * TangramGame.SCALE]
            if converted_piece['rot'] == '270':
                converted_piece['pos'] = [(2 * int(pos[1]) + 2) * TangramGame.SCALE,
                                          (-2 * int(pos[0]) + 1) * TangramGame.SCALE]
        #print("convert_piece after: ", converted_piece['pos'])
        return converted_piece



class TangramGame:
    cog_tangram_selection = None
    SCALE = None
    window_size = []

    def __init__(self, parent_app):
        print ("TangramGame init")
        self.the_app = parent_app
        self.the_widget = GameWidget()
        self.pieces = {}
        self.task = TaskLayout()

        self.counter = 0
        self.clock = None

    def reset(self):
        the_layout = FloatLayout()

        # pieces
        self.pieces = {}
        for p in TangramPiece.tangram_list:
            self.pieces[p] = TangramPiece(self)
            self.pieces[p].name = p

        for key, value in self.pieces.items():
            value.init_position()
            value.set_shape()
            the_layout.add_widget(value)

        # task
        self.task = TaskLayout()
        self.task.reset('0')
        self.task.set_background()
        the_layout.add_widget(self.task)

        # button
        button_rotate = Rotate(self)
        button_rotate.size_hint_x = 0.1
        button_rotate.size_hint_y = 0.1
        button_rotate.pos = [15 * TangramGame.SCALE, 5 * TangramGame.SCALE]
        the_layout.add_widget(button_rotate)

        self.start_clock()

        # root layout
        self.the_widget.clear_widgets()
        self.the_widget.add_widget(the_layout)

    def is_selected(self):
        for k,p in self.pieces.items():
            if p.selected:
                return True
        return False

    def reset_sizes(self):
        for k, p in self.pieces.items():
            p.size = [TangramPiece.piece_size[p.name][0] * TangramGame.SCALE,
                      TangramPiece.piece_size[p.name][1] * TangramGame.SCALE]

    def show_game(self):
        self.task.canvas.ask_update()
        self.the_widget.canvas.ask_update()

    def export_task(self):
        # export current pieces to json string in Task format
        task_dict = {}
        task_dict['size']='5 5'
        task_dict['pieces']=[]

        for p in self.pieces:
            name = self.pieces[p].name
            rot = self.pieces[p].rot
            pos = [self.pieces[p].pos[0], self.pieces[p].pos[1]]

            # print 'pieces:'
            # print  [self.pieces[p].name, self.pieces[p].rot,self.pieces[p].pos[0], self.pieces[p].pos[1] ]

            pos[0] += -13 * TangramGame.SCALE
            pos[1] += -20 * TangramGame.SCALE

            if 'small triangle' in name:
                pos = [(-0.5 * (pos[1]/ TangramGame.SCALE - 1))-0.5, (0.5 * (pos[0]/ TangramGame.SCALE - 1))+0.5]
            elif 'medium triangle' in name:
                if rot == '0':
                    pos = [-0.5 * (pos[1]/ TangramGame.SCALE - 1)-1 , 0.5 * (pos[0]/ TangramGame.SCALE - 2)+1]
                elif rot == '90':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE)-1, 0.5 * (pos[0]/ TangramGame.SCALE - 1)+1]
                elif rot == '180':
                    pos = [-0.5 * (pos[1]/ TangramGame.SCALE - 1)-1, 0.5 * (pos[0]/ TangramGame.SCALE - 2)+1]
                elif rot == '270':
                    pos = [-0.5 * (pos[1]/ TangramGame.SCALE)-1 , 0.5 * (pos[0] / TangramGame.SCALE - 1)+1]
            elif 'large triangle' in name:
                pos = [-0.5 * (pos[1]/ TangramGame.SCALE)-1 , 0.5 * (pos[0]/ TangramGame.SCALE - 2)+1]
            elif 'square' in name:
                pos = [-0.5 * (pos[1]/ TangramGame.SCALE - 1)-0.5 , 0.5 * (pos[0]/ TangramGame.SCALE - 1)+0.5]
            elif 'parrallelogram' in name:
                if rot == '0':
                    pos = [-0.5 * (pos[1]/ TangramGame.SCALE) -1, 0.5 * (pos[0]/ TangramGame.SCALE - 1)+1]
                elif rot == '90':
                    pos = [-0.5 * (pos[1]/ TangramGame.SCALE - 1)-1 , 0.5 * (pos[0]/ TangramGame.SCALE - 2)+1]
                elif rot == '180':
                    pos = [-0.5 * (pos[1]/ TangramGame.SCALE)-1, 0.5 * (pos[0]/ TangramGame.SCALE - 1)+1]
                elif rot == '270':
                    pos = [-0.5 * (pos[1]/ TangramGame.SCALE - 1)-1, 0.5 * (pos[0]/ TangramGame.SCALE - 2)+1]
                    # print 'new pos:'
            #print [name, rot, pos]
            task_dict['pieces'].append((name, rot, str(pos[0])+' '+str(pos[1])))
        json_str = json.dumps(task_dict)
        # print json_str
        return json_str

    def check_solution(self):
        # json_str = self.export_task()
        # print json_str
        # temp_task = Task()
        # temp_task.create_from_json(json_str)
        # temp_task.print_me()
        # t1 = Task()
        # t1.create_from_json('{"1": ["small triangle1", "0", "0 0"], "0": ["square", "90", "1 2"], "size": "5 5"}')
        #
        # print temp_task.check_solution(t1.x, temp_task.solution)


        # TODO convert TaskSelection piece to Task pieces and compare actual coverage
        self.reset_sizes()
        for p in self.task.pieces:
            maybe_solution = False
            for k,piece in self.pieces.items():
                same_name = TangramPiece.only_shape(piece.name) == TangramPiece.only_shape(p['name'])
                same_rot = piece.rot == p['rot']
                same_position = round(piece.pos[0] + piece.size[0]/2) == p['pos'][0] and round(piece.pos[1] + piece.size[1]/2) == p['pos'][1]
                if same_name and same_rot and same_position:
                    maybe_solution = True
            if not maybe_solution:
                break
        if maybe_solution:
            print('Found solution')
            self.the_app.task_ended()

    def start_clock(self):
        self.counter = 60
        Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        if self.clock is not None:
            self.the_widget.canvas.remove(self.clock)
        self.clock = Ellipse(pos=(self.SCALE * 10, self.SCALE * 10),
                             size=(self.SCALE, self.SCALE),
                             angle_start = 0, angle_end = self.counter * 6)
        self.the_widget.canvas.add(self.clock)
        self.counter -= 1
        if self.counter <= 0:
            return False
        return True


class GameWidget(FloatLayout):

    def __init__(self):
        super(GameWidget, self).__init__()
        with self.canvas.before:
            self.rect = Rectangle(source='cg_background_img.jpg')
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size