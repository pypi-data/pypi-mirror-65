from emora_stdm import KnowledgeBase, DialogueFlow, NatexNLU
from enum import Enum, auto
import os

# Define the states that your conversation will use
# All states that you use in transitions later need to be in this class

class State(Enum):
    S0 = auto()
    U0 = auto()
    S1A = auto()
    S1B = auto()
    U1 = auto()
    S2_google = auto()
    S2_htc = auto()
    S2_samsung = auto()
    S2_oculus = auto()
    S2_playstation = auto()
    U2 = auto()
    S3A = auto()
    S3B = auto()
    U3A = auto()
    U3B = auto()
    S4A = auto()
    S4B = auto()
    S4C = auto()
    U4 = auto()
    S5A = auto()
    S5B = auto()
    U5 = auto()
    S6_ugly= auto()
    S6_expensive = auto()
    U6 = auto()
    S7A = auto()
    S7B = auto()
    U7 = auto()
    S8A = auto()
    S8B = auto()
    S8C = auto()
    U8 = auto()
    S9 = auto()
    U9 = auto()
    S10A = auto()
    S10B = auto()
    U10 = auto()
    END = auto()
    ERR = auto()
    STOP_AR = auto()

    S2_what_is_vr = auto()
    vr_unknown = auto()
    S4_what_is_ar = auto()
    ar_unknown = auto()
    unknown_model=auto()
    unknown_reason=auto()
    unknown_vr_time=auto()
    dont_remember_like=auto()
    dont_remember_sick=auto()
    dont_know_ar_reason=auto()
    dont_know_glasses=auto()
    dont_know_ar_success=auto()
    dont_remember_current_state=auto()
    dont_know_investment=auto()
    dont_remember_using=auto()

knowledge = KnowledgeBase()
knowledge.load_json_file(os.path.join('modules',"vr.json"))
df = DialogueFlow(State.S0, initial_speaker=DialogueFlow.Speaker.USER, kb=knowledge)

dont_know = '[{' \
            'dont know,do not know,unsure,[not,{sure,certain}],hard to say,no idea,uncertain,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[{dont,do not}, have, {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[!{cant,cannot,dont} {think,remember,recall}]' \
            '}]'

# Initalize Yes, Yes+vr, and No for first question
df.add_system_transition(State.S0, State.U0,
                         r'[!I have recently started learning about Virtual Reality"." Have you ever used Virtual Reality"," otherwise known as V R"," before"?"]')
df.set_error_successor(State.S0, State.S0)

# Yes+VR Company Answer
df.add_user_transition(State.U0, State.S2_google, "<$VR=#ONT(ontgoogle)>")
df.add_user_transition(State.U0, State.S2_htc, "<$VR=#ONT(onthtc)>")
df.add_user_transition(State.U0, State.S2_samsung, "<$VR=#ONT(ontsamsung)>")
df.add_user_transition(State.U0, State.S2_oculus, "<$VR=#ONT(ontoculus)>")
df.add_user_transition(State.U0, State.S2_playstation, "<$VR=#ONT(ontsony)>")
vr_unknown = '{' \
               '[{[!{dont,do not}, know],not sure,unsure,uncertain}, what, {that,v r,vr,virtual,reality,it,you said}, {is,mean,means}],' \
               '[what,is,{that,it,v r,vr,virtual,reality,you said}],' \
               '[what,does,{that,v r,vr,virtual,reality,it,you said},mean]' \
               '}'
df.add_user_transition(State.U0, State.S2_what_is_vr, vr_unknown, score=0.9)
df.add_system_transition(State.S2_what_is_vr, State.U0, '"Oh, that\'s alright. Virtual reality is a new technology '
                                                        'that puts you into the middle of a three dimensional virtual world and lets you interact with it, like a video game. '
                                                        'You wear a pair of special glasses. Some companies that make these devices right now are google and oculus. So, have you ever tried anything like this before?"')

df.add_user_transition(State.U0, State.dont_remember_using, dont_know, score=0.8)
df.add_system_transition(State.dont_remember_using, State.U4, '"I feel like you would remember if you had tried V R before. It is pretty cool! '
                                                              'Another emerging area is augmented reality, or A R. What do you think of augmented reality?"')

# Fact about company

df.add_system_transition(State.S2_google, State.U2,
                         r'[!Google Cardboard is really amazing and my personal favorite"," it lets anyone with a smartphone '
                         r'experience the future with Virtual Reality"!" When was the last time you tried V R "?"]')

df.add_system_transition(State.S2_htc, State.U2,
                         r'[!HTC Vive"," although expensive"," uses futuristic 3D tracked controllers to let you '
                         r'feel even closer to the Virtual Environment"!" When was the last time you tried V R "?"]')

df.add_system_transition(State.S2_samsung, State.U2,
                         r'[!Samsung Gear are glasses that make use of a samsung phone along with a controller '
                         r'to allow you to do cool things like browse the web or watch netflix in a seemingly theater sized room"!" '
                         r'When did you try it last "?"]')

df.add_system_transition(State.S2_oculus, State.U2,
                         r'[!Oculus Rift was the first PC powered gaming headset"," letting you delve into your '
                         r'favorite games"!" When was the last time you tried V R"?"]')

df.add_system_transition(State.S2_playstation, State.U2,
                         r'[!Playstation morpheus was revolutionary to bring the full V R experience to console gaming'
                         r' "!" When was the last time you tried V R "?"]')

# Yes Answer
yes_natex = NatexNLU('{yes,yeah,yea,have,yup,once,twice,few,sometimes,occasionally,frequently}')
df.add_user_transition(State.U0, State.S1B, yes_natex)
df.add_system_transition(State.S1B, State.U1, r'[!Which V R device did you use "?"]')
df.add_user_transition(State.U1, State.S2_google, "<$VR=#ONT(ontgoogle)>")
df.add_user_transition(State.U1, State.S2_htc, "<$VR=#ONT(onthtc)>")
df.add_user_transition(State.U1, State.S2_samsung, "<$VR=#ONT(ontsamsung)>")
df.add_user_transition(State.U1, State.S2_oculus, "<$VR=#ONT(ontoculus)>")
df.add_user_transition(State.U1, State.S2_playstation, "<$VR=#ONT(ontsony)>")

df.add_system_transition(State.unknown_model, State.S2_google, '"Ok, well, "')
df.update_state_settings(State.S2_google, system_multi_hop=True)

# No Answer
no = r"[{no,not,nope,nah,never,havent,didnt}]"
no_natex = NatexNLU(no)
df.add_user_transition(State.U0, State.S1A, no_natex)
df.add_system_transition(State.S1A, State.U4,
                         r'[!"Oh, that is unfortunate, you should definitely try it sometime, V R is slowly becoming the future of gaming and even '
                         r' industrial uses. My favorite is Google Cardboard because of how accessible it is to everyone! Another emerging area'
                         r' is augmented reality, or A R"." what do you think of augmented reality?"]')

# Time since used

# Dont remember
df.add_user_transition(State.U2, State.unknown_vr_time, dont_know)
df.add_system_transition(State.unknown_vr_time, State.U3A,
                         '"That\'s ok. I have a hard time remembering specific details like that sometimes, too. '
                         'What did you like about the V R headset you used?"')

# Short Time

short = r"[{today,hour,hours,yesterday,week,weeks,day, days,month,months}]"
short_natex = NatexNLU(short)

df.add_user_transition(State.U2, State.S3A, short_natex)
df.add_system_transition(State.S3A, State.U3A,
                         r'[!Thats great "!" You may have used one of the newer models with many new features such as higher resolution displays and '
                         r' faster refresh rates to help with motion sickness "!" What did you like about the V R headset you used "?"]')

df.add_user_transition(State.U3A, State.dont_remember_like, dont_know)
df.add_system_transition(State.dont_remember_like, State.U4, '"Yeah, it can be hard to pick out something that you like. Even though V R was getting a lot of press, '
                                                             'something else is kind of taking its place at the moment. Augmented Reality, or A R, is more widespread '
                                                             'than V R right now. What do you think of augmented reality?"')

sentence_natex = NatexNLU('/.*/')
df.add_user_transition(State.U3A, State.S4A, sentence_natex, score=0.9)
df.add_system_transition(State.S4A, State.U4,
                         r'[!Yeah"," well"," just wait"." With time"," this technology will progress even more "!" But there has been '
                         r'a decrease in the presence of V R"," in favor of Augmented Reality"," or A R"." what do you think of A R "?"]')

# Long Time
long = r"[{year,years,long,while}]"
long_natex = NatexNLU(long)

df.add_user_transition(State.U2, State.S3B, long_natex)
df.add_system_transition(State.S3B, State.U3B,
                         r'[!It sounds like it may have been some time since you have used a V R headset"." there have been many new upgrades since the older models"." '
                         r'Do you remember ever feeling motion sickness or nauseousness from using the headset "?"]')

yes_nat = r"[{yes,yeah,have,did}]"
yes_natex_reader = NatexNLU(yes_nat)
df.add_user_transition(State.U3B, State.S4B, yes_natex_reader)
df.add_system_transition(State.S4B, State.U4,
                         r'[!You most likely felt sick because the older generation of headsets had worse graphics '
                         r'that would cause motion sickness"." These issues are being fixed in todays models"." '
                         r'Even so"," there has been a decrease in the popularity of V R"," in favor of '
                         r'Augmented Reality"," or A R"." What do you think of A R "?"]')

df.add_user_transition(State.U3B, State.S4C, no_natex)
df.add_system_transition(State.S4C, State.U4,
                         r'"That is really interesting. Because studies have found that 40 to 60 percent of people on V R headsets were motion sick after playing. But there has been a decrease in the progression of V R, as it gives way to Augmented Reality, or A R. What do you think of A R?"')

df.add_user_transition(State.U3B, State.dont_remember_sick, dont_know, score=0.8)
df.add_system_transition(State.dont_remember_sick, State.U4, '"Hopefully you didn\'t feel that way. It is not fun! '
                                                              'Another emerging area is augmented reality, or A R. What do you think of augmented reality?"')

# AR Section:

# What is AR
ar_unknown = '{' \
               '[{[!{dont,do not}, know],not sure,unsure,uncertain}, what, {that,a r,ar,augmented,reality,it,you said}, {is,mean,means}],' \
               '[what,is,{that,it,a r,ar,augmented,reality,you said}],' \
               '[what,does,{that,a r,ar,augmented,reality,it,you said},mean],' \
               '[#NOT(you),never,heard,{that,a r,ar,augmented,reality,it,you said}],' \
               '[#NOT(you),have,no,idea,what,{that,a r,ar,augmented,reality,it,you said},{is,mean,means}]' \
               '}'
df.add_user_transition(State.U4, State.S4_what_is_ar, ar_unknown, score=0.9)
df.add_system_transition(State.S4_what_is_ar, State.STOP_AR, '"Yeah, not everyone knows of augmented reality devices. Augmented reality is a new technology '
                                                        'that allows virtual images to be placed on top of what you are looking at in the real world, using either  '
                                                        ' glasses or cameras. You should definitely check it out. Anyways, "')
# df.add_system_transition(State.S4_what_is_ar, State.STOP_AR, '"Since you do not seem to know too much about it, I think we should talk about something else. "', score=0.0)
df.update_state_settings(State.STOP_AR, system_multi_hop=True)

df.add_user_transition(State.U4, State.dont_know_ar_reason, dont_know, score=0.8)
df.add_system_transition(State.dont_know_ar_reason, State.STOP_AR, '"You don\'t have any ideas? That is ok. It is still a relatively new thing, so it may be hard '
                                                              'to form an opinion. Anyways, "')
# df.add_system_transition(State.dont_know_ar_reason, State.U6, '"You don\'t have any ideas? That is ok. It is still a relatively new thing, so it may be hard '
#                                                               'to form an opinion. If you were to play a mobile game using A R, what would make it the most fun, '
#                                                               'do you think?"')

# Gaming
game = r"[{game,games,gaming}]"
game_natex = NatexNLU(game)
df.add_user_transition(State.U4, State.S5B, game_natex)
df.add_system_transition(State.S5B, State.U6,
                         r'[!A R is becoming popularized by mobile gaming applications"." Companies like Apple are pushing '
                         r' things such as the A R kit"," bringing games to the space around you with the aid of the camera"."'
                         r' what do you think is important for making a good A R game "?"]')

# Glasses
glass = r"[{glass,glasses,wearable,wearables}]"
glass_natex = NatexNLU(glass)
df.add_user_transition(State.U4, State.S5A, glass_natex)
df.add_system_transition(State.S5A, State.U5,
                         r'[!Different types of A R glasses have slowly been growing in popularity"." '
                         r'what is your opinion on A R glasses"?"]')


df.add_system_transition(State.unknown_reason, State.S5B, '"Sure, that\'s a good point. What I have heard is that "')
df.update_state_settings(State.S5B, system_multi_hop=True)

# why not glasses
# Ugly
ugly = r"[{ugly,clunky,poor ergonomics,bad,dont,[not,stylish],[not,fashionable]}]"
ugly_natex = NatexNLU(ugly)
df.add_user_transition(State.U5, State.S6_ugly, ugly_natex)
df.add_system_transition(State.S6_ugly, State.U6,
                         r'[!That is very true"." Glasses today have become more of a fashion statement"," and '
                         r'the A R glasses are not very stylish"." But A R has had some popular successes"," especially in gaming"."'
                         r' why do you think A R games have been so successful"?"]')

# Expensive
expensive = r"[{pricey,expensive,money,cost}]"
expensive_natex = NatexNLU(expensive)
df.add_user_transition(State.U5, State.S6_expensive, expensive_natex)
df.add_system_transition(State.S6_expensive, State.U6,
                         r'[!Because of the low amount of A R glasses in the market and their complex design"," '
                         r'they are very expensive compared to regular prescription glasses"." '
                         r'But A R still has had some popular successes"," especially in gaming"." '
                         r'why do you think A R games are so much fun to many people"?"]')

df.add_user_transition(State.U5, State.dont_know_glasses, dont_know)
df.add_system_transition(State.dont_know_glasses, State.S6_expensive, '"No opinion on A R glasses? yeah, i guess it is a pretty specialized topic. What I know about it is that, "')
df.update_state_settings(State.S6_expensive, system_multi_hop=True)

# Reasons for Pokemon Go success
# Health
health = r"[{physical,exercise,roam,outdoors,outside,walk,walking,adventure,nature,sun,sunlight}]"
health_natex = NatexNLU(health)
df.add_user_transition(State.U6, State.S7A, health_natex)
df.add_system_transition(State.S7A, State.U7,
                         r'[!Yeah"," in my opinion"," the best A R games encourage individuals to '
                         r' move around and interact with their real world environment to progress in the game"." '
                         r'how do you think augmented reality will effect society as it becomes more mainstream "?"]')

# Social Interaction
social = r"[{social,interaction,talk,interact,friends,communication,teamwork}]"
social_natex = NatexNLU(social)
df.add_user_transition(State.U6, State.S7B, social_natex)
df.add_system_transition(State.S7B, State.U7, r'[!A R games have a powerful ability to increase physical '
                                              r'social interactions rather than the virtual ones found in other games.'
                                              r'how do you think augmented reality will effect society as it becomes more mainstream "?"]')

df.add_user_transition(State.U6, State.dont_know_ar_success, dont_know)
df.add_system_transition(State.dont_know_ar_success, State.U7, '"It is hard to predict what could be fun without actually trying it out yourself, for sure. '
                                                              'For you personally, how do you predict that augmented reality will affect you in the future? "')

# Effects of AR
# positive
positive = r"[{efficiency,good,positive,positively,awesome,cool,helpful,nice,sweet,fun,enjoyable,entertaining,entertainment,engaging,engagement,interactive}]"
positive_natex = NatexNLU(positive)
df.add_user_transition(State.U7, State.S8A, positive_natex)
df.add_system_transition(State.S8A, State.U8,
                         r'[!You think it will have some positive effect"?" I tend to agree"," but the effects of A R are highly debated right now"." '
                         r'I believe that A R has the power to improve human life"," such as making shopping easier '
                         r'or being used as a form of job training"." So"," How do you feel '
                         r'about the current state of mobile A R"?"]')

df.add_system_transition(State.S8C, State.U8,
                         '[!Interesting"." Well"," I believe that A R has the power to improve'
                         r' human life"," such as making shopping easier or being used as a form of job training"."'
                         r'So"," How do you feel about the current state of mobile A R"?"]')

# Negative
negative = r"[{distractions,distraction,distracted,distract,unaware, annoying,negative,antisocial,bad,dangerous,scary,horrible,awful,terrible,frightening}]"
negative_natex = NatexNLU(negative)
df.add_user_transition(State.U7, State.S8B, negative_natex)
df.add_system_transition(State.S8B, State.U8,
                         r'[!I can see why you would think about the negative impacts of A R"." It can be dangerous to have a screen always in our vision while '
                         r'doing daily tasks"." It definitely needs to be carefully implemented to preserve safety"." '
                         r'How do you feel about the current state of mobile A R"?"]')

# Current State of Mobile AR
df.add_user_transition(State.U8, State.S9, sentence_natex,score=0.9)

df.add_user_transition(State.U8, State.dont_remember_current_state, dont_know)
df.add_system_transition(State.dont_remember_current_state, State.END, '"That\'s alright to not have an opinion. It is a difficult question to assess the current state of mobile A R. '
                                                                      'I think that the future of this technology is very exciting!"')

# Is AR a good investment today
df.add_system_transition(State.S9, State.END,
                         r'"For sure. I think that they may not be super impressive right now, but their future is exciting!"')


# df.add_user_transition(State.U10, State.END, "/.*/")
# df.add_system_transition(State.END, State.END,
#                          r'[!Thank you for the wonderful conversation, have a nice rest of your day "!"]')

#df.add_system_transition(State.ERR, State.ERR, r"[!Oops...I Broke]")
#ERROR STATES
df.add_system_transition(State.ERR, State.END, r"")
df.update_state_settings(State.ERR, system_multi_hop=True)
df.update_state_settings(State.END, system_multi_hop=True)

df.set_error_successor(State.U0, error_successor=State.S1B)
df.set_error_successor(State.U1, error_successor=State.unknown_model)
df.set_error_successor(State.U2, error_successor=State.S3A)
df.set_error_successor(State.U3A, error_successor=State.S4C)
df.set_error_successor(State.U3B, error_successor=State.S4C)
df.set_error_successor(State.U4, error_successor=State.unknown_reason)
df.set_error_successor(State.U5, error_successor=State.S6_ugly)
df.set_error_successor(State.U6, error_successor=State.S7A)
df.set_error_successor(State.U7, error_successor=State.S8C)
df.set_error_successor(State.U8, error_successor=State.S9)
# df.set_error_successor(State.U9, error_successor=State.S10B)

if __name__ == "__main__":
    #df.precache_transitions()
    df.run(debugging=True)