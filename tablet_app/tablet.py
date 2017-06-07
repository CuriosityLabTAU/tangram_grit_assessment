from interaction_control.component import *


class TabletComponent(Component):
    hourglass_widget = None
    app = None

    def change_state(self, state):
        self.current_state = state

    def first_screen(self):
        print(self.name, 'first_screen')
        self.current_state = 'idle'
        self.app.first_screen()

    def party_screen(self):
        print(self.name, 'party_screen')
        self.current_state = 'idle'
        self.app.party_screen()

    def yes(self):
        print(self.name, 'yes in tablet')
        self.app.yes()
        self.current_state = 'yes'

        # self.current_state = "selection_screen_room"

    def wait(self):
        #print(self.name, 'wait')
        self.current_state = 'wait'

    def selection_screen(self, x):
        print(self.name, 'selection_screen', x)
        self.current_state = 'idle'
        self.current_param = x
        self.app.selection_screen(x)

    def select_treasure(self, x):
        print(self.name, 'select_treasure', x)
        self.current_state = 'idle'
        self.app.select_treasure(x)

    def tangram_screen(self, x):
        print(self.name, 'tangram_screen', x)
        self.app.tangram_screen(x)
        self.current_state = None
        self.current_param = x[0]


    def hourglass_update(self, x):
        # print(self.name, 'hourglass update', x)
        # print ("self.hourglass_widget", self.hourglass_widget)
        if self.hourglass_widget:
            self.hourglass_widget.update_hourglass(x)

    def change_pieces(self, x):
        print(self.name, 'change_pieces', self.current_param, x)
        self.current_state = 'idle'
        self.current_param = x
        self.app.change_pieces(self.current_param)

    def solved(self, x):
        print(self.name, 'solved', x)
        self.current_state = 'solved'
        self.current_param = x
        self.app.solved()

    def not_solved(self,x):
        print(self.name, 'not_solved',x)
        self.current_state = 'not_solved'
        self.current_param = x

    def robot_solve(self, x):
        print(self.name, 'robot solve', x)
        self.app.robot_solve(x)

    def finish(self, x):
        print(self.name, 'finish', x)
        self.current_state = 'finish'
        self.app.finish()

    def disable_tablet(self):
        print(self.name, 'disable tablet')
        self.app.disable_tablet()
        self.current_state = 'disable_tablet'

    def enable_tablet(self):
        print(self.name, 'enable tablet')
        self.app.enable_tablet()
        self.current_state = 'enable_tablet'