from random import randint, random, choice, choices, sample
from functools import partial
from kivy.graphics import Line, Rectangle, Color, Ellipse

event_texts = {'event_get_3_warmup' : "'ВСЕ игроки берут по три разных красных и зеленых существа, но не '  + game.key_object.upper()",
               'event_get_3' : "'Выбери игрока. Он берет красное и зеленое существо разных форм и ' + game.key_object.upper()",
               'event_get_3_choice' : "game.rules_player_names[player - 1] + ' берет ' + game.key_object.upper() + ', красное и зеленое существо разных форм'",
               'event_all_get_1' : "'ВСЕ берут любое существо, но НЕ ' + game.key_object.upper()",
               'event_all_get_key' : "'ВСЕ берут ' + game.key_object.upper()",
               'event_get_2' : "'Возьми красное и зеленое существо разных форм, но не ' + game.key_object.upper()",
               'event_get_rotate': "'Возьми ' + card_color + card_object.upper() + '[/color]' +'. Ход идет в обратную сторону.'",
               'event_get_key_object': "'Выбери существо. Все игроки с этим существом возьмут один ' + game.key_object.upper()",
               'event_get_key_object_choice' : "'Все игроки с ' + str(object).upper() + ' берут один ' + game.key_object.upper()",
               'event_get_key_min_num_cards': "'Выбери число. Все у кого столько или больше существ - возьмут ' + game.key_object.upper()",
               'event_get_key_min_num_cards_choice' : "'Все, у кого ' + str(num_cards) + ' или больше существ берут ' + game.key_object.upper()",
               'event_get_key_max_num_cards' : "'Выбери число. Все у кого столько или меньше существ - возьмут ' + game.key_object.upper()", 
               'event_get_key_max_num_cards_choice': "'Все, у кого ' + str(num_cards) + ' или меньше существ берут ' + game.key_object.upper()",
               'event_get_key_object_delayed' : "'Возьми ' + card_color + card_object.upper() + '[/color].\\n Все игроки с ' + card_object_strategic +  ' через 2 раунда возьмут ' + game.key_object.upper()",
               'event_get_key_object_delayed_final' : "'Все игроки с ' + object.upper() + ' берут один ' + game.key_object.upper()",
               'event_drop_key_object_delayed' : "'Возьми ' + card_color + card_object.upper() + '[/color].\\n Все игроки с ' + card_object_strategic +  ' через 2 раунда сбросят ' + game.key_object.upper()",
               'event_drop_key_object_delayed_final' : "'Все игроки с ' + object.upper() + ' сбрасывают один ' + game.key_object.upper()",
               'event_drop_3': "'Выбери игрока. Он сбрасывает красное существо, зеленое существо и ' + game.key_object.upper()",
               'event_drop_3_choice' : "game.rules_player_names[player - 1] + ' сбрасывает красное существо, зеленое существо и ' + game.key_object.upper()",
               'event_drop_object' : "'Выбери существо. Все игроки сбрасывают все такие существа.'",
               'event_drop_object_choice' : "'Все игроки сбрасывают все ' + str(object).upper()",
               'event_all_drop_1' : "'Все сбрасывают любое существо'",
               'event_drop_key_object' : "'Выбери существо. Все игроки с этим существом сбросят один ' + game.key_object.upper()",
               'event_drop_key_object_choice' : "'Все игроки с ' + str(object).upper() + ' сбрасывают ' + game.key_object.upper()",
               'event_switch_hands' : "'Все переложите всех существ из правой руки в левую и наоборот. В этот ход можно держать разные цвета вместе.'",
               'event_give_1_right' : "'Все кладут существо перед игроком СПРАВА. После старта таймера возьмите существо перед вами.'",
               'event_give_1_left' : "'Все кладут существо перед игроком СЛЕВА. После старта таймера возьмите существо перед вами.'",
               'event_give_1_any' : "'Все кладут существо перед ЛЮБЫМ игроком. После старта таймера возьмите существа перед вами.'",
               'event_win_test_drop_keys' : "'Для победы выложи все шарики, не уронив другие объекты'",
               'event_win_test_switch_hands' : "'Для победы переложи существ из левой руки в правую и наоборот. В этот ход можно держать разные цвета вместе.'",
               'event_win_test_give_2' : "'ВСЕ кладут по два существа перед тобой. Для победы возьми этих существ.'",
               'event_steal_key' : "'Выбери игрока. Если у него есть ' + game.key_object.upper() +', он кладет его перед тобой. После старта таймера, возьми его.'",
               'event_steal_key_choice' : "'Если у ' + game.rules_player_names[player - 1] + ' есть шарик - возьми его'",
               'event_exchange_hands_with_player_red' : "'Выбери игрока. Вы кладете все свои красные существа друг перед другом. После старта таймера возьмите их.'",
               'event_exchange_hands_with_player_choice_red' : "'Возьмите все красные существа перед вами'",
               'event_exchange_hands_with_player_green' : "'Выбери игрока. Вы кладете все свои зеленые существа друг перед другом. После старта таймера возьмите их.'",
               'event_exchange_hands_with_player_choice_green' : "'Возьмите все красные существа перед вами'"
              }

## GET EVENTS
#def turn_confirmation(game)

def event_set_confirmation(game, force_confirm = False):
    if (game.confirm_events) or (force_confirm):
        game.show_event_choice_buttons(event_confirm = True)        
        if game.test_mode == True:
            game.get_screen('game').ids['event_button1'].trigger_action(0)
    
def event_get_3_warmup(game):
    game.turn_object = eval(event_texts['event_get_3_warmup'])
    event_set_confirmation(game, force_confirm = True)
    for i in game.rules_players:
        game.log.game_results[i]['random_red'] += 3
        game.log.game_results[i]['random_green'] += 3
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_3_warmup', '', game.test_mode)  

def event_get_3(game):                     
    game.turn_object = eval(event_texts['event_get_3'])
    # Display player choice buttons        
    players_to_choose_from = [player for player in game.rules_players if player != game.turn_player]
    n = 1
    game.show_event_choice_buttons(choices = len(players_to_choose_from), event_confirm = False)
    
    for player in players_to_choose_from: 
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + game.rules_player_names[player - 1] + '[/color]'
        event_callback = partial(event_get_3_choice, game, player, button_id)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1      
    if game.paused == 0:
        game.pause_resume()
    # Press random button in test mode
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(players_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)

def event_get_3_choice(game, player, button_id, *args):
    game.turn_object = eval(event_texts['event_get_3_choice'])
    game.log.game_results[player]['key_black'] += 1
    game.log.game_results[player]['random_green'] += 1
    game.log.game_results[player]['random_red'] += 1
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_3', player, game.test_mode)

def event_all_get_1(game):
    game.turn_object = eval(event_texts['event_all_get_1'])
    event_set_confirmation(game)
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_all_get_1', '', game.test_mode)    

def event_all_get_key(game):
    game.turn_object = eval(event_texts['event_all_get_key'])
    event_set_confirmation(game)
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_all_get_key', '', game.test_mode)     
    for player in game.rules_players:
        game.log.game_results[player]['key_black'] += 1
    
def event_get_2(game):
    game.turn_object = eval(event_texts['event_get_2'])
    event_set_confirmation(game)
    game.log.game_results[game.turn_player]['random_green'] += 1
    game.log.game_results[game.turn_player]['random_red'] += 1
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_2', '', game.test_mode)    
    
def event_get_rotate(game):
    card_object, card_color, card_color_text, card_color_key = game.random_card_object_color()
#    event_set_confirmation(game)
    game.log.game_results[game.turn_player][card_object + card_color_key] += 1
    game.log.game_results[game.turn_player]['actions'] += 1
    game.turn_object = eval(event_texts['event_get_rotate'])
    game.img_source = "ObjectImages/JPGs/" + game.objects_dict[card_object] + card_color_key + ".jpg"                
    game.get_screen('game').ids.object_image.canvas.add(Ellipse(source  = game.img_source,  
                                                                    pos = (game.width * 0.5 - game.height * 0.2,
                                                                           game.height * 0.3),
                                                                    size = (game.height * 0.4,
                                                                            game.height * 0.4)))
    game.turn_rotation = - game.turn_rotation
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_rotate', card_object + card_color_key, game.test_mode)

## GET MIDGAME EVENTS
def event_get_key_object(game):
    game.turn_object = eval(event_texts['event_get_key_object'])
    objects_to_choose_from = sample(game.rules_objects, k = 4)
    game.show_event_choice_buttons(choices = len(objects_to_choose_from), event_confirm = False)
    n = 1
    for object in objects_to_choose_from:            
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + object + '[/color]'
        event_callback = partial(event_get_key_object_choice, game, object, button_id)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1          
    if game.paused == 0:
        game.pause_resume()
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(objects_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)

def event_get_key_object_choice(game, object, button_id, *args):
    # Change turn text
    game.turn_object = eval(event_texts['event_get_key_object_choice'])    
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_key_object', object, game.test_mode) 

def event_get_key_min_num_cards(game):
    game.turn_object = eval(event_texts['event_get_key_min_num_cards'])
    num_cards_to_choose_from = [3,6,9,12]
    game.show_event_choice_buttons(choices = len(num_cards_to_choose_from), event_confirm = False)
    n = 1
    for num_cards in num_cards_to_choose_from:            
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + str(num_cards) + '[/color]'
        event_callback = partial(event_get_key_min_num_cards_choice, game, num_cards, button_id)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1          
    if game.paused == 0:
        game.pause_resume()
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(num_cards_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)

def event_get_key_min_num_cards_choice(game, num_cards, button_id, *args):
    # Change turn text
    game.turn_object = eval(event_texts['event_get_key_min_num_cards_choice'])
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_key_min_num_cards', num_cards, game.test_mode)        

def event_get_key_max_num_cards(game):
    game.turn_object = eval(event_texts['event_get_key_max_num_cards'])
    num_cards_to_choose_from = [3,6,9,12]
    game.show_event_choice_buttons(choices = len(num_cards_to_choose_from), event_confirm = False)
    n = 1
    for num_cards in num_cards_to_choose_from:            
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + str(num_cards) + '[/color]'
        event_callback = partial(event_get_key_max_num_cards_choice, game, num_cards, button_id)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1          
    if game.paused == 0:
        game.pause_resume()
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(num_cards_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)

def event_get_key_max_num_cards_choice(game, num_cards, button_id, *args):
    # Change turn text
    game.turn_object = eval(event_texts['event_get_key_max_num_cards_choice'])
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_key_max_num_cards', num_cards, game.test_mode)
    
def event_get_key_object_delayed(game):
    card_object, card_color, card_color_text, card_color_key = game.random_card_object_color()
    card_object_strategic = game.random_card_object_color()[0]
    # Add GET event so players have a chance to get required card
    game.strategic_pool.append([game.turn_round + 1, 
                                choice(game.rules_players), 
                                partial(event_all_get_1, game)])
    
    game.strategic_pool.append([game.turn_round + 2, 
                                choice(game.rules_players), 
                                partial(event_get_key_object_delayed_final, game, card_object_strategic)])
    # Change turn text
#    event_set_confirmation(game)
    game.turn_object = eval(event_texts['event_get_key_object_delayed'])

    game.img_source = "ObjectImages/JPGs/" + game.objects_dict[card_object] + card_color_key + ".jpg"                
    game.get_screen('game').ids.object_image.canvas.add(Ellipse(source  = game.img_source,  
                                                                pos = (game.width * 0.5 - game.height * 0.2,
                                                                       game.height * 0.3),
                                                                size = (game.height * 0.4,
                                                                        game.height * 0.4)))
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_key_object_delayed', card_object_strategic, game.test_mode)
            
def event_get_key_object_delayed_final(game, object):
    # Change turn text
    event_set_confirmation(game)
    game.turn_object = eval(event_texts['event_get_key_object_delayed_final'])
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_get_key_object_delayed_final', object, game.test_mode)

def event_drop_key_object_delayed(game):
    # Event logic
    card_object, card_color, card_color_text, card_color_key = game.random_card_object_color()
    card_object_strategic = game.random_card_object_color()[0]
    # Add GET event so players have a chance to get required card
    game.strategic_pool.append([game.turn_round + 1,
                                choice(game.rules_players), 
                                partial(event_all_drop_1, game)])
    
    game.strategic_pool.append([game.turn_round + 2, 
                                choice(game.rules_players), 
                                partial(event_drop_key_object_delayed_final, game, card_object_strategic)])
    # Change turn text
    game.turn_object = eval(event_texts['event_drop_key_object_delayed'])

    game.img_source = "ObjectImages/JPGs/" + game.objects_dict[card_object] + card_color_key + ".jpg"                
    game.get_screen('game').ids.object_image.canvas.add(Ellipse(source  = game.img_source,  
                                                                    pos = (game.width * 0.5 - game.height * 0.2,
                                                                           game.height * 0.3),
                                                                    size = (game.height * 0.4,
                                                                            game.height * 0.4)))
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_drop_key_object_delayed', card_object_strategic, game.test_mode)
            
def event_drop_key_object_delayed_final(game, object):
    # Change turn text
    game.turn_object = eval(event_texts['event_drop_key_object_delayed_final'])
    event_set_confirmation(game)
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_drop_key_object_delayed_final', object, game.test_mode)

## DROP EVENTS
def event_drop_3(game):
    game.turn_object = eval(event_texts['event_drop_3'])
    
    players_to_choose_from = [player for player in game.rules_players if player != game.turn_player]
    game.show_event_choice_buttons(choices = len(players_to_choose_from), event_confirm = False)
    n = 1
    for player in players_to_choose_from:            
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + game.rules_player_names[player - 1] + '[/color]'
        event_callback = partial(event_drop_3_choice, game, player, button_id)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1          
    # Pause for decision making
    if game.paused == 0:
        game.pause_resume()
    #Press random button in test mode
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(players_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)

def event_drop_3_choice(game, player, button_id, *args):
    game.turn_object = eval(event_texts['event_drop_3_choice'])
#    if game.calculate_objects_on_hand(player, 'key') > 0:
#        game.log.game_results[player]['key_black'] += -1    
    if game.calculate_objects_on_hand(player, 'green') > 0:
        game.log.game_results[player]['random_green'] += -1
    if game.calculate_objects_on_hand(player, 'red') > 0:
        game.log.game_results[player]['random_red'] += -1
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_drop_3', player, game.test_mode)

def event_drop_object(game):
    game.turn_object = eval(event_texts['event_drop_object'])

    objects_to_choose_from = sample(game.rules_objects, k = 4)
    game.show_event_choice_buttons(choices = len(objects_to_choose_from), event_confirm = False)
    n = 1
    for object in objects_to_choose_from:            
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + object + '[/color]'
        event_callback = partial(event_drop_object_choice, game, object, button_id)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1          
    if game.paused == 0:
        game.pause_resume()
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(objects_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)

def event_drop_object_choice(game, object, button_id, *args):
    # Change turn text
    game.turn_object = eval(event_texts['event_drop_object_choice'])
    # Update cards on hands
    for i in game.rules_players:
        game.log.game_results[i][object+'_green'] = 0
        game.log.game_results[i][object+'_red'] = 0
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_drop_object', object, game.test_mode)              

def event_all_drop_1(game):
    # Change turn text
    game.turn_object = eval(event_texts['event_all_drop_1'])
    event_set_confirmation(game)
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_all_drop_1', '', game.test_mode)

def event_drop_key_object(game):
    game.turn_object = eval(event_texts['event_drop_key_object'])

    objects_to_choose_from = sample(game.rules_objects, k = 4)
    game.show_event_choice_buttons(choices = len(objects_to_choose_from), event_confirm = False)
    n = 1
    for object in objects_to_choose_from:            
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + object + '[/color]'
        event_callback = partial(event_drop_key_object_choice, game, object, button_id)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1          
    if game.paused == 0:
        game.pause_resume()
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(objects_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)

def event_drop_key_object_choice(game, object, button_id, *args):
    # Change turn text
    game.turn_object = eval(event_texts['event_drop_key_object_choice'])
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_drop_key_object', object, game.test_mode)
    
     
    
## OTHER EVENTS    
def event_switch_hands(game, placeholder = ''):
    # Change turn text
    event_set_confirmation(game)
    game.turn_object = eval(event_texts['event_switch_hands'])
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_switch_hands', '', game.test_mode)
    if game.test_mode == False:
        game.turn_seconds_left += min(game.turn_round * 1.5, 12)
        game.turn_additional_seconds += min(game.turn_round * 1.5, 12)

def event_give_1(game, direction):
    event_set_confirmation(game, force_confirm = True)
    if direction == 'right':
        game.turn_object = eval(event_texts['event_give_1_right'])
        game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_give_1_right', '', game.test_mode)
    elif direction == 'left':
        game.turn_object = eval(event_texts['event_give_1_left'])
        game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_give_1_left', '', game.test_mode)
    elif direction == 'any':
        game.turn_object = eval(event_texts['event_give_1_any'])
        game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_give_1_any', '', game.test_mode)
        
    game.turn_seconds_left += -1
    game.turn_additional_seconds += -1
        
def event_steal_key(game, placeholder = ''):
    game.turn_object = eval(event_texts['event_steal_key'])
    # Display player choice buttons        
    players_to_choose_from = [player for player in game.rules_players if player != game.turn_player]
    n = 1
    game.show_event_choice_buttons(choices = len(players_to_choose_from), event_confirm = False)    
    for player in players_to_choose_from: 
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + game.rules_player_names[player - 1] + '[/color]'
        event_callback = partial(event_steal_key_choice, game, player, button_id)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1      
    # Press random button in test mode
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(players_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)
        
def event_steal_key_choice(game, player, button_id, *args):
    game.turn_object = eval(event_texts['event_steal_key_choice'])
    if game.test_mode:
        if game.calculate_objects_on_hand(player, 'key') > 0:
            game.log.game_results[player]['key_black'] += -1
            game.log.game_results[game.turn_player]['key_black'] += 1
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_steal_key', player, game.test_mode)
    
def event_exchange_hands_with_player(game, color):
    if color == 'red':
        game.turn_object = eval(event_texts['event_exchange_hands_with_player_red'])
    else:
        game.turn_object = eval(event_texts['event_exchange_hands_with_player_green'])
        
    # Display player choice buttons        
    players_to_choose_from = [player for player in game.rules_players if player != game.turn_player]
    n = 1
    game.show_event_choice_buttons(choices = len(players_to_choose_from), event_confirm = False)
    
    for player in players_to_choose_from: 
        button_id = 'event_button' + str(n)
        game.get_screen('game').ids[button_id].disabled = False
        game.get_screen('game').ids[button_id].text = '[color=#FFFFFF]' + game.rules_player_names[player - 1] + '[/color]'
        event_callback = partial(event_exchange_hands_with_player_choice, game, player, button_id, color)
        game.get_screen('game').ids[button_id]._cb.append(event_callback)
        game.get_screen('game').ids[button_id].fbind('on_press', event_callback)
        n += 1      
    if game.paused == 0:
        game.pause_resume()
    # Press random button in test mode
    if game.test_mode == True:
        random_button_to_press = 'event_button' + str(randint(1, len(players_to_choose_from)))
        game.get_screen('game').ids[random_button_to_press].trigger_action(0)
        
def event_exchange_hands_with_player_choice(game, player, button_id, color, *args):
    if color == 'red':
        game.turn_object = eval(event_texts['event_exchange_hands_with_player_choice_red'])
        game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_exchange_hands_with_player_red', player, game.test_mode)  
    else:
        game.turn_object = eval(event_texts['event_exchange_hands_with_player_choice_green'])
        game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_exchange_hands_with_player_green', player, game.test_mode)  
    if game.test_mode == False:
        game.turn_seconds_left += 2
        game.turn_additional_seconds += 2
        
# WIN EVENTS
def event_win_test_drop_keys(game, placeholder = ''):
    event_set_confirmation(game)
    # Change turn text
    game.turn_object = eval(event_texts['event_win_test_drop_keys'])
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_win_test_drop_keys', '', game.test_mode)
    if game.test_mode == False:
        game.turn_seconds_left += 1
        game.turn_additional_seconds += 1
        
def event_win_test_switch_hands(game, placeholder = ''):
    event_set_confirmation(game)
    # Change turn text
    game.turn_object = eval(event_texts['event_win_test_switch_hands'])
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_win_test_switch_hands', '', game.test_mode)
    if game.test_mode == False:
        game.turn_seconds_left += min(game.turn_round * 1.3, 16)
        game.turn_additional_seconds += min(game.turn_round * 1.3, 16)
        
def event_win_test_give_2(game, placeholder = ''):
    event_set_confirmation(game, force_confirm = True)
    # Change turn text
    game.turn_object = eval(event_texts['event_win_test_give_2'])
    # Log event
    game.log.append_event(game.turn_round, game.turn_player, game.rules_player_names[game.turn_player - 1], 'event_win_test_give_2', '', game.test_mode)
    if game.test_mode == False:
        game.turn_seconds_left += 2
        game.turn_additional_seconds += 2