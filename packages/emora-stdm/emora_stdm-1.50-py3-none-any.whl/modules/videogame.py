from emora_stdm import DialogueFlow
from enum import Enum




# states are typically represented as an enum
class State(Enum):
    START = 0
    IF_PLAY = 1
    DO_PLAY = 2
    NOT_PLAY = 3
    # IF_PLAY_ERROR = 4
    CONSOLE = 5
    COMPUTER = 6
    MOBILE = 7
    WHICH_PLATFORM_ERROR = 8
    WHICH_PLATFORM = 9
    RECOMMEND = 10
    WHICH_COMPUTER = 11
    LOL = 12
    PUBG = 13
    FORTNITE = 14
    OVERWATCH = 15
    HEARTHSTONE = 16
    WHICH_COMPUTER_ERROR = 17
    WHICH_CHAMPION = 18
    FIZZ = 19
    RIVEN = 20
    YASUO = 21
    KATERINA = 22
    VAYNE = 23
    LEESIN = 24
    WHICH_CHAMPION_ERROR = 25
    GREAT = 26
    GARBAGE = 27
    ADC = 28
    PLAYRECENTLY = 29
    NOTPLAYRECENTLY = 30
    ADCWEAK = 31
    ADCSTRONG = 32
    GREAT_ERROR = 33
    ADC_ERROR = 34
    IF_WIN = 35
    PLAYATALL = 36
    EMORAADCWEAK = 37
    EMORAADCSTRONG = 38
    DIDWIN = 39
    DIDNOTWIN = 40
    VLADIMIR = 41
    KAYN = 42
    EZREAL = 43
    TEEMO = 44
    ORNN =45
    DARIUS = 46
    MASTERYI = 47
    SINGED = 48
    TALON = 49
    PYKE = 50
    SETT = 51
    SORAKA = 52
    DRMUNDO =  53
    ZOE = 54
    MORDEKAISER = 55
    GAREN = 56
    ZED = 57
    VR = 58
    VR_Component = 59
    CONGRATS = 60
    OKTOLOSE = 61
    CARRYGAME = 62
    BADTEAMMATE = 63
    ENDSTATE = 64
    RECOMMEND_PLEASE = 65
    RECOMMEND_WHICH_PLATFORM = 66
    RECOMMEND_COMPUTER = 67
    RECOMMEND_CONSOLE = 68
    RECOMMEND_MOBILE = 69
    RECOMMEND_PLATFORM_ERROR= 70
    RECOMMEND_LEAGUE = 71
    RECOMMEND_APEX = 72
    RECOMMEND_HEARTHSTONE = 73
    RANDOMGAME = 74
    RECOMMEND_RANDOMGAME = 75
    WHICH_CONSOLE = 76
    WHICH_MOBILE = 77
    WHICH_CONSOLE_ERROR = 78
    WHICH_MOBILE_ERROR = 79
    RECOMMEND_COMPUTER2 = 80
    RECOMMEND_OVERWATCH = 81
    RECOMMEND_CONSOLE2 = 82
    RECOMMEND_MOBILE2 = 83
    RECOMMEND_MINECRAFT = 84
    RECOMMEND_POKEMONGO = 85
    CONSOLE2 = 86
    APEX = 87
    MINECRAFT = 88
    WHENPLAY = 89
    WITHFRIEND = 90
    LONGTIMEAGO = 91
    SHORTTIMEAGO = 92
    WITHFRIEND_IF_WIN = 93
    WITHOUTFRIEND_IF_WIN = 94
    WHICH_PLATFORM2 = 95
    WHICH_PLATFORM_ERROR_2 = 96
    POKEMONGO = 97
    WHICH_PLATFORM_2 = 98
    WHICH_PLATFORM_ERROR2 = 99
    RECOMMEND_CONSOLE_2 = 100


# initialize the DialogueFlow object, which uses a state-machine to manage dialogue
df = DialogueFlow(State.START)

df.add_system_transition(State.START, State.IF_PLAY, '"do you play video games"')

df.add_user_transition(State.IF_PLAY, State.DO_PLAY,'[{yes, yea, yup, yep, i do, yeah, sometimes,sure}]')
df.add_user_transition(State.IF_PLAY, State.NOT_PLAY, '[{no, nope, not really}]')
df.set_error_successor(State.IF_PLAY, State.NOT_PLAY)

# , or do you like vr
df.add_system_transition(State.DO_PLAY, State.WHICH_PLATFORM, '"great, i play a lot of PC games. which kind of platform do you play games? on PC, mobile phones, on console such as Xbox or PS4?"')

df.add_user_transition(State.WHICH_PLATFORM, State.COMPUTER, '[{computer, windows, mac, pc}]')
df.add_user_transition(State.WHICH_PLATFORM, State.CONSOLE, '[{xbox, psfour, nintendo, psp, console,ps,p.s.}]')
df.add_user_transition(State.WHICH_PLATFORM, State.MOBILE, '[{phone, mobile phone, iphone, ios, android,mobile}]')
df.add_user_transition(State.WHICH_PLATFORM, State.VR, '[{vr,v.r.}]')
df.set_error_successor(State.WHICH_PLATFORM, State.WHICH_PLATFORM_ERROR)

df.add_user_transition(State.WHICH_PLATFORM_2, State.COMPUTER, '[{computer, windows, mac, pc}]')
df.add_user_transition(State.WHICH_PLATFORM_2, State.CONSOLE, '[{xbox, psfour, nintendo, psp, console,ps,p.s.}]')
df.add_user_transition(State.WHICH_PLATFORM_2, State.MOBILE, '[{phone, mobile phone, iphone, ios, android,mobile}]')
# df.add_user_transition(State.WHICH_PLATFORM2, State.VR, '[{vr,v.r.}]')
df.set_error_successor(State.WHICH_PLATFORM_2, State.WHICH_PLATFORM_ERROR_2)

df.add_system_transition(State.COMPUTER, State.WHICH_COMPUTER, '"great, which computer game is your favorite"')
df.add_system_transition(State.CONSOLE, State.WHICH_CONSOLE, '"great, which console game is your favorite"')
df.add_system_transition(State.MOBILE, State.WHICH_MOBILE, '"great, which mobile game is your favorite"')
# df.add_system_transition(State.VR, State.VR_Component, '" Lets talk about virtual reality! Have you used VR before?"')


df.add_user_transition(State.WHICH_CONSOLE, State.APEX,'[{apex}]')
df.add_user_transition(State.WHICH_CONSOLE, State.MINECRAFT, '[{minecraft}]')
df.set_error_successor(State.WHICH_CONSOLE, State.WHICH_CONSOLE_ERROR)


df.add_user_transition(State.WHICH_MOBILE, State.HEARTHSTONE,'[{hearthstone, stone}]')
df.add_user_transition(State.WHICH_MOBILE, State.POKEMONGO, '[{pokemongo, pokemon}]')
df.set_error_successor(State.WHICH_MOBILE, State.WHICH_MOBILE_ERROR)


df.add_system_transition(State.WHICH_CONSOLE_ERROR, State.RECOMMEND_CONSOLE, '"sorry, i actually dont know that game, what was that game? it sounds like a game that requires teamwork."')
df.add_system_transition(State.MINECRAFT, State.WHENPLAY, '"wow, i am glad that you do play minecraft. I also love sandbox games when was the last time that you played minecraft?"')
df.add_system_transition(State.APEX, State.WHENPLAY, '"wow, i am glad that you do play apex. when was the last time that you played apex?"')
df.add_system_transition(State.POKEMONGO, State.WHENPLAY, '"wow, i am glad that you do play pokemon go. It is a fun game based on the popular pokemon anime. when was the last time that you played pokemon go?"')
df.add_system_transition(State.HEARTHSTONE, State.WHENPLAY, '"wow, i am glad that you do play hearthstone. it is a very successful strategy game developed by blizzard. my friend George loves this game so much that he actually bought many extension card packs. when was the last time that you played hearthstone?"')
df.add_system_transition(State.PUBG, State.WHENPLAY, '"wow, i am glad that you do play player unknowns battleground.it is a very popular first person shooting game and many of my friends love this game. when was the last time that you played PUBG?"')
df.add_system_transition(State.OVERWATCH, State.WHENPLAY, '"wow, i am glad that you do play overwatch. it is a very popular first person shooting game and many of my friends love this game. when was the last time that you played overwatch?"')
df.add_system_transition(State.FORTNITE, State.WHENPLAY, '"wow, i am glad that you do play fortnite. it is a very popular first person shooting game and many of my friends love this game. when was the last time that you played fortnite?"')



df.set_error_successor(State.WHENPLAY, State.WITHFRIEND)
df.add_user_transition(State.WHENPLAY, State.LONGTIMEAGO, '[{years, year, months, month}]')
df.add_user_transition(State.WHENPLAY, State.SHORTTIMEAGO, '[{weeks, days, week, day, yesterday, today, just now, now, a moment}]')

df.add_system_transition(State.LONGTIMEAGO, State.WITHFRIEND, '"well, that was actually a long time ago. did you play with your friends"')
df.add_system_transition(State.SHORTTIMEAGO, State.WITHFRIEND, '"wow, that was pretty recent. you must love this game very much. did you play with your friends"')
df.add_system_transition(State.WITHFRIEND, State.WITHFRIEND, '"alright, did you play with your friends"')


df.set_error_successor(State.WITHFRIEND, State.WITHOUTFRIEND_IF_WIN)
df.add_user_transition(State.WITHFRIEND, State.WITHFRIEND_IF_WIN, '[{yes, yea, yup, yep, i do, yeah, sometimes,sure}]')

df.add_system_transition(State.WITHFRIEND_IF_WIN, State.IF_WIN, '"nice, it is always fun to play with friends. I personally love multiplayer games and I would love to play videogames with other people. Also, It is easier to win with teamwork. By the way, did you win the game last time you played?"')
df.add_system_transition(State.WITHOUTFRIEND_IF_WIN, State.IF_WIN, '" well,  I personally love multiplayer games and I would love to play videogames with other people. Also, It is easier to win with teamwork. But at the same time, it is also true that some games are not suitable for multiple players playing together. By the way, did you win the game last time you played?"')








df.set_error_successor(State.RECOMMEND_CONSOLE, State.RECOMMEND_CONSOLE_2)

df.add_system_transition(State.RECOMMEND_CONSOLE_2, State.RECOMMEND_APEX, '"wow it sounds pretty fun. actually, i would love to talk about some console games that i like personally"')

# df.set_error_successor(State.RECOMMEND_APEX, State.RECOMMEND_CONSOLE)

df.set_error_successor(State.WHICH_MOBILE, State.WHICH_MOBILE_ERROR)
df.add_system_transition(State.WHICH_MOBILE_ERROR, State.RECOMMEND_CONSOLE, '"sorry, i actually dont know that game, what was that game? it sounds like a game that requires teamwork."')
# df.set_error_successor(State.RECOMMEND_MOBILE, State.RECOMMEND_MOBILE)


df.add_user_transition(State.WHICH_COMPUTER, State.LOL,'[{LOL, league of legends, league,lol}]')
df.add_user_transition(State.WHICH_COMPUTER, State.PUBG,'[{player unknown, pubg}]' )
df.add_user_transition(State.WHICH_COMPUTER, State.FORTNITE,'[{fortnite}]' )
df.add_user_transition(State.WHICH_COMPUTER, State.OVERWATCH,'[{overwatch}]' )
df.add_user_transition(State.WHICH_COMPUTER, State.HEARTHSTONE,'[{hearthstone}]' )
df.set_error_successor(State.WHICH_COMPUTER, State.WHICH_COMPUTER_ERROR)

df.add_system_transition(State.LOL,State.WHICH_CHAMPION,'"I am so glad that you play league of legends. It is one of the my most favorite computer games. I am super good at using fizz. which champion is your favorite"')

df.add_user_transition(State.WHICH_CHAMPION, State.FIZZ, '[{fizz, me too}]')
df.add_user_transition(State.WHICH_CHAMPION, State.RIVEN, '[{riven}]')
df.add_user_transition(State.WHICH_CHAMPION, State.YASUO, '[{yasuo}]')
df.add_user_transition(State.WHICH_CHAMPION, State.KATERINA, '[{kat,katerina}]')
df.add_user_transition(State.WHICH_CHAMPION, State.VAYNE, '[{vayne,vn}]')
df.add_user_transition(State.WHICH_CHAMPION, State.LEESIN, '[{lee,lee sin, sin}]')
df.set_error_successor(State.WHICH_COMPUTER, State.WHICH_CHAMPION_ERROR)
df.add_user_transition(State.WHICH_CHAMPION, State.VLADIMIR, '[{vlad, vladimir}]')
df.add_user_transition(State.WHICH_CHAMPION, State.KAYN, '[{kane, kayn}]')
df.add_user_transition(State.WHICH_CHAMPION, State.EZREAL, '[{ezreal, ez}]')
df.add_user_transition(State.WHICH_CHAMPION, State.TEEMO, '[{teemo}]')
df.add_user_transition(State.WHICH_CHAMPION, State.ORNN, '[{ornn}]')
df.add_user_transition(State.WHICH_CHAMPION, State.DARIUS, '[{dar, darius}]')
df.add_user_transition(State.WHICH_CHAMPION, State.MASTERYI, '[{yi, master yi}]')
df.add_user_transition(State.WHICH_CHAMPION, State.SINGED, '[{singed}]')
df.add_user_transition(State.WHICH_CHAMPION, State.TALON, '[{talon}]')
df.add_user_transition(State.WHICH_CHAMPION, State.PYKE, '[{pyke}]')
df.add_user_transition(State.WHICH_CHAMPION, State.SETT, '[{sett}]')
df.add_user_transition(State.WHICH_CHAMPION, State.SORAKA, '[{soraka, raka}]')
df.add_user_transition(State.WHICH_CHAMPION, State.DRMUNDO, '[{dr mundo, mundo}]')
df.add_user_transition(State.WHICH_CHAMPION, State.ZOE, '[{zoe}]')
df.add_user_transition(State.WHICH_CHAMPION, State.MORDEKAISER, '[{mordkaiser, mord}]')
df.add_user_transition(State.WHICH_CHAMPION, State.GAREN, '[{garen}]')
df.add_user_transition(State.WHICH_CHAMPION, State.ZED, '[{zed}]')
df.set_error_successor(State.WHICH_CHAMPION, State.WHICH_CHAMPION_ERROR)



df.add_system_transition(State.VLADIMIR,State.GREAT,'"vlad is a really interesting champion, although not that many people play him. He is super strong late game, and he can definitely carry your team to victory. have you played this champ recently "')
df.add_system_transition(State.KAYN,State.GREAT,'"kayn is a very cool champion, and his ability to choose between two different forms is very versatile, because of their very different playstyles. have you played this champ recently "')
df.add_system_transition(State.EZREAL,State.GREAT,'"ezreal is a pretty interesting champion, because of his longe range and safety. He has a lot of damage when he hits his abilities. have you played this champ recently "')
df.add_system_transition(State.TEEMO,State.GREAT,'"teemo is an interesting character, although a lot of people hate him for it. his mushrooms are really annoying to play against. have you played this champ recently "')
df.add_system_transition(State.ORNN,State.GREAT,'"ornn is very strong right now, because of his high base damage and ability to upgrade items an extra time, which is very useful. have you played this champ recently "')
df.add_system_transition(State.DARIUS,State.GREAT,'"darius isl a very strong, because his passive makes it hard to fight him for a long time. have you played this champ recently "')
df.add_system_transition(State.MASTERYI,State.GREAT,'"master yi is an interesting champion, and he has a tn of damage. hes pretty easy to pick up, but he also has a lot of potential for more skilled players. have you played this champ recently "')
df.add_system_transition(State.SINGED,State.GREAT,'"singed is a really weird champion but interesting champion. i really dont like playing against him since hes really hard to catch and kills you if you chase him. have you played this champ recently "')
df.add_system_transition(State.TALON,State.GREAT,'"talon is super cool, although hes pretty hard to play. he can really get his teammates ahead by roaming, and he does a ton of damage to squishies. have you played this champ recently "')
df.add_system_transition(State.PYKE,State.GREAT,'"pyke is super cool, and i really like how he can carry games even though  hes a support. he has a ton of damage and also gives his teammates gold, so hes pretty strong. have you played this champ recently "')
df.add_system_transition(State.SETT,State.GREAT,'"sett is a very cool champion. i like how he gets to do a bunch of damage after taking damage. even after riot nerfed him i still think hes pretty strong. have you played this champ recently "')
df.add_system_transition(State.ZED,State.GREAT,'"zed is super cool, although hes really hard to play. his shadows give him a lot of potential to dodge enemies, which is really strong. have you played this champ recently "')
df.add_system_transition(State.SORAKA,State.GREAT,'"soraka is a very powerful champion. she heals a lot right now, and her ultimate gives her a global presence. playing her top lane still seems weird to me, even though its really strong. at least riot is getting rid of that this patch. have you played this champ recently "')
df.add_system_transition(State.DRMUNDO,State.GREAT,'"dr mundo is really cool, and ive had fun playing him. i guess you like being able to tank an entire teams damage and survivng.  have you played this champ recently "')
df.add_system_transition(State.ZOE,State.GREAT,'"zoe is super cool, although i dont like playing against her. there have been too many times where she completely one shots me, although i see why you would like playing her. have you played this champ recently "')
df.add_system_transition(State.MORDEKAISER,State.GREAT,'"mordekaiser is super cool, and he has enough damage to miss his abilities and still kill people. i also think its really cool how he can force a 1v1 with his ultimate. there have been too many times where she completely one shots me, although i see why you would like playing her. have you played this champ recently "')
df.add_system_transition(State.GAREN,State.GREAT,'"garen is pretty cool, even if he is the classic starter champion. he does a lot of damage while also being really tanky, so i see why you would like playing him. have you played this champ recently "')

df.add_system_transition(State.FIZZ,State.GREAT,'"great, i am so glad that you like same champion with me. fizz is currently a tier one champion and has an overall winrate of fifty one percent. it is a very good choice for ranked games. have you played this champ recently "')
df.add_system_transition(State.RIVEN,State.GREAT,'"riven is a super cool champion. in fact, she is one of the most popular champions in league right now. however, this champion is not easy to master. currently, riven only has an overall winrate of forty nine percent and she is a tier four champion. have you played this champ recently"')
df.add_system_transition(State.YASUO,State.GREAT,'"yasuo is super cool. i love it as well. but in my opinion yasuo is acutally a very difficult champion. I lose many games using this champion. have you played this champ recently"')
df.add_system_transition(State.KATERINA,State.GREAT,'"wow, i always respect good katerina players. because katerina is a very difficult champion and she is definitely a good game changer with her passives that refreshes her abilities. have you played this champ recently"')
df.add_system_transition(State.VAYNE,State.ADC,'"it seems that you are an adc player. in this patch, league is not so friendly to adc players because assasins deal too much damage. what do you think "')
df.add_system_transition(State.LEESIN,State.GREAT,'"lee is a super cool champion. in fact, he is one of the most popular champions in league right now. this champion is not easy to master. currently, lee has an overall winrate of forty eight percent and he is a tier one jungler champion. have you played this champ recently "')


df.add_user_transition(State.GREAT, State.PLAYRECENTLY, '[{yes, yea, yup, yep, i do, yeah, sometimes,sure}]')
df.add_user_transition(State.GREAT, State.NOTPLAYRECENTLY,'[{no, nope, not really}]' )

df.add_user_transition(State.ADC, State.ADCWEAK, '[{weak, bad, sad, low, dont}]')
df.add_user_transition(State.ADC, State.ADCSTRONG, '[{not, strong, good}]')
df.set_error_successor(State.GREAT, State.GREAT_ERROR)
df.set_error_successor(State.ADC, State.ADC_ERROR)

df.add_system_transition(State.PLAYRECENTLY, State.IF_WIN, '"wow nice did you win the game?"')
df.add_system_transition(State.NOTPLAYRECENTLY, State.PLAYATALL, '"ok did you play any league game recently at all."')
df.add_system_transition(State.ADCWEAK, State.EMORAADCWEAK, '"yeah, i think a d carrys are weak as well. riot should seriously consider rebalance the game. ok, now guess which position is my favorite."')
df.add_system_transition(State.ADCSTRONG, State.EMORAADCSTRONG, '"well. you must be a very good a d carry player.  ok, now guess which position is my favorite."')

df.add_user_transition(State.IF_WIN, State.DIDWIN, '[{yes, yea, yup, yep, i do, yeah, sometimes,sure}]')
df.add_user_transition(State.IF_WIN, State.DIDNOTWIN, '[{no, nope, not really}]')
df.set_error_successor(State.IF_WIN,State.DIDNOTWIN)

df.add_system_transition(State.DIDWIN, State.CONGRATS,  '"wow, nice, you must have enjoyed that game. tell me more about it. did you perform well"')
df.add_system_transition(State.DIDNOTWIN, State.OKTOLOSE,  '"well, its ok, i mean, its just a game, did you play with some bad players"')

df.set_error_successor(State.CONGRATS, State.CARRYGAME)
df.set_error_successor(State.OKTOLOSE, State.BADTEAMMATE)

df.add_system_transition(State.CARRYGAME, State.ENDSTATE, '"you must be a very good teammate, i hope i could play with you, but i cant. "')
df.add_system_transition(State.BADTEAMMATE, State.ENDSTATE, '"well. thats just so unfortunate"')




df.add_system_transition(State.NOT_PLAY, State.RECOMMEND, '"it is ok, i know some cool games, do you want me to recommend some of those games to you"')

df.add_user_transition(State.RECOMMEND, State.RECOMMEND_PLEASE,'[{yes, yea, yup, yep, i do, yeah, sometimes,sure,please}]')
df.set_error_successor(State.RECOMMEND,State.ENDSTATE)

df.add_system_transition(State.RECOMMEND_PLEASE, State.RECOMMEND_WHICH_PLATFORM, '"alright, games from which platform are you interested in? popular options are pc, console like xbox and psfour or games on mobile phone"')

df.add_user_transition(State.RECOMMEND_WHICH_PLATFORM, State.RECOMMEND_COMPUTER, '[{computer, windows, mac, pc}]')
df.add_user_transition(State.RECOMMEND_WHICH_PLATFORM, State.RECOMMEND_CONSOLE, '[{xbox, psfour, nintendo, psp, console}]')
df.add_user_transition(State.RECOMMEND_WHICH_PLATFORM, State.RECOMMEND_MOBILE, '[{phone, mobile phone, iphone, ios, android}]')
df.set_error_successor(State.RECOMMEND_WHICH_PLATFORM, State.RECOMMEND_PLATFORM_ERROR)


df.add_system_transition(State.RECOMMEND_COMPUTER, State.RECOMMEND_LEAGUE, '"wow, i like playing computer games, i particularly like league of legends. it is a MOBA game that requires teamwork from multiple players.  you could play this game both on mac and on windows. It is actually very popular right now. have you heard about this game before?"')
df.add_system_transition(State.RECOMMEND_CONSOLE, State.RECOMMEND_APEX, '"APEX is a very popular console game right now. it is a free-to-play Battle Royale game where contenders from across the Frontier team up to battle for glory, fame, and fortune. it is actually also available on the pc end "')
df.add_system_transition(State.RECOMMEND_MOBILE, State.RECOMMEND_HEARTHSTONE, '"Hearthstone is my personal favorite mobile game. It is a strategic card game. it is actually very popular"')


df.set_error_successor(State.RECOMMEND_LEAGUE, State.RECOMMEND_COMPUTER2)
df.set_error_successor(State.RECOMMEND_APEX, State.RECOMMEND_CONSOLE2)
df.set_error_successor(State.RECOMMEND_HEARTHSTONE, State.RECOMMEND_MOBILE2)


df.add_system_transition(State.RECOMMEND_COMPUTER2, State.RECOMMEND_OVERWATCH, '"right, i actually have many friends interested in this game. oh, by the way, i also like overwatch, which is a first person shooter game. it is developed by blizzard and it is also pretty popular. "')
df.add_system_transition(State.RECOMMEND_CONSOLE2, State.RECOMMEND_MINECRAFT, '"right, i actually have many friends interested in this game. oh, by the way, i also like minecraft, which is a sandbox video game. it has been released for over 10 years now and it is still extremely popular. "')
df.add_system_transition(State.RECOMMEND_MOBILE2, State.RECOMMEND_POKEMONGO, '"right, i actually have many friends interested in this game. oh, by the way, i also like pokemon go, which is an augmented reality (AR) mobile game . it is based on the popular anime pokemon. it is very fun to play. "')
df.add_system_transition(State.RECOMMEND_PLATFORM_ERROR, State.RANDOMGAME, '"I am actually not familiar with the platform that you must mentioned. I could just recommend some games that I like personally.  "')

df.set_error_successor(State.RANDOMGAME, State.RECOMMEND_RANDOMGAME)



df.add_system_transition(State.RECOMMEND_RANDOMGAME, State.RECOMMEND_LEAGUE, '"to be honest, i like playing computer games, i particularly like league of legends. it is a MOBA game that requires teamwork from multiple players. It is very popular right now. "')

# df.set_error_successor(State.IF_PLAY, State.IF_PLAY_ERROR)
# df.set_error_successor(State.IF_PLAY, State.WHICH_PLATFORM_ERROR)
# df.add_system_transition(State.IF_PLAY_ERROR, State.IF_PLAY, '"I did not hear you clearly, pardon"')
df.add_system_transition(State.WHICH_PLATFORM_ERROR, State.WHICH_PLATFORM_2, '"I did not hear you clearly, pardon"')
df.add_system_transition(State.WHICH_PLATFORM_ERROR_2, State.GARBAGE, '"Alright, i am not very familiar with the platform you just mentioned."')

df.add_system_transition(State.WHICH_COMPUTER_ERROR, State.GARBAGE, '"I just learned to play video games recently so my knowledge in this domain is still limited. could you tell me more about this game? i am very interested in this game. is this game fun? "')
df.add_system_transition(State.WHICH_CHAMPION_ERROR, State.GARBAGE, '"well, i actually dont know this game. could you tell me more about this game"')
df.add_system_transition(State.ADC_ERROR, State.GARBAGE, '"well, i actually dont know this champion. could you tell me more about this champion"')

df.add_system_transition(State.GREAT_ERROR, State.GARBAGE, '"I just learned to play video games recently so my knowledge in this domain is still limited. could you tell me more about this game? i am very interested in this game. is this game fun?"')


#df.add_system_transition(State.ENDSTATE, State.ENDSTATE, '"Alright"')
#df.add_system_transition(State.GARBAGE,State.GARBAGE,'"to be continued"')
df.update_state_settings(State.ENDSTATE, system_multi_hop=True)
df.update_state_settings(State.GARBAGE, system_multi_hop=True)



# add transitions to create an arbitrary graph for the state machine
# df.add_system_transition(State.START, State.FAM_ANS, '[!do you have a $F={brother, sister, son, daughter, cousin}]')
# df.add_user_transition(State.FAM_ANS, State.FAM_Y, '[{yes, yea, yup, yep, i do, yeah}]')
# df.add_user_transition(State.FAM_ANS, State.FAM_N, '[{no, nope}]')
# df.add_system_transition(State.FAM_Y, State.WHATEV, 'thats great i wish i had a $F')
# df.add_system_transition(State.FAM_N, State.WHATEV, 'ok then')
# df.add_system_transition(State.FAM_ERR, State.WHATEV, 'im not sure i understand')

# each state that will be reached on the user turn should define an error transition if no other transition matches
# df.set_error_successor(State.FAM_ANS, State.FAM_ERR)
# df.set_error_successor(State.WHATEV, State.START)

if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    df.precache_transitions()
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=True)

    # 1.29