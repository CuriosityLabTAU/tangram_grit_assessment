from interaction_control.component import *


class HourglassComponent(Component):

    the_clock = None

    def end_run(self):
        Clock.unschedule(self.event)
        Clock.unschedule(self.the_clock)

    def start(self):
        print(self.name, 'start')
        if not self.general_param:
            self.general_param = {'update_interval': 0.25, 'max_counter': 120}
        if 'update_interval' not in self.general_param:
            self.general_param['update_interval'] = 0.25
        else:
            self.general_param['update_interval'] = float(self.general_param['update_interval'])
        if 'max_counter' not in self.general_param:
            self.general_param['max_counter'] = 120
        else:
            self.general_param['max_counter'] = float(self.general_param['max_counter'])

        self.current_state = 'update'
        self.current_param = [self.general_param['max_counter'], self.general_param['max_counter']]
        self.the_clock = Clock.schedule_interval(self.update, self.general_param['update_interval'])

    def stop(self):
        print(self.name, 'stopped')
        self.current_state = 'idle'
        Clock.unschedule(self.the_clock)

    def update(self, dt):
        self.current_param[0] -= self.general_param['update_interval']

        if self.current_param[0] <= 0:
            self.current_state = 'finish'
            self.current_param[0] = 0
            return False

    def after_called(self):
        if self.current_state is not 'update':
            self.current_state = 'idle'
