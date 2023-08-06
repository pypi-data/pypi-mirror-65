from emora_stdm import DialogueFlow, Macro
from enum import Enum
import json, os
import random

# Zahara
# 04/09/2020

# bug fixed, added dialogue to a previous end


class State(Enum):

    START = 0
    START_TRAVEL = 1
    END = 2
    ROBOT=3

    ASK_TRAVEL = 5
    TRAVEL_N = 6
    TRAVEL_Y= 7

    CITY_NOT_TRAVELED=10
    CITY_TRAVELED=11
    ASK_OPINION_REASON=12
    CITY_DISCUSS=13
    CITY_DISLIKE = 14

    REASON_NOT_SURE = 15
    REASON_N=16
    REASON_Y=17

    CITY_TOURISM=20
    OK_THE_CITY=21
    NOT_THE_CITY=22


    ATTRACTION_OPINION=25
    ATTRACTION_OPINION_N=26
    ATTRACTION_OPINION_D=27
    ATTRACTION_OPINION_Y=28

    CITY_RECOMMEND=30
    CITY_RECOMMEND_N=31
    CITY_RECOMMEND_Y=32

    FOOD_RECOMMEND=35
    FOOD_RECOMMEND_N=36
    FOOD_RECOMMEND_Y=37

    FOOD_OPINION=40
    FOOD_LIKE = 41
    FOOD_DISLIKE=42
    FOOD_NOT_KNOW=43

    ATTRACTION_RECOMMEND = 45
    ATTRACTION_RECOMMEND_D =46
    ATTRACTION_RECOMMEND_N = 47
    ATTRACTION_RECOMMEND_Y = 48

    USER_REC_CITY=50
    USER_REC_ANSWER=51
    USER_REC_NO=52
   


    # ASK_TRAVEL_CITY = 5
    # ASK_TRAVEL_CITY_DONTKNOW = 6
    # ASK_TRAVEL_CITY_UNKNOWN = 7
    # ASK_TRAVEL_CITY_UNKNOWN_INLIST = 8

    # CITY_TOURISM = 10
    # CITY_TOURISM_Y = 11
    # CITY_TOURISM_UNKNOWN = 12
    # CITY_TOURISM_CERTAIN = 13
    # CITY_TOURISM_CERTAIN_Y = 14
    # CITY_TOURISM_CERTAIN_N = 15

    # CITY_FOOD = 20
    # CITY_FOOD_Y = 21
    # CITY_FOOD_UNKNOWN = 22
    # CITY_FOOD_CERTAIN = 23
    # CITY_FOOD_CERTAIN_Y = 24
    # CITY_FOOD_CERTAIN_N = 25

    # CITY_SPORTS = 30
    # CITY_SPORTS_Y = 31
    # CITY_SPORTS_N = 32

    # CITY_EVENTS = 40
    # CITY_EVENTS_Y = 41
    # CITY_EVENTS_UNKNOWN = 42
    # CITY_EVENTS_CERTAIN = 43
    # CITY_EVENTS_CERTAIN_Y = 44
    # CITY_EVENTS_CERTAIN_N = 45

    # CITY_CULTURE = 50
    # CITY_CULTURE_Y = 51
    # CITY_CULTURE_N = 52

    # CITY_REASON = 60
    # CITY_REASON_POSITIVE = 61
    # CITY_REASON_NEGATIVE = 62
    # CITY_REASON_UNKNOWN = 63
    # CITY_REASON_ANS = 64


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
CITY_IN_THE_LIST = {"honolulu","chicago","miami","orlando","philadelphia","san francisco","new orleans", "washington dc","houston","san diego","las vegas","los angeles","atlanta","seattle","bangkok","london","hong kong","macau","singapore","paris","dubai","kuala lumpur"}
# The cities not in the database
CITY_LIST = {"tokyo","jakarta","chongqing","manila","delhi","seoul","mumbai","shanghai","sao paulo","beijing",
             "lagos","mexico city","guangzhou","dhaka","osaka","cairo","karachi","moscow","chengdu",
             "kolkata","buenos aires","tehran","tianjin","kinshasa","rio de janeiro",
             "baoding", "lahore", "lima", "bangalore", "ho chi minh", "harbin", "wuhan", "shijiazhuang", "bogota", "suzhou",
             "linyi", "chennai", "nagoya", "nanyang", "zhengzhou", "hyderabad", "surabaya", "hangzhou", "johannesburg",
             "quanzhou", "taipei", "dongguan", "bandung", "hanoi", "shenyang", "baghdad", "onitsha",
             "ahmedabad", "luanda", "dallas", "pune", "nanjing", "boston", "santiago",
             "riyadh", "dusseldorf", "madrid", "toronto", "surat"}
YES = {"yes", "yea", "yup", "yep", "i do", "yeah", "a little", "sure", "of course", "i have", "i am", "sometimes", "too", "as well", "also", "agree","good", "keep","why not", "ok", "okay", "fine", "continue", "go on","definitely"}
NO = {"no", "nope", "dont", "nothing","nuh","not"}

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
df.add_system_transition(State.START, State.START_TRAVEL,'"Now we are all going through a tough time. We should all stay at home and stay safe and healthy. But it is still nice to think about where we might travel to in the future. Do you like to travel?"')
#df.add_system_transition(State.START_TRAVEL, State.ASK_TRAVEL,'"I was planning to travel to"$city={seattle, houston, atlanta}". However, because of the global pandemic, I had to cancel my travel plan. I was curious about this. Which city do you wanna try to after everything gets better?"')

# User Turn
df.add_user_transition(State.START_TRAVEL,State.TRAVEL_N,'[{#CATCH_NO(), hate, worst, dislike, tired}]')
df.add_user_transition(State.START_TRAVEL, State.TRAVEL_Y, '[{#CATCH_YES(), love, like, favorite, hobby, best, said}]')
# df.add_user_transition(State.START, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.START, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
df.add_user_transition(State.START_TRAVEL, State.ROBOT, '[{robot, bot}]')
# Error Transition
df.set_error_successor(State.START_TRAVEL, State.TRAVEL_Y)
# df.add_system_transition(State.START, State.START, NULL)
df.set_error_successor(State.START, State.START)
# df.add_system_transition(State.START, State.START, NULL)

# System Turn
df.add_system_transition(State.ROBOT, State.END,'"i can be a robot, but I am also your companion and I do have my own preferences. why would you want an emotionless machine when you have me? "')
df.add_system_transition(State.TRAVEL_Y, State.ASK_TRAVEL, '"Yay! We share the same view on this. One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}". I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before?"')
df.add_system_transition(State.TRAVEL_N, State.END,'"Okay. I understand everyone has different ways of spending their leisure time. I also like to spend time with my loved ones at home. Location doesnt matter as long as we are having fun. "')
#df.add_system_transition(State.TRAVEL_Y, State.ASK_TRAVEL, '"Awesome! Last year, one of my friends went to"$city={seattle, houston, atlanta}"and she liked there very much. I know several wonderful cities to travel to in the United States. Which city do you want to go in the United States?"')

# User Turn
df.add_user_transition(State.ASK_TRAVEL, State.CITY_DISLIKE, '[{hate, worst, dislike, tired, hated, didnt}]')
df.add_user_transition(State.ASK_TRAVEL, State.CITY_NOT_TRAVELED, '[{#CATCH_NO(), havent, never}]')
df.add_user_transition(State.ASK_TRAVEL, State.CITY_TRAVELED, '[{#CATCH_YES(), love, like, favorite, hobby, best, good, hometown, grew up, work, live, here}]')
df.add_user_transition(State.ASK_TRAVEL, State.ROBOT, '[{robot, bot}]')
# df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY_DONTKNOW, '[{i dont know, have no idea, who knows, no, nope, not, no idea}]')
# df.add_user_transition(State.ASK_TRAVEL, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
df.set_error_successor(State.ASK_TRAVEL, State.CITY_NOT_TRAVELED)

# System Turn
df.add_system_transition(State.CITY_DISLIKE, State.CITY_RECOMMEND, '"Oh really? Maybe I should consider a different city. Do you have any city in mind that you would recommend me on going then?"')
df.add_system_transition(State.CITY_NOT_TRAVELED, State.CITY_DISCUSS, '"Oh thats fine. I love it because I heard that"#DETAIL(city, reason_for_travel)" I also love its food, culture, and I even know some of its tourist attractions. do you want to go there one day?"')
df.add_system_transition(State.CITY_TRAVELED, State.ASK_OPINION_REASON, '{Thats nice, Yay}"! then I can ask you opinions on this before I go. I heard that "#DETAIL(city, reason_for_travel)" Is that right?"')
# df.add_system_transition(State.ASK_TRAVEL_CITY, State.CITY_TOURISM, '{Nice choice, Good choice, Cool, Wonderful, Wow, Awesome}"! I love"$city"!"#DETAIL(city, brief_intro)"I am familiar with many aspects of this city, like tourist attraction, famous food, sports, events or the culture there. Would you like to know about the tourist attraction first?"')
# df.add_system_transition(State.ASK_TRAVEL_CITY_DONTKNOW, State.CITY_TOURISM, '"That\'s OK! One of my favorite cities is"$city={#RANDOM()}". do you want to talk about this city?"')
# df.add_system_transition(State.ASK_TRAVEL_CITY_UNKNOWN, State.CITY_TOURISM, '"Oops, I\'m not quite familiar with this city. One of my favorite cities is"$city={#RANDOM()}". do you want to talk about city"')
# df.add_system_transition(State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, State.CITY_TOURISM, '{Interesting, Cool, Wow, Awesome}".I heard"$city"is a good place to travel, but I know little about this place. One of my favorite cities is"$city={#RANDOM()}". do u want to talk about this city?"')

############################# Tourist Attraction Part ############################################################################################################
# User Turn
df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_NOT_SURE,'[{dont know, no idea, who knows, not sure, not quite sure}]')
df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_N, '[{#CATCH_NO(), havent, never}]')
df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_Y, '[{#CATCH_YES(), love, like, favorite, best, good}]')
df.add_user_transition(State.ASK_OPINION_REASON, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ASK_OPINION_REASON, State.REASON_NOT_SURE)

df.add_user_transition(State.CITY_DISCUSS,State.NOT_THE_CITY, '[{#CATCH_NO(), never}]')
df.add_user_transition(State.CITY_DISCUSS,State.OK_THE_CITY,'[{#CATCH_YES(), love, like, favorite, best, good, i would, maybe, might}]')
df.add_user_transition(State.CITY_DISCUSS, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.CITY_DISCUSS, State.OK_THE_CITY)


df.add_user_transition(State.CITY_RECOMMEND,State.CITY_RECOMMEND_N,'[{#CATCH_NO(), never}]')
df.add_user_transition(State.CITY_RECOMMEND,State.CITY_RECOMMEND_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would}]')
df.add_user_transition(State.CITY_RECOMMEND, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.CITY_RECOMMEND,State.CITY_RECOMMEND_N)
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_Y, '[{#CATCH_YES(),tourist attraction, tourist, tourism, attraction, tour}]')
# df.add_user_transition(State.CITY_TOURISM, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_TOURISM, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# df.add_user_transition(State.CITY_TOURISM, State.ASK_TRAVEL_CITY_DONTKNOW, '[[{no, nope, dont, nuh}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
# df.set_error_successor(State.CITY_TOURISM, State.CITY_TOURISM_UNKNOWN)
# df.set_error_successor(State.CITY_TOURISM, State.CITY_TOURISM_CERTAIN_N)

# System Turn
#df.add_system_transition(State.CITY_TOURISM_Y, State.CITY_TOURISM_CERTAIN, '"Good choice! I know several famous tourist attraction in"$city",Like"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}".Would you like to know more detail about this tourist attraction?"')
df.add_system_transition(State.REASON_NOT_SURE,State.FOOD_OPINION, '"Ah ok. I will take that into consideration. Thanks! I also want to try out the food there. i know their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}" If you have tried it there, did you like it?"')
df.add_system_transition(State.REASON_N,State.CITY_RECOMMEND, '"Oh no, thats sad. I wanted to go because of that. Do you have any city in mind that you would recommend me on going then?"')
df.add_system_transition(State.REASON_Y,State.ATTRACTION_OPINION,'"Good to know! I know they have "$tourism={#RANDOM_TOURISM(city, tourist_attraction)}" which is quite popular. I actually wanna go there. Would you recommend the place?"')
df.add_system_transition(State.NOT_THE_CITY, State.FOOD_RECOMMEND,'"Ah thats okay. After all, it is better for us to stay home for now. One of my favorite cities also includes "$city={seattle, new york}", because"#DETAIL(city, reason_for_travel)" but it is undergoing a huge crisis right now. I hope everything will get better soon. Besides, I love their "$food={#RANDOM_FOOD(city, famous_food)}". Would you like to try that there one day."')
df.add_system_transition(State.OK_THE_CITY,State.FOOD_RECOMMEND,'"Yay! We have the same wishes now! But I bet I know more about this city than you do. For example, i know their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}". You should definitely try if you go there one day!"')
df.add_system_transition(State.CITY_RECOMMEND_N,State.END,'"Well thats fine. I am sure both of us will find a place that each will enjoy. "')
df.add_system_transition(State.CITY_RECOMMEND_Y,State.USER_REC_CITY,'"Thanks for your recommendation！I will take that into consideration. Do you want to tell me more about the city?"')
# df.add_system_transition(State.CITY_TOURISM_UNKNOWN, State.CITY_TOURISM, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like tourist attraction there?"')

# User Turn
df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_D,'[{dont know, no idea, who knows, not sure, not quite sure, never been}]')
df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_N,'[{#CATCH_NO(), never, shouldnt}]')
df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine}]')
df.add_user_transition(State.ATTRACTION_OPINION, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_D)

df.add_user_transition(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_N, '[{#CATCH_NO(), never, shouldnt, wont, wouldnt}]')
df.add_user_transition(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_Y, '[{#CATCH_YES(), love, like, favorite, best, good, i would, fine, delicious, tasty, maybe}]')
df.add_user_transition(State.FOOD_RECOMMEND, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_N)

df.add_user_transition(State.FOOD_OPINION,State.FOOD_NOT_KNOW,'[{dont know, no idea, who knows, not sure, not quite sure, never been, never tried, never had it}]')
df.add_user_transition(State.FOOD_OPINION,State.FOOD_DISLIKE,'[{#CATCH_NO(), never, shouldnt, wont, wouldnt, didnt, hated, not that good}]')
df.add_user_transition(State.FOOD_OPINION,State.FOOD_LIKE,'[{#CATCH_YES(), love, like, favorite, best, good, i would, delicious, tasty, maybe, great, good, wonderful, should be}]')
df.add_user_transition(State.FOOD_OPINION,State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.FOOD_OPINION,State.FOOD_NOT_KNOW)

df.add_user_transition(State.USER_REC_CITY, State.USER_REC_ANSWER,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine, delicious, tasty, maybe, temperature, weather, beach, culture, event, people, nice}]')
df.add_user_transition(State.USER_REC_CITY, State.USER_REC_NO,'[{#CATCH_NO(), dont want to}]')
df.add_user_transition(State.USER_REC_CITY, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.USER_REC_CITY, State.USER_REC_NO)

# df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_N, '[#CATCH_NO()]')
# df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_Y, '[#CATCH_YES()]')
# # df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.set_error_successor(State.CITY_TOURISM_CERTAIN, State.CITY_TOURISM_CERTAIN_N)

# System Turn
df.add_system_transition(State.USER_REC_ANSWER, State.END,'"Nice nice! I will definitely look into it. Thanks again! "')
df.add_system_transition(State.USER_REC_NO, State.END,'"Ok but still thanks again! "')
df.add_system_transition(State.ATTRACTION_OPINION_Y,State.FOOD_OPINION, '"Nice! I will definitely go one day once everything is fine. I also want to try out the food there. i know their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}". "$food","#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')
df.add_system_transition(State.ATTRACTION_OPINION_N,State.FOOD_OPINION, '"Ah ok. I will take that into consideration. Thanks! I also want to try out the food there. i know their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}". "$food","#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')
df.add_system_transition(State.ATTRACTION_OPINION_D,State.FOOD_OPINION, '"Okay, thats fine. I also want to try out the food there. i know their popular cuisines such as"$food={#RANDOM_FOOD(city, famous_food)}". "$food","#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')

df.add_system_transition(State.FOOD_RECOMMEND_Y,State.ATTRACTION_RECOMMEND, '"Good to know! I also know they have the tourist attraction"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}"which is quite popular. I actually wanna go there. "$tourism","#DETAIL(city, tourist_attraction, tourism)" Would you consider this could be a good place to visit?"' )
df.add_system_transition(State.FOOD_RECOMMEND_N,State.ATTRACTION_RECOMMEND,'"haha thats fine. maybe we dont share the same taste. but I also know they have the tourist attraction"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}"which is quite popular. I actually wanna go there. "$tourism","#DETAIL(city, tourist_attraction, tourism)" Would you consider this could be a good place to visit?"' )
# df.add_system_transition(State.CITY_TOURISM_CERTAIN_N, State.CITY_FOOD, '{Alright, Ok, Then}".I also know lots of famous food in"$city". Would you like to talk about the famous food in this city?"')
# df.add_system_transition(State.CITY_TOURISM_CERTAIN_Y, State.CITY_FOOD, '{Nice choice,Good choice, Wonderful,Awesome}"!"$tourism","#DETAIL(city, tourist_attraction, tourism)"I also know lots of famous food in"$city". Would you like to talk about it?"')

df.add_system_transition(State.FOOD_NOT_KNOW,State.END,'"oh ok. I will try by myself then. Hope it will turn out to be good. "')
df.add_system_transition(State.FOOD_LIKE,State.END,'"Awesome, I have found the right person to ask! I will try once I get there. "')
df.add_system_transition(State.FOOD_DISLIKE, State.END,'"oh no. that’s ok. i will look for something else to eat then. "')
############################# Famous Food Part #####################################################################################################################
# User Turn
df.add_user_transition(State.ATTRACTION_RECOMMEND,State.ATTRACTION_RECOMMEND_N,'[{#CATCH_NO(), never, shouldnt, wont, wouldnt, not really, else, elsewhere}]')
df.add_user_transition(State.ATTRACTION_RECOMMEND,State.ATTRACTION_RECOMMEND_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine}]')
df.add_user_transition(State.ATTRACTION_RECOMMEND, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ATTRACTION_RECOMMEND, State.ATTRACTION_RECOMMEND_N)
# df.add_user_transition(State.CITY_FOOD, State.CITY_FOOD_Y, '[#CATCH_YES()]')
# # df.add_user_transition(State.CITY_FOOD, State.CITY_FOOD_CERTAIN_N, '[[{no, nope, dont}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_FOOD, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_FOOD, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# # df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
# df.set_error_successor(State.CITY_FOOD, State.CITY_FOOD_CERTAIN_N)

# System Turn
df.add_system_transition(State.ATTRACTION_RECOMMEND_N,State.END, '"Well, thats fine. We can still enjoy some events and celebrations there. after all, people are the most fun. "')
df.add_system_transition(State.ATTRACTION_RECOMMEND_Y,State.END, '"Thanks for you suggestion. Maybe I will go one day. and I know we have similar tastes. My friend recommended the event "$rec_event={#RANDOM_EVENT(city, event)}" to me. I would like to check it out."')
# df.add_system_transition(State.CITY_FOOD_Y, State.CITY_FOOD_CERTAIN, '"I like food! There are lots of famous food in"$city",Like"$food={#RANDOM_FOOD(city, famous_food)}".Would you like to know more detail about it?"')
# df.add_system_transition(State.CITY_FOOD_UNKNOWN, State.CITY_FOOD, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like famous food there?"')

# # User Turn
# df.add_user_transition(State.CITY_FOOD_CERTAIN, State.CITY_FOOD_CERTAIN_N, '[#CATCH_NO()]')
# df.add_user_transition(State.CITY_FOOD_CERTAIN, State.CITY_FOOD_CERTAIN_Y, '[#CATCH_YES()]')
# df.set_error_successor(State.CITY_FOOD_CERTAIN, State.CITY_FOOD_CERTAIN_N)

# # System Turn
# df.add_system_transition(State.CITY_FOOD_CERTAIN_N, State.CITY_SPORTS, '{Alright, Ok, Then}".I also know a little sports information in"$city".Would you like to listen? or do you want to talk about something else other than cities, like music, movie, pet, etc."')
# df.add_system_transition(State.CITY_FOOD_CERTAIN_Y, State.CITY_SPORTS, '$food","#DETAIL(city, famous_food, food)"I also know a little sports information in"$city".Would you like to listen?"')

# ############################ Sports Part ###########################################################################################################################
# # User Turn

# df.add_user_transition(State.CITY_SPORTS, State.CITY_SPORTS_Y, '[#CATCH_YES()]')
# # df.add_user_transition(State.CITY_SPORTS, State.CITY_SPORTS_N, '[[{no, nope, dont}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_SPORTS, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_SPORTS, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# # df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
# df.set_error_successor(State.CITY_SPORTS, State.CITY_SPORTS_N)

# # System Turn
# df.add_system_transition(State.CITY_SPORTS_N, State.CITY_EVENTS, '{Alright, Ok, Then}".Besides sports, there are also some interesting events in"$city".Would you like to know one?"')
# df.add_system_transition(State.CITY_SPORTS_Y, State.CITY_EVENTS, '{Nice,Good, Wonderful,Awesome,Great}"!"#DETAIL(city, sports)"Besides sports, there are also some interesting events in"$city".Would you like to know one?"')

# ############################# Events Part ##########################################################################################################################
# # User Turn
# df.add_user_transition(State.CITY_EVENTS, State.CITY_EVENTS_Y, '[#CATCH_YES()]')
# # df.add_user_transition(State.CITY_EVENTS, State.CITY_EVENTS_CERTAIN_N, '[[{no, nope, dont}] #NOT(know, idea)]')
# df.add_user_transition(State.CITY_EVENTS, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_EVENTS, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# # df.add_user_transition(State.CITY_TOURISM, State.CITY_TOURISM_DONTKNOW, '[{i dont know, have no idea, who knows}]')
# df.set_error_successor(State.CITY_EVENTS, State.CITY_EVENTS_CERTAIN_N)

# # System Turn
# df.add_system_transition(State.CITY_EVENTS_Y, State.CITY_EVENTS_CERTAIN, '{Nice choice,Good choice}"! I enjoy festivals and events! There are different events in"$city",Like"$event={#RANDOM_EVENT(city, event)}".Would you like to know more detail about it?"')
# df.add_system_transition(State.CITY_EVENTS_UNKNOWN, State.CITY_EVENTS, '"Interesting. I am not quite familiar with this aspect of"$city"What about talking about something that I know, like interesting events there?"')

# # User Turn
# df.add_user_transition(State.CITY_EVENTS_CERTAIN, State.CITY_EVENTS_CERTAIN_Y, '[{yes, yea, yup, yep, i do, yeah, a little, sure, of course, i have, i am, sometimes, too, as well, also, agree, ok, fine, okay, famous food, food}]')
# # df.add_user_transition(State.CITY_TOURISM_CERTAIN, State.CITY_EVENTS_CERTAIN_N, '[{no, nope, dont}]')
# df.add_user_transition(State.CITY_EVENTS_CERTAIN, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.set_error_successor(State.CITY_EVENTS_CERTAIN, State.CITY_EVENTS_CERTAIN_N)

# # System Turn
# df.add_system_transition(State.CITY_EVENTS_CERTAIN_N, State.CITY_CULTURE, '{Alright, Ok, Then}".I am also familiar with the culture in"$city". Would you like to know about it?"')
# df.add_system_transition(State.CITY_EVENTS_CERTAIN_Y, State.CITY_CULTURE, '{Nice,Good,Great, Cool,Wonderful,Awesome}"!"$event","#DETAIL(city, event, event)"I am also familiar with the culture in"$city".Would you like to know about it?"')

# ############################# Culture Part #########################################################################################################################
# # User Turn
# df.add_user_transition(State.CITY_CULTURE, State.CITY_CULTURE_Y, '[#CATCH_YES()]')
# df.add_user_transition(State.CITY_CULTURE, State.ASK_TRAVEL_CITY, '[$city=#CATCH()]')
# df.add_user_transition(State.CITY_CULTURE, State.ASK_TRAVEL_CITY_UNKNOWN_INLIST, '[$city=#CATCH_CITY_LIST()]')
# df.set_error_successor(State.CITY_CULTURE, State.CITY_CULTURE_N)

# # System Turn
# df.add_system_transition(State.CITY_CULTURE_Y, State.CITY_REASON, '{Nice,Good, Great, Cool,Wonderful,Awesome}"!About the"$certain_culture={#RANDOM_CULTURE(city,culture)}","#DETAIL(city, culture, certain_culture)"So, why do you want to travel to"$city"?"')
# df.add_system_transition(State.CITY_CULTURE_N, State.CITY_REASON, '{Alright, Ok, Then}"So, why do you want to travel to"$city"?"')

# ############################# Travel Reason ##########################################################################################################
# # User Turn
# df.add_user_transition(State.CITY_REASON, State.CITY_REASON_NEGATIVE,'[#CATCH_NO()]')
# df.add_user_transition(State.CITY_REASON, State.CITY_REASON_POSITIVE, '[{interesting, beautiful, weather,love,temperature,like,good,nice}]')
# df.set_error_successor(State.CITY_REASON, State.CITY_REASON_UNKNOWN)

# # System Turn
# df.add_system_transition(State.CITY_REASON_POSITIVE, State.END, '{Nice,Good, Great, Cool,Wonderful,Awesome, I agree}"!I have to say"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')
# df.add_system_transition(State.CITY_REASON_NEGATIVE, State.END, '{Alright, Ok, Then}".But I think"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')
# df.add_system_transition(State.CITY_REASON_UNKNOWN, State.END, '{Interesting, I see}".In my opinion, I think"$city"is a wonderful city which is worth traveling to because it"#DETAIL(city, reason_for_travel)"!"')

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
    #df.precache_transitions()
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=True)