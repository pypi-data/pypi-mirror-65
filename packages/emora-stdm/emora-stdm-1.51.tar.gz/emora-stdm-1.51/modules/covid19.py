import os, sys
sys.path.append('.')
sys.path.append('..')

from enum import Enum
from emora_stdm import DialogueFlow
from modules.dataset import CovidDataset

# from modules.macro import *
from modules.macro import *


# states are typically represented as an enum
class State(Enum):
    START = 0
    ERROR = 1
    END = 2

    START_COVID19 = 3
    START_COVID19_YES = 4
    START_COVID19_NO = 5

    OPEN_SOCIAL_DISTANCING = 6
    CLOSE_SOCIAL_DISTANCING = 7

    DETECT_TRAVEL = 8
    DETECT_FAMILY = 9
    DETECT_WORK = 10
    DETECT_SOCIAL = 11
    DETECT_YES = 12
    DETECT_FAILURE = 13
    REPLY_TRAVEL = 14
    REPLY_FAMILY = 15
    REPLY_WORK = 16
    REPLY_SOCIAL = 17

    DETECT_FOLLOWUP_TRAVEL = 18
    DETECT_FOLLOWUP_FAMILY = 19
    DETECT_FOLLOWUP_WORK_YES = 20
    DETECT_FOLLOWUP_WORK_NO = 21
    DETECT_FOLLOWUP_SOCIAL = 22
    FOLLOWUP_TRAVEL = 23
    FOLLOWUP_TRAVEL_GENERIC = 24
    FOLLOWUP_FAMILY = 25
    FOLLOWUP_WORK = 26
    FOLLOWUP_WORK_GENERIC = 27
    FOLLOWUP_SOCIAL = 28

    START_INFO = 29
    START_INFO_PASS = 30
    ASK_INFO = 31
    INFO_NO = 32
    INFO_YES = 33
    INFO_LOC = 34
    INFO_REPLY = 35
    INFO_LOOP = 36
    INFO_NOT_FOUND = 37
    INFO_REPLY_AGAIN = 38



# initialize objects
covid = CovidDataset()
custom_macros = {'DetectTravel': DetectTravel(keywords=covid.travel_keywords),
                 'DetectFamily': DetectFamily(keywords=covid.family_keywords),
                 'DetectWork': DetectWork(keywords=covid.work_keywords),
                 'DetectSocial': DetectSocial(keywords=covid.social_keywords),
                 'DetectLocation': DetectLocation(locations=covid.locations),
                 'TravelSummary': TravelSummary(stats=covid.stats),
                 'True': DummyTrue(),
                 'InfoSummary': InfoSummary(stats=covid.stats)}
df = DialogueFlow(State.START, macros=custom_macros)

# rules
yes_keywords = "[{sure, yes, yea, yup, yep, i do, yeah, okay, of course, please, ok}]"
no_keywords = "[{no, not, stop, exit, shut up, sorry, nah, nope, none}]"

# 1st turn
df.add_system_transition(State.START, State.START_COVID19, "I heard that many countries are encouraging social distancing now. This must be very tough. Have you been practicing social distancing actively")
df.add_user_transition(State.START_COVID19, State.START_COVID19_YES, yes_keywords)
df.add_user_transition(State.START_COVID19, State.START_COVID19_NO, no_keywords)
df.add_system_transition(State.START_COVID19_YES, State.OPEN_SOCIAL_DISTANCING, "I am glad you are. One user said that he stopped going to cinemas since two weeks ago. Do you have something that you cannot do anymore because of the ongoing restrictions")
df.add_system_transition(State.START_COVID19_NO, State.CLOSE_SOCIAL_DISTANCING, "Well I highly encourage social distancing to protect you and the people around you. "
                                                                                "As of today, there are about {} confirmed cases in the united states. The {} percent global death rate is also pretty shocking".format(covid.us_confirmed, covid.global_dr))
df.set_error_successor(State.START_COVID19, State.ERROR)
df.set_error_successor(State.CLOSE_SOCIAL_DISTANCING, State.ERROR)


# 2nd turn
df.add_user_transition(State.OPEN_SOCIAL_DISTANCING, State.DETECT_TRAVEL, "[$keyword=#DetectTravel()]")
df.add_user_transition(State.OPEN_SOCIAL_DISTANCING, State.DETECT_FAMILY, "[$keyword=#DetectFamily()]")
df.add_user_transition(State.OPEN_SOCIAL_DISTANCING, State.DETECT_WORK, "[$keyword=#DetectWork()]")
df.add_user_transition(State.OPEN_SOCIAL_DISTANCING, State.DETECT_SOCIAL, "[$keyword=#DetectSocial()]")
df.add_user_transition(State.OPEN_SOCIAL_DISTANCING, State.DETECT_YES, yes_keywords)

df.add_system_transition(State.DETECT_TRAVEL, State.REPLY_TRAVEL, "Many others agree with you. Stuck in one place with no freedom to travel outside is terrible. Which nation or state county were you planning to visit before")
df.add_system_transition(State.DETECT_FAMILY, State.REPLY_FAMILY, "Well, I hope your $keyword is doing well. Definitely try to tell your $keyword to practice social distancing. When was the last time you saw your $keyword")
df.add_system_transition(State.DETECT_WORK, State.REPLY_WORK, "I have heard that maintaining productivity at work these days is difficult. Not surprisingly, over 10 million people applied for unemployemnt benefits. Are you also worried about increasing unemployment")
df.add_system_transition(State.DETECT_SOCIAL, State.REPLY_SOCIAL, "It is completely normal to feel that way since the coronavirus is something that nobody expected or prepared for. How do you feel about the recent stay at home acts from various states")
df.add_system_transition(State.DETECT_YES, State.OPEN_SOCIAL_DISTANCING, "Ok, can you tell me more about it")

df.set_error_successor(State.OPEN_SOCIAL_DISTANCING, State.DETECT_FAILURE)
df.add_system_transition(State.DETECT_FAILURE, State.ASK_INFO, "Yeah, the virus is spreading so rapidly that it is affecting all lives now. Do you want to hear live updates about coronavirus statistics")


# 3rd turn
df.add_user_transition(State.REPLY_TRAVEL, State.DETECT_FOLLOWUP_TRAVEL, "[$location=#DetectLocation()]")
df.add_system_transition(State.DETECT_FOLLOWUP_TRAVEL, State.FOLLOWUP_TRAVEL, "#TravelSummary(location)")

df.add_user_transition(State.REPLY_FAMILY, State.DETECT_FOLLOWUP_FAMILY, "[$dummy=#True()]")
df.add_system_transition(State.DETECT_FOLLOWUP_FAMILY, State.FOLLOWUP_FAMILY, "Thanks for letting me know. I hope everything works out well in the near future for you and your $keyword")

df.add_user_transition(State.REPLY_WORK, State.DETECT_FOLLOWUP_WORK_YES, yes_keywords)
df.add_user_transition(State.REPLY_WORK, State.DETECT_FOLLOWUP_WORK_NO, no_keywords)
df.add_system_transition(State.DETECT_FOLLOWUP_WORK_YES, State.FOLLOWUP_WORK, "I understand. 54 percent of the American population expressed concerns about their own economic situations. The government is introducing new acts to alleviate this issue and lets try to be optimistic for now.")
df.add_system_transition(State.DETECT_FOLLOWUP_WORK_NO, State.FOLLOWUP_WORK, "Glad to hear that. Since you are in stable economic condition, you can primarily focus on staying safe and protecting your loved ones.")

df.add_user_transition(State.REPLY_SOCIAL, State.DETECT_FOLLOWUP_SOCIAL, "[$dummy=#True()]")
df.add_system_transition(State.DETECT_FOLLOWUP_SOCIAL, State.FOLLOWUP_SOCIAL, "Thanks for sharing. I believe stay at home acts are necessary to help people practice social distancing. Bill Gates also claimed the immediate needs of social distancing and potential shutdowns.")

df.set_error_successor(State.REPLY_TRAVEL, State.FOLLOWUP_TRAVEL_GENERIC)
df.set_error_successor(State.REPLY_FAMILY, State.ERROR)
df.set_error_successor(State.REPLY_WORK, State.FOLLOWUP_WORK_GENERIC)
df.set_error_successor(State.REPLY_SOCIAL, State.ERROR)

df.add_system_transition(State.FOLLOWUP_TRAVEL_GENERIC, State.FOLLOWUP_TRAVEL, "Well, I was unable to lookup that place for detailed statistics. However, experts are encouraging everyone to postpone travels for now and I believe you made the right decision")
df.add_system_transition(State.FOLLOWUP_WORK_GENERIC, State.FOLLOWUP_WORK, "I understand. 54 percent of American population expressed concerns about their own economic situations. The government is introducing new acts to alleviate this issue and lets try to be optimistic for now.")


# 4th turn - start info chat
df.add_user_transition(State.FOLLOWUP_TRAVEL, State.START_INFO_PASS, "[$dummy=#True()]")
df.add_user_transition(State.FOLLOWUP_FAMILY, State.START_INFO_PASS, "[$dummy=#True()]")
df.add_user_transition(State.FOLLOWUP_WORK, State.START_INFO_PASS, "[$dummy=#True()]")
df.add_user_transition(State.FOLLOWUP_SOCIAL, State.START_INFO_PASS, "[$dummy=#True()]")
df.add_system_transition(State.START_INFO_PASS, State.ASK_INFO, "Allright. Are you interested in hearing about detailed coronavirus statistics of a specific region")

df.set_error_successor(State.FOLLOWUP_TRAVEL, State.ERROR)
df.set_error_successor(State.FOLLOWUP_FAMILY, State.ERROR)
df.set_error_successor(State.FOLLOWUP_WORK, State.ERROR)
df.set_error_successor(State.FOLLOWUP_SOCIAL, State.ERROR)


# 5th turn
df.add_user_transition(State.ASK_INFO, State.INFO_LOC, "[$location=#DetectLocation()]")
df.add_user_transition(State.ASK_INFO, State.INFO_YES, yes_keywords)
df.add_system_transition(State.INFO_LOC, State.INFO_REPLY, "#InfoSummary(location)")
df.add_system_transition(State.INFO_YES, State.INFO_REPLY, "Sure which country or state county are you interested in")

df.set_error_successor(State.ASK_INFO, State.ERROR)


# potential loop
df.add_user_transition(State.INFO_REPLY, State.INFO_LOOP, "[$location=#DetectLocation()]")
df.add_system_transition(State.INFO_LOOP, State.INFO_REPLY_AGAIN, "#InfoSummary(location)")

df.set_error_successor(State.INFO_REPLY, State.INFO_NOT_FOUND)
df.add_system_transition(State.INFO_NOT_FOUND, State.INFO_REPLY_AGAIN, "Sorry, I was unable to find the location information. Can you say states or counties in the united states")

df.add_user_transition(State.INFO_REPLY_AGAIN, State.INFO_LOOP, "[$location=#DetectLocation()]")
df.set_error_successor(State.INFO_REPLY_AGAIN, State.ERROR)


# infinite loop
# df.add_system_transition(State.ERROR, State.END, "No problem. What do you want to chat next")
# df.set_error_successor(State.END, State.ERROR)



if __name__ == "__main__":
    df.check()
    df.run(debugging=False)

