from emora_stdm import DialogueFlow, Macro
from enum import Enum
import json, os
import random

# Xiangjue Dong
# 3/21/2020

# states are typically represented as an enum


class State(Enum):

    START = 0
    START_TRAVEL = 1
    END = 2
    ASK_TRAVEL = 3
    TRAVEL_Y = 4
    ASK_TRAVEL_CITY = 5
    ASK_TRAVEL_CITY_DONTKNOW = 6
    ASK_TRAVEL_CITY_UNKNOWN = 7
    ASK_TRAVEL_CITY_UNKNOWN_INLIST = 8

    CITY_TOURISM = 10
    CITY_TOURISM_Y = 11
    CITY_TOURISM_UNKNOWN = 12
    CITY_TOURISM_CERTAIN = 13
    CITY_TOURISM_CERTAIN_Y = 14
    CITY_TOURISM_CERTAIN_N = 15

    CITY_FOOD = 20
    CITY_FOOD_Y = 21
    CITY_FOOD_UNKNOWN = 22
    CITY_FOOD_CERTAIN = 23
    CITY_FOOD_CERTAIN_Y = 24
    CITY_FOOD_CERTAIN_N = 25

    CITY_SPORTS = 30
    CITY_SPORTS_Y = 31
    CITY_SPORTS_N = 32

    CITY_EVENTS = 40
    CITY_EVENTS_Y = 41
    CITY_EVENTS_UNKNOWN = 42
    CITY_EVENTS_CERTAIN = 43
    CITY_EVENTS_CERTAIN_Y = 44
    CITY_EVENTS_CERTAIN_N = 45

    CITY_CULTURE = 50
    CITY_CULTURE_Y = 51
    CITY_CULTURE_N = 52

    CITY_REASON = 60
    CITY_REASON_POSITIVE = 61
    CITY_REASON_NEGATIVE = 62
    CITY_REASON_UNKNOWN = 63
    CITY_REASON_ANS = 64


class TRAVEL_CATCH(Macro):
    """Catch user utterance

    Attribute:
        path: Path of database.
    """

    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Catch user utterance in first key
        if len(args) == 0:
            return ngrams & self.db.keys()

        # Catch the user utterance in the third key
        if len(args) == 1:
            return ngrams & self.db[vars[args[0]]].keys()

        # Catch the user utterance in the third key
        if len(args) == 2:
            return ngrams & self.db[vars[args[0]]][vars[args[1]]].keys()


class TRAVEL_RANDOM(Macro):
    """Random generate keys

    Attribute:
        path: Path of database.
    """
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Random generate the first key
        name = 'db_keys' + self.path
        name_1 = 'db_keys_1' + self.path
        name_2 = 'db_keys_2' + self.path
        name_3 = 'db_keys_3' + self.path

        if len(args) == 0:
            if vars.get(name) is None or len(vars[name]) == 0:
                vars[name] = list(self.db.keys())
            key = random.choice(vars[name])
            vars[name] = vars[name].remove(key)
            return key

        # Random generate unduplicated the first key
        elif len(args) == 1:
            if vars.get(name_1) is None or len(vars[name_1]) <= 1:
                vars[name_1] = list(self.db[vars[args[0]]].keys())
            if vars[args[0]] in vars[name_1]:
                vars[name_1].remove(vars[args[0]])
            key_1 = random.choice(vars[name_1])
            vars[name_1] = vars[name_1].remove(key_1)
            return key_1

        # Random generate the third key
        elif len(args) == 2:
            if vars.get(name_2) is None or len(vars[name_2]) <= 1:
                vars[name_2] = list(self.db[vars[args[0]]][args[1]].keys())
            key_2 = random.choice(vars[name_2])
            vars[name_2] = vars[name_2].remove(key_2)
            return key_2

        # Random generate unduplicated the third key
        elif len(args) == 3:
            if vars.get(name_3) is None or len(vars[name_3]) <= 1:
                vars[name_3] = list(self.db[vars[args[0]]][vars[args[1]]].keys())
            if vars[args[-1]] in vars[name_3]:
                vars[name_3].remove(vars[args[0]])
            key_3 = random.choice(vars[name_3])
            vars[name_3] = vars[name_3].remove(key_3)
            return key_3


class TRAVEL_DETAIL(Macro):
    """Get keys value

    Attribute:
        path: Path of database.
    """
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Get the value of the first key
        if len(args) == 1:
            return self.db[vars[args[0]]]

        # Get the value of the second key
        elif len(args) == 2:
            return self.db[vars[args[0]]][args[1]]

        # Catch the value of the third key
        elif len(args) == 3:
            return self.db[vars[args[0]]][args[1]][vars[args[2]]]


class CATCH_LIST(Macro):
    """Catch user utterance with list.

    Attribute:
        list: A list whether user utterance is in or not.
    """

    def __init__(self, list):
        """Inits CATCH with list"""
        self.list = list

    def run(self, ngrams, vars, args):
        """Performs operation"""
        return ngrams & self.list


# Database
travel_db = os.path.join('modules','travel_database.json')

# Variables
TRANSITION_OUT = ["movies", "music", "sports"]
NULL = "NULL TRANSITION"
# The cities not in the database
CITY_LIST = {"tokyo","jakarta","chongqing","manila","delhi","seoul","mumbai","shanghai","sao paulo","beijing",
             "lagos","mexico city","guangzhou","dhaka","osaka","cairo","karachi","moscow","chengdu",
             "kolkata","buenos aires","istanbul","tehran","shenzhen","tianjin","kinshasa","rio de janeiro",
             "baoding", "lahore", "lima", "bangalore", "ho chi minh", "harbin", "wuhan", "shijiazhuang", "bogota", "suzhou",
             "linyi", "chennai", "nagoya", "nanyang", "zhengzhou", "hyderabad", "surabaya", "hangzhou", "johannesburg",
             "chicago", "quanzhou", "taipei", "dongguan", "bandung", "hanoi", "shenyang", "baghdad", "onitsha",
             "ahmedabad", "luanda", "washington dc", "dallas", "pune", "nanjing", "boston", "santiago",
             "riyadh", "dusseldorf", "madrid", "toronto", "surat"}
YES = {"yes", "yea", "yup", "yep", "i do", "yeah", "a little", "sure", "of course", "i have", "i am", "sometimes", "too", "as well", "also", "agree","good", "keep","why not", "ok", "okay", "fine", "continue", "go on"}
NO = {"no", "nope", "dont", "nothing"}

# Functions
macros = {
    'CATCH': TRAVEL_CATCH(travel_db),
    'RANDOM': TRAVEL_RANDOM(travel_db),
    'RANDOM_TOURISM': TRAVEL_RANDOM(travel_db),
    'RANDOM_FOOD': TRAVEL_RANDOM(travel_db),
    'RANDOM_EVENT': TRAVEL_RANDOM(travel_db),
    'RANDOM_CULTURE': TRAVEL_RANDOM(travel_db),
    'DETAIL': TRAVEL_DETAIL(travel_db),
    'CATCH_CITY_LIST': CATCH_LIST(CITY_LIST),
    'CATCH_YES':CATCH_LIST(YES),
    'CATCH_NO':CATCH_LIST(NO)
}

###################### Initialization Part ####################################################################################################################
# Initialize the DialogueFlow object, which uses a state-machine to manage dialogue
# Each user turn should consider error transition

df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.USER, macros=macros)

# df.add_state(State.START)
# For dialogue manager initialization
# test
# df.add_user_transition(State.START, State.START_TRAVEL, 'test')
df.add_system_transition(State.START_TRAVEL, State.ASK_TRAVEL,'"Last month, one of my friends went to"$city={seattle, houston, atlanta}". Which city is your dream city for travelling?"')

# User Turn
df.add_user_transition(State.START, State.TRAVEL_Y, '[{travel, traveling, city, cities}]')
df.add_user_transition(State.START, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.add_user_transition(State.START, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')

# Error Transition
df.set_error_successor(State.START, State.START)
df.add_system_transition(State.START, State.START, NULL)

# System Turn
df.add_system_transition(State.TRAVEL_Y, State.ASK_TRAVEL, '"Awesome! Last month, one of my friends went to"$city={seattle, houston, atlanta}"and she liked there very much. I know several wonderful cities to travel to in the United States. Which city do you want to go in the United States?"')

# User Turn
df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY_DONTKNOW, '[{i dont know, have no idea, who knows}]')
df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
df.set_error_successor(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY_UNKNOWN)

# System Turn
df.add_system_transition(State.ASK_TRAVEL_CITY, State.CITY_TOURISM, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! I love"$city"!"#DETAIL(city, brief_intro)"I am familiar with many aspects of this city, like tourist attraction, famous food, sports, events or the culture there. Would you like to know about the tourist attraction first?"')
df.add_system_transition(State.ASK_TRAVEL_CITY_DONTKNOW, State.CITY_TOURISM, '"That\'s OK! That\'s why I am here. One of my favorite cities is"$city={#RANDOM()}".I am familiar with many aspects of this city, like tourist attraction, famous food, sports, events or the culture there. Would you like to know about the tourist attraction first?"')
df.add_system_transition(State.ASK_TRAVEL_CITY_UNKNOWN, State.CITY_TOURISM, '"Oops, I\'m not quite familiar with this city. One of my favorite cities is"$city={#RANDOM()}".I am familiar with many aspects of this city, like tourist attraction, famous food, sports, events or the culture there. Would you like to know about the tourist attraction first?"')
df.add_system_transition(State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, State.CITY_TOURISM, '{Interesting, Cool, Wow, Awesome}".I heard"$city"is a good place to travel, but I know little about this place. One of my favorite cities is"$city={#RANDOM()}".I am familiar with many aspects of this city, like tourist attraction, famous food, sports, events or the culture there. Would you like to know about the tourist attraction first?"')

############################# Tourist Attraction Part ############################################################################################################
# User Turn
df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_Y, '[{#CATCH_YES(),tourist attraction, tourist, tourism, attraction, tour}]')
df.add_user_transition(State.CITY_TOURISM, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.add_user_transition(State.CITY_TOURISM, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_CERTAIN_N, '[[{no, nope, dont}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
# df.set_error_successor(State.CITY_TOURISM, State.CITY_TOURISM_UNKNOWN)
df.set_error_successor(State.CITY_TOURISM, State.CITY_TOURISM_CERTAIN_N)

# System Turn
df.add_system_transition(State.CITY_TOURISM_Y, State.CITY_TOURISM_CERTAIN, '"Good choice! I know several famous tourist attraction in"$city",Like"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}".Would you like to know more detail about this tourist attraction?"')
# df.add_system_transition(State.CITY_TOURISM_UNKNOWN, State.CITY_TOURISM, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like tourist attraction there?"')

# User Turn
df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_Y, '[#CATCH_YES()]')
df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_N, '[#CATCH_NO()]')
# df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.set_error_successor(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_N)

# System Turn
df.add_system_transition(State.CITY_TOURISM_CERTAIN_Y, State.CITY_FOOD, '{Nice choice,Good choice, Wonderful,Awesome}"!"$tourism","#DETAIL(city, tourist_attraction, tourism)"I also know lots of famous food in"$city".Would you like to talk about it?"')
df.add_system_transition(State.CITY_TOURISM_CERTAIN_N, State.CITY_FOOD, '{Alright, Ok, Then}".I also know lots of famous food in"$city".Would you like to talk about the famous food in this city?"')

############################# Famous Food Part #####################################################################################################################
# User Turn
df.add_user_transition(State.CITY_FOOD, State.CITY_FOOD_Y, '[#CATCH_YES()]')
# df.add_user_transition(State.CITY_FOOD, State.CITY_FOOD_CERTAIN_N, '[[{no, nope, dont}] #NOT(know, idea)]')
df.add_user_transition(State.CITY_FOOD, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.add_user_transition(State.CITY_FOOD, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
df.set_error_successor(State.CITY_FOOD, State.CITY_FOOD_CERTAIN_N)

# System Turn
df.add_system_transition(State.CITY_FOOD_Y, State.CITY_FOOD_CERTAIN, '"I like food! There are lots of famous food in"$city",Like"$food={#RANDOM_FOOD(city, famous_food)}".Would you like to know more detail about it?"')
df.add_system_transition(State.CITY_FOOD_UNKNOWN, State.CITY_FOOD, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like famous food there?"')

# User Turn
df.add_user_transition(State.CITY_FOOD_CERTAIN, State.CITY_FOOD_CERTAIN_Y, '[#CATCH_YES()]')
df.add_user_transition(State.CITY_FOOD_CERTAIN, State.CITY_FOOD_CERTAIN_N, '[#CATCH_NO()]')
df.set_error_successor(State.CITY_FOOD_CERTAIN, State.CITY_FOOD_CERTAIN_N)

# System Turn
df.add_system_transition(State.CITY_FOOD_CERTAIN_Y, State.CITY_SPORTS, '$food","#DETAIL(city, famous_food, food)"I also know a little sports information in"$city".Would you like to listen?"')
df.add_system_transition(State.CITY_FOOD_CERTAIN_N, State.CITY_SPORTS, '{Alright, Ok, Then}".I also know a little sports information in"$city".Would you like to listen?"')

############################ Sports Part ###########################################################################################################################
# User Turn
df.add_user_transition(State.CITY_SPORTS, State.CITY_SPORTS_Y, '[#CATCH_YES()]')
# df.add_user_transition(State.CITY_SPORTS, State.CITY_SPORTS_N, '[[{no, nope, dont}] #NOT(know, idea)]')
df.add_user_transition(State.CITY_SPORTS, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.add_user_transition(State.CITY_SPORTS, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
df.set_error_successor(State.CITY_SPORTS, State.CITY_SPORTS_N)

# System Turn
df.add_system_transition(State.CITY_SPORTS_Y, State.CITY_EVENTS, '{Nice,Good, Wonderful,Awesome,Great}"!"#DETAIL(city, sports)"Besides sports, there are also some interesting events in"$city".Would you like to know one?"')
df.add_system_transition(State.CITY_SPORTS_N, State.CITY_EVENTS, '{Alright, Ok, Then}".Besides sports, there are also some interesting events in"$city".Would you like to know one?"')

############################# Events Part ##########################################################################################################################
# User Turn
df.add_user_transition(State.CITY_EVENTS, State.CITY_EVENTS_Y, '[#CATCH_YES()]')
# df.add_user_transition(State.CITY_EVENTS, State.CITY_EVENTS_CERTAIN_N, '[[{no, nope, dont}] #NOT(know, idea)]')
df.add_user_transition(State.CITY_EVENTS, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.add_user_transition(State.CITY_EVENTS, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
df.set_error_successor(State.CITY_EVENTS, State.CITY_EVENTS_CERTAIN_N)

# System Turn
df.add_system_transition(State.CITY_EVENTS_Y, State.CITY_EVENTS_CERTAIN, '{Nice choice,Good choice}"! I enjoy festivals and events! There are different events in"$city",Like"$event={#RANDOM_EVENT(city, event)}".Would you like to know more detail about it?"')
df.add_system_transition(State.CITY_EVENTS_UNKNOWN, State.CITY_EVENTS, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like interesting events there?"')

# User Turn
df.add_user_transition(State.CITY_EVENTS_CERTAIN, State.CITY_EVENTS_CERTAIN_Y, '[{yes, yea, yup, yep, i do, yeah, a little, sure, of course, i have, i am, sometimes, too, as well, also, agree, ok, fine, okay, famous food, food}]')
# df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_EVENTS_CERTAIN_N, '[{no, nope, dont}]')
df.add_user_transition(State.CITY_EVENTS_CERTAIN, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.set_error_successor(State.CITY_EVENTS_CERTAIN, State.CITY_EVENTS_CERTAIN_N)

# System Turn
df.add_system_transition(State.CITY_EVENTS_CERTAIN_Y, State.CITY_CULTURE, '{Nice,Good,Great, Cool,Wonderful,Awesome}"!"$event","#DETAIL(city, event, event)"I am also familiar with the culture in"$city".Would you like to know about it?"')
df.add_system_transition(State.CITY_EVENTS_CERTAIN_N, State.CITY_CULTURE, '{Alright, Ok, Then}".I am also familiar with the culture in"$city". Would you like to know about it?"')

############################# Culture Part #########################################################################################################################
# User Turn
df.add_user_transition(State.CITY_CULTURE, State.CITY_CULTURE_Y, '[#CATCH_YES()]')
df.set_error_successor(State.CITY_CULTURE, State.CITY_CULTURE_N)
df.add_user_transition(State.CITY_CULTURE, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
df.add_user_transition(State.CITY_CULTURE, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')

# System Turn
df.add_system_transition(State.CITY_CULTURE_Y, State.CITY_REASON, '{Nice,Good, Great, Cool,Wonderful,Awesome}"!About the"$certain_culture={#RANDOM_CULTURE(city,culture)}","#DETAIL(city, culture, certain_culture)"So, why do you want to travel to"$city"?"')
df.add_system_transition(State.CITY_CULTURE_N, State.CITY_REASON, '{Alright, Ok, Then}"So, why do you want to travel to"$city"?"')

############################# Travel Reason ##########################################################################################################
# User Turn
df.add_user_transition(State.CITY_REASON, State.CITY_REASON_POSITIVE, '[{interesting, beautiful, weather}]')
df.add_user_transition(State.CITY_REASON, State.CITY_REASON_NEGATIVE,'[#CATCH_NO()]')
df.set_error_successor(State.CITY_REASON, State.CITY_REASON_UNKNOWN)

# System Turn
df.add_system_transition(State.CITY_REASON_POSITIVE, State.END, '{Nice,Good, Great, Cool,Wonderful,Awesome, I agree}"!I have to say"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')
df.add_system_transition(State.CITY_REASON_NEGATIVE, State.END, '{Alright, Ok, Then}".But I think"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')
df.add_system_transition(State.CITY_REASON_UNKNOWN, State.END, '{Interesting, I see}".In my opinion, I think"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')

####################### End Travel Component ##############################################################################################################################################
# # END
# df.set_error_successor(State.CITY_REASON_ANS, State.TRAVEL_END)
# df.add_system_transition(State.TRAVEL_END, State.END, '"I\'m glad to talk with you. What other topics would you like to talk about?"')

df.update_state_settings(State.END, system_multi_hop=True)
# df.add_system_transition(State.END, State.START, '" "')
# end (recurrent) the dialogue
# end (recurrent) the dialogue

if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    # df.precache_transitions()
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=True)