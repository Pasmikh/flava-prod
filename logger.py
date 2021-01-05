import os
import csv
import json
from random import randint

class Logger():
    user_id = 0
    game_id = 0
    game_results = {}
    green_objects = []
    red_objects = []
    
    def __init__(self):
        os.makedirs(os.path.dirname('stats/'), exist_ok=True)
        player_id_filename = 'stats/player_id.txt'    
        try:
            with open(player_id_filename, 'r+') as f:
                self.user_id = int(f.read())
        except:
            with open(player_id_filename, 'w+') as f:
                self.user_id = randint(1, 100000000)
                f.write(str(self.user_id))

    def calc_game_id(self):
        max_game_id = 0
        coh_filename = 'stats/game_results.txt'
        if os.path.isfile('stats/game_results.txt'):
            with open(coh_filename, newline='') as statsfile:
                stats = csv.reader(statsfile, delimiter = ',')
                for row in stats:
                    try:
                        max_game_id = max(int(row[1]), max_game_id)
                    except:
                        pass
        else:
            return     
        self.game_id = max_game_id + 1        
    
    def append_event(self, turn_round, player, player_name, event, extra, is_test_mode):
#        if is_test_mode == False:
#            return
        if ~os.path.isfile('stats/events.txt'):
            open('stats/events.txt', 'a').close()
        print([self.user_id, self.game_id, turn_round, player, event, extra])
        with open('stats/events.txt', 'a+') as f:
            f.seek(0)
            data = f.read(100)
            if len(data) > 0 :
                f.write("\n")
            f.write(','.join([str(self.user_id), str(self.game_id), str(turn_round), str(player), str(player_name), event, str(extra)]))

    def add_action(self):
        for i in self.game_results:
            if i['eliminated_at'] == 0:
                [i]['actions'] += 1
                
    def add_object(self, player, form, num):
        self.game_results[player][form] += num
#        print('It works')
                
    def reset_game_results(self, rules_players, rules_objects, game_mode):
        self.calc_game_id()
        for i in rules_players:
            self.game_results[i] = {**{'user_id' : self.user_id},
                                        **{'game_id' : self.game_id},
                                        **{'game_mode' : game_mode},
                                        **{'max_round' : 0},
                                        **{'players_n' : len(rules_players)},
                                        **{'get_events' : 0},
                                        **{'drop_events' : 0},
                                        **{'other_events' : 0},
                                        **{'get_midgame_events' : 0},
                                        **{'strategic_events' : 0},
                                        **{'player' : i},
                                        **{'eliminated_at' : 0},
                                        **{'actions' : 0},
                                        **{el+'_green' : 0 for el in rules_objects},
                                        **{el+'_red' : 0 for el in rules_objects},
                                        **{'key_green' : 0},
                                        **{'key_red' : 0},
                                        **{'key_black' : 0},
                                        **{'random_green' : 0},
                                        **{'random_red' : 0},
                                        **{'random_black' : 0},
                                        **{'is_winner' : 0},
                                        **{'victory_type' : ''}}  
        self.green_objects = [el+'_green' for el in rules_objects] + ['random_green']
        self.red_objects = [el+'_red' for el in rules_objects] + ['random_red']
            
    def save_game_results(self):
        coh_filename = 'stats/game_results.txt'
        if os.path.isfile(coh_filename):
            with open(coh_filename, 'a', newline='') as f:
                w = csv.DictWriter(f, self.game_results[1].keys())
                for i in self.game_results.keys():
                    w.writerow(self.game_results[i])
        else:
            with open(coh_filename, 'w', newline='') as f:
                w = csv.DictWriter(f, self.game_results[1].keys())
                w.writeheader()
                for i in self.game_results.keys():
                    w.writerow(self.game_results[i])