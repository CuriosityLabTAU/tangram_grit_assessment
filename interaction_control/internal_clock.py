from component import *
from kivy.clock import Clock


class ClockComponent(Component):
    general_param = {'how_long': 20}

    def run_function(self, action):
        print(self.name, action)
        if action[0] == 'stop':
            self.stop()
        else:
            print(self.name, 'wait for ', self.general_param['how_long'], ' seconds')
            self.current_state = action[0]
            self.current_param = float(self.general_param['how_long'])
            Clock.schedule_once(self.prompt, self.current_param)

    def prompt(self, *args):
        print(self.name, 'prompt', self.current_state)
        self.current_state = 'prompt_' + self.current_state
        self.current_param = None

    def stop(self):
        print(self.name, 'stop')
        self.current_state = 'idle'
