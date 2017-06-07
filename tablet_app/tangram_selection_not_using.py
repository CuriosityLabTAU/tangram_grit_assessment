from tangram_game import *
from kivy.uix.gridlayout import GridLayout


class TangramSelection:

    def __init__(self, parent_app):
        self.the_app = parent_app
        self.the_widget = SelectionWidget()

        self.tasks = []     # array of Tasks

    def set_tasks(self, new_tasks):
        self.tasks = []
        for k in range(0, len(new_tasks)):
            ts = TaskSelection()
            ts.reset(str(k + 1))
            ts.the_app = self.the_app
            ts.import_task(new_tasks[k])
            ts.original_task = new_tasks[k]
            self.tasks.append(ts)
        for t in range(0, len(self.tasks)):
            self.tasks[t].correct_pos()

    def show_tasks(self):
        self.the_widget.clear_widgets()
        selection_layout = GridLayout(cols=3, rows=3)
        selection_layout.add_widget(BoxLayout())
        selection_layout.add_widget(BoxLayout())
        selection_layout.add_widget(BoxLayout())
        for t in self.tasks:
            t.update_task()
            selection_layout.add_widget(t)
        selection_layout.add_widget(BoxLayout())
        selection_layout.add_widget(BoxLayout())
        selection_layout.add_widget(BoxLayout())
        selection_layout.canvas.ask_update()
        self.the_widget.add_widget(selection_layout)
        print("end show_tasks")


class TaskSelection(Button, TaskLayout):
    the_app = None
    original_task = None

    def convert(self, task):
        self.name = task.name
        self.pieces = []
        for p in task.solution:
            self.pieces.append(TaskLayout.convert_piece(p))
        self.groups = []
        self.original_task = task

    def correct_pos(self):
        index = int(self.name) - 1
        print("correct_pos")
        print('index=',index)
        for p in self.pieces:
            print ("p=",p)
            print('pos[0]',p['pos'][0])
            print('pos[1]',p['pos'][1])
            print (p['pos'])
            p['pos'][0] += 10 + index * TangramGame.SCALE * 15
            t=TangramGame.window_size
            print(t)
            p['pos'][1] += round(TangramGame.window_size[1] / 2.2)

    def incorrect_pos(self):
        index = int(self.name) - 1
        for p in self.pieces:
            p['pos'][0] -= 8 + index * TangramGame.SCALE * 17
            p['pos'][1] -= round(TangramGame.window_size[1] / 2.2)

    def on_press(self, *args):
        super(Button, self).on_press()
        self.incorrect_pos()
        self.the_app.selected_task(self.original_task)

class SelectionWidget(FloatLayout):

    def __init__(self):
        super(SelectionWidget, self).__init__()
        with self.canvas.before:
            self.rect = Rectangle(source='cg_background_img.jpg')
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
