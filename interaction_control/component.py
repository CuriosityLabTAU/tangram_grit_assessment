import sys
from functools import partial

from kivy.clock import Clock
is_logged = True
try:
    from kivy_communication import *
except:
    print('no logging')
    is_logged = False


class Component:
    def __init__(self, inter, name_in):
        self.interaction = inter
        self.actors = {}
        self.name = name_in
        self.current_state = 'idle'
        self.current_action = {}
        self.current_param = None
        self.general_param = None
        self.event = None

    def init_transitions(self):
        self.actors = {}
        self.current_state = 'idle'
        self.current_action = {}
        self.current_param = None
        self.general_param = None
        self.event = None

    def add_transition(self, state, target, fun, value, param=None):
        if state not in self.actors:
            self.actors[state] = {}
        if target not in self.actors[state]:
            self.actors[state][target] = {}
        self.actors[state][target][fun] = (value, param)

    def show(self):
        print(self.name, self.actors)

    def run(self):
        print(self.name, 'running ...')
        self.event = Clock.schedule_interval(self.resolve, 0.5)

    def end_run(self):
        Clock.unschedule(self.event)

    def resolve(self, *args):
        # print('resolve', self.name, self.current_state)
        self.current_action = {}
        if self.current_state != 'idle':
            called = False
            if self.current_state in self.actors:
                # check if end
                if 'interaction' in self.actors[self.current_state]:
                    if 'end' in self.actors[self.current_state]['interaction']:
                        self.end_interaction()
                        return False
                for target, funs in self.actors[self.current_state].items():
                    Q = []
                    for value in funs.values():
                        Q.append(float(value[0]))
                    selected_action = self.select_action(Q)
                    selected_function = funs.keys()[selected_action]
                    selected_param = funs.values()[selected_action][1]
                    self.current_action[target] = [selected_function, selected_param]

                # BIG CHANGE!!!
                for target,action in self.current_action.items():
                    if self.is_done(action):
                        self.current_state = 'idle'
                # ========

                for target,action in self.current_action.items():
                    if target != self.name:     # run own functions last
                        if action[1]:
                            action[1] = self.set_action1(action)

                        self.log_data(target=target, action=action)
                        self.interaction.components[target].schedule_running(action)
                        called = True
                if self.name in self.current_action.keys():
                    action = self.current_action[self.name]
                    if action[1]:
                        action[1] = self.set_action1(action)
                    self.log_data(action=action)
                    self.schedule_running(action)
                    called = True

                self.current_action = {}
            if called:
                self.after_called()

    def after_called(self):
        self.current_state = 'idle'

    def schedule_running(self, action):
        # self.run_function(action)
        Clock.schedule_once(lambda dt: self.run_function(action), 0.01)

    def run_function(self, action):
        if(action[0] != 'hourglass_update'):
            print("run_function ", self.name, action)
        try:
            if action[1] is not None:
                if len(action) == 2:
                    getattr(self, action[0])(action[1])
                else:
                    getattr(self, action[0])(action[1:])
            else:
                getattr(self, action[0])()
            return True
        except:
            print ("unexpected error:", action,sys.exc_info())
            print('No function: ', self.name, action)
        return False

    def is_done(self, action):
        if isinstance(action[1], list):
            for k in range(0, len(action[1])):
                if action[1][k] == 'done':
                    return True
        else:
            if action[1] == 'done':
                return True
        return False

    def select_action(self, Q):
        # winner takes all
        return Q.index(max(Q))

    def log_data(self, target=None, action=None):
        if is_logged:
            KL.log.insert(action=LogAction.data, obj=self.name, comment=[self.current_state, self.current_param, target, action])

    def set_action1(self, action):
        new_action1 = None
        if isinstance(action[1], list):
            for k in range(0, len(action[1])):
                if action[1][k] == 'x':
                    new_action1 = self.get_param()
                if action[1][k] == 'mark':
                    new_action1 = 'mark'
                if action[1][k] == 'done':
                    self.add_something('done')
        else:
            if action[1] == 'x':
                new_action1 = self.get_param()
            if action[1] == 'mark':
                new_action1 = 'mark'
            if action[1] == 'done':
                self.add_something('done')
        return new_action1

    def get_param(self):
        x = []
        if isinstance(self.current_param, list):
            if 'done' in self.current_param:
                x = self.current_param.remove('done')
            elif len(self.current_param) == 1:
                x = self.current_param[0]
            else:
                x = self.current_param
        else:
            x = self.current_param
        return x

    def add_something(self, something):
        if self.current_param:
            if isinstance(self.current_param, list):
                self.current_param.append(something)
            else:
                self.current_param = [self.current_param, something]
        else:
            self.current_param = [something]

    def end_interaction(self):
        print('end interaction, please work')
        Clock.unschedule(self.event)
        self.interaction.end_interaction()