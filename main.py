from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, BooleanProperty, DictProperty)
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.graphics import Line, Rectangle, Color, Ellipse
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from random import randint, random, choice, choices, sample
import string
from copy import copy, deepcopy
from functools import partial
from kivy.config import Config
import events
from onboarding import onboarding_wizard
from logger import Logger
        

Config.set('graphics', 'allow_screensaver', '0')
Config.write()

class ScreenManager(ScreenManager):
    turn = Clock
    # Hardcode parameters
    rules_objects = ListProperty(['Шнурок', 'Червяк', "Резинка", "Наперсток", "Вилка", "Ковид", "Бусина", "Перчик", "Прищепка", "Головоломка"])
    key_object = 'Шарик'
    test_mode = BooleanProperty(False)
    infinite_test_mode = BooleanProperty(False)
    confirm_events = BooleanProperty(False)
    onboarding_mode = BooleanProperty(True)
    
    # Variables with game rules
    start_turn_length = NumericProperty(0)
    end_turn_length = NumericProperty(0)
    rules_players = ListProperty()
    rules_player_names = ListProperty()
    rules_game_mode = ObjectProperty('beginner')
    
    # Game state variables
    game_results = DictProperty()
    eliminated_players = ListProperty([])
    turn_turn_length = NumericProperty(5.)    
    turn_player = NumericProperty(0)
    turn_player_name = ObjectProperty('')
    turn_object = ObjectProperty('')
    turn_added_seconds = NumericProperty(0)
    turn_seconds_left = NumericProperty(0)
    turn_progress_bar_value = NumericProperty(100)
    previous_turn_object = ObjectProperty('')
    turn_round = NumericProperty(1)
    turn_rotation = 1
    paused = NumericProperty(0)    
    get_event_chance = NumericProperty(0)
    drop_event_chance = NumericProperty(0.)
    other_event_chance = NumericProperty(0.)
    get_midgame_event_chance = NumericProperty(0.)
    strategic_event_chance = NumericProperty(0.)
    turn_additional_seconds = NumericProperty(0)
    heart_slow_sound = SoundLoader.load('Sounds/heartbeat_slow.wav')
    heart_norm_sound = SoundLoader.load('Sounds/heartbeat_normal.wav')
    heart_fast_sound = SoundLoader.load('Sounds/heartbeat_fast.wav')
    end_turn_sound = SoundLoader.load('Sounds/end_turn.wav')    
    eliminate_sound = SoundLoader.load('Sounds/eliminate.wav')    
    win_sound = SoundLoader.load('Sounds/win.wav')  
    
    # Object image sources
    img_source = "ObjectImages/JPGs/golovolomka.jpg"
    img_golovolomka_green = "ObjectImages/JPGs/golovolomka_green.jpg"
    img_golovolomka_red = "ObjectImages/JPGs/golovolomka_red.jpg"
    img_busina_green = "ObjectImages/JPGs/busina_green.jpg"
    img_busina_red = "ObjectImages/JPGs/busina_red.jpg"
    img_list_green = "ObjectImages/JPGs/list_green.jpg"
    img_list_red = "ObjectImages/JPGs/list_red.jpg"
    img_pero_green = "ObjectImages/JPGs/pero_green.jpg"
    img_pero_red = "ObjectImages/JPGs/pero_red.jpg"
    img_covid_green = "ObjectImages/JPGs/covid_big_green.jpg"
    img_covid_red = "ObjectImages/JPGs/covid_big_red.jpg"
    img_naperstok_green = "ObjectImages/JPGs/naperstok_green.jpg"
    img_naperstok_red = "ObjectImages/JPGs/naperstok_red.jpg"
    img_plastilin_green = "ObjectImages/JPGs/plastilin_green.jpg"
    img_plastilin_red = "ObjectImages/JPGs/plastilin_red.jpg"
    img_poloska_green = "ObjectImages/JPGs/poloska_green.jpg"
    img_poloska_red = "ObjectImages/JPGs/poloska_red.jpg"
    img_rezinka_green = "ObjectImages/JPGs/rezinka_green.jpg"
    img_rezinka_red = "ObjectImages/JPGs/rezinka_red.jpg"
    img_sharik_green = "ObjectImages/JPGs/sharik_green.jpg"
    img_sharik_red = "ObjectImages/JPGs/sharik_red.jpg"
    img_shnurok_green = "ObjectImages/JPGs/shnurok_green.jpg"
    img_shnurok_red = "ObjectImages/JPGs/shnurok_red.jpg"
    img_vilka_green = "ObjectImages/JPGs/vilka_green.jpg"
    img_vilka_red = "ObjectImages/JPGs/vilka_red.jpg"
    
    objects_dict = {'Шнурок' : 'shnurok',
                  'Червяк' : 'poloska',
                  "Резинка" : 'rezinka',
                  "Наперсток" : 'naperstok',
                  "Вилка" : 'vilka',
                  "Ковид" : 'covid_big',
                  "Лист" : 'list',
                  "Перчик" : 'perchik',
                  "Прищепка" : 'prischepka',
                  "Перо" : 'pero',
                  'key': 'sharik'}
    
    # Tech variables
    event_choice_hidden = False
    stats_game_id = NumericProperty(0)
    strategic_pool = ListProperty()
    randomize_game_mode = ObjectProperty(False)
    timer_tick = 0.1
    end_game_check = False
    round_counter = 1
    is_win_test_give_2 = False
    is_win_test_drop_keys = False
    master_round = False
    window_sizes = (414, 736)
    Window.size = window_sizes
    
    # Game modes
    get_key_probability = {'onboarding' : 0.15,
                           'beginner' : 0.15,
                           'fun' : 0.12,
                           'master' : 0.1}
    
    ## Get, Drop, Other, Midgame, Strategic
    event_group_probability = { 'onboarding' : [0.02, 0.02, 0.01, 0, 0],
                                'beginner' : [0.02, 0.02, 0.01, 0, 0],
                                'fun' : [0.012, 0.01, 0.015, 0.007, 0.007],
                                'master' : [0.015, 0.01, 0.015, 0.007, 0.007]}
    
    event_group_composition = {'full':    [[events.event_get_3, events.event_get_rotate, events.event_all_get_1, events.event_get_2,                                               events.event_all_get_key],
                                           [events.event_drop_3, events.event_drop_object, events.event_drop_key_object, events.event_all_drop_1],
                                           [(events.event_switch_hands, ''), (events.event_give_1, 'right'), (events.event_give_1, 'left'), (events.event_give_1, 'any'), events.event_steal_key],
                                           [events.event_get_key_min_num_cards, events.event_get_key_max_num_cards, events.event_get_key_object],
                                           [events.event_get_key_object_delayed, events.event_drop_key_object_delayed]],
#                               'onboarding':
#                                          [[events.event_get_3, events.event_get_rotate, events.event_all_get_1],
#                                           [events.event_drop_3, events.event_drop_object],
#                                           [(events.event_switch_hands, '')],
#                                           [],
#                                           []],
                               'beginner':
                                          [[events.event_get_3, events.event_get_rotate, events.event_all_get_1],
                                           [events.event_drop_3, events.event_drop_object],
                                           [(events.event_switch_hands, '')],
                                           [],
                                           []],
                               'fun':
                                          [[events.event_get_3, events.event_get_rotate, events.event_all_get_1, events.event_get_2],
                                           [events.event_drop_3, events.event_drop_object, events.event_drop_key_object],
                                           [(events.event_switch_hands, ''), (events.event_steal_key, ''), (events.event_steal_key, ''), [events.event_give_1, 'any'], [events.event_give_1, 'any'], [events.event_exchange_hands_with_player, 'red'], [events.event_exchange_hands_with_player, 'green']],
                                           [events.event_get_key_min_num_cards, events.event_get_key_max_num_cards, events.event_get_key_object],
                                           [events.event_get_key_object_delayed, events.event_drop_key_object_delayed]],
                               'master': [[events.event_get_3, events.event_get_rotate, events.event_all_get_1, events.event_get_2,                   events.event_all_get_1, events.event_get_2],
                                           [events.event_drop_3, events.event_drop_object, events.event_drop_key_object],
                                            [(events.event_switch_hands, ''), (events.event_steal_key, ''), (events.event_steal_key, ''), [events.event_give_1, 'any'], [events.event_give_1, 'any'], [events.event_exchange_hands_with_player, 'red'], [events.event_exchange_hands_with_player, 'green']],
                                           [events.event_get_key_min_num_cards, events.event_get_key_max_num_cards, events.event_get_key_object],
                                           [events.event_get_key_object_delayed, events.event_drop_key_object_delayed]]}
    
    # Initiate logger
    log = Logger()
    
    # Skip objects choice screen
    #rules_objects = basic_objects
    
    # Change screen color
#    Window.clearcolor = (1, 1, 1, 1)
    
    def calculate_objects_on_hand(self, player, object_type = 'all'):
        """
        Types: green, red, key, all
        """        
        if object_type == 'green':
            objects = self.log.green_objects + ['key_green']
        elif object_type == 'red':
            objects = self.log.red_objects + ['key_red']
        elif self.test_mode == False:
            return None
        elif object_type == 'key':
            objects = ['key_green', 'key_red', 'key_black']
        elif object_type == 'all':
            objects = self.log.green_objects + self.log.red_objects + ['key_green', 'key_red', 'key_black', 'random_black']
        return sum([self.log.game_results[player][frm] for frm in objects])        
    
    def calculate_key_chance(self):
        base_chance = self.get_key_probability[self.rules_game_mode]
#        max_keys_on_hand = max([self.calculate_objects_on_hand(i, 'key') for i in self.rules_players if i not in self.eliminated_players])
#        min_keys_on_hand = min([self.calculate_objects_on_hand(i, 'key') for i in self.rules_players if i not in self.eliminated_players])
#        advantage = (self.calculate_objects_on_hand(self.turn_player, 'key') - min_keys_on_hand)
#        disadvantage = (max_keys_on_hand - self.calculate_objects_on_hand(self.turn_player, 'key'))

#        if (self.calculate_objects_on_hand(self.turn_player, 'key') >= 3) and (self.turn_round < 12):
#            # No chance if not enough cards on hand
#            key_chance = 0
#        else:
        key_chance = base_chance * (max(7, self.turn_round) / 7)# * game_speed_modifier
        return key_chance
    
    def calculate_green_chance(self):
        greens_on_hand = self.calculate_objects_on_hand(self.turn_player, 'green')
        reds_on_hand = self.calculate_objects_on_hand(self.turn_player, 'red')
        green_chance = 0.5 - 0.2 * (greens_on_hand - reds_on_hand)
        return green_chance
    
    ######## EVENTS
    def toggle_widget(self, wid, dohide = False):
        if dohide == False:
            wid.opacity = 1
            wid.disabled = False
#            del wid.saved_attrs
        elif dohide == True:
            wid.opacity = 0
            wid.disabled = True        
            
    def show_event_choice_buttons(self, choices = 4, event_confirm = False, round_confirm = False, round_change = False):
        def show_turn_text(*args):
            self.get_screen('game').ids['up_turn_text'].font_size = '22sp'
            self.get_screen('game').ids['down_turn_text'].font_size = '22sp'
        
        # Round change in master - no confirmation        
        self.pause_resume() #Pause game
        # Hide pause button
        self.get_screen('game').ids['pause_button'].disabled = True
        self.get_screen('game').ids['pause_button'].opacity = 0        
        self.get_screen('game').ids['next_turn_button'].disabled = True
        self.get_screen('game').ids['next_turn_button'].opacity = 0
        
        for i in range(choices):
            self.get_screen('game').ids['event_button'+str(i+1)].disabled = False
        self.toggle_widget(self.get_screen('game').ids.event_choice_buttons, dohide = False)
        self.get_screen('game').ids.event_choice_pie.canvas.add(Color(0.173, 0.243, 0.314, 1))
        self.get_screen('game').ids.event_choice_pie.canvas.add(Ellipse(pos =  (self.width * 0.5 - self.height * 0.2,
                                                                                self.height * 0.3),
                                                                        size = (self.height * 0.4,
                                                                                self.height * 0.4),
                                                                        angle_start = -90,
                                                                        angle_end = -90 + choices * 90))

        if round_change:
            self.pause_resume() #Pause game
            self.get_screen('game').ids['up_turn_text'].font_size = '1sp'
            self.get_screen('game').ids['down_turn_text'].font_size = '1sp'
            self.turn_seconds_left = 2
            self.master_round = True
            for i in [1, 2, 3, 4]:
                event_callback = show_turn_text
                self.get_screen('game').ids['event_button'+str(i)]._cb.append(event_callback)
                self.get_screen('game').ids['event_button'+str(i)].fbind('on_press', event_callback)
            
            confirm_text = '[color=#FFFFFF]Раунд ' + str(self.turn_round) +'[/color]'
            label_up = Label(text = confirm_text, markup = True, font_size = '30sp',
                              text_size = (self.height * 0.38 * 0.7, None), 
                              halign = 'center', valign = 'top')
            label_down = Label(text = confirm_text, markup = True, font_size = '30sp',
                              text_size = (self.height * 0.38 * 0.7, None), 
                              halign = 'center', valign = 'top')
            self.get_screen('game').ids.middle_text_up.add_widget(label_up)
            self.get_screen('game').ids.middle_text_down.add_widget(label_down)   
            
            if self.test_mode:
                self.get_screen('game').ids['event_button1'].trigger_action(0)            
        
        elif event_confirm:
            confirm_text = '[color=#FFFFFF]Прочитайте задание и нажмите в центр экрана, чтобы запустить таймер[/color]' 
            label_up = Label(text = confirm_text, markup = True, font_size = '16sp',
                              text_size = (self.height * 0.38 * 0.7, None), 
                              halign = 'center', valign = 'top')
            label_down = Label(text = confirm_text, markup = True, font_size = '16sp',
                              text_size = (self.height * 0.38 * 0.7, None), 
                              halign = 'center', valign = 'top')
            self.get_screen('game').ids.middle_text_up.add_widget(label_up)
            self.get_screen('game').ids.middle_text_down.add_widget(label_down)    
            
            if self.test_mode:
                self.get_screen('game').ids['event_button1'].trigger_action(0)

        elif round_confirm:
            self.get_screen('game').ids['up_turn_text'].font_size = '1sp'
            self.get_screen('game').ids['down_turn_text'].font_size = '1sp'
            for i in [1, 2, 3, 4]:
                event_callback = show_turn_text
                self.get_screen('game').ids['event_button'+str(i)]._cb.append(event_callback)
                self.get_screen('game').ids['event_button'+str(i)].fbind('on_press', event_callback)
            
            confirm_text = '[color=#FFFFFF]Раунд ' + str(self.turn_round) + '\n Нажмите в центр экрана, чтобы запустить таймер[/color]'
            label_up = Label(text = confirm_text, markup = True, font_size = '16sp',
                              text_size = (self.height * 0.38 * 0.7, None), 
                              halign = 'center', valign = 'top')
            label_down = Label(text = confirm_text, markup = True, font_size = '16sp',
                              text_size = (self.height * 0.38 * 0.7, None), 
                              halign = 'center', valign = 'top')
            self.get_screen('game').ids.middle_text_up.add_widget(label_up)
            self.get_screen('game').ids.middle_text_down.add_widget(label_down)   
            
            if self.test_mode:
                self.get_screen('game').ids['event_button1'].trigger_action(0)  

        else:
            self.get_screen('game').ids.event_choice_pie.canvas.add(Color(0.925, 0.941, 0.945, 1))
            self.get_screen('game').ids.event_choice_pie.canvas.add(
                Line(points = (self.width / 2 - self.height * 0.4 * 0.7,
                               self.height / 2,
                               self.width / 2 + self.height * 0.4 * 0.7, 
                               self.height / 2),
                     width = self.width / 100))        
            self.get_screen('game').ids.event_choice_pie.canvas.add(
                Line(points = (self.width / 2,
                               self.height * 0.3 + self.height * 0.005, 
                               self.width / 2,
                               self.height * 0.7 - self.height * 0.005),
                     width = self.width / 100))              
            
    def reset_event_choice_buttons(self, *args):                
        buttons = [self.get_screen('game').ids['event_button1'],
                   self.get_screen('game').ids['event_button2'],
                   self.get_screen('game').ids['event_button3'],
                   self.get_screen('game').ids['event_button4']]

        for btn in buttons:
            btn.text = ''
            btn.disabled = True
            for cb in btn._cb:
                btn.funbind('on_press', cb)
                btn._cb = []

        self.toggle_widget(self.get_screen('game').ids.event_choice_buttons, dohide = True)
        self.get_screen('game').ids.event_choice_pie.canvas.clear()
        self.get_screen('game').ids.event_choice_pie.clear_widgets()
        self.get_screen('game').ids.middle_text_up.clear_widgets()
        self.get_screen('game').ids.middle_text_down.clear_widgets()

        if self.paused == 1:
            self.pause_resume()
    
    def calculate_event_occurance(self):
        egp = self.event_group_probability[self.rules_game_mode]
        if (random() < self.get_event_chance):
            self.get_event_chance = 0.
            for i in self.rules_players:
                if i not in self.eliminated_players:
                    self.log.game_results[i]['get_events'] += 1
            etype = 'get'
        elif (random() < self.get_midgame_event_chance) & (self.turn_round >= 7):
            self.get_midgame_event_chance = 0.
            for i in self.rules_players:
                if i not in self.eliminated_players:
                    self.log.game_results[i]['get_midgame_events'] += 1
            etype = 'get_midgame'  
        elif (random() < self.strategic_event_chance) & (self.turn_round >= 6):
            self.strategic_event_chance = 0.
            for i in self.rules_players:
                if i not in self.eliminated_players:
                    self.log.game_results[i]['strategic_events'] += 1
            etype = 'strategic'              
        elif (random() < self.drop_event_chance) & (self.turn_round >= 3):
            self.drop_event_chance = 0.
            for i in self.rules_players:
                if i not in self.eliminated_players:
                    self.log.game_results[i]['drop_events'] += 1
            etype = 'drop'       
        elif (random() < self.other_event_chance) & (self.turn_round >= 5):
            self.other_event_chance = 0.
            for i in self.rules_players:
                if i not in self.eliminated_players:
                    self.log.game_results[i]['other_events'] += 1
            etype = 'other'
        else:
            etype = 'none'
        self.get_event_chance += egp[0]
        self.drop_event_chance += egp[1]
        self.other_event_chance += egp[2]
        self.get_midgame_event_chance += egp[3]
        self.strategic_event_chance += egp[4]
        return etype
                               
    def event(self, etype):
        egc = self.event_group_composition[self.rules_game_mode]
        if etype == 'get':       
            choice(egc[0])(self)
        elif etype == 'drop':
            choice(egc[1])(self) 
        elif etype == 'other':
            chc = choice(egc[2])
            chc[0](self, chc[1])
        elif etype == 'get_midgame':
            choice(egc[3])(self)
        elif etype == 'strategic':
            choice(egc[4])(self)
    
    def random_card_object_color(self):
        # define card object
        card_object = self.rules_objects[randint(0, len(self.rules_objects) - 1)]
        # define card color
        if random() < self.calculate_green_chance():
            card_color_text = 'зеленый'
            card_color = '[color=#27ae60]'
            card_color_key = '_green'
        else:
            card_color_text = 'красный'
            card_color = '[color=#e74c3c]'
            card_color_key = '_red'   
        return  card_object, card_color, card_color_text, card_color_key
        
    def take_card(self, card_type = 'any'):
        if ((random() < self.calculate_key_chance()) or card_type == 'key') and card_type != 'basic':
            card_object, card_color, card_color_text, card_color_key = self.random_card_object_color()
            self.turn_object = 'Возьми [b]' + card_color + self.key_object.upper() + '[/color][/b]'
            card_object = 'key'
        else:
            self.previous_turn_object = self.turn_object  
            while self.turn_object == self.previous_turn_object:
                card_object, card_color, card_color_text, card_color_key = self.random_card_object_color()
                self.turn_object = 'Возьми [b]' +  card_color + card_object.upper() + '[/color][/b]'                            
        # store card
        self.img_source = "ObjectImages/JPGs/" + self.objects_dict[card_object] + card_color_key + ".jpg"                
        self.get_screen('game').ids.object_image.canvas.add(Ellipse(source  = self.img_source,  
                                                                    pos = (self.width * 0.5 - self.height * 0.2,
                                                                           self.height * 0.3),
                                                                    size = (self.height * 0.4,
                                                                            self.height * 0.4)))
        self.log.append_event(self.turn_round, self.turn_player, self.rules_player_names[self.turn_player - 1], 'turn_get', card_object + card_color_key, self.test_mode)
        self.log.game_results[self.turn_player][card_object + card_color_key] += 1
        self.log.game_results[self.turn_player]['actions'] += 1
    
    def update_progress_bar(self):
        self.turn_progress_bar_value = self.turn_seconds_left / max(1, self.turn_turn_length + self.turn_additional_seconds)
    
    
    def start_game(self):
        # Initialize logger to collect game events
        if self.randomize_game_mode:
            self.rules_game_mode = choice(['beginner', 'fun', 'master'])
        self.log.reset_game_results(rules_players = self.rules_players, rules_objects = self.rules_objects, game_mode = self.rules_game_mode)
                
        # Randomize first player
        def rotate(l, n):
            return l[n:] + l[:n]
        self.rules_player_names = rotate(self.rules_player_names, randint(0, len(self.rules_player_names)))
        
        #Starting parameters
        self.turn_player = 1
        self.turn_player_name = self.rules_player_names[self.turn_player - 1]
        self.eliminated_players = []
        self.turn_turn_length = self.start_turn_length
        self.turn_seconds_left = self.turn_turn_length
        self.strategic_pool = []
        self.turn_progress_bar_value = 1
        self.turn_round = 1
        self.round_counter = 1
        self.turn_rotation = 1
        self.end_game_check = 0
        self.event_chance = 0
        self.reset_event_choice_buttons()
        self.get_screen('game').ids.object_image.canvas.clear()
        self.get_screen('game').ids.event_choice_pie.canvas.clear()        
        
        #Reset event chances
        self.get_event_chance, self.drop_event_chance, self.other_event_chance, self.get_midgame_event_chance, self.strategic_event_chance = self.event_group_probability[self.rules_game_mode]
        
        # Fast forward in test mode
        if self.test_mode == True:
            self.schedule_time = 0.001
        else:
            self.schedule_time = self.timer_tick
        
        # Bind win function
        self.get_screen('game').ids['win_test_button'].text = '[color=#2c3e50]Улететь[/color]'
        self.get_screen('game').ids['win_test_button']._cb.append(self.win_test)
        self.get_screen('game').ids['win_test_button'].fbind('on_press', self.win_test)
        
        #Schedule timer
        self.turn.schedule_interval(self.call_next, self.schedule_time)   
        
        #Start with first action        
        if self.rules_game_mode == 'master':
            events.event_get_3_warmup(self)         
        elif self.rules_game_mode == 'onboarding':
            self.onboarding = onboarding_wizard(len(self.rules_players))
            next_step = self.onboarding.next_turn()
            eval(next_step)
        else:
            self.take_card()               
    
    def call_next(self, dt):   
        self.update_progress_bar()        
        if self.turn_seconds_left <= 0:         
            self.turn_additional_seconds = 0            
            
            # Calculate next player
            if (self.turn_player == len(self.rules_players)) & (self.turn_rotation == 1):
                next_player = 1
            elif (self.turn_player == 1) & (self.turn_rotation == -1):
                next_player = len(self.rules_players)                        
            else:
                next_player = self.turn_player + self.turn_rotation
            
            # Check if win condition achieved
            if self.end_game_check:
#            if self.turn_player == 2:
                self.end_game_check_f()
    
            # Check next player for round confirm
            elif (self.round_counter == len(self.rules_players)) and (self.rules_game_mode != 'master'):
                self.turn_round += 1    
                self.round_counter = 0
                self.get_screen('game').ids.object_image.canvas.clear()                                        
                self.show_event_choice_buttons(round_confirm = True)
                self.turn_turn_length = min (self.turn_turn_length + 0.2, self.end_turn_length)   
                for i in self.log.game_results.keys():
                    self.log.game_results[i]['max_round'] = self.turn_round 
#                self.round_changed = True

            elif (self.round_counter == len(self.rules_players)) and (self.rules_game_mode == 'master'):
                self.turn_round += 1    
                self.round_counter = 0
                self.get_screen('game').ids.object_image.canvas.clear()                                        
                self.show_event_choice_buttons(round_change = True)
                self.turn_turn_length = min (self.turn_turn_length + 0.2, self.end_turn_length)   
                for i in self.log.game_results.keys():
                    self.log.game_results[i]['max_round'] = self.turn_round 
#                self.round_changed = True

            elif (self.master_round == True) and (self.rules_game_mode == 'master'):
                self.get_screen('game').ids['event_button1'].trigger_action(0)
                self.master_round = False
                                        
            else:   
                # Show next turn button
                self.get_screen('game').ids['next_turn_button'].disabled = False
                self.get_screen('game').ids['next_turn_button'].opacity = 1
                
                # Change player and turn player name                
                self.turn_player = next_player
                self.turn_player_name = self.rules_player_names[self.turn_player - 1] 
#                self.round_changed = False
                self.round_counter += 1
                
                # Refresh turn seconds, progress bar and eliminate button, object image
#                self.get_screen('game').ids.eliminate_button.disabled = True
                self.get_screen('game').ids.object_image.canvas.clear()
                self.turn_seconds_left = self.turn_turn_length

                # Check win condition in test mode
                if (self.test_mode) and (self.calculate_objects_on_hand(self.turn_player, 'key') >= 4):
                    self.win_test()
                else:
                    # Calculate action    
                    ## Check for strategic event from pool
                    if self.rules_game_mode == 'onboarding':     
                        # Print game info             
                        print([str(self.calculate_objects_on_hand(i, 'all')) + '/' + str(self.calculate_objects_on_hand(i, 'key')) for i in self.rules_players])

                        next_step = self.onboarding.next_turn()
                        eval(next_step)
                    else:
                        pass_action = False
                        for i in self.strategic_pool[:]:
                            if self.turn_round > i[0]:
                                i[2]()
                                pass_action = True
                                self.strategic_pool.remove(i)
                                break
                            elif (self.turn_round == i[0]) and (self.turn_player >= i[1]):
                                i[2]()
                                pass_action = True
                                self.strategic_pool.remove(i)
                                break
                        if pass_action == False:
                            turn_event = self.calculate_event_occurance()
                            if turn_event != 'none':
                                self.event(etype = turn_event)
                            else:
                                self.take_card()                
                    
                    #Drop key in test mode                    
                    if self.test_mode == True:
                        is_failed = random() < (self.calculate_objects_on_hand(self.turn_player, 'all') - 5) * 0.05
                        if (is_failed) and (self.calculate_objects_on_hand(self.turn_player, 'key') > 0):                
                            self.log.add_object(self.turn_player, 'key_black', -1)
                        if (self.calculate_objects_on_hand(self.turn_player, 'all') > 12):
                            self.log.add_object(self.turn_player, 'random_black', -4)  
                            self.log.add_object(self.turn_player, 'key_black', 1)  
#                        elif (is_failed) and (self.calculate_objects_on_hand(self.turn_player, 'key') == 0):
#                            self.log.add_object(self.turn_player, 'random_black', 2)
            
        elif self.turn_seconds_left in [1, 2]:
            self.heart_fast_sound.play()
            self.turn_seconds_left = round(self.turn_seconds_left-self.timer_tick, 1)
        
        elif self.turn_seconds_left in [3, 4]:

            self.heart_norm_sound.play()
            self.turn_seconds_left = round(self.turn_seconds_left-self.timer_tick, 1)
        
        elif (self.turn_seconds_left % 1 == 0) and (self.turn_seconds_left >= 5):
            self.heart_slow_sound.play()
            self.turn_seconds_left = round(self.turn_seconds_left-self.timer_tick, 1)
                
        elif self.turn_seconds_left == 0.4:
            self.end_turn_sound.play() 
            self.turn_seconds_left = round(self.turn_seconds_left-self.timer_tick, 1) 
            
        else:
            self.turn_seconds_left = round(self.turn_seconds_left-self.timer_tick, 1)
        
    def pause_resume(self, do_pause = False):
        if (self.paused == 0) or do_pause:
            self.turn.unschedule(self.call_next)
            self.paused = 1
            self.get_screen('game').ids.pause_button.text = '[color=#2c3e50]Дальше[/color]'
        else:
            self.turn.schedule_interval(self.call_next, self.schedule_time)
            self.paused = 0
            self.get_screen('game').ids.pause_button.text = '[color=#2c3e50]Пауза[/color]'
    
    def restart(self, *args):
        if self.paused == 1:
            self.paused = 0
        self.turn.unschedule(self.call_next)
        self.end_game_check = False
        self.turn_player = 1
        self.log.save_game_results()
        self.current = "define_players"
    
    def next_turn(self):
        self.turn_seconds_left = 1
        
    def eliminate_player(self):
        pass
#        self.eliminated_players.append(self.turn_player)
#        if self.test_mode == False: 
#            self.turn_seconds_left = 2
#        self.update_progress_bar()        
#        self.log.game_results[self.turn_player]['eliminated_at'] = self.turn_round
#        self.log.append_event(self.turn_round, self.turn_player, 'eliminated', '', self.test_mode)
#        self.eliminate_sound.play()
#        self.get_screen('game').ids.eliminate_button.disabled = True
        
    def test_f1(self):
#        random.choice(random.choice(event_group_composition))
        self.get_screen('game').ids.object_image.canvas.clear()
        events.event_switch_hands(self)
        
    def test_f2(self):
        self.get_screen('game').ids.object_image.canvas.clear()
        events.event_steal_key(self)
        
    def test_f3(self):
        self.turn_seconds_left = 1
#         print(self.get_screen('game').ids.event_buttons.size_hint_y)
#        events.event_get_key_object(self)

    def reset_win_test_button(self, *args):
        self.get_screen('game').ids['win_test_button'].text = 'Win Test'
        for cb in self.get_screen('game').ids['win_test_button']._cb:
            self.get_screen('game').ids['win_test_button'].funbind('on_press', cb)
            self.get_screen('game').ids['win_test_button']._cb = []

    def win_test(self, *args):
        # Clear current turn
        self.turn_seconds_left = self.turn_turn_length
        self.get_screen('game').ids.object_image.canvas.clear()
        self.get_screen('game').ids['event_button1'].trigger_action(0)        
                        
        ## Unbind win function
        for cb in self.get_screen('game').ids['win_test_button']._cb:
            self.get_screen('game').ids['win_test_button'].funbind('on_press', cb)
            self.get_screen('game').ids['win_test_button']._cb = []
            
        # Bind cancel function
        self.get_screen('game').ids['win_test_button'].text = '[color=#2c3e50]Отменить[/color]'
        self.get_screen('game').ids['win_test_button']._cb.append(self.cancel_win_test)
        self.get_screen('game').ids['win_test_button'].fbind('on_press', self.cancel_win_test)
        
        if self.turn_round >= 16:
            events.event_win_test_drop_keys(self)
            self.is_win_test_drop_keys = True
        elif self.turn_round >= 10:
            events.event_win_test_switch_hands(self)
        else:
            events.event_win_test_give_2(self)
            self.is_win_test_give_2 = True
        self.update_progress_bar()  
        self.end_game_check = True
        
    def cancel_win_test(self, *args):           
        self.end_game_check = False
        self.get_screen('game').ids['event_button3'].trigger_action(0)     
        self.turn_seconds_left = self.turn_turn_length
        self.turn_additional_seconds = 0
        self.update_progress_bar()
        if self.is_win_test_give_2:
            self.turn_object = 'Сбрось ' + self.key_object.upper() +' или возьми красное и зеленое существо. Сбрось все существа, полученные от других игроков.'
            self.is_win_test_give_2 = False
        if self.is_win_test_drop_keys:
            self.turn_object = 'Возьми все ШАРИКИ, которые сбросил. Сбрось ' + self.key_object.upper() +' или возьми красное и зеленое существо.'
            self.is_win_test_drop_keys = False
        else:    
            self.turn_object = 'Сбрось ' + self.key_object.upper() +' или возьми красное и зеленое существо'
        
        # Unbind cancel function
        for cb in self.get_screen('game').ids['win_test_button']._cb:
            self.get_screen('game').ids['win_test_button'].funbind('on_press', cb)
            self.get_screen('game').ids['win_test_button']._cb = []                
        
        # Bind win function
        self.get_screen('game').ids['win_test_button'].text = '[color=#2c3e50]Улететь[/color]'
        self.get_screen('game').ids['win_test_button']._cb.append(self.win_test)
        self.get_screen('game').ids['win_test_button'].fbind('on_press', self.win_test)
        
        if self.test_mode:
            if self.calculate_objects_on_hand(self.turn_player, 'key') > 0:
                self.log.add_object(self.turn_player, 'key_black', -1)
            else:
                self.log.add_object(self.turn_player, 'random_black', 2)          
    
    def end_game_success(self, *args):
#        self.turn_seconds_left = 0
        self.log.game_results[self.turn_player]['is_winner'] = 1
        self.log.game_results[self.turn_player]['victory_type'] = 'keys'                    
        self.log.append_event(self.turn_round, self.turn_player, self.rules_player_names[self.turn_player - 1], 'victory', 'keys', self.test_mode)
        self.log.save_game_results()                  
        # Simulate new game right away in infinite test mode
        self.restart() 
        if self.infinite_test_mode:
            self.get_screen('ready_check').ids.start_button.trigger_action(0)
        else:
#            self.win_test()
            self.win_sound.play()                    
    
    def end_game_check_f(self):
        self.show_event_choice_buttons(choices = 2)
        self.get_screen('game').ids['event_button1'].disabled = False
        self.get_screen('game').ids['event_button1'].text = '[color=#FFFFFF]Победа[/color]'        
        self.get_screen('game').ids['event_button1']._cb.append(self.end_game_success)
        self.get_screen('game').ids['event_button1'].fbind('on_press', self.end_game_success)
        
        self.get_screen('game').ids['event_button2'].disabled = False
        self.get_screen('game').ids['event_button2'].text = '[color=#FFFFFF]Провал[/color]'
        self.get_screen('game').ids['event_button2']._cb.append(self.cancel_win_test)
        self.get_screen('game').ids['event_button2'].fbind('on_press', self.cancel_win_test)
        
        if self.paused == 0:
            self.pause_resume()
        if self.test_mode == True:
            if random() < 0.5:
                self.get_screen('game').ids['event_button1'].trigger_action(0)
            else:   
                self.get_screen('game').ids['event_button2'].trigger_action(0)        

class DefinePlayers(Screen):    
    def add_player(self, test_mode = False):
        if test_mode == True:
            self.ids.player_input.text = "".join([choice(string.ascii_letters) for i in range(7)])
        self.ids.players_box.add_widget(Label(text = '[color=##2c3e50]' + self.ids.player_input.text + '[/color]', 
                                              markup = True, 
                                              font_size = '30sp'))
        self.manager.rules_player_names.append(str(self.ids.player_input.text))
        self.ids.player_input.text = ''
        if len(self.manager.rules_player_names) == 5:
            self.ids.add_player_button.disabled = True                   
            
    def add_player_test(self):
        if len(self.manager.rules_player_names) == 5:
            self.ids.add_player_button.disabled = True
        else:
            try:
                self.ids.player_input.text = str(int(self.manager.rules_player_names[-1]) + 1)
            except:
                self.ids.player_input.text = '1'
                #self.ids.player_input.text = "".join([choice(string.ascii_letters) for i in range(7)])
            self.ids.players_box.add_widget(Label(text = self.ids.player_input.text))
            self.manager.rules_player_names.append(str(self.ids.player_input.text))
            self.ids.player_input.text = ''   
    
    def clear_players(self):
        self.ids.players_box.clear_widgets()
        self.manager.rules_players = []
        self.manager.rules_player_names = []
        self.ids.add_player_button.disabled = False
        
    def finalise_players(self):
        n = 1
        self.manager.rules_players = []
        for i in range(len(self.manager.rules_player_names)):
            self.manager.rules_players.append(n)
            n += 1
        
class DefineTurnLength(Screen):    
    pass
        
class ReadyCheck(Screen):
    pass
            
class Game(Screen):
    pass

class Event(Screen):
    pass

class LavaApp(App):    
    def build(self):
        return ScreenManager()     

if __name__ == '__main__':
    LavaApp().run()
    