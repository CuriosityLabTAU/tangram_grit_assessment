import json
from random import choice
import time
from tablet_app.tangram_game import *

the_tts = None
try:
    from plyer import tts
    tts.speak('')
    the_tts = 'plyer'
except:
    pass

try:
    import pyttsx
    the_tts = 'pyttsx'
except:
    pass


class TextHandler:

    def __init__(self, condition='c-g-'):
        self.data = None
        self.condition = condition
        self.what = None
        self.question_index =0
        if the_tts is 'pyttsx':
            self.engine = pyttsx.init()
            self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Speech/Voices/Tokens/TTS_MS_EN-US_ZIRA_11.0')
            self.engine.connect(topic='finished-utterance', cb=self.finished)

    def load_text(self, filename='./tablet_app/robot_text_revised3.json'):
        with open(filename) as data_file:
            self.data = json.load(data_file)

    def finished(self):
        print('finished', self.what)
        return True

    def say(self, what):
        self.what = what
        if what in self.data:
            the_options = self.data[what]
            the_text = []
            if isinstance(the_options, list):
                if what=="ask_question_party":
                    if self.condition=='c+g-' or self.condition == 'c+g+':
                        the_text.append(the_options[0][0])
                else:
                    the_text.append(choice(the_options)[0])
            elif isinstance(the_options, dict):
                if what == "ask_question_robot_play":
                    self.question_index += 1
                    if self.condition=='c+g-' or self.condition == 'c+g+':
                        the_text.append(the_options['question'+str(self.question_index)][0])
                        print("the_text="+ the_options['question'+str(self.question_index)][0] + str(self.question_index))
                elif what == "my_turn":
                    print ("my turn","selection=",TangramGame.cog_tangram_selection,"text=",the_options[self.condition][TangramGame.cog_tangram_selection][0])
                    the_text.append(the_options[self.condition][TangramGame.cog_tangram_selection][0])
                else:
                    if 'all' in the_options:
                        the_text.append(choice(the_options['all'])[0])
                    if self.condition in the_options:
                        the_text.append(choice(the_options[self.condition])[0])

            print('speak: ', the_text)
            if the_tts is 'pyttsx':
                for txt in the_text:
                    self.engine.say(txt)
                self.engine.runAndWait()
                time.sleep(1)
            if the_tts is 'plyer':
                txt = ''
                for t in the_text:
                    txt += t
                tts.speak(txt)
                time.sleep(float(len(txt)) * 0.075)

            return self.finished()
        else:
            return False