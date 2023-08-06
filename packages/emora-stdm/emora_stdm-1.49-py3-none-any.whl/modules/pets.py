from emora_stdm import DialogueFlow, Macro
from enum import Enum
import json, os
import random

# Xiangjue Dong
# 3/21/2020

# States are typically represented as an enum
class State(Enum):

    START = 0
    START_PET = 1
    END = 2
    PETS_Y = 3
    ASK_PETS = 4
    ASK_PETS_Y = 5
    ASK_PETS_N = 6

    FIRST_PET = 10
    FIRST_PET_DOG = 11
    FIRST_PET_DOG_ANS = 12
    FIRST_PET_DOG_UNKNOWN = 13
    FIRST_PET_DOG_BREED = 14
    FIRST_PET_DOG_BREED_ANS = 15
    FIRST_PET_DOG_NAME = 16
    FIRST_PET_DOG_NAME_KNOWN = 17
    FIRST_PET_DOG_NAME_UNKNOWN = 18
    FIRST_PET_DOG_FOOD = 19
    FIRST_PET_DOG_FOOD_Y = 20
    FIRST_PET_DOG_FOOD_N = 211
    FIRST_PET_DOG_FOOD_USER = 212

    FIRST_PET_CAT = 21
    FIRST_PET_CAT_ANS = 22
    FIRST_PET_CAT_UNKNOWN = 23
    FIRST_PET_CAT_BREED = 24
    FIRST_PET_CAT_BREED_ANS = 25
    FIRST_PET_CAT_NAME = 26
    FIRST_PET_CAT_NAME_KNOWN = 27
    FIRST_PET_CAT_NAME_UNKNOWN = 28
    FIRST_PET_CAT_FOOD = 29
    FIRST_PET_CAT_FOOD_Y = 30
    FIRST_PET_CAT_FOOD_N = 221
    FIRST_PET_CAT_FOOD_USER = 222

    FIRST_PET_OTHER = 31
    FIRST_PET_OTHER_ANS = 32
    FIRST_PET_OTHER_UNKNOWN = 33
    FIRST_PET_OTHER_BREED = 34
    FIRST_PET_OTHER_NAME = 35
    FIRST_PET_OTHER_NAME_KNOWN = 36
    FIRST_PET_OTHER_NAME_UNKNOWN= 37
    FIRST_PET_OTHER_FOOD = 38

    NO_PETS = 40
    NO_PETS_Y = 41
    NO_PETS_N = 42
    NO_PETS_DAD = 43
    NO_PETS_DAD_ANS = 44
    NO_PETS_DAD_ANS_ANS = 45
    NO_PETS_UNKNOWN = 46

    FAVORITE_PET = 50
    FAVORITE_PET_UNKNOWN = 51
    FAVORITE_PET_DONTKNOW = 150

    FAVORITE_PET_DOG = 52
    FAVORITE_PET_DOG_ANS = 53
    FAVORITE_PET_DOG_BREED = 54
    FAVORITE_PET_DOG_UNKNOWN = 55
    FAVORITE_PET_DOG_DONTKNOW = 56
    FAVORITE_PET_DOG_DONTKNOW_ANS = 57

    FAVORITE_PET_CAT = 62
    FAVORITE_PET_CAT_ANS = 63
    FAVORITE_PET_CAT_BREED = 64
    FAVORITE_PET_CAT_UNKNOWN = 65
    FAVORITE_PET_CAT_DONTKNOW = 66
    FAVORITE_PET_CAT_DONTKNOW_ANS = 67

    FAVORITE_PET_OTHER = 72
    FAVORITE_PET_OTHER_ANS = 73
    FAVORITE_PET_OTHER_BREED = 74
    FAVORITE_PET_OTHER_UNKNOWN = 75
    FAVORITE_PET_OTHER_DONTKNOW = 76

    DOG_INTERESTING = 80
    DOG_INTERESTING_Y = 81
    DOG_INTERESTING_N = 82
    DOG_INTERESTING_OTHER = 83

    CAT_INTERESTING = 90
    CAT_INTERESTING_Y = 91
    CAT_INTERESTING_N = 92
    CAT_INTERESTING_OTHER = 93

    OTHER_INTERESTING = 100
    OTHER_INTERESTING_Y = 101
    OTHER_INTERESTING_N = 102
    OTHER_INTERESTING_OTHER = 103

    DOG_MOVIE = 110
    DOG_MOVIE_Y = 111
    DOG_MOVIE_N = 112
    DOG_MOVIE_DETAIL = 113
    DOG_MOVIE_ANOTHER_Y = 114
    DOG_MOVIE_ANOTHER_N = 115

    CAT_MOVIE = 120
    CAT_MOVIE_Y = 121
    CAT_MOVIE_N = 122
    CAT_MOVIE_DETAIL = 123
    CAT_MOVIE_ANOTHER_Y = 124
    CAT_MOVIE_ANOTHER_N = 125

    OTHER_MOVIE = 130
    OTHER_MOVIE_Y = 131
    OTHER_MOVIE_N = 132
    OTHER_MOVIE_DETAIL = 133
    OTHER_MOVIE_ANOTHER_Y = 134
    OTHER_MOVIE_ANOTHER_N = 135

    ANOTHER_DOG_BREED = 140
    ANOTHER_DOG_BREED_Y = 141
    ANOTHER_DOG_BREED_N = 142
    ANOTHER_DOG_BREED_DETAIL = 143

    ANOTHER_CAT_BREED = 150
    ANOTHER_CAT_BREED_Y = 151
    ANOTHER_CAT_BREED_N = 152
    ANOTHER_CAT_BREED_DETAIL = 153

    PETS_PROS = 160
    PETS_PROS_DB = 161
    PETS_PROS_N = 162
    PETS_PROS_UNKNOWN = 163


class CATCH(Macro):
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


class RANDOM(Macro):
    """Generate random information from database.

    Attributes:
        path: Path of database.
        db_keys: Keys of database.
    """

    def __init__(self, path):
        """Inits RANDOM_BREED with path and db_keys"""
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        """Performs operation"""
        name = 'db_keys'+self.path
        if len(args) == 0:
            if vars.get(name) is None or len(vars[name]) == 0:
                vars[name] = list(self.db.keys())
            key = random.choice(vars[name])
            vars[name].remove(key)
            return key

        elif len(args) == 1:
            if vars.get(name) is None or len(vars[name]) <= 1:
                vars[name] = list(self.db.keys())
            if vars[args[0]] in vars[name]:
                vars[name].remove(vars[args[0]])
            key = random.choice(vars[name])
            vars[name].remove(key)
            return key

        elif len(args) == 2:
            return self.db[vars[args[1]]]


class EMORA(Macro):
    """Generate EMORA preferences."""

    def run(self, ngrams, vars, args):
        """Performs operation"""
        if vars[args[0]] in ("cat", "cats"):
            response = "my favorite cat is toyger."
        elif vars[args[0]] in ("dog", "dogs"):
            response = "my favorite dog is german shepherd."
        elif vars[args[0]] in ("pet", "pets"):
            response = "my favorite pet is a german shepherd dog."
        else:
            response = "my favorite pet is a german shepherd dog."

        return response


class INTERESTING(Macro):
    """Generate interesting facts from database.

    Attributes:
        path: Path of database.
        db_backup: Copy of database.
    """

    def __init__(self, path):
        """Inits INTERESTING with path and db_backup"""
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        """Performs operation"""
        db_backup = self.db.copy()
        name = 'db' + self.path
        if vars.get(name) is None or len(vars[name]) == 0:
            vars[name] = db_backup
        response = random.choice(vars[name])
        vars[name].remove(response)

        return response


class BREED_DESC(Macro):
    """Generate breed information from database.

    Attribute:
        path: Path of database.
    """

    def __init__(self, path):
        """Inits BREED_DESC with path"""
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        """Performs operation"""
        return self.db[vars[args[0]]]


class BREED(Macro):
    """Generate breed name from database.

    Attributes:
        path: Path of database.
        db: Database.
    """

    def __init__(self, path):
        """Inits BREED with path"""
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        """Performs operation"""
        return ngrams & self.db.keys()

# Variables
TRANSITION_OUT = ["movies", "movie", "music", "sports", "sport", "travel"]
NULL = "NULL TRANSITION"
PET_TYPE = {"dog", "dogs", "puppies", "puppy", "kitties", "kitty", "cat", "cats", "pet", "pets", "animal", "animals"}
NAME = {"alex","max","charlie","cooper","buddy","rocky","milo","jack","bear","duke","teddy","oliver","bentley","tucker","beau","leo","toby","jax","zeus","winston","blue","finn","louie","ollie","murphy","gus","moose",
        "jake","loki","dexter","hank","bruno","apollo","buster","thor","bailey","gunnar","lucky","diesel","harley","henry","koda","jackson","riley", "ace", "oscar","chewy","bandit","baxter","scout","jasper",
        "maverick","sam","cody","gizmo","shadow","simba","rex","brody","tank","marley","otis","remi","remy","roscoe","rocco","sammy","cash","boomer","prince","benji","benny","archie","chance","ranger","ziggy",
        "luke","george","oreo","hunter","rusty","king","odin","coco","frankie","tyson","chase","theo","romeo","bruce","rudy","zeke","kobe","peanut","joey","oakley","chico","mac","walter","brutus","samson","bella",
        "luna","lucy","daisy","lily","zoe","lola","molly","sadie","bailey","stella","maggie","roxy","sophie","chloe","penny","coco","nala","rosie","ruby","gracie","ellie","mia","piper","callie","abby","lexi","ginger",
        "lulu","pepper","willow","riley","millie","harley","sasha","lady","izzy","layla","charlie","dixie","maya","annie","kona","hazel","winnie","olive","princess","emma","athena","nova","belle","honey","ella",
        "marley","cookie","maddie","remi","remy","phoebe","scout","minnie","dakota","holly","angel","josie","leia","harper","ava","missy","mila","sugar","shelby","poppy","blue","mocha","cleo","penelope","ivy","peanut",
        "fiona","xena","gigi","sandy","bonnie","jasmine","baby","macy","paisley","shadow","koda","pearl","skye","delilah","nina","trixie","charlotte","aspen","arya","diamond","georgia","dolly"}
YES = {"yes", "yea", "yup", "yep", "i do", "yeah", "a little", "sure", "of course", "i have", "i am", "sometimes", "too", "as well", "also", "agree","good", "keep","why not", "ok", "okay", "fine", "continue", "go on"}
NO = {"no", "nope", "dont", "nothing"}


# Functions
cat_breed = os.path.join('modules','cat_breed_database.json')
dog_breed = os.path.join('modules','dog_breed_database.json')
other_breed = os.path.join('modules','other_breed_database.json')
cat_movie = os.path.join('modules','cat_movie_database.json')
dog_movie = os.path.join('modules','dog_movie_database.json')
other_movie = os.path.join('modules','other_movie_database.json')
cat_interesting = os.path.join('modules','cat_interesting_database.json')
dog_interesting = os.path.join('modules','dog_interesting_database.json')
other_interesting = os.path.join('modules','other_interesting_database.json')
cat_food = os.path.join('modules','cat_food_database.json')
dog_food = os.path.join('modules','dog_food_database.json')
pet_pros = os.path.join('modules','pets_pros.json')

macros = {
    'DOG_BREED': BREED(dog_breed),
    'DOG_BREED_DESC': BREED_DESC(dog_breed),
    'CAT_BREED': BREED(cat_breed),
    'CAT_BREED_DESC': BREED_DESC(cat_breed),
    'OTHER_BREED': BREED(other_breed),
    'OTHER_BREED_DESC': BREED_DESC(other_breed),
    'CATCH_PET_TYPE':CATCH(PET_TYPE),
    'CATCH_YES':CATCH(YES),
    'CATCH_NO':CATCH(NO),
    'EMORA':EMORA(),
    'DOG_INTERESTING':INTERESTING(dog_interesting),
    'CAT_INTERESTING':INTERESTING(cat_interesting),
    'OTHER_INTERESTING':INTERESTING(other_interesting),
    'DOG_MOVIE':RANDOM(dog_movie),
    'CAT_MOVIE':RANDOM(cat_movie),
    'OTHER_MOVIE':RANDOM(other_movie),
    'DOG_MOVIE_DESC': BREED_DESC(dog_movie),
    'CAT_MOVIE_DESC': BREED_DESC(cat_movie),
    'OTHER_MOVIE_DESC':BREED_DESC(other_movie),
    'DOG_RANDOM_BREED': RANDOM(dog_breed),
    'CAT_RANDOM_BREED': RANDOM(cat_breed),
    'OTHER_RANDOM_BREED': RANDOM(other_breed),
    'DOG_FOOD': RANDOM(dog_food),
    'CAT_FOOD': RANDOM(cat_food),
    'CATCH_DOG_FOOD':BREED(dog_food),
    'CATCH_CAT_FOOD':BREED(cat_food),
    'CATCH_DOG_FOOD_DESC': BREED_DESC(dog_food),
    'CATCH_CAT_FOOD_DESC': BREED_DESC(cat_food),
    'NAME':CATCH(NAME),
    'CATCH_PROS':BREED(pet_pros),
    'CATCH_PROS_DESC':BREED_DESC(pet_pros)
}

###################### Initialization Part ####################################################################################################################
# Initialize the DialogueFlow object, which uses a state-machine to manage dialogue
# Each user turn should consider error transition
df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.USER, macros=macros)

# For dialogue manager initialization
# test
# df.add_user_transition(State.START, State.START_PET, 'test')
df.add_system_transition(State.START_PET, State.ASK_PETS, '"So, do you have any pets at home? like a"$breed={dog, cat}"?"')

# df.add_user_transition(State.START, State.ASK_PETS_Y, '[{pet, pets}]')
# df.add_user_transition(State.START, State.ASK_PETS_Y, '[![!i have] {pet, pets}]')
# df.add_user_transition(State.START, State.FIRST_PET_ANS, '[![!i, have] {dog, dogs, cat, cats}]')
# df.add_user_transition(State.START, State.ASK_PETS_N, '[![!i, dont, have] {dog, dogs}]') # This didn't work well with next line at the same time

# User Turn
df.add_user_transition(State.START, State.PETS_Y, '[$breed={#OTHER_BREED(),#DOG_BREED(),#CAT_BREED(),#CATCH_PET_TYPE()}]')
# df.add_user_transition(State.START, State.PETS_Y_1, '[$breed=#DOG_BREED()]')
# df.add_user_transition(State.START, State.PETS_Y_2, '[$breed=#CAT_BREED()]')

# Error Transition
df.set_error_successor(State.START, State.START)
df.add_system_transition(State.START, State.START, NULL)

# df.add_system_transition(State.START_PET, State.START_PET_Q, '"I like pets very much, especially dogs. Do you want to talk about pets?"')
# df.add_user_transition(State.START_PET_Q, State.PETS_Y, '[{yes, yea, yup, yep, i do, yeah, a little, sure, of course, i have, i am, sometimes, too, as well, also, agree}]')
# df.add_user_transition(State.START_PET_Q, State.NO_NO_PETS_NO, '[{no, nope, dont}]')

###################### Pet Opening Part ###########################################################################################################################
# System Turn
df.add_system_transition(State.PETS_Y, State.ASK_PETS, '"That\'s great! I love" $breed "! actually, " #EMORA(breed) "Do you have any pets at your home now?"')
# df.add_system_transition(State.PETS_Y_1, State.ASK_PETS, '"That\'s cool! I love" $breed "! actually, " #EMORA(breed) "Do you have any pets at your home now?"')
# df.add_system_transition(State.PETS_Y_2, State.ASK_PETS, '"Sounds cool! I love" $breed "! actually, " #EMORA(breed) "Do you have any pets at your home now?"')

df.add_user_transition(State.ASK_PETS, State.ASK_PETS_Y, '[![{yes, yea, yup, yep, i do, yeah, a little, sure, of course, i have, i am, sometimes, too, as well, also, agree, ok, okay, good, keep, why}] #NOT(no, dont, nope, dog, dogs, cat, cats, pet, pets)]')

# User Turn
# df.add_user_transition(State.ASK_PETS, State.ASK_PETS_N, '[[{no, nope, dont}] -{know, idea}]')
df.add_user_transition(State.ASK_PETS, State.ASK_PETS_N, '[[{no, nope, dont,allergic,allergy}] #NOT(know, idea)]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_DOG, '[!-{dont, not}[{dog, dogs}]]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_CAT, '[!-{dont, not}[{cat, cats}]]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_OTHER, '[{other, others}]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_OTHER_BREED, '[$breed=#OTHER_BREED()]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_DOG_BREED, '[$breed=#DOG_BREED()]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_CAT_BREED, '[$breed=#CAT_BREED()]')
df.add_user_transition(State.ASK_PETS, State.FAVORITE_PET_DOG_DONTKNOW, '[{i dont know, i have no idea, who knows}]')

# Error transition
# df.set_error_successor(State.ASK_PETS, State.FIRST_PET_OTHER_UNKNOWN)
df.set_error_successor(State.ASK_PETS, State.NO_PETS_Y)

# df.add_system_transition(State.ASK_PETS_UNKNOWN, State.ASK_PETS_UNKNOWN_ANS, '"Sorry, I was sleeping just now. What did you mean? If you mean you have a pet, what is it? If you mean you don\'t have a pet, would you like to know something about the pets?"')
# df.add_user_transition(State.ASK_PETS_UNKNOWN_ANS, State.FIRST_PET_DOG, '[$breed=#DOG_BREED()]')
# df.add_user_transition(State.ASK_PETS_UNKNOWN_ANS, State.FIRST_PET_CAT, '[$breed=#CAT_BREED()]')
# df.add_user_transition(State.ASK_PETS_UNKNOWN_ANS, State.FIRST_PET_OTHER, '[$breed=#OTHER_BREED()]')
# df.set_error_successor(State.ASK_PETS_UNKNOWN_ANS, State.ASK_PETS_UNKNOWN)

df.add_system_transition(State.ASK_PETS_Y, State.ASK_PETS, '"Cool! What is it? A cat or a dog?"')
# df.add_user_transition(State.FIRST_PET, State.FIRST_PET_DOG, '[{dog, dogs}]')
# df.add_user_transition(State.FIRST_PET, State.FIRST_PET_CAT, '[{cat, cats}]')
# df.add_user_transition(State.FIRST_PET, State.FIRST_PET_DOG_BREED_ANS, '[$breed=#DOG_BREED()]')
# df.add_user_transition(State.FIRST_PET, State.FIRST_PET_CAT_BREED_ANS, '[$breed=#CAT_BREED()]')
# df.add_user_transition(State.FIRST_PET, State.FIRST_PET_OTHER, '[$breed=#CATCH_PET_TYPE_OTHER()]')
# df.set_error_successor(State.FIRST_PET, State.FIRST_PET_OTHER_UNKNOWN)
# df.add_system_transition(State.FIRST_PET_UNKNOWN, State.FIRST_PET_NAME, '"Sorry, I\'m not quite familiar with this animal. But I would like to talk about it with you. Can you tell me more information of it? it must have a cute name. What is its name?"')

# System Turn
df.add_system_transition(State.ASK_PETS_N, State.NO_PETS, '"You don\'t have any pets? '
                                                          'Well, would you consider getting one? '
                                                          'They are pretty cute."')

df.add_user_transition(State.NO_PETS, State.NO_PETS_Y, '[#CATCH_YES()]')
df.add_user_transition(State.NO_PETS, State.NO_PETS_N, '[!-{why}[{no, nope, dont, nothing, not}]]')


# Error Transition
df.set_error_successor(State.NO_PETS, State.NO_PETS_UNKNOWN)

# System Turn
df.add_system_transition(State.NO_PETS_UNKNOWN, State.ANOTHER_DOG_BREED, '"I see..., but I know a lot about dogs. Would you like to know some information about breed of dogs, like" $another_breed={#DOG_RANDOM_BREED(breed)} "?"')

# User Turn
# df.add_user_transition(State.FAVORITE_PET_UNKNOWN_DOG, State.FAVORITE_PET_DOG, '[{yes, yea, yup, yep, i do, yeah, a little, sure, of course, i have, i am, sometimes, too, as well, also, agree, ok, okay}]')
# df.add_user_transition(State.FAVORITE_PET_UNKNOWN_DOG, State.NO_NO_PETS_NO, '[{no, nope, dont}]')
# df.set_error_successor(State.FAVORITE_PET_UNKNOWN_DOG, State.NO_NO_PETS_NO)

#################### Transition Part ###########################################################################################################################
# System Turn
df.add_system_transition(State.NO_PETS_N, State.ANOTHER_DOG_BREED, '"Oh ok, that\'s fine. It is indeed a big decision to introduce new members into your family or life. I know a lot about dogs. Although you won\'t keep a dog, would you like to know some information about dog breed, like" $another_breed={#DOG_RANDOM_BREED(breed)} "?"')

# User Turn
# df.add_user_transition(State.NO_NO_PETS, State.FAVORITE_PET_DOG, '[{yes, yea, yup, yep, i do, yeah, a little, sure, of course, i have, i am, sometimes, too, as well, also, agree, ok, okay}]')
# df.add_user_transition(State.NO_NO_PETS, State.NO_NO_PETS_NO, '[{no, nope, dont}]')

# Error Transition
# df.set_error_successor(State.NO_NO_PETS, State.NO_PETS_UNKNOWN)
# df.set_error_successor(State.NO_NO_PETS, State.NO_NO_PETS_NO)
# df.add_system_transition(State.NO_NO_PETS_NO, State.START, '"Ok, Ok. Then, what other topics do you want to talk about?"')
# df.set_error_successor(State.NO_NO_PETS, State.START_OTHER)
# df.add_user_transition(State.NO_NO_PETS, State.START_OTHER, TRANSITION_OUT)
# df.set_error_successor(State.NO_NO_PETS_YES, State.START_OTHER)
# df.set_error_successor(State.NO_NO_PETS_NO, State.START_OTHER)
# df.add_system_transition(State.NO_NO_PETS_YES, State.FAVORITE_PET, '"I like dogs best! Which do you want to talk about? Dogs or cats?"')

################## First Pet Part ################################################################################################################################
# System Turn
df.add_system_transition(State.FIRST_PET_DOG, State.FIRST_PET_DOG_ANS, '{Cool,Wonderful,Wow, Awesome}"! That\'s great! I like dogs! What is its breed?"')
df.add_system_transition(State.FIRST_PET_CAT, State.FIRST_PET_CAT_ANS, '{Cool,Wonderful,Wow, Awesome}"! That\'s great! I like cats! What is its breed?"')
df.add_system_transition(State.FIRST_PET_OTHER, State.FIRST_PET_OTHER_ANS, '{Cool,Wonderful,Wow, Awesome}"! That\'s interesting! What is it? A fish? a bird?"')

# User Turn
df.add_user_transition(State.FIRST_PET_DOG_ANS, State.FIRST_PET_DOG_BREED, '[$breed=#DOG_BREED()]')
df.add_user_transition(State.FIRST_PET_CAT_ANS, State.FIRST_PET_CAT_BREED, '[$breed=#CAT_BREED()]')
df.add_user_transition(State.FIRST_PET_OTHER_ANS, State.FIRST_PET_OTHER_BREED, '[$breed=#OTHER_BREED()]')

# Error Transition
df.set_error_successor(State.FIRST_PET_DOG_ANS, State.FIRST_PET_DOG_UNKNOWN)
df.set_error_successor(State.FIRST_PET_CAT_ANS, State.FIRST_PET_CAT_UNKNOWN)
df.set_error_successor(State.FIRST_PET_OTHER_ANS, State.FIRST_PET_OTHER_UNKNOWN)

# System Turn - Ask Name
df.add_system_transition(State.FIRST_PET_DOG_BREED, State.FIRST_PET_DOG_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting!" #DOG_BREED_DESC(breed) "I guess it must have a cute name. What is its name?"')
df.add_system_transition(State.FIRST_PET_CAT_BREED, State.FIRST_PET_CAT_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting!" #CAT_BREED_DESC(breed) "I guess it must have a cute name. What is its name?"')
df.add_system_transition(State.FIRST_PET_OTHER_BREED, State.FIRST_PET_OTHER_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting. " #OTHER_BREED_DESC(breed)"I guess it must have a cute name. What is its name?"')

df.add_system_transition(State.FIRST_PET_DOG_UNKNOWN, State.FIRST_PET_DOG_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting. Although I am not quite familiar with this dog breed, I guess it must have a cute name. What is its name?"')
df.add_system_transition(State.FIRST_PET_CAT_UNKNOWN, State.FIRST_PET_CAT_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting. Although I am not quite familiar with this cat breed, I guess it must have a cute name. What is its name?"')
df.add_system_transition(State.FIRST_PET_OTHER_UNKNOWN, State.FIRST_PET_OTHER_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting. Although I am not quite familiar with this kind of pets, I guess it must have a cute name. What is its name?"')

# User Turn
df.add_user_transition(State.FIRST_PET_DOG_NAME, State.FIRST_PET_DOG_NAME_KNOWN, '[$name=#NAME()]')
df.add_user_transition(State.FIRST_PET_CAT_NAME, State.FIRST_PET_CAT_NAME_KNOWN, '[$name=#NAME()]')
df.add_user_transition(State.FIRST_PET_OTHER_NAME, State.FIRST_PET_OTHER_NAME_KNOWN, '[$name=#NAME()]')

# Error Transition - Answer Name
df.set_error_successor(State.FIRST_PET_DOG_NAME, State.FIRST_PET_DOG_NAME_UNKNOWN)
df.set_error_successor(State.FIRST_PET_CAT_NAME, State.FIRST_PET_CAT_NAME_UNKNOWN)
df.set_error_successor(State.FIRST_PET_OTHER_NAME, State.FIRST_PET_OTHER_NAME_UNKNOWN)

######################### Pet Food Part ##############################################################################################
# System Turn - Ask Food
df.add_system_transition(State.FIRST_PET_DOG_NAME_KNOWN, State.FIRST_PET_DOG_FOOD, '"Oh!" $name ".That\'s a sweet name! If I had a dog, I would just named it puppy in a lazy way. You know, there are lots of food dogs cannot eat. Would you like to know about one, like" $food={#DOG_FOOD()}"?"')
df.add_system_transition(State.FIRST_PET_CAT_NAME_KNOWN, State.FIRST_PET_CAT_FOOD, '"Oh!" $name ".That\'s a sweet name! If I had a cat, I would just named it kitty in a lazy way. You know, there are lots of food cats cannot eat. Would you like to know about one, like" $food={#CAT_FOOD()} "?"')
df.add_system_transition(State.FIRST_PET_OTHER_NAME_KNOWN, State.FIRST_PET_OTHER_FOOD, '"Oh!" $name ".That\'s a sweet name! If I had a dog, I would just named it puppy in a lazy way. You know, there are lots of food dogs cannot eat. Would you like to know about one, like" $food={#DOG_FOOD()} "?"')

df.add_system_transition(State.FIRST_PET_DOG_NAME_UNKNOWN, State.FIRST_PET_DOG_FOOD, '"Interesting. If I had a dog, I would just named it puppy in a lazy way. You know, there are lots of food dogs cannot eat. Would you like to know about one, like" $food={#DOG_FOOD()} "?"')
df.add_system_transition(State.FIRST_PET_CAT_NAME_UNKNOWN, State.FIRST_PET_CAT_FOOD, '"Interesting. If I had a cat, I would just named it kitty in a lazy way. You know, there are lots of food cats cannot eat. Would you like to know about one, like" $food={#CAT_FOOD()} "?"')
df.add_system_transition(State.FIRST_PET_OTHER_NAME_UNKNOWN, State.FIRST_PET_DOG_FOOD, '"Interesting. If I had a dog, I would just named it puppy in a lazy way. You know, there are lots of food dogs cannot eat. Would you like to know about one, like" $food={#DOG_FOOD()} "?"')

# User Turn & Error Transition - Answer Food
# User Turn
df.add_user_transition(State.FIRST_PET_DOG_FOOD, State.FIRST_PET_DOG_FOOD_Y, '[#CATCH_YES()]')
df.add_user_transition(State.FIRST_PET_DOG_FOOD, State.FIRST_PET_DOG_FOOD_N, '[#CATCH_NO()]')

df.add_user_transition(State.FIRST_PET_CAT_FOOD, State.FIRST_PET_CAT_FOOD_Y, '[#CATCH_YES()]')
df.add_user_transition(State.FIRST_PET_CAT_FOOD, State.FIRST_PET_CAT_FOOD_N, '[#CATCH_NO()]')

df.add_user_transition(State.FIRST_PET_OTHER_FOOD, State.FIRST_PET_DOG_FOOD_Y, '[#CATCH_YES()]')
df.add_user_transition(State.FIRST_PET_OTHER_FOOD, State.FIRST_PET_DOG_FOOD_N, '[#CATCH_NO()]')

df.add_user_transition(State.FIRST_PET_DOG_FOOD, State.FIRST_PET_DOG_FOOD_USER, '[$food=#CATCH_DOG_FOOD()]')
df.add_user_transition(State.FIRST_PET_CAT_FOOD, State.FIRST_PET_CAT_FOOD_USER, '[$food=#CATCH_CAT_FOOD()]')

df.add_system_transition(State.FIRST_PET_DOG_FOOD_USER, State.FIRST_PET_DOG_FOOD, '"My pleasure." #CATCH_DOG_FOOD_DESC(food) "Would you like to know about a different food too, like" $food={#DOG_FOOD(food)} "?"')
df.add_system_transition(State.FIRST_PET_CAT_FOOD_USER, State.FIRST_PET_CAT_FOOD, '"My pleasure." #CATCH_CAT_FOOD_DESC(food) "Would you like to know about a different food too, like" $food={#CAT_FOOD(food)} "?"')

df.add_system_transition(State.FIRST_PET_DOG_FOOD_Y, State.FIRST_PET_DOG_FOOD, '{Nice choice,Good choice,My pleasure}"." #CATCH_DOG_FOOD_DESC(food) "Would you like to know about a different food too, like" $food={#DOG_FOOD(food)} "?"')
df.add_system_transition(State.FIRST_PET_CAT_FOOD_Y, State.FIRST_PET_CAT_FOOD, '{Nice choice,Good choice,My pleasure}"." #CATCH_CAT_FOOD_DESC(food) "Would you like to know about a different food too, like" $food={#CAT_FOOD(food)} "?"')

df.set_error_successor(State.FIRST_PET_DOG_FOOD, State.FIRST_PET_DOG_FOOD_N)
df.set_error_successor(State.FIRST_PET_CAT_FOOD, State.FIRST_PET_DOG_FOOD_N)

# System Turn - Transition to Another Dog and Cat Breed Introduction Part
df.add_system_transition(State.FIRST_PET_DOG_FOOD_N, State.ANOTHER_DOG_BREED, '{Ok, Alright, Then, Well}", Would you like to know some information about another breed of dogs, like" $another_breed={#DOG_RANDOM_BREED(breed)} "?"')
df.add_system_transition(State.FIRST_PET_CAT_FOOD_N, State.ANOTHER_CAT_BREED, '{Ok, Alright, Then, Well}", Would you like to know some information about another breed of cats, like" $another_breed={#CAT_RANDOM_BREED(breed)} "?"')

####################### Favorite Pet Part ##########################################################################################################################
# System Turn
df.add_system_transition(State.NO_PETS_Y, State.FAVORITE_PET, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! I suggest to adopt instead of buying. i love both dogs and cats. but they can be quite different. which one would you prefer to be your companion?"')

# User Turn
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_DOG, '[{dog, dogs}]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_CAT, '[{cat, cats}]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_OTHER, '[{other, others}]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_DONTKNOW, '[{i dont know, i have no idea}]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_DOG_BREED, '[$breed=#DOG_BREED()]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_CAT_BREED, '[$breed=#CAT_BREED()]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_OTHER_BREED, '[$breed=#OTHER_BREED()]')

# Error Transition
df.set_error_successor(State.FAVORITE_PET, State.FAVORITE_PET_UNKNOWN)

# System Turn - Transition to Another Dog Breed Introduction Part
df.add_system_transition(State.FAVORITE_PET_DOG, State.FAVORITE_PET_DOG_ANS, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! I like dogs! Among various dog breeds, which one do you like the best? I mean, like german shepherd, golden retriever, husky?"')
df.add_system_transition(State.FAVORITE_PET_CAT, State.FAVORITE_PET_CAT_ANS, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! I like cats! Among various cat breeds, which breed is your favorite? I mean, like turkish angora, toyger?"')
df.add_system_transition(State.FAVORITE_PET_OTHER, State.FAVORITE_PET_OTHER_ANS, '"there are lots of other types of pets, i am curious what it is, a bird? or a rabbit?"')
df.add_system_transition(State.FAVORITE_PET_UNKNOWN, State.ANOTHER_DOG_BREED, '{Cool,Wow, Awesome}"! that\'great! But I\'m not quite familiar with this animal. I know a lot about dogs. Would you like to know some information about dog breed, like" $another_breed={#DOG_RANDOM_BREED(breed)} "?"')

# User Turn
df.add_user_transition(State.FAVORITE_PET_DOG_ANS, State.FAVORITE_PET_DOG_BREED, '[$breed=#DOG_BREED()]')
df.add_user_transition(State.FAVORITE_PET_DOG_ANS, State.FAVORITE_PET_DOG_DONTKNOW, '[{i dont know, i have no idea}]')

df.add_user_transition(State.FAVORITE_PET_CAT_ANS, State.FAVORITE_PET_CAT_BREED, '[$breed=#CAT_BREED()]')
df.add_user_transition(State.FAVORITE_PET_CAT_ANS, State.FAVORITE_PET_CAT_DONTKNOW, '[{i dont know, i have no idea}]')

df.add_user_transition(State.FAVORITE_PET_OTHER_ANS, State.FAVORITE_PET_OTHER_BREED, '[$breed=#OTHER_BREED()]')
df.add_user_transition(State.FAVORITE_PET_OTHER_ANS, State.FAVORITE_PET_OTHER_DONTKNOW, '[{i dont know, i have no idea}]')

# Error Transition
df.set_error_successor(State.FAVORITE_PET_DOG_ANS, State.FAVORITE_PET_DOG_UNKNOWN)
df.set_error_successor(State.FAVORITE_PET_CAT_ANS, State.FAVORITE_PET_CAT_UNKNOWN)
df.set_error_successor(State.FAVORITE_PET_OTHER_ANS, State.FAVORITE_PET_OTHER_UNKNOWN)

# System Turn - Transition to Another Dog or Cat Breed Introduction Part
df.add_system_transition(State.FAVORITE_PET_DOG_UNKNOWN, State.ANOTHER_DOG_BREED, '{Cool,Wonderful,Wow, Awesome}"! although i know lots of dog breed, I\'m not quite familiar with the one you mentioned, but i\'m sure they must be very lovable in some way. Also, Would you like to know some information about another breed of dogs, like" $another_breed={#DOG_RANDOM_BREED(breed)} "?"')
df.add_system_transition(State.FAVORITE_PET_DOG_BREED, State.ANOTHER_DOG_BREED, '{Cool,Wonderful,Wow, Awesome}"! they are wonderful creatures!" #DOG_BREED_DESC(breed) "I may consider adopt one in the future! Also, Would you like to know some information about another breed of dogs, like" $another_breed={#DOG_RANDOM_BREED(breed)} "?"')
df.add_system_transition(State.FAVORITE_PET_DOG_DONTKNOW, State.FAVORITE_PET_DOG_DONTKNOW_ANS, '"That\'s OK, that\'s why I\'m here. My favorite dog is" $breed="german shepherd" ".Would you like to know some information about this dog breed?"')

df.add_system_transition(State.FAVORITE_PET_CAT_UNKNOWN, State.ANOTHER_CAT_BREED, '{Cool,Wow, Awesome}"! although i know lots of cat breed, I\'m not quite familiar with the one you mentioned, but i\'m sure they must be very lovable in some way. Also, Would you like to know some information about another breed of cats, like" $another_breed={#CAT_RANDOM_BREED(breed)} "?"')
df.add_system_transition(State.FAVORITE_PET_CAT_BREED, State.ANOTHER_CAT_BREED, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! they are wonderful creatures!" #CAT_BREED_DESC(breed) "I may consider adopt one in the future! Also, Would you like to know some information about another breed of cats, like" $another_breed={#CAT_RANDOM_BREED(breed)} "?"')
df.add_system_transition(State.FAVORITE_PET_CAT_DONTKNOW, State.FAVORITE_PET_CAT_DONTKNOW_ANS, '"That\'s OK, that\'s why I\'m here. My favorite cat is" $another_breed="toyger" ".Would you like to know some information about this cat breed?"')

# User Turn
df.add_user_transition(State.FAVORITE_PET_DOG_DONTKNOW_ANS, State.ANOTHER_DOG_BREED, '[#CATCH_YES()]')
df.add_user_transition(State.FAVORITE_PET_DOG_DONTKNOW_ANS, State.ANOTHER_DOG_BREED_N, '[#CATCH_NO()]')

df.add_user_transition(State.FAVORITE_PET_CAT_DONTKNOW_ANS, State.ANOTHER_CAT_BREED, '[#CATCH_YES()]')
df.add_user_transition(State.FAVORITE_PET_CAT_DONTKNOW_ANS, State.ANOTHER_CAT_BREED_N, '[#CATCH_NO()]')

# Error Transition
df.set_error_successor(State.FAVORITE_PET_OTHER_ANS, State.FAVORITE_PET_OTHER_UNKNOWN)
df.set_error_successor(State.FAVORITE_PET_DOG_DONTKNOW_ANS, State.ANOTHER_DOG_BREED)
df.set_error_successor(State.FAVORITE_PET_CAT_DONTKNOW_ANS, State.ANOTHER_CAT_BREED_N)

# System Turn - Transition to Interesting Facts Part
df.add_system_transition(State.FAVORITE_PET_OTHER_UNKNOWN, State.OTHER_INTERESTING, '"oops, sorry, although i know people love all kinds of animals, I\'m not quite familiar with the one you mentioned, but i\'m sure they must be very lovable in some way. Also, I know lots of interesting facts about animals. would you like to listen one?"')
df.add_system_transition(State.FAVORITE_PET_OTHER_BREED, State.OTHER_INTERESTING, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! they are wonderful creatures!" #OTHER_BREED_DESC(breed) "I may consider keep one in the future! I know lots of interesting facts about animals. would you like to listen one?"')
df.add_system_transition(State.FAVORITE_PET_OTHER_DONTKNOW, State.ANOTHER_DOG_BREED, '"That\'s OK, that\'s why I\'m here. I know lots of information about different dog breeds, like" $breed="german shepherd" ".Would you like to know some information about it?"')

####################### Another Dog and Cat Breed Introduction Part ################################################################################################
# User Turn
df.add_user_transition(State.ANOTHER_DOG_BREED, State.ANOTHER_DOG_BREED_Y, '[#CATCH_YES()]')
df.add_user_transition(State.ANOTHER_DOG_BREED, State.ANOTHER_DOG_BREED_N, '[#CATCH_NO()]')

df.add_user_transition(State.ANOTHER_CAT_BREED, State.ANOTHER_CAT_BREED_Y, '[#CATCH_YES()]')
df.add_user_transition(State.ANOTHER_CAT_BREED, State.ANOTHER_CAT_BREED_N, '[#CATCH_NO()]')

# Error Transition
df.set_error_successor(State.ANOTHER_DOG_BREED, State.ANOTHER_DOG_BREED_N)
df.set_error_successor(State.ANOTHER_CAT_BREED, State.ANOTHER_CAT_BREED_N)

# System Turn
df.add_system_transition(State.ANOTHER_DOG_BREED_Y, State.ANOTHER_DOG_BREED_DETAIL, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"!" #DOG_RANDOM_BREED(breed, another_breed)"Would you like to know some other breed of dogs, like" $another_breed={#DOG_RANDOM_BREED(another_breed)} "?"')
df.add_system_transition(State.ANOTHER_DOG_BREED_N, State.DOG_INTERESTING, '{Ok, Alright, Then, Well}", besides various dog breeds, I also know lots of interesting things about dogs. Do you want to hear some?"')

df.add_system_transition(State.ANOTHER_CAT_BREED_Y, State.ANOTHER_CAT_BREED_DETAIL, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"!" #CAT_RANDOM_BREED(breed, another_breed)"Would you like to know some other breed of cats, like" $another_breed={#CAT_RANDOM_BREED(another_breed)} "?"')
df.add_system_transition(State.ANOTHER_CAT_BREED_N, State.CAT_INTERESTING, '{Ok, Alright, Then, Well}", besides various cat breeds, I also know lots of interesting things about cats. Do you want to hear some?"')

# User Turn
df.add_user_transition(State.ANOTHER_DOG_BREED_DETAIL, State.ANOTHER_DOG_BREED_Y, '[{#CATCH_YES(),$another_breed=#DOG_BREED()}]')
df.add_user_transition(State.ANOTHER_DOG_BREED_DETAIL, State.ANOTHER_DOG_BREED_N, '[#CATCH_NO()]')

df.add_user_transition(State.ANOTHER_CAT_BREED_DETAIL, State.ANOTHER_CAT_BREED_Y, '[{#CATCH_YES(),$another_breed=#CAT_BREED()}]')
df.add_user_transition(State.ANOTHER_CAT_BREED_DETAIL, State.ANOTHER_CAT_BREED_N, '[#CATCH_NO()]')

# Error Transition
df.set_error_successor(State.ANOTHER_DOG_BREED_DETAIL, State.ANOTHER_DOG_BREED_N)
df.set_error_successor(State.ANOTHER_CAT_BREED_DETAIL, State.ANOTHER_CAT_BREED_N)

####################### Interesting Facts Part ######################################################################################################################
# User Turn
df.add_user_transition(State.DOG_INTERESTING, State.DOG_INTERESTING_Y, '[#CATCH_YES()]')
df.add_user_transition(State.DOG_INTERESTING, State.DOG_INTERESTING_N, '[#CATCH_NO()]')

df.add_user_transition(State.CAT_INTERESTING, State.CAT_INTERESTING_Y, '[#CATCH_YES()]')
df.add_user_transition(State.CAT_INTERESTING, State.CAT_INTERESTING_N, '[#CATCH_NO()]')

df.add_user_transition(State.OTHER_INTERESTING, State.OTHER_INTERESTING_Y, '[#CATCH_YES()]')
df.add_user_transition(State.OTHER_INTERESTING, State.OTHER_INTERESTING_N, '[#CATCH_NO()]')

# Error Transition
df.set_error_successor(State.DOG_INTERESTING, State.DOG_INTERESTING_N)
df.set_error_successor(State.CAT_INTERESTING, State.CAT_INTERESTING_N)
df.set_error_successor(State.OTHER_INTERESTING, State.OTHER_INTERESTING_N)

# System Turn
df.add_system_transition(State.DOG_INTERESTING_Y, State.DOG_INTERESTING, '#DOG_INTERESTING(){Would you like to know more, Would you like to know another one, Would you like to listen another one}"?"')
df.add_system_transition(State.CAT_INTERESTING_Y, State.CAT_INTERESTING, '#CAT_INTERESTING(){Would you like to know more, Would you like to know another one, Would you like to listen another one}"?"')
df.add_system_transition(State.OTHER_INTERESTING_Y, State.OTHER_INTERESTING, '#OTHER_INTERESTING(){Would you like to know more, Would you like to know another one, Would you like to listen another one}"?"')

# Error Transition
df.set_error_successor(State.DOG_INTERESTING_Y, State.DOG_INTERESTING_OTHER)
df.set_error_successor(State.CAT_INTERESTING_Y, State.CAT_INTERESTING_OTHER)
df.set_error_successor(State.OTHER_INTERESTING_Y, State.OTHER_INTERESTING_OTHER)

df.add_system_transition(State.DOG_INTERESTING_OTHER, State.DOG_MOVIE, '"Oops, no more fun facts about them that I know of right now. But I also know lots of movies about dogs. My favorite one is" $movie={#DOG_MOVIE()} ".Would you like to know some detail about it?"')
df.add_system_transition(State.CAT_INTERESTING_OTHER, State.DOG_MOVIE, '"Oops, no more fun facts about them that I know of right now. But I also know lots of movies about cats. My favorite one is" $movie={#CAT_MOVIE()} ".Would you like to know some detail about it?"')
df.add_system_transition(State.OTHER_INTERESTING_OTHER, State.DOG_MOVIE, '"Oops, no more fun facts about them that I know of right now. But I also know lots of movies about animals. My favorite one is" $movie={#OTHER_MOVIE()} ".Would you like to know some detail about it?"')

####################### Movie Part ##############################################################################################################################
# System Turn
df.add_system_transition(State.DOG_INTERESTING_N, State.DOG_MOVIE, '{Ok, Alright, Then, Well}", I also know lots of movies about dogs. My favorite one is" $movie={#DOG_MOVIE()} ".Would you like to know some details about it?"')
df.add_system_transition(State.CAT_INTERESTING_N, State.CAT_MOVIE, '{Ok, Alright, Then, Well}", I also know lots of movies about cats. My favorite one is" $movie={#CAT_MOVIE()} ".Would you like to know some details about it?"')
df.add_system_transition(State.OTHER_INTERESTING_N, State.OTHER_MOVIE, '{Ok, Alright, Then, Well}", I also know lots of movies about animals. My favorite one is" $movie={#OTHER_MOVIE()} ".Would you like to know some details about it?"')

# User Turn
df.add_user_transition(State.DOG_MOVIE, State.DOG_MOVIE_Y, '[#CATCH_YES()]')
df.add_user_transition(State.DOG_MOVIE, State.DOG_MOVIE_N,'[#CATCH_NO()]')

df.add_user_transition(State.CAT_MOVIE, State.CAT_MOVIE_Y, '[#CATCH_YES()]')
df.add_user_transition(State.CAT_MOVIE, State.CAT_MOVIE_N,'[#CATCH_NO()]')

df.add_user_transition(State.OTHER_MOVIE, State.OTHER_MOVIE_Y, '[#CATCH_YES()]')
df.add_user_transition(State.OTHER_MOVIE, State.OTHER_MOVIE_N,'[#CATCH_NO()]')

# Error Transition
df.set_error_successor(State.DOG_MOVIE, State.DOG_MOVIE_N)
df.set_error_successor(State.CAT_MOVIE, State.CAT_MOVIE_N)
df.set_error_successor(State.OTHER_MOVIE, State.OTHER_MOVIE_N)

# System Turn
df.add_system_transition(State.DOG_MOVIE_Y, State.DOG_MOVIE_DETAIL, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $movie "is that" #DOG_MOVIE_DESC(movie) "I also know some other movies about dogs. Would you like to listen one, like" $movie={#DOG_MOVIE(movie)} "?"')
df.add_system_transition(State.DOG_MOVIE_N, State.DOG_MOVIE_DETAIL, '{Ok, Alright, Then, Well}", I also know some other movies about dogs. Would you like to listen one, like" $movie={#DOG_MOVIE(movie)} ".Would you like to know some detail about it?"')

df.add_system_transition(State.CAT_MOVIE_Y, State.CAT_MOVIE_DETAIL, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $movie "is that" #CAT_MOVIE_DESC(movie) "I also know some other movies about cats. Would you like to listen one, like" $movie={#CAT_MOVIE(movie)} "?"')
df.add_system_transition(State.CAT_MOVIE_N, State.CAT_MOVIE_DETAIL, '{Ok, Alright, Then, Well}", I also know some other movies about cats. Would you like to listen one, like" $movie={#CAT_MOVIE(movie)} "?"')

df.add_system_transition(State.OTHER_MOVIE_Y, State.OTHER_MOVIE_DETAIL, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $movie "is that" #OTHER_MOVIE_DESC(movie) "I also know some other animal movies. Would you like to listen one, like" $movie={#OTHER_MOVIE(movie)} "?"')
df.add_system_transition(State.OTHER_MOVIE_N, State.OTHER_MOVIE_DETAIL, '{Ok, Alright, Then, Well}", I also know some movies about other animals. Would you like to listen one, like" $movie={#OTHER_MOVIE(movie)} "?"')

# User Turn
df.add_user_transition(State.DOG_MOVIE_DETAIL, State.DOG_MOVIE_ANOTHER_Y, '[#CATCH_YES()]')
df.add_user_transition(State.DOG_MOVIE_DETAIL, State.DOG_MOVIE_ANOTHER_N,'[#CATCH_NO()]')
df.set_error_successor(State.DOG_MOVIE_DETAIL, State.DOG_MOVIE_ANOTHER_N)

df.add_user_transition(State.CAT_MOVIE_DETAIL, State.CAT_MOVIE_ANOTHER_Y, '[#CATCH_YES()]')
df.add_user_transition(State.CAT_MOVIE_DETAIL, State.CAT_MOVIE_ANOTHER_N,'[#CATCH_NO()]')
df.set_error_successor(State.CAT_MOVIE_DETAIL, State.CAT_MOVIE_ANOTHER_N)

df.add_user_transition(State.OTHER_MOVIE_DETAIL, State.OTHER_MOVIE_ANOTHER_Y, '[#CATCH_YES()]')
df.add_user_transition(State.OTHER_MOVIE_DETAIL, State.OTHER_MOVIE_ANOTHER_N,'[#CATCH_NO()]')
df.set_error_successor(State.OTHER_MOVIE_DETAIL, State.OTHER_MOVIE_ANOTHER_N)

# System Turn
df.add_system_transition(State.DOG_MOVIE_ANOTHER_Y, State.DOG_MOVIE_DETAIL, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $movie "is that" #DOG_MOVIE_DESC(movie) "Would you like to know another one,like" $movie={#DOG_MOVIE(movie)} "?"')
df.add_system_transition(State.DOG_MOVIE_ANOTHER_N, State.PETS_PROS, '{Ok, Alright, Then, Well}", I know lots of people have pets. What do you think are the benefits of keeping a pet?"')

df.add_system_transition(State.CAT_MOVIE_ANOTHER_Y, State.CAT_MOVIE_DETAIL, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $movie"is that" #CAT_MOVIE_DESC(movie) "Would you like to know another one,like" $movie={#CAT_MOVIE(movie)} "?"')
df.add_system_transition(State.CAT_MOVIE_ANOTHER_N, State.PETS_PROS, '{Ok, Alright, Then, Well}", I know lots of people have pets. What do you think are the benefits of keeping a pet?"')

df.add_system_transition(State.OTHER_MOVIE_ANOTHER_Y, State.OTHER_MOVIE_DETAIL, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $movie"is that" #OTHER_MOVIE_DESC(movie) "Would you like to know another one,like" $movie={#OTHER_MOVIE(movie)} "?"')
df.add_system_transition(State.OTHER_MOVIE_ANOTHER_N, State.PETS_PROS, '{Ok, Alright, Then, Well}", I know lots of people have pets. What do you think are the benefits of keeping a pet?"')

####################### Pet Pros #######################################################################################################################################################
# User Turn
df.add_user_transition(State.PETS_PROS, State.PETS_PROS_DB, '[$pros=#CATCH_PROS()]')
df.add_user_transition(State.PETS_PROS, State.PETS_PROS_N, '[#CATCH_NO()]')
df.set_error_successor(State.PETS_PROS, State.PETS_PROS_UNKNOWN)

# System Turn
df.add_system_transition(State.PETS_PROS_DB, State.END, '"Yes, I think so."#CATCH_PROS_DESC(pros)')
df.add_system_transition(State.PETS_PROS_N, State.END, '"I understand. Although they may bring allergies or schedule disorder, we can\'t deny that they also bring so much joy into our lives."')
df.add_system_transition(State.PETS_PROS_UNKNOWN, State.END, '"Interesting idea. I have to say that with almost no effort at all, pets manage to bring so much joy into our lives. They make us laugh, comfort us when we’re sick or upset, and are always there for us no matter what."')

####################### End Pet Component ##############################################################################################################################################
# END
# df.set_error_successor(State.PETS_PROS_ANS, State.PETS_END)
# df.add_system_transition(State.PETS_END, State.END, '"I\'m glad to talk with you. What other topics would you like to talk about?"')

df.update_state_settings(State.END, system_multi_hop=True)
# df.add_system_transition(State.END, State.START, '" "')

# end (recurrent) the dialogue

if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    df.precache_transitions()
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=True)

#GATE()