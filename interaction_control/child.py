from component import *


class ChildComponent(Component):
    def run_function(self, action):
        if action[0] == 'action':
            self.on_action(action[1:][0])
        else:
            print(self.name, 'wait for ', action[0], action[1:])
            self.current_state = action[0]
            self.current_param = action[1:]

    def on_action(self, action):
        try:
            print(self.name, 'action ', action)
            self.current_state = action[0]
            self.current_param = action[1:]
        except:
            print ("child unexpected error:", action,sys.exc_info())
