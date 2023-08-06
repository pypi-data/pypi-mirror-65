from emora_stdm import DialogueFlow, Macro
from enum import Enum
import json, os
import random

# Xiangjue Dong
# 02/14/2020 v1.0
# 03/21/2020 v1.1
# 04/04/2020 v1.2

# States are typically represented as an enum
class State(Enum):

    START = 0
    START_PET = 1
    END = 2
    PETS_Y = 3
    ASK_PETS = 4
    ASK_PETS_Y = 5
    ASK_PETS_N = 6
    OFFENSE = 7
    STOP = 8

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
    FIRST_PET_DOG_FOOD_UNKNOWN = 213

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
    FIRST_PET_CAT_FOOD_UNKNOWN = 223

    FIRST_PET_OTHER = 31
    FIRST_PET_OTHER_ANS = 32
    FIRST_PET_OTHER_UNKNOWN = 33
    FIRST_PET_OTHER_BREED = 34
    FIRST_PET_OTHER_NAME = 35
    FIRST_PET_OTHER_NAME_KNOWN = 36
    FIRST_PET_OTHER_NAME_UNKNOWN= 37

    NO_PETS = 40
    NO_PETS_Y = 41
    NO_PETS_N = 42
    NO_PETS_DAD = 43
    NO_PETS_DAD_ANS = 44
    NO_PETS_DAD_ANS_ANS = 45
    NO_PETS_UNKNOWN = 46

    FAVORITE_PET = 50
    FAVORITE_PET_UNKNOWN = 51

    FAVORITE_PET_DOG = 52
    FAVORITE_PET_DOG_ANS = 53
    FAVORITE_PET_DOG_BREED = 54
    FAVORITE_PET_DOG_UNKNOWN = 55
    FAVORITE_PET_DOG_DONTKNOW = 56

    FAVORITE_PET_CAT = 62
    FAVORITE_PET_CAT_ANS = 63
    FAVORITE_PET_CAT_BREED = 64
    FAVORITE_PET_CAT_UNKNOWN = 65
    FAVORITE_PET_CAT_DONTKNOW = 66

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

    MOVIE_USER = 136
    MOVIE_UNKNOWN = 137
    MOVIE_DETAIL_INTERESTING = 138
    MOVIE_DETAIL_INTERESTING_Y = 139

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
    DOG_PROS = 1600
    DOG_PROS_DB = 1601
    DOG_PROS_N = 1602
    DOG_PROS_UNKNOWN = 1603
    CAT_PROS = 1604
    CAT_PROS_DB = 1605
    CAT_PROS_N = 1606
    CAT_PROS_UNKNOWN = 1607

    PETS_CONS = 170
    PETS_CONS_DB = 171
    PETS_CONS_N = 172
    PETS_CONS_UNKNOWN = 173

    JOKE_Q = 180
    JOKE_A = 181
    JOKE_W = 182

    STOP_FINAL = 183


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

class PET_CATCH(Macro):
    """Catch breed name and food name from database.

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
        # Catch breed name under breed key, food name under food key, movie name under movie key
        if len(args) == 2:
            return ngrams & self.db[vars[args[0]]][vars[args[1]]].keys()

        # Generate breed detail under breed key, food detail under food key, movie detail under movie key
        if len(args) == 3:
            return ngrams & self.db[vars[args[0]]][vars[args[1]]][vars[args[2]]]


class PET_RANDOM(Macro):
    """Generate random breed name, movie name, food name from database.

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
        # Catch breed name under breed key, food name under food key
        if len(args) == 2:
            # return ngrams & self.db[vars[args[0]]][vars[args[1]]].keys()
            return ngrams & self.db[args[0]][args[1]].keys()

        # Generate breed detail under breed key, food detail under food key
        if len(args) == 3:
            return ngrams & self.db[vars[args[0]]][vars[args[1]]][vars[args[2]]]


# Variables
TRANSITION_OUT = ["movies", "movie", "music", "sports", "sport", "travel"]
NULL = "NULL TRANSITION"
PET_TYPE = {"dog", "dogs", "puppies", "puppy", "kitties", "kitty", "cat", "cats", "pet", "pets", "animal", "animals"}

NAME = {"alex","max","charlie","cooper","buddy","rocky","milo","jack","bear","duke","teddy","oliver","bentley","tucker",
        "beau","leo","toby","jax","zeus","winston","blue","finn","louie","ollie","murphy","gus","moose","jake","loki",
        "dexter","hank","bruno","apollo","buster","thor","bailey","gunnar","lucky","diesel","harley","henry","koda",
        "jackson","riley", "ace", "oscar","chewy","bandit","baxter","scout","jasper","maverick","sam","cody","gizmo",
        "shadow","simba","rex","brody","tank","marley","otis","remi","remy","roscoe","rocco","sammy","cash","boomer",
        "prince","benji","benny","archie","chance","ranger","ziggy","luke","george","oreo","hunter","rusty","king","odin",
        "coco","frankie","tyson","chase","theo","romeo","bruce","rudy","zeke","kobe","peanut","joey","oakley","chico","mac",
        "walter","brutus","samson","bella", "luna","lucy","daisy","lily","zoe","lola","molly","sadie","bailey","stella",
        "maggie","roxy","sophie","chloe","penny","coco","nala","rosie","ruby","gracie","ellie","mia","piper","callie","abby",
        "lexi","ginger", "lulu","pepper","willow","riley","millie","harley","sasha","lady","izzy","layla","charlie","dixie",
        "maya","annie","kona","hazel","winnie","olive","princess","emma","athena","nova","belle","honey","ella", "marley",
        "cookie","maddie","remi","remy","phoebe","scout","minnie","dakota","holly","angel","josie","leia","harper","ava",
        "missy","mila","sugar","shelby","poppy","blue","mocha","cleo","penelope","ivy","peanut", "fiona","xena","gigi","sandy",
        "bonnie","jasmine","baby","macy","paisley","shadow","koda","pearl","skye","delilah","nina","trixie","charlotte","aspen",
        "arya","diamond","georgia","dolly", "fluffy"}

YES = {"yes", "yea", "yup", "yep", "i do", "yeah", "a little", "sure", "of course", "i have", "i am", "sometimes", "too",
       "as well", "also", "agree","good", "keep","why not", "ok", "okay", "fine", "continue", "go on"}

NO = {"no", "nope", "dont", "nothing"}

DIRTY_WORDS = {"nigger", "nigga", "fuck", "sex", "sexy", "mother", "mom", "prick", "bastard", "bellend", "ass", "arse", "butt", "cunt",
                 "vagina", "balls", "testicles", "shit", "shitty", "poop", "crap", "bullshit", "bitch", "whore", "hell", "dick",
                 "dickhead", "witch", "fucker", "dumbass", "motherfucking", "cock", "prick", "tit", "titties", "titty", "asshole", "cocksucker",
                 "shithead", "wanker", "fucker", "fart", "slut", "hag", "die", "idiot", "penis", "piss", "damn", "bollocks",
                 "bugger", "choad", "crikey", "rubbish", "shag", "twat", "bloody", "root", "stuffed", "bugger", "suck", "sucks",
               "taste my", "shaved beaver", "shaved pussy", "throating", "vibrator", "tongue in a"}

STOP_WORDS = {"i dont wanna talk about pets","I dont want to hear anymore about"}

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
pet_cons = os.path.join('modules','pets_cons.json')
pet_data = os.path.join('modules', 'pets_database.json')
pet_joke = os.path.join('modules', 'pets_qa_database.json')

macros = {
    'CATCH_DOG_BREED': BREED(dog_breed),
    'DOG_BREED_DESC': BREED_DESC(dog_breed),
    'CATCH_CAT_BREED': BREED(cat_breed),
    'CAT_BREED_DESC': BREED_DESC(cat_breed),
    'CATCH_OTHER_BREED': BREED(other_breed),
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
    'CATCH_PROS_DESC':BREED_DESC(pet_pros),
    'CATCH_CONS': BREED(pet_cons),
    'CATCH_CONS_DESC': BREED_DESC(pet_cons),
    'PET_CATCH': PET_CATCH(pet_data),
    'CATCH_OFFENSE': CATCH(DIRTY_WORDS),
    'CATCH_STOP':CATCH(STOP_WORDS),
    'CATCH_DOG_MOVIE': BREED(dog_movie),
    'CATCH_CAT_MOVIE': BREED(cat_movie),
    'CATCH_OTHER_MOVIE': BREED(other_movie),
    'PET_JOKE':RANDOM(pet_joke),
    'PET_JOKE_DESC':BREED_DESC(pet_joke),
}

###################### Initialization Part ####################################################################################################################
# Initialize the DialogueFlow object, which uses a state-machine to manage dialogue
# Each user turn should consider error transition
df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.USER, macros=macros)

# For dialogue manager initialization
# test
df.add_user_transition(State.START, State.START_PET, 'test')
df.add_system_transition(State.START_PET, State.ASK_PETS, '"So, do you have any"$breed=pets"at home?"')

# User Turn
df.add_user_transition(State.START, State.PETS_Y, '[$breed={#CATCH_OTHER_BREED(),#CATCH_DOG_BREED(),#CATCH_CAT_BREED(),#CATCH_PET_TYPE()}]')

# Error Transition
df.set_error_successor(State.START, State.START)
df.add_system_transition(State.START, State.START, NULL)

###################### Pet Opening Part ###########################################################################################################################
# System Turn
df.add_system_transition(State.PETS_Y, State.ASK_PETS, '"That\'s great! I love" $breed "! actually, " #EMORA(breed) '
                                                       '"Do you have any pets at your home now?"')

# User Turn
df.add_user_transition(State.ASK_PETS, State.ASK_PETS_Y, '[![{yes, yea, yup, yep, i do, yeah, a little, sure, of course,'
                                                         ' i have, i am, sometimes, too, as well, also, agree, ok, okay,'
                                                         ' good, keep, why}] #NOT(no, dont, nope, dog, dogs, cat, cats, pet, pets,#CATCH_DOG_BREED(),#CATCH_CAT_BREED(),#CATCH_OTHER_BREED())]')
df.add_user_transition(State.ASK_PETS, State.ASK_PETS_N, '[[{no, nope, dont,allergic,allergy}] #NOT(know, idea)]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_DOG, '[!-{dont, not}[{dog, dogs, puppies, puppy}]]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_CAT, '[!-{dont, not}[{cat, cats, kitties, kitty}]]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_OTHER, '[{other, others}]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_OTHER_BREED, '[$breed=#CATCH_OTHER_BREED()]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_DOG_BREED, '[$breed=#CATCH_DOG_BREED()]')
df.add_user_transition(State.ASK_PETS, State.FIRST_PET_CAT_BREED, '[$breed=#CATCH_CAT_BREED()]')
df.add_user_transition(State.ASK_PETS, State.FAVORITE_PET_DOG_DONTKNOW, '[{i dont know, i have no idea, who knows, no idea, dont know}]')
df.add_user_transition(State.ASK_PETS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.ASK_PETS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.ASK_PETS, State.NO_PETS_UNKNOWN)

# System Turn
df.add_system_transition(State.ASK_PETS_Y, State.ASK_PETS, '{Cool,Wonderful,Wow, Awesome}"!What is it?"')
df.add_system_transition(State.ASK_PETS_N, State.NO_PETS, '"You don\'t have any pets? '
                                                          'Well, would you consider getting one in the future? '
                                                          'They are pretty cute."')

# User Turn
df.add_user_transition(State.NO_PETS, State.NO_PETS_Y, '[#CATCH_YES() #NOT(#CATCH_DOG_BREED(),#CATCH_CAT_BREED(),#CATCH_OTHER_BREED())]')
df.add_user_transition(State.NO_PETS, State.FAVORITE_PET_DOG, '[{dog, dogs, puppies, puppy}]')
df.add_user_transition(State.NO_PETS, State.FAVORITE_PET_CAT, '[{cat, cats, kitties, kitty}]')
df.add_user_transition(State.NO_PETS, State.FAVORITE_PET_DOG_DONTKNOW, '[{i dont know, i have no idea, no idea, dont know}]')
df.add_user_transition(State.NO_PETS, State.FAVORITE_PET_DOG_BREED, '[$breed=#CATCH_DOG_BREED()]')
df.add_user_transition(State.NO_PETS, State.FAVORITE_PET_CAT_BREED, '[$breed=#CATCH_CAT_BREED()]')
df.add_user_transition(State.NO_PETS, State.FAVORITE_PET_OTHER_BREED, '[$breed=#CATCH_OTHER_BREED()]')
df.add_user_transition(State.NO_PETS, State.NO_PETS_N, '[!-{why}[{no, nope, dont, nothing, not}]]')
df.add_user_transition(State.NO_PETS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.NO_PETS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.NO_PETS, State.NO_PETS_UNKNOWN)

# System Turn
df.add_system_transition(State.NO_PETS_Y, State.FAVORITE_PET, '{Nice choice, Good choice, Cool, Wonderful, Wow, Awesome}'
                                                              '"! I suggest adopting instead of buying. Although I love both dogs and cats, I prefer dogs to be my companion." '
                                                              '{"What about you?", "Which one would you prefer?","Which pet would you like to keep?"}')
df.add_system_transition(State.NO_PETS_N, State.PETS_CONS, '{Oh ok, thats fine}"."{It is indeed a big decision to introduce new members into your family or life, Keeping a pet should not be treated as a light matter}"."'
                                                                   ' {But I am still curious about that, But I would like to listen to your reason} '
                                                                   '"why you don\'t want to keep a pet."')
df.add_system_transition(State.NO_PETS_UNKNOWN, State.ANOTHER_DOG_BREED, '{I see, Interesting}"."{It is indeed a big decision to introduce new members into your family or life, Keeping a pet should not be treated as a light matter}'
                                                                         '".I know a lot about dog breed and I \'d like to share with you. Have you heard about the" '
                                                                         '$another_breed=#DOG_RANDOM_BREED(breed)"?"')

################## First Pet Part ################################################################################################################################
# System Turn
df.add_system_transition(State.FIRST_PET_DOG, State.FIRST_PET_DOG_ANS, '{Cool,Wonderful,Wow, Awesome}"! That\'s great! '
                                                                       'I like dogs! What is its breed?"')
df.add_system_transition(State.FIRST_PET_CAT, State.FIRST_PET_CAT_ANS, '{Cool,Wonderful,Wow, Awesome}"! That\'s great! '
                                                                       'I like cats! What is its breed?"')
df.add_system_transition(State.FIRST_PET_OTHER, State.FIRST_PET_OTHER_ANS, '{Cool,Wonderful,Wow, Awesome}'
                                                                           '"! That\'s interesting! What is it?"')

# User Turn
df.add_user_transition(State.FIRST_PET_DOG_ANS, State.FIRST_PET_DOG_BREED, '[$breed=#CATCH_DOG_BREED()]')
df.add_user_transition(State.FIRST_PET_DOG_ANS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FIRST_PET_DOG_ANS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FIRST_PET_DOG_ANS, State.FIRST_PET_DOG_UNKNOWN)

df.add_user_transition(State.FIRST_PET_CAT_ANS, State.FIRST_PET_CAT_BREED, '[$breed=#CATCH_CAT_BREED()]')
df.add_user_transition(State.FIRST_PET_CAT_ANS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FIRST_PET_CAT_ANS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FIRST_PET_CAT_ANS, State.FIRST_PET_CAT_UNKNOWN)

df.add_user_transition(State.FIRST_PET_OTHER_ANS, State.FIRST_PET_OTHER_BREED, '[$breed=#CATCH_OTHER_BREED()]')
df.add_user_transition(State.FIRST_PET_OTHER_ANS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FIRST_PET_OTHER_ANS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FIRST_PET_OTHER_ANS, State.FIRST_PET_OTHER_UNKNOWN)

# System Turn - Ask Name
df.add_system_transition(State.FIRST_PET_DOG_BREED, State.FIRST_PET_DOG_NAME, '{Cool,Wonderful,Wow, Awesome}"!" #DOG_BREED_DESC(breed) '
                                                                              '"Amazing creature! I guess it must have a cute name. What is its name?"')
df.add_system_transition(State.FIRST_PET_CAT_BREED, State.FIRST_PET_CAT_NAME, '{Cool,Wonderful,Wow, Awesome}"!" #CAT_BREED_DESC(breed) '
                                                                              '"Amazing creature! I guess it must have a cute name. What is its name?"')
df.add_system_transition(State.FIRST_PET_OTHER_BREED, State.FIRST_PET_OTHER_NAME, '{Cool,Wonderful,Wow, Awesome}"!" #OTHER_BREED_DESC(breed)'
                                                                                  '"Amazing creature! I guess it must have a cute name. What is its name?"')

df.add_system_transition(State.FIRST_PET_DOG_UNKNOWN, State.FIRST_PET_DOG_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting. '
                                                                                'Although I am not quite familiar with this dog breed, I guess it must have a cute name. '
                                                                                'What is its name?"')
df.add_system_transition(State.FIRST_PET_CAT_UNKNOWN, State.FIRST_PET_CAT_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting. '
                                                                                'Although I am not quite familiar with this cat breed, I guess it must have a cute name. '
                                                                                'What is its name?"')
df.add_system_transition(State.FIRST_PET_OTHER_UNKNOWN, State.FIRST_PET_OTHER_NAME, '{Cool,Wonderful,Wow, Awesome}"! Sounds interesting. '
                                                                                    'Although I am not quite familiar with this kind of pets, I guess it must have a cute name. '
                                                                                    'What is its name?"')

# User Turn
df.add_user_transition(State.FIRST_PET_DOG_NAME, State.FIRST_PET_DOG_NAME_KNOWN, '[$name=#NAME()]')
df.add_user_transition(State.FIRST_PET_DOG_NAME, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FIRST_PET_DOG_NAME, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FIRST_PET_DOG_NAME, State.FIRST_PET_DOG_NAME_UNKNOWN)

df.add_user_transition(State.FIRST_PET_CAT_NAME, State.FIRST_PET_CAT_NAME_KNOWN, '[$name=#NAME()]')
df.add_user_transition(State.FIRST_PET_CAT_NAME, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FIRST_PET_CAT_NAME, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FIRST_PET_CAT_NAME, State.FIRST_PET_CAT_NAME_UNKNOWN)

df.add_user_transition(State.FIRST_PET_OTHER_NAME, State.FIRST_PET_OTHER_NAME_KNOWN, '[$name=#NAME()]')
df.add_user_transition(State.FIRST_PET_OTHER_NAME, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FIRST_PET_OTHER_NAME, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FIRST_PET_OTHER_NAME, State.FIRST_PET_OTHER_NAME_UNKNOWN)

# System Turn - Ask Food
# df.add_system_transition(State.FIRST_PET_DOG_NAME_KNOWN, State.FIRST_PET_DOG_FOOD, '"Oh!" $name ".That\'s a sweet name! If I had a dog, I would just named it puppy in a lazy way. I am a novice to keep a dog. Do you know whether dog can eat" $food={#DOG_FOOD()}"?"')
# df.add_system_transition(State.FIRST_PET_CAT_NAME_KNOWN, State.FIRST_PET_CAT_FOOD, '"Oh!" $name ".That\'s a sweet name! If I had a cat, I would just named it kitty in a lazy way. I am a novice to keep a cat. Do you know whether cat can eat" $food={#CAT_FOOD()} "?"')
# df.add_system_transition(State.FIRST_PET_OTHER_NAME_KNOWN, State.FIRST_PET_DOG_FOOD, '"Oh!" $name ".That\'s a sweet name! If I had a dog, I would just named it puppy in a lazy way. I am a novice to keep a dog. Do you know whether dog can eat" $food={#DOG_FOOD()} "?"')
#
# df.add_system_transition(State.FIRST_PET_DOG_NAME_UNKNOWN, State.FIRST_PET_DOG_FOOD, '"Interesting. If I had a dog, I would just named it puppy in a lazy way. I am a novice to keep a dog. Do you know whether dog can eat" $food={#DOG_FOOD()} "?"')
# df.add_system_transition(State.FIRST_PET_CAT_NAME_UNKNOWN, State.FIRST_PET_CAT_FOOD, '"Interesting. If I had a cat, I would just named it kitty in a lazy way. I am a novice to keep a cat. Do you know whether cat can eat" $food={#CAT_FOOD()} "?"')
# df.add_system_transition(State.FIRST_PET_OTHER_NAME_UNKNOWN, State.FIRST_PET_DOG_FOOD, '"Interesting. If I had a dog, I would just named it puppy in a lazy way. I am a novice to keep a dog. Do you know whether dog can eat" $food={#DOG_FOOD()} "?"')

# System Turn - Ask Pros
df.add_system_transition(State.FIRST_PET_DOG_NAME_KNOWN, State.DOG_PROS, '"Oh!" $name ".That\'s a sweet name! '
                                                                         'If I had a dog, I would just name it puppy in a lazy way. '
                                                                         'During the epidemic, you may have more time to accompany your dog. What do you think are the benefits of keeping dogs?"')
df.add_system_transition(State.FIRST_PET_CAT_NAME_KNOWN, State.CAT_PROS, '"Oh!" $name ".That\'s a sweet name! '
                                                                         'If I had a cat, I would just name it kitty in a lazy way. '
                                                                         'During the epidemic, you may have more time to accompany your cat. What do you think are the benefits of keeping cats?"')
df.add_system_transition(State.FIRST_PET_OTHER_NAME_KNOWN, State.PETS_PROS, '"Oh!" $name ".That\'s a sweet name! '
                                                                            'If I had a dog, I would just name it puppy in a lazy way. '
                                                                            'During the epidemic, you may have more time to accompany your pets. What do you think are the benefits of keeping pets?"')

df.add_system_transition(State.FIRST_PET_DOG_NAME_UNKNOWN, State.DOG_PROS, '"If I had a dog, I would just name it puppy in a lazy way. '
                                                                           'What do you think are the benefits of keeping dogs?"')
df.add_system_transition(State.FIRST_PET_CAT_NAME_UNKNOWN, State.CAT_PROS, '"If I had a cat, I would just name it kitty in a lazy way. '
                                                                           'What do you think are the benefits of keeping cats?"')
df.add_system_transition(State.FIRST_PET_OTHER_NAME_UNKNOWN, State.PETS_PROS, '"If I had a dog, I would just name it puppy in a lazy way. '
                                                                              'What do you think are the benefits of keeping pets?"')

####################### Pet Pros and Cons #######################################################################################################################################################
# User Turn
df.add_user_transition(State.DOG_PROS, State.DOG_PROS_DB, '[$pros=#CATCH_PROS()]')
df.add_user_transition(State.DOG_PROS, State.DOG_PROS_N, '[#CATCH_NO()]')
df.add_user_transition(State.DOG_PROS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.DOG_PROS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.DOG_PROS, State.DOG_PROS_UNKNOWN)

df.add_user_transition(State.CAT_PROS, State.CAT_PROS_DB, '[$pros=#CATCH_PROS()]')
df.add_user_transition(State.CAT_PROS, State.CAT_PROS_N, '[#CATCH_NO()]')
df.add_user_transition(State.CAT_PROS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.CAT_PROS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.CAT_PROS, State.CAT_PROS_UNKNOWN)

df.add_user_transition(State.PETS_PROS, State.PETS_PROS_DB, '[$pros=#CATCH_PROS()]')
df.add_user_transition(State.PETS_PROS, State.PETS_PROS_N, '[#CATCH_NO()]')
df.add_user_transition(State.PETS_PROS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.PETS_PROS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.PETS_PROS, State.PETS_PROS_UNKNOWN)

# System Turn
df.add_system_transition(State.DOG_PROS_DB, State.FIRST_PET_DOG_FOOD, '"Yes, I think so."#CATCH_PROS_DESC(pros) "You must have rich experience in keeping dogs. Do you know whether dogs can eat" $food={#DOG_FOOD()}"?"')
df.add_system_transition(State.DOG_PROS_N, State.FIRST_PET_DOG_FOOD, '"I understand. Although they may bring allergies or schedule disorder, we can\'t deny that they also bring so much joy into our lives. You must have rich experience in keeping dogs. Do you know whether dogs can eat" $food={#DOG_FOOD()}"?"')
df.add_system_transition(State.DOG_PROS_UNKNOWN, State.FIRST_PET_DOG_FOOD, '"Interesting idea. I have to say that with almost no effort at all, pets manage to bring so much joy into our lives. They make us laugh, comfort us when we’re sick or upset, and are always there for us no matter what. You must have rich experience in keeping dogs. Do you know whether dogs can eat" $food={#DOG_FOOD()}"?"')

df.add_system_transition(State.CAT_PROS_DB, State.FIRST_PET_CAT_FOOD, '"Yes, I think so."#CATCH_PROS_DESC(pros) "You must have rich experience in keeping cats. Do you know whether cats can eat" $food={#CAT_FOOD()} "?"')
df.add_system_transition(State.CAT_PROS_N, State.FIRST_PET_CAT_FOOD, '"I understand. Although they may bring allergies or schedule disorder, we can\'t deny that they also bring so much joy into our lives. You must have rich experience in keeping cats. Do you know whether cats can eat" $food={#CAT_FOOD()} "?"')
df.add_system_transition(State.CAT_PROS_UNKNOWN, State.FIRST_PET_CAT_FOOD, '"Interesting idea. I have to say that with almost no effort at all, pets manage to bring so much joy into our lives. They make us laugh, comfort us when we’re sick or upset, and are always there for us no matter what. You must have rich experience in keeping cats. Do you know whether cats can eat" $food={#CAT_FOOD()} "?"')

df.add_system_transition(State.PETS_PROS_DB, State.FIRST_PET_DOG_FOOD, '"Yes, I think so."#CATCH_PROS_DESC(pros) "You must have rich experience in keeping pets. Do you know whether dog can eat" $food={#DOG_FOOD()}"?"')
df.add_system_transition(State.PETS_PROS_N, State.FIRST_PET_DOG_FOOD, '"I understand. Although they may bring schedule disorder, we can\'t deny that they also bring so much joy into our lives. You must have rich experience in keeping pets. Do you know whether dogs can eat" $food={#DOG_FOOD()}"?"')
df.add_system_transition(State.PETS_PROS_UNKNOWN, State.FIRST_PET_DOG_FOOD, '"Interesting idea. I have to say that with almost no effort at all, pets manage to bring so much joy into our lives. They make us laugh, comfort us when we’re sick or upset, and are always there for us no matter what. You must have rich experience in keeping pets. Do you know whether dogs can eat" $food={#DOG_FOOD()}"?"')

# User Turn
df.add_user_transition(State.PETS_CONS, State.PETS_CONS_DB, '[$cons=#CATCH_CONS()]')
df.add_user_transition(State.PETS_CONS, State.PETS_CONS_N, '[#CATCH_NO()]')
df.add_user_transition(State.PETS_CONS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.PETS_CONS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.PETS_CONS, State.PETS_CONS_UNKNOWN)

# System Turn
df.add_system_transition(State.PETS_CONS_DB, State.END, '"Yes, I think so."#CATCH_CONS_DESC(cons)')
df.add_system_transition(State.PETS_CONS_N, State.END, '"I understand. Also, it\'s really a great responsibility to keep a pet."')
df.add_system_transition(State.PETS_CONS_UNKNOWN, State.END, '"Interesting idea. I have to say that owning a pet is a great responsibility."')

######################### Pet Food Part ##############################################################################################
# User Turn & Error Transition - Answer Food
df.add_user_transition(State.FIRST_PET_DOG_FOOD, State.FIRST_PET_DOG_FOOD_Y, '[#CATCH_YES()]')
df.add_user_transition(State.FIRST_PET_DOG_FOOD, State.FIRST_PET_DOG_FOOD_N, '[#CATCH_NO()]')
df.add_user_transition(State.FIRST_PET_DOG_FOOD, State.FIRST_PET_DOG_FOOD_USER, '[$food=#CATCH_DOG_FOOD()]')
df.add_user_transition(State.FIRST_PET_DOG_FOOD, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FIRST_PET_DOG_FOOD, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FIRST_PET_DOG_FOOD, State.FIRST_PET_DOG_FOOD_UNKNOWN)

df.add_user_transition(State.FIRST_PET_CAT_FOOD, State.FIRST_PET_CAT_FOOD_Y, '[{#CATCH_YES(), can, should}]')
df.add_user_transition(State.FIRST_PET_CAT_FOOD, State.FIRST_PET_CAT_FOOD_N, '[{#CATCH_NO(), cant, shouldnt}]')
df.add_user_transition(State.FIRST_PET_CAT_FOOD, State.FIRST_PET_CAT_FOOD_USER, '[$food=#CATCH_CAT_FOOD()]')
df.add_user_transition(State.FIRST_PET_CAT_FOOD, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FIRST_PET_CAT_FOOD, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FIRST_PET_CAT_FOOD, State.FIRST_PET_CAT_FOOD_UNKNOWN)

# System Turn
df.add_system_transition(State.FIRST_PET_DOG_FOOD_Y, State.ANOTHER_DOG_BREED, '"Yes. As far as I know," #CATCH_DOG_FOOD_DESC(food) "I know a lot about dog breeds."{Are you familiar with, Do you know} $another_breed=#DOG_RANDOM_BREED(breed)"?"')
df.add_system_transition(State.FIRST_PET_CAT_FOOD_Y, State.ANOTHER_CAT_BREED, '"Yes. As far as I know," #CATCH_CAT_FOOD_DESC(food) "I know a lot about cat breeds."{Are you familiar with, Do you know} $another_breed=#CAT_RANDOM_BREED(breed)"?"')

df.add_system_transition(State.FIRST_PET_DOG_FOOD_N, State.ANOTHER_DOG_BREED, '"Well. As far as I know," #CATCH_DOG_FOOD_DESC(food) "I know a lot about dog breeds."{Are you familiar with, Do you know} $another_breed=#DOG_RANDOM_BREED(breed)"?"')
df.add_system_transition(State.FIRST_PET_CAT_FOOD_N, State.ANOTHER_CAT_BREED, '"Well. As far as I know," #CATCH_CAT_FOOD_DESC(food) "I know a lot about cat breeds."{Are you familiar with, Do you know} $another_breed=#CAT_RANDOM_BREED(breed)"?"')

df.add_system_transition(State.FIRST_PET_DOG_FOOD_USER, State.ANOTHER_DOG_BREED, '"My pleasure. As far as I know," #CATCH_DOG_FOOD_DESC(food) "I know a lot about dog breeds."{Are you familiar with, Do you know} $another_breed=#DOG_RANDOM_BREED(breed)"?"')
df.add_system_transition(State.FIRST_PET_CAT_FOOD_USER, State.ANOTHER_CAT_BREED, '"My pleasure. As far as I know," #CATCH_CAT_FOOD_DESC(food) "I know a lot about cat breeds."{Are you familiar with, Do you know} $another_breed=#CAT_RANDOM_BREED(breed)"?"')

df.add_system_transition(State.FIRST_PET_DOG_FOOD_UNKNOWN, State.ANOTHER_DOG_BREED, '"I am not familiar with it, but I will learn about it in the future. Also, I know a lot about dog breeds."{Are you familiar with, Do you know} $another_breed=#DOG_RANDOM_BREED(breed)"?"')
df.add_system_transition(State.FIRST_PET_CAT_FOOD_UNKNOWN, State.ANOTHER_CAT_BREED, '"I am not familiar with it, but I will learn about it in the future. Also, I know a lot about cat breeds."{Are you familiar with, Do you know} $another_breed=#CAT_RANDOM_BREED(breed)"?"')

####################### Favorite Pet Part ##########################################################################################################################
# User Turn
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_DOG, '[{dog, dogs}]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_CAT, '[{cat, cats}]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_OTHER, '[{other, others}]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_DOG_DONTKNOW, '[{i dont know, i have no idea}]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_DOG_BREED, '[$breed=#CATCH_DOG_BREED()]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_CAT_BREED, '[$breed=#CATCH_CAT_BREED()]')
df.add_user_transition(State.FAVORITE_PET, State.FAVORITE_PET_OTHER_BREED, '[$breed=#CATCH_OTHER_BREED()]')
df.add_user_transition(State.FAVORITE_PET, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FAVORITE_PET, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FAVORITE_PET, State.FAVORITE_PET_UNKNOWN)

# System Turn - Transition to Another Dog Breed Introduction Part
df.add_system_transition(State.FAVORITE_PET_DOG, State.FAVORITE_PET_DOG_ANS, '{Nice choice, Good choice, Cool, Wonderful, Wow, Awesome}"! I like dogs! Among various dog breeds, my favorite one is" #DOG_RANDOM_BREED() ".What about you?"')
df.add_system_transition(State.FAVORITE_PET_CAT, State.FAVORITE_PET_CAT_ANS, '{Nice choice, Good choice, Cool, Wonderful, Wow, Awesome}"! I like cats! Among various cat breeds, my favorite one is" #CAT_RANDOM_BREED() ".What about you?"')
df.add_system_transition(State.FAVORITE_PET_OTHER, State.FAVORITE_PET_OTHER_ANS, '"There are lots of other types of pets, i am curious about what it is?"')
df.add_system_transition(State.FAVORITE_PET_UNKNOWN, State.ANOTHER_DOG_BREED, '{Cool,Wow, Awesome}"! that\'s great! But I\'m not quite familiar with this animal, I will learn about it in the future. I know a lot about dogs."{Are you familiar with, Do you know} $another_breed=#DOG_RANDOM_BREED(breed)"?"')

# User Turn
df.add_user_transition(State.FAVORITE_PET_DOG_ANS, State.FAVORITE_PET_DOG_BREED, '[$breed=#CATCH_DOG_BREED()]')
df.add_user_transition(State.FAVORITE_PET_DOG_ANS, State.FAVORITE_PET_DOG_DONTKNOW, '[{i dont know, i have no idea, no idea, dont know}]')
df.add_user_transition(State.FAVORITE_PET_DOG_ANS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FAVORITE_PET_DOG_ANS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FAVORITE_PET_DOG_ANS, State.FAVORITE_PET_DOG_UNKNOWN)

df.add_user_transition(State.FAVORITE_PET_CAT_ANS, State.FAVORITE_PET_CAT_BREED, '[$breed=#CATCH_CAT_BREED()]')
df.add_user_transition(State.FAVORITE_PET_CAT_ANS, State.FAVORITE_PET_CAT_DONTKNOW, '[{i dont know, i have no idea, no idea, dont know}]')
df.add_user_transition(State.FAVORITE_PET_CAT_ANS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FAVORITE_PET_CAT_ANS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FAVORITE_PET_CAT_ANS, State.FAVORITE_PET_CAT_UNKNOWN)

df.add_user_transition(State.FAVORITE_PET_OTHER_ANS, State.FAVORITE_PET_OTHER_BREED, '[$breed=#CATCH_OTHER_BREED()]')
df.add_user_transition(State.FAVORITE_PET_OTHER_ANS, State.FAVORITE_PET_OTHER_DONTKNOW, '[{i dont know, i have no idea, no idea, dont know}]')
df.add_user_transition(State.FAVORITE_PET_OTHER_ANS, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.FAVORITE_PET_OTHER_ANS, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.FAVORITE_PET_OTHER_ANS, State.FAVORITE_PET_OTHER_UNKNOWN)

# System Turn - Transition to Another Dog or Cat Breed Introduction Part
df.add_system_transition(State.FAVORITE_PET_DOG_UNKNOWN, State.ANOTHER_DOG_BREED, '{Cool,Wonderful,Wow, Awesome}"!although i know lots of dog breed, I\'m not quite familiar with the one you mentioned, but i\'m sure they must be very lovable in some way. I know some other dog breeds."{Are you familiar with, Do you know} $another_breed=#DOG_RANDOM_BREED(breed)"?"')
df.add_system_transition(State.FAVORITE_PET_DOG_BREED, State.ANOTHER_DOG_BREED, '{Cool,Wonderful,Wow, Awesome}"!"$breed",they are wonderful creatures! I may consider adopting one in the future! I also know many other dog breeds."{Are you familiar with, Do you know}$another_breed=#DOG_RANDOM_BREED(breed)"?"')
df.add_system_transition(State.FAVORITE_PET_DOG_DONTKNOW, State.ANOTHER_DOG_BREED, '"That\'s OK. I know a lot about dog breeds. My favorite dog breed is" $another_breed=#DOG_RANDOM_BREED()".Have you heard about it?"')

df.add_system_transition(State.FAVORITE_PET_CAT_UNKNOWN, State.ANOTHER_CAT_BREED, '{Cool,Wow, Awesome}"!although I know lots of cat breed, I\'m not quite familiar with the one you mentioned, but i\'m sure they must be very lovable in some way. I know some other cat breeds."{Are you familiar with, Do you know}$another_breed=#CAT_RANDOM_BREED(breed)"?"')
df.add_system_transition(State.FAVORITE_PET_CAT_BREED, State.ANOTHER_CAT_BREED, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"!"$breed",they are wonderful creatures! I may consider adopting one in the future! I also know many other cat breeds. "{Are you familiar with, Do you know}$another_breed=#CAT_RANDOM_BREED(breed)"?"')
df.add_system_transition(State.FAVORITE_PET_CAT_DONTKNOW, State.ANOTHER_CAT_BREED, '"That\'s OK. I know a lot about cat breeds. My favorite cat breed is" $another_breed=#CAT_RANDOM_BREED()".Have you heard about it?"')

# System Turn - Transition to Interesting Facts Part
df.add_system_transition(State.FAVORITE_PET_OTHER_UNKNOWN, State.OTHER_INTERESTING, '"oops, sorry, although i know people love all kinds of animals, I\'m not quite familiar with the one you mentioned, but i\'m sure they must be very lovable in some way. I learned some interesting facts about animals recently. would you like to listen one?"')
df.add_system_transition(State.FAVORITE_PET_OTHER_BREED, State.OTHER_INTERESTING, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"!"#OTHER_BREED_DESC(breed)",they are wonderful creatures! I may consider keeping one in the future. I learned some interesting facts about animals recently. would you like to listen one?"')
df.add_system_transition(State.FAVORITE_PET_OTHER_DONTKNOW, State.ANOTHER_DOG_BREED, '"That\'s OK. I know lots of information about different dog breeds. One of my favorite dog breed is" $another_breed=#DOG_RANDOM_BREED() ".Have you heard about it?"')

####################### Another Dog and Cat Breed Introduction Part ################################################################################################
# User Turn
df.add_user_transition(State.ANOTHER_DOG_BREED, State.ANOTHER_DOG_BREED_Y, '[#CATCH_YES()]')
df.add_user_transition(State.ANOTHER_DOG_BREED, State.ANOTHER_DOG_BREED_N, '[#CATCH_NO()]')
df.add_user_transition(State.ANOTHER_DOG_BREED, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.ANOTHER_DOG_BREED, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.ANOTHER_DOG_BREED, State.ANOTHER_DOG_BREED_N)

df.add_user_transition(State.ANOTHER_CAT_BREED, State.ANOTHER_CAT_BREED_Y, '[#CATCH_YES()]')
df.add_user_transition(State.ANOTHER_CAT_BREED, State.ANOTHER_CAT_BREED_N, '[#CATCH_NO()]')
df.add_user_transition(State.ANOTHER_CAT_BREED, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.ANOTHER_CAT_BREED, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.ANOTHER_CAT_BREED, State.ANOTHER_CAT_BREED_N)

# System Turn
df.add_system_transition(State.ANOTHER_DOG_BREED_Y, State.DOG_INTERESTING, '{Nice,Good, Cool,Wonderful,Wow, Awesome}"!Sounds like you know a lot about dogs. I also know a lot about other dog breeds too. I learned some interesting facts about dogs recently."{Would you like to listen one, Would you like to know one}"?"')
# df.add_system_transition(State.ANOTHER_DOG_BREED_N, State.DOG_INTERESTING, '{"Well,"} #DOG_RANDOM_BREED(breed, another_breed) "I also know a lot about other dog breeds too. I would like to share one interesting thing about dogs which I learned recently."{Would you like to listen one, Would you like to know one}"?"')
df.add_system_transition(State.ANOTHER_DOG_BREED_N, State.DOG_INTERESTING, '{"Well,"} #DOG_BREED_DESC(another_breed) "I also know a lot about other dog breeds too. I would like to share one interesting thing about dogs which I learned recently."{Would you like to listen one, Would you like to know one}"?"')

df.add_system_transition(State.ANOTHER_CAT_BREED_Y, State.CAT_INTERESTING, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"!Sounds like you know a lot about cats. I also know a lot about other cat breeds too.I learned some interesting facts about cats recently."{Would you like to listen one, Would you like to know one}"?"')
# df.add_system_transition(State.ANOTHER_CAT_BREED_N, State.CAT_INTERESTING, '{"Well,"} #CAT_RANDOM_BREED(breed, another_breed) "I also know a lot about other cat breeds too. I would like to share one interesting thing about cats which I learned recently."{Would you like to listen one, Would you like to know one}"?"')
df.add_system_transition(State.ANOTHER_CAT_BREED_N, State.CAT_INTERESTING, '{"Well,"} #CAT_BREED_DESC(another_breed) "I also know a lot about other cat breeds too. I would like to share one interesting thing about cats which I learned recently."{Would you like to listen, Would you like to know}"?"')

# # User Turn
# df.add_user_transition(State.ANOTHER_DOG_BREED_DETAIL, State.ANOTHER_DOG_BREED_Y, '[{#CATCH_YES(),$another_breed=#DOG_BREED()}]')
# df.add_user_transition(State.ANOTHER_DOG_BREED_DETAIL, State.ANOTHER_DOG_BREED_N, '[#CATCH_NO()]')
# df.set_error_successor(State.ANOTHER_DOG_BREED_DETAIL, State.ANOTHER_DOG_BREED_N)
#
# df.add_user_transition(State.ANOTHER_CAT_BREED_DETAIL, State.ANOTHER_CAT_BREED_Y, '[{#CATCH_YES(),$another_breed=#CAT_BREED()}]')
# df.add_user_transition(State.ANOTHER_CAT_BREED_DETAIL, State.ANOTHER_CAT_BREED_N, '[#CATCH_NO()]')
# df.set_error_successor(State.ANOTHER_CAT_BREED_DETAIL, State.ANOTHER_CAT_BREED_N)

####################### Interesting Facts Part ######################################################################################################################
# User Turn
df.add_user_transition(State.DOG_INTERESTING, State.DOG_INTERESTING_Y, '[#CATCH_YES()]')
df.add_user_transition(State.DOG_INTERESTING, State.DOG_INTERESTING_N, '[#CATCH_NO()]')
df.add_user_transition(State.DOG_INTERESTING, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.DOG_INTERESTING, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.DOG_INTERESTING, State.DOG_INTERESTING_N)

df.add_user_transition(State.CAT_INTERESTING, State.CAT_INTERESTING_Y, '[#CATCH_YES()]')
df.add_user_transition(State.CAT_INTERESTING, State.CAT_INTERESTING_N, '[#CATCH_NO()]')
df.add_user_transition(State.CAT_INTERESTING, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.CAT_INTERESTING, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.CAT_INTERESTING, State.CAT_INTERESTING_N)

df.add_user_transition(State.OTHER_INTERESTING, State.OTHER_INTERESTING_Y, '[#CATCH_YES()]')
df.add_user_transition(State.OTHER_INTERESTING, State.OTHER_INTERESTING_N, '[#CATCH_NO()]')
df.add_user_transition(State.OTHER_INTERESTING, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.OTHER_INTERESTING, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.OTHER_INTERESTING, State.OTHER_INTERESTING_N)

# System Turn
df.add_system_transition(State.DOG_INTERESTING_Y, State.DOG_MOVIE, '"One of the most intereting fact I think is that,"#DOG_INTERESTING()"Since I am a dog lover, I watched lots of dog movies. My favorite one is" $movie={#DOG_MOVIE()} ".Have you watched it?"')
df.add_system_transition(State.CAT_INTERESTING_Y, State.CAT_MOVIE, '"One of the most intereting fact I think is that,"#CAT_INTERESTING()"Since I am a cat lover, I watched lots of cat movies. My favorite one is" $movie={#CAT_MOVIE()} ".Have you watched it?"')
df.add_system_transition(State.OTHER_INTERESTING_Y, State.OTHER_MOVIE, '"One of the most intereting fact I think is that,"#OTHER_INTERESTING()"Since I am an animal lover, I watched lots of animal movies. My favorite one is" $movie={#OTHER_MOVIE()} ".Have you watched it?"')

df.add_system_transition(State.DOG_INTERESTING_N, State.DOG_MOVIE, '{Ok, Alright, Then, Well}",since I am a dog lover, I watched lots of dog movies. My favorite one is" $movie={#DOG_MOVIE()} ".Have you watched it?"')
df.add_system_transition(State.CAT_INTERESTING_N, State.CAT_MOVIE, '{Ok, Alright, Then, Well}",since I am a cat lover, I watched lots of cat movies. My favorite one is" $movie={#CAT_MOVIE()} ".Have you watched it?"')
df.add_system_transition(State.OTHER_INTERESTING_N, State.OTHER_MOVIE, '{Ok, Alright, Then, Well}",since I am an animal lover, I watched lots of animal movies. My favorite one is" $movie={#OTHER_MOVIE()} ".Have you watched it?"')

# Error Transition
# df.set_error_successor(State.DOG_INTERESTING_Y, State.DOG_INTERESTING_OTHER)
# df.set_error_successor(State.CAT_INTERESTING_Y, State.CAT_INTERESTING_OTHER)
# df.set_error_successor(State.OTHER_INTERESTING_Y, State.OTHER_INTERESTING_OTHER)

# df.add_system_transition(State.DOG_INTERESTING_OTHER, State.DOG_MOVIE, '"Oops, no more fun facts about them that I know of right now. But I also know lots of movies about dogs. My favorite one is" $movie={#DOG_MOVIE()} ".Would you like to know some detail about it?"')
# df.add_system_transition(State.CAT_INTERESTING_OTHER, State.DOG_MOVIE, '"Oops, no more fun facts about them that I know of right now. But I also know lots of movies about cats. My favorite one is" $movie={#CAT_MOVIE()} ".Would you like to know some detail about it?"')
# df.add_system_transition(State.OTHER_INTERESTING_OTHER, State.DOG_MOVIE, '"Oops, no more fun facts about them that I know of right now. But I also know lots of movies about animals. My favorite one is" $movie={#OTHER_MOVIE()} ".Would you like to know some detail about it?"')

####################### Movie Part ##############################################################################################################################
# User Turn
df.add_user_transition(State.DOG_MOVIE, State.DOG_MOVIE_Y, '[#CATCH_YES()]')
df.add_user_transition(State.DOG_MOVIE, State.DOG_MOVIE_N,'[#CATCH_NO()]')
df.add_user_transition(State.DOG_MOVIE, State.MOVIE_USER,'[$user_movie={#CATCH_DOG_MOVIE(),#CATCH_CAT_MOVIE(),#CATCH_OTHER_MOVIE()}]')
df.add_user_transition(State.DOG_MOVIE, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.DOG_MOVIE, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.DOG_MOVIE, State.MOVIE_UNKNOWN)

df.add_user_transition(State.CAT_MOVIE, State.CAT_MOVIE_Y, '[#CATCH_YES()]')
df.add_user_transition(State.CAT_MOVIE, State.CAT_MOVIE_N,'[#CATCH_NO()]')
df.add_user_transition(State.CAT_MOVIE, State.MOVIE_USER,'[$user_movie={#CATCH_DOG_MOVIE(),#CATCH_CAT_MOVIE(),#CATCH_OTHER_MOVIE()}]')
df.add_user_transition(State.CAT_MOVIE, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.CAT_MOVIE, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.CAT_MOVIE, State.MOVIE_UNKNOWN)

df.add_user_transition(State.OTHER_MOVIE, State.OTHER_MOVIE_Y, '[#CATCH_YES()]')
df.add_user_transition(State.OTHER_MOVIE, State.OTHER_MOVIE_N,'[#CATCH_NO()]')
df.add_user_transition(State.OTHER_MOVIE, State.MOVIE_USER,'[$user_movie={#CATCH_DOG_MOVIE(),#CATCH_CAT_MOVIE(),#CATCH_OTHER_MOVIE()}]')
df.add_user_transition(State.OTHER_MOVIE, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.OTHER_MOVIE, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.OTHER_MOVIE, State.MOVIE_UNKNOWN)

# System Turn
# df.add_system_transition(State.DOG_MOVIE_Y, State.DOG_MOVIE_DETAIL, '{Nice,Good, Cool,Wonderful,Wow, Awesome}"It is really an amazing movie. I also watched many other dog movies. Would you like to hear some details about the one called" $another_movie=#DOG_MOVIE(movie) "?"')
# df.add_system_transition(State.DOG_MOVIE_N, State.DOG_MOVIE_DETAIL, '"It is really an amazing movie. An overview of" $movie "is that" #DOG_MOVIE_DESC(movie) "I also watched many other dog movies. Would you like to hear some details about the one called" $another_movie=#DOG_MOVIE(movie) "?"')
#
# df.add_system_transition(State.CAT_MOVIE_Y, State.CAT_MOVIE_DETAIL, '{Nice,Good, Cool,Wonderful,Wow, Awesome}"It is really an amazing movie. I also watched many other cat movies. Would you like to hear some details about the one called" $another_movie=#CAT_MOVIE(movie) "?"')
# df.add_system_transition(State.CAT_MOVIE_N, State.CAT_MOVIE_DETAIL, '"It is really an amazing movie. An overview of" $movie "is that" #CAT_MOVIE_DESC(movie) "I also watched many other cat movies. Would you like to hear some details about the one called" $another_movie=#CAT_MOVIE(movie) "?"')
#
# df.add_system_transition(State.OTHER_MOVIE_Y, State.OTHER_MOVIE_DETAIL, '{Nice,Good, Cool,Wonderful,Wow, Awesome}"It is really an amazing movie. I also watched many other animal movies. Would you like to hear some details about the one called" $another_movie=#OTHER_MOVIE(movie) "?"')
# df.add_system_transition(State.OTHER_MOVIE_N, State.OTHER_MOVIE_DETAIL, '"It is really an amazing movie. An overview of" $movie "is that" #OTHER_MOVIE_DESC(movie) "I also watched many other animal movies. Would you like to hear some details about the one called" $another_movie=#OTHER_MOVIE(movie) "?"')
#
# df.add_system_transition(State.MOVIE_USER, State.DOG_MOVIE_DETAIL, '{Ok, Well}",An overview of" $user_movie "is that" {#DOG_MOVIE_DESC(user_movie),#CAT_MOVIE_DESC(user_movie),#OTHER_MOVIE_DESC(user_movie)} "It is really an amazing movie. I also watched many other dog movies. Would you like to hear some details about the one called" $another_movie=#DOG_MOVIE(movie)"?"')
# df.add_system_transition(State.MOVIE_UNKNOWN, State.DOG_MOVIE_DETAIL, '{Ok, Well}",I didn\'t hear about this movie before. I will learn about it in the future. I watched many other dog movies. Would you like to hear some details about the one called" another_$movie=#DOG_MOVIE(movie) "?"')

df.add_system_transition(State.DOG_MOVIE_Y, State.DOG_MOVIE_DETAIL, '{Nice,Good, Cool,Wonderful,Wow, Awesome}"It is really an amazing movie. I also watched many other dog movies. Would you like to hear some details about the one called" $another_movie=#DOG_MOVIE(movie) "?"')
df.add_system_transition(State.DOG_MOVIE_N, State.MOVIE_DETAIL_INTERESTING, '"It is really an amazing movie. An overview of" $movie "is that" #DOG_MOVIE_DESC(movie) {"It\'s worth watching.","Does it sound interesting to you?"}')

df.add_system_transition(State.CAT_MOVIE_Y, State.CAT_MOVIE_DETAIL, '{Nice,Good, Cool,Wonderful,Wow, Awesome}"It is really an amazing movie. I also watched many other cat movies. Would you like to hear some details about the one called" $another_movie=#CAT_MOVIE(movie) "?"')
df.add_system_transition(State.CAT_MOVIE_N, State.MOVIE_DETAIL_INTERESTING, '"It is really an amazing movie. An overview of" $movie "is that" #CAT_MOVIE_DESC(movie) {"It\'s worth watching.","Does it sound interesting to you?"}')

df.add_system_transition(State.OTHER_MOVIE_Y, State.OTHER_MOVIE_DETAIL, '{Nice,Good, Cool,Wonderful,Wow, Awesome}"It is really an amazing movie. I also watched many other animal movies. Would you like to hear some details about the one called" $another_movie=#OTHER_MOVIE(movie) "?"')
df.add_system_transition(State.OTHER_MOVIE_N, State.MOVIE_DETAIL_INTERESTING, '"It is really an amazing movie. An overview of" $movie "is that" #OTHER_MOVIE_DESC(movie) {"It\'s worth watching.","Does it sound interesting to you?"}')

df.add_system_transition(State.MOVIE_USER, State.DOG_MOVIE_DETAIL, '"Oh,"$user_movie".I watched this movie before. It is really an amazing movie. I also watched many other dog movies. Would you like to hear some details about the one called" $another_movie=#DOG_MOVIE(movie)"?"')
df.add_system_transition(State.MOVIE_UNKNOWN, State.DOG_MOVIE_DETAIL, '{Ok, Well}",I didn\'t hear about this movie before. I will learn about it in the future. I watched many other dog movies. Would you like to hear some details about the one called" another_$movie=#DOG_MOVIE(movie) "?"')

# User Turn
df.add_user_transition(State.DOG_MOVIE_DETAIL, State.DOG_MOVIE_ANOTHER_Y, '[#CATCH_YES()]')
df.add_user_transition(State.DOG_MOVIE_DETAIL, State.DOG_MOVIE_ANOTHER_N,'[#CATCH_NO()]')
df.add_user_transition(State.DOG_MOVIE_DETAIL, State.MOVIE_USER,'[$user_movie={#CATCH_DOG_MOVIE(),#CATCH_CAT_MOVIE(),#CATCH_OTHER_MOVIE()}]')
df.add_user_transition(State.DOG_MOVIE_DETAIL, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.DOG_MOVIE_DETAIL, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.DOG_MOVIE_DETAIL, State.DOG_MOVIE_ANOTHER_N)

df.add_user_transition(State.CAT_MOVIE_DETAIL, State.CAT_MOVIE_ANOTHER_Y, '[#CATCH_YES()]')
df.add_user_transition(State.CAT_MOVIE_DETAIL, State.CAT_MOVIE_ANOTHER_N,'[#CATCH_NO()]')
df.add_user_transition(State.CAT_MOVIE_DETAIL, State.MOVIE_USER,'[$user_movie={#CATCH_DOG_MOVIE(),#CATCH_CAT_MOVIE(),#CATCH_OTHER_MOVIE()}]')
df.add_user_transition(State.CAT_MOVIE_DETAIL, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.CAT_MOVIE_DETAIL, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.CAT_MOVIE_DETAIL, State.CAT_MOVIE_ANOTHER_N)

df.add_user_transition(State.OTHER_MOVIE_DETAIL, State.OTHER_MOVIE_ANOTHER_Y, '[#CATCH_YES()]')
df.add_user_transition(State.OTHER_MOVIE_DETAIL, State.OTHER_MOVIE_ANOTHER_N,'[#CATCH_NO()]')
df.add_user_transition(State.OTHER_MOVIE_DETAIL, State.MOVIE_USER,'[$user_movie={#CATCH_DOG_MOVIE(),#CATCH_CAT_MOVIE(),#CATCH_OTHER_MOVIE()}]')
df.add_user_transition(State.OTHER_MOVIE_DETAIL, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.OTHER_MOVIE_DETAIL, State.STOP, '[#CATCH_STOP()]')
df.set_error_successor(State.OTHER_MOVIE_DETAIL, State.OTHER_MOVIE_ANOTHER_N)

df.add_user_transition(State.MOVIE_DETAIL_INTERESTING, State.MOVIE_DETAIL_INTERESTING_Y, '[#CATCH_YES()]')
df.add_user_transition(State.MOVIE_DETAIL_INTERESTING, State.DOG_MOVIE_ANOTHER_N,'[#CATCH_NO()]')
df.add_user_transition(State.MOVIE_DETAIL_INTERESTING, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.MOVIE_DETAIL_INTERESTING, State.STOP, '[#CATCH_STOP()]')
df.add_user_transition(State.MOVIE_DETAIL_INTERESTING, State.MOVIE_USER,'[$user_movie={#CATCH_DOG_MOVIE(),#CATCH_CAT_MOVIE(),#CATCH_OTHER_MOVIE()}]')
df.set_error_successor(State.MOVIE_DETAIL_INTERESTING, State.DOG_MOVIE_ANOTHER_N)

# System Turn
df.add_system_transition(State.DOG_MOVIE_ANOTHER_Y, State.JOKE_Q, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $another_movie "is that" #DOG_MOVIE_DESC(another_movie) "By the way," $joke=#PET_JOKE()')
df.add_system_transition(State.DOG_MOVIE_ANOTHER_N, State.JOKE_Q, '{Ok, Alright, Then, Well}",I have to say it is really a good time to stay at home and watch some movies because of the coronavirus. By the way,"$joke=#PET_JOKE()')

df.add_system_transition(State.CAT_MOVIE_ANOTHER_Y, State.JOKE_Q, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $another_movie"is that" #CAT_MOVIE_DESC(another_movie)"By the way," $joke=#PET_JOKE()')
df.add_system_transition(State.CAT_MOVIE_ANOTHER_N, State.JOKE_Q, '{Ok, Alright, Then, Well}",I have to say it is really a good time to stay at home and watch some movies because of the coronavirus. By the way,"$joke=#PET_JOKE()')

df.add_system_transition(State.OTHER_MOVIE_ANOTHER_Y, State.JOKE_Q, '{Nice choice,Good choice, Cool,Wonderful,Wow, Awesome}"! An overview of" $another_movie"is that" #OTHER_MOVIE_DESC(another_movie) "By the way," $joke=#PET_JOKE()')
df.add_system_transition(State.OTHER_MOVIE_ANOTHER_N, State.JOKE_Q, '{Ok, Alright, Then, Well}",I have to say it is really a good time to stay at home and watch some movies because of the coronavirus. By the way," $joke=#PET_JOKE()')

df.add_system_transition(State.MOVIE_DETAIL_INTERESTING_Y, State.JOKE_Q, '"I\'m glad that you like it. By the way," $joke=#PET_JOKE()')

######################## Little Components ################################################################################################
# User Turn
df.add_user_transition(State.JOKE_Q, State.JOKE_W, '[what]')
df.set_error_successor(State.JOKE_Q, State.JOKE_A)
df.add_user_transition(State.JOKE_Q, State.OFFENSE, '[#CATCH_OFFENSE()]')
df.add_user_transition(State.JOKE_Q, State.STOP, '[#CATCH_STOP()]')

# System Turn
df.add_system_transition(State.JOKE_A, State.END, '"Yeah, the answer is,"#PET_JOKE_DESC(joke) "I hope you enjoyed the joke!"')
df.add_system_transition(State.JOKE_W, State.END, '"Hahaha, it\'s just a joke. The answer is,"#PET_JOKE_DESC(joke) "I hope you enjoyed it!"')

######################## Offense and Stop #######################################################################################################
# System Turn
df.add_system_transition(State.OFFENSE, State.END, '"That was not the nicest thing to say. Anyways, "')
df.add_system_transition(State.STOP, State.STOP_FINAL, '"Well, I have been glad to talk about pets with you, but we can move on."')

####################### End Pet Component ##############################################################################################################################################
# END
# df.set_error_successor(State.PETS_PROS_ANS, State.PETS_END)
# df.add_system_transition(State.PETS_END, State.END, '"I\'m glad to talk with you. What other topics would you like to talk about?"')

df.update_state_settings(State.END, system_multi_hop=True)
df.update_state_settings(State.STOP_FINAL, system_multi_hop=True)

# df.add_system_transition(State.END, State.START, '" "')

# end (recurrent) the dialogue

if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    df.precache_transitions()
    # run the DialogueFlow in interactive mode to test
    # df.run(debugging=True)
    df.run(debugging=False)

#GATE()