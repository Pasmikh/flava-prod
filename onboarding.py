from random import randint, random, choice, choices, sample
import events

class onboarding_wizard(object):            
    active_scenario = []
    active_step = 0
    onboarding_dict = {5: [ #Round 1
                            'self.take_card(card_type = "basic")', #1
                            'self.take_card(card_type = "key")', #2
                            'self.take_card(card_type = "basic")', #3
                            'self.take_card(card_type = "key")', #4
                            'self.take_card(card_type = "basic")', #5
                            #Round 2
                            'events.event_all_get_1(self)', #1
                            'self.take_card(card_type = "basic")', #2
                            'self.take_card(card_type = "key")', #3
                            'self.take_card(card_type = "basic")', #4
                            'self.take_card(card_type = "key")', #5
                            #Round 3
                            'self.take_card(card_type = "key")', #1
                            'self.take_card(card_type = "basic")', #2
                            'events.event_get_3(self)', #3
                            'self.take_card(card_type = "basic")', #4
                            'events.event_get_rotate(self)', #5
                            #Round 4
                            'self.take_card(card_type = "basic")', #4
                            'self.take_card(card_type = "key")', #3
                            'self.take_card(card_type = "basic")', #2
                            'events.event_switch_hands(self)', #1
                            'self.take_card(card_type = "basic")', #5
                            #Round 5
                            'self.take_card(card_type = "basic")', #4
                            'events.event_drop_object(self)', #3
                            'self.take_card(card_type = "basic")', #2
                            'self.take_card(card_type = "basic")', #1
                            'self.take_card(card_type = "basic")', #5
                            #Round 6
                            'events.event_drop_3(self)',#4
                            'self.take_card(card_type = "basic")',#3
                            'self.take_card(card_type = "key")',#2
                            'events.event_get_2(self)',#1
                            'self.take_card(card_type = "basic")', #5
                            #Round 7
                            'self.take_card(card_type = "key")',#4
                            'events.event_get_key_object(self)',#3
                            'self.take_card(card_type = "basic")', #2
                            'events.event_get_rotate(self)',#1
                            'self.take_card(card_type = "key")',#2
                            #Round 8
                            'self.take_card(card_type = "basic")', #3
                            'events.event_give_1(self, direction = "any")',#4
                            'self.take_card(card_type = "key")',#5
                            'self.take_card(card_type = "basic")',#1
                            'events.event_get_key_min_num_cards(self)',#2
                            #Round 9
                            'events.event_all_get_key(self)',#3
                            'self.take_card(card_type = "basic")',#4            
                            'events.event_switch_hands(self)',#5
                            'self.take_card(card_type = "basic")', #1
                            'events.event_drop_3(self)',#2
                            #Round 10
                            'events.event_get_3(self)',#3
                            'self.take_card(card_type = "key")',#4
                            'self.take_card(card_type = "basic")', #5
                            'events.event_steal_key(self)',#1
                            'self.take_card(card_type = "basic")',#2
                            #Round 11
                            'self.take_card(card_type = "key")',#3
                            'events.event_get_key_max_num_cards(self)',#4
                            'events.event_steal_key(self)',#5
                            'events.event_get_key_object(self)',#3
                            'self.take_card(card_type = "basic")',#2
                            #Round 12
                            'events.event_exchange_hands_with_player(self, color = "green")',#3
                            'self.take_card(card_type = "key")',#4
                            'events.event_get_key_object(self)',#5
                            'self.take_card(card_type = "basic")', #1
                            'events.event_exchange_hands_with_player(self, color = "red")',#2
                            #Round 13
                            'events.event_get_3(self)',#3
                            'self.take_card(card_type = "key")',#4
                            'self.take_card(card_type = "basic")',#5
                            'events.event_get_key_min_num_cards(self)',#1
                            'self.take_card(card_type = "basic")', #2
                            #Round 14
                            'self.take_card(card_type = "key")',#3
                            'self.take_card(card_type = "basic")',#4          
                            'events.event_all_get_1(self)',#5
                            'self.take_card(card_type = "basic")', #1
                            'events.event_get_2(self)',#2
                            #Round 15
                            'self.take_card(card_type = "basic")',#3
                            'self.take_card(card_type = "basic")', #4
                            'events.event_steal_key(self)',#5
                            'self.take_card(card_type = "basic")',#1
                            'self.take_card(card_type = "key")',#2
                            #Round 16
                            'events.event_get_key_max_num_cards(self)',#3
                            'self.take_card(card_type = "basic")',#4
                            'self.take_card(card_type = "key")',#5                      
                            'events.event_give_1(self, direction = "any")',#1
                            'self.take_card(card_type = "basic")', #2
                            #Round 17
                            'events.event_all_get_key(self)',#3
                            'self.take_card(card_type = "basic")',#4                
                            'events.event_get_key_object(self)',#5
                            'self.take_card(card_type = "basic")', #1
                            'self.take_card(card_type = "key")'#2
                            ],
                       4: [ #Round 1
                            'self.take_card(card_type = "basic")', #1
                            'self.take_card(card_type = "basic")', #2
                            'self.take_card(card_type = "key")', #3
                            'self.take_card(card_type = "basic")', #4
                            #Round 2
                            'events.event_all_get_1(self)', #1
                            'self.take_card(card_type = "key")', #2
                            'self.take_card(card_type = "basic")', #3
                            'self.take_card(card_type = "key")', #4
                            #Round 3
                            'self.take_card(card_type = "key")', #1
                            'events.event_get_3(self)', #2
                            'self.take_card(card_type = "basic")', #3
                            'events.event_get_rotate(self)', #4
                            #Round 4
                            'self.take_card(card_type = "basic")', #3
                            'self.take_card(card_type = "key")', #2
                            'events.event_switch_hands(self)', #1    
                            'self.take_card(card_type = "basic")', #4
                            #Round 5
                            'self.take_card(card_type = "basic")', #3
                            'events.event_drop_object(self)', #2
                            'self.take_card(card_type = "basic")', #1
                            'self.take_card(card_type = "basic")', #4
                            #Round 6
                            'events.event_drop_3(self)',#3
                            'self.take_card(card_type = "basic")',#2
                            'self.take_card(card_type = "key")',#1
                            'events.event_get_2(self)',#4
                            #Round 7
                            'self.take_card(card_type = "basic")',#3
                            'events.event_get_key_object(self)',#2          
                            'events.event_get_rotate(self)',#1
                            'events.event_all_get_key(self)',#2
                            #Round 8
                            'events.event_give_1(self, direction = "any")',#3
                            'self.take_card(card_type = "key")',#4                   
                            'self.take_card(card_type = "basic")',#1
                            'events.event_get_key_min_num_cards(self)',#2
                            #Round 9
                            'self.take_card(card_type = "key")',#3
                            'self.take_card(card_type = "basic")',#4            
                            'events.event_switch_hands(self)',#1                
                            'events.event_drop_3(self)',#2
                            #Round 10
                            'events.event_get_3(self)',#3
                            'events.event_steal_key(self)',#4
                            'self.take_card(card_type = "basic")',#1
                            'self.take_card(card_type = "basic")',#2
                            #Round 11
                            'self.take_card(card_type = "key")',#3
                            'events.event_get_key_max_num_cards(self)',#4
                            'self.take_card(card_type = "key")',#1
                            'events.event_steal_key(self)',#2                       
                            #Round 12
                            'events.event_exchange_hands_with_player(self, color = "green")',#3
                            'self.take_card(card_type = "basic")',#4
                            'events.event_get_key_object(self)',#1
                            'self.take_card(card_type = "key")',#2 
                            #Round 13
                            'events.event_get_3(self)',#3
                            'self.take_card(card_type = "key")',#4
                            'self.take_card(card_type = "basic")',#1
                            'events.event_get_key_min_num_cards(self)',#2
                            #Round 14
                            'self.take_card(card_type = "key")',#3
                            'self.take_card(card_type = "basic")',#4          
                            'events.event_all_get_1(self)',#1
                            'events.event_get_2(self)',#2
                            #Round 15
                            'self.take_card(card_type = "basic")',#3
                            'self.take_card(card_type = "key")',#4
                            'events.event_steal_key(self)',#1
                            'self.take_card(card_type = "key")',#2
                            #Round 16
                            'events.event_get_key_max_num_cards(self)',#3
                            'self.take_card(card_type = "basic")',#4
                            'self.take_card(card_type = "key")',#1                      
                            'events.event_give_1(self, direction = "any")',#2
                            #Round 17
                            'self.take_card(card_type = "basic")',#3
                            'self.take_card(card_type = "basic")',#4                
                            'events.event_get_key_object(self)',#1
                            'events.event_all_get_key(self)'#2
                            ],
                       3 :[ #Round 1
                            'self.take_card(card_type = "basic")', #1
                            'self.take_card(card_type = "key")', #2
                            'self.take_card(card_type = "basic")', #3
                            #Round 2
                            'events.event_all_get_1(self)', #1
                            'self.take_card(card_type = "basic")', #2
                            'self.take_card(card_type = "key")', #3
                            #Round 3
                            'self.take_card(card_type = "key")', #1
                            'events.event_get_3(self)', #2
                            'events.event_get_rotate(self)', #3
                            #Round 4
                            'self.take_card(card_type = "basic")', #2
                            'self.take_card(card_type = "basic")', #1
                            'events.event_get_2(self)', #3
                            #Round 5
                            'self.take_card(card_type = "key")', #2
                            'events.event_drop_object(self)', #1
                            'self.take_card(card_type = "basic")', #3
                            #Round 6
                            'events.event_switch_hands(self)', #2
                            'self.take_card(card_type = "basic")', #1
                            'events.event_exchange_hands_with_player(self, color = "green")', #3
                            #Round 7
                            'self.take_card(card_type = "basic")',#2
                            'events.event_all_get_key(self)',#1
                            'self.take_card(card_type = "basic")',#3
                            #Round 8
                            'events.event_get_key_object(self)',#2
                            'self.take_card(card_type = "key")',#1
                            'self.take_card(card_type = "basic")',#3
                            #Round 9
                            'self.take_card(card_type = "basic")',#2
                            'self.take_card(card_type = "basic")',#1                   
                            'events.event_steal_key(self)',#3
                            #Round 10
                            'events.event_get_3(self)',#2
                            'self.take_card(card_type = "basic")',#1
                            'self.take_card(card_type = "basic")',#3
                            #Round 11
                            'events.event_all_get_key(self)',#2
                            'events.event_get_key_object(self)',#1
                            'self.take_card(card_type = "basic")',#3
                            #Round 12
                            'self.take_card(card_type = "basic")',#3
                            'events.event_get_key_max_num_cards(self)',#2
                            'self.take_card(card_type = "key")',#1                            
                            #Round 9
                            'events.event_get_key_object(self)  ',#3                  
                            'self.take_card(card_type = "basic")',#2                            
                            'events.event_get_3(self)',#1
                            #Round 10
                            'events.event_all_get_1(self)',#3
                            'self.take_card(card_type = "basic")',#2
                            'events.event_steal_key(self)',#1
                            #Round 11
                            'self.take_card(card_type = "key")',#3
                            'events.event_get_key_object(self)',#2
                            'self.take_card(card_type = "key")'#1
                        ],
                       2 :[ #Round 1
                            'self.take_card(card_type = "basic")', #1-1-0
                            'self.take_card(card_type = "key")', #2-1-1
                            #Round 2
                            'events.event_all_get_1(self)', #1-2-0
                            'self.take_card(card_type = "basic")', #2-3-1
                            #Round 3
                            'self.take_card(card_type = "basic")', #1-3-0
                            'events.event_get_3(self)', #2-3-1
                            #Round 4
                            'self.take_card(card_type = "basic")', #1-6-1
                            'events.event_get_2(self)', #2-5-1                               
                            #Round 5
                            'self.take_card(card_type = "key")', #1-9-2
                            'self.take_card(card_type = "basic")', #2-6-1
                            #Round 6
                            'events.event_switch_hands(self)', #1-9-2
                            'events.event_steal_key(self)', #2-7-2
                            #Round 7
                            'events.event_drop_object(self)', #1-7-1
                            'events.event_all_get_key(self)', #2-8-2
                            #Round 8
                            'self.take_card(card_type = "key")', #1-8-2
                            'events.event_get_key_object(self)', #2-9-3
                            #Round 9
                            'self.take_card(card_type = "key")', #1-9-3
                            'self.take_card(card_type = "basic")', #2-10-3
                            #Round 10
                            'events.event_all_get_1(self)', #1-10-3
                            'events.event_get_3(self)', #2-10-3
                            #Round 11
                            'self.take_card(card_type = "basic")', #1-13-4
                            'self.take_card(card_type = "key")', #1-11-4
                            #Round 12
                            'events.event_get_key_max_num_cards(self)',#2
                            'self.take_card(card_type = "basic")', #2-10-3
                            #Round 13                            
                            'events.event_get_3(self)', #2-10-3
                            'self.take_card(card_type = "key")', #1-11-4
                            #Round 14
                            'self.take_card(card_type = "basic")', #1-13-4
                            'events.event_all_get_key(self)', #1-11-4
                            #Round 15
                            'events.event_exchange_hands_with_player(self, color = "green")', #2-10-3
                            'self.take_card(card_type = "basic")', #1-11-4
                            #Round 16
                            'self.take_card(card_type = "basic")', #1-13-4
                            'self.take_card(card_type = "key")' #1-11-4
                       ]
                      }
    
    def __init__(self, num_players):
        self.active_scenario = self.onboarding_dict[num_players]
    
    def next_turn(self):
        self.active_step += 1
        try: 
            turn = self.active_scenario[self.active_step - 1]
        except: 
            self.active_step = 0
            turn = self.active_scenario[self.active_step - 1]
        return turn