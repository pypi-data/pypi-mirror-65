import sys
sys.path.append('.')
sys.path.append('..')

from emora_stdm import DialogueFlow
from modules.macro import *
from enum import Enum


# states are typically represented as an enum
class State(Enum):
    START = 0
    ERROR = 1
    END = 2

    START_COVID19 = 3
    START_COVID19_YES = 4
    GENERAL_SUMMARY = 5
    ASK_LOCATION = 6
    REPLY_LOCATION = 7
    REPLY_NO_LOCATION = 8
    ASK_FACT = 9
    REPLY_FACT = 10
    ASK_SYMPTOM_YES = 11
    ASK_SYMPTOM_NO = 12
    REPLY_SYMPTOM = 13


# initialize objects
covid = Dataset()
custom_macros = {'DetectLocation': DetectLocation(locations=covid.locations, stats=covid.stats),
                 'SummaryLocation': SummaryLocation(stats=covid.stats),
                 'RandomFact': RandomFact()}
df = DialogueFlow(State.START, macros=custom_macros)


# summary of region - 1st turn
df.add_system_transition(State.START, State.START_COVID19, "I heard there is a serious outbreak happening right now and really hope you are feeling healthy. Do you want to chat about coronavirus happenings")
df.add_user_transition(State.START_COVID19, State.START_COVID19_YES, "[{sure, yes, yea, yup, yep, i do, yeah, okay, of course, please}]")
df.add_system_transition(State.START_COVID19_YES, State.GENERAL_SUMMARY, "As of today, {} people are tested positive with {} confirmed deaths from COVID 19. Lets continue. which U.S. state, county or nation do you live in".format(int(covid.total_confirmed_today), int(covid.total_deaths_today)))

# error handling - 1st turn
df.set_error_successor(State.START_COVID19, State.END)


# provide location stats - 2nd turn
df.add_user_transition(State.GENERAL_SUMMARY, State.ASK_LOCATION, "[$location=#DetectLocation()]")
df.add_system_transition(State.ASK_LOCATION, State.REPLY_LOCATION, "#SummaryLocation(location)")
df.add_user_transition(State.REPLY_LOCATION, State.ASK_LOCATION, "[$location=#DetectLocation()]") # loop back
df.set_error_successor(State.GENERAL_SUMMARY, State.REPLY_NO_LOCATION)
df.add_system_transition(State.REPLY_NO_LOCATION, State.REPLY_LOCATION, "Well, I did not find any statistic of this region. You can try county or state names. Are you interested in hearing some facts about coronavirus")


# ask random fact - 3rd turn
df.add_user_transition(State.REPLY_LOCATION, State.ASK_FACT, "[{sure, yes, yea, yup, yep, i do, yeah, okay, of course, please}]")
df.add_system_transition(State.ASK_FACT, State.REPLY_FACT, "#RandomFact(). Are you aware of known symptoms for coronavirus")
df.set_error_successor(State.REPLY_LOCATION, State.ERROR)


# ask symptom - 4th turn
df.add_user_transition(State.REPLY_FACT, State.ASK_SYMPTOM_YES, "[{sure, yes, yea, yup, yep, i do, yeah, okay, of course, please}]")
df.add_user_transition(State.REPLY_FACT, State.ASK_SYMPTOM_NO, "[{no, nope, nah, sorry, stop, exit, shut up, cancel}]")
df.add_system_transition(State.ASK_SYMPTOM_YES, State.REPLY_SYMPTOM, "Cool, this must be a reminder for you. Coronavirus has 2 to 14 days of incubation period. Common symptoms include fever, dry cough and breathing problems. Please seek immediate treatment if you are experiencing these symptoms.")
df.add_system_transition(State.ASK_SYMPTOM_NO, State.REPLY_SYMPTOM, "Well, you should definitely remember this fact. Coronavirus has 2 to 14 days of incubation period. Common symptoms include fever, dry cough and breathing problems. Please seek immediate treatment if you are experiencing these symptoms.")
df.add_user_transition(State.REPLY_FACT, State.ASK_LOCATION, "[$location=#DetectLocation()]") # loop back


# error handling - 4th turn
df.set_error_successor(State.REPLY_FACT, State.ERROR)
df.set_error_successor(State.REPLY_SYMPTOM, State.ERROR)


# loop back to start
# df.add_system_transition(State.ERROR, State.END, "Allright, what do you want to chat next")
# df.set_error_successor(State.END, State.START)


# infinite loop
#df.add_system_transition(State.ERROR, State.END, "Allright, what do you want to chat next")
#df.set_error_successor(State.END, State.ERROR)

if __name__ == "__main__":
    df.check()
    df.precache_transitions()
    df.run(debugging=False)

