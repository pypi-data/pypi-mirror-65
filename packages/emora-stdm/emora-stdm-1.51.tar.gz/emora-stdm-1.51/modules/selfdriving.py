from emora_stdm import KnowledgeBase, DialogueFlow, Macro
from emora_stdm.state_transition_dialogue_manager import natex_common
from enum import Enum, auto

class State(Enum):
    CORONAENTRY = auto()
    S1 = auto()
    U1 = auto()
    S2a = auto()
    S2b = auto()
    U2a = auto()
    U2b = auto()
    S3a = auto()
    S3b = auto()
    S3c = auto()
    S3d = auto()
    U3a = auto()
    U3b = auto()
    S4a = auto()
    S4b = auto()
    S4c = auto()
    S4d = auto()
    S4e = auto()
    U4a = auto()
    U4b = auto()
    U4c = auto()
    S5a = auto()
    S5b = auto()
    S5c = auto()
    S5d = auto()
    U5a = auto()
    U5b = auto()
    S6a = auto()
    S6b = auto()
    S6c = auto()
    S6d = auto()
    S6e = auto()
    S6f = auto()
    U6a = auto()
    S7a = auto()
    S7b = auto()
    S7c = auto()
    U7a = auto()
    S8a = auto()
    S8b = auto()
    U8a = auto()
    S9a = auto()
    U9a = auto()
    S10a = auto()
    S10b = auto()
    S10c = auto()
    U10a = auto()
    S11a = auto()
    S11b = auto()
    S11c = auto()
    S11d = auto()
    U11a = auto()
    U11b = auto()
    U11c = auto()
    END = auto()
    END2 = auto()
    ERR1 = auto()
    ERR2 = auto()
    ERR3 = auto()
    ERR4 = auto()
    ERR5 = auto()
    ERR6 = auto()
    ERR7 = auto()
    ERR8 = auto()
    ERR9 = auto()
    ERR10 = auto()
    ERR11 = auto()
    ERR12 = auto()


exp_con = {'more_traffic': 'I agree. Since more people will be able to access to cars, there will be more people and more cars on the road.',
           'less_safety': 'Actually autonomous cars are much safer than human-driven cars based on many studies, so hopefully this helps to calm some of those fears.',
           'hackers': 'Yeah, that is true. Like all computer systems, there is always a risk of the computer being hacked by people with ill intent.',
           'more_crash': 'Actually autonomous cars are much safer and have less crashes than human-driven cars, based on many studies, so hopefully this helps to calm some of those fears.',
           'less_jobs': 'Oh, yeah, that is a concern. Autonomous cars can replace many driving-based jobs, for sure.',
           'expensive': 'I agree. Just like any new technology that has taken years to develop and make, the cost of autonomous cars is likely to be pretty high at first.',
           'enjoy_drive': 'Absolutely. There must be some people who sincerely love driving, so the fully integration of autonomous cars in our transportation system will definitely disappoint them.',
           'laws': 'I agree. There is no comprehensive regulation currently available for autonomous vehicles at the moment and this will need to be figured out.',
           'morals': 'Yeah, this is a pretty big concern with people right now. How to program a machine to make the most ethical choice has a lot of social considerations.',
           'default': 'I had not thought of that, but that is probably a concern to many people.'
           }

exp_pro = {'more_safety': 'For sure! 90% of car accidents are due to human errors such as speeding and drunk driving. Autonomous cars will improve safety a lot since machines are way more accurate.',
           'less_crash': 'For sure! 90% of car accidents are due to human errors such as speeding and drunk driving. Autonomous cars will improve safety a lot since machines are way more accurate.',
           'good_disable': 'For sure! With fully automated cars, people who are not able to drive will now have access to personal vehicles.',
           'less_traffic': 'For sure! Since autonomous cars can sense and communicate with each other, bumper to bumper traffic jams will not happen anymore. Speed limits will probably increase since cars will be in tune with one another.',
           'good_environment': 'For sure! Autonomous cars can be programmed to drive with the most eco-friendly behavior, which will largely reduce the amount of emissions from cars and even improve gas mileage.',
           'free_attention': 'For sure! There definitely are some people who do not like driving or who wish to spend their time in car more efficiently, so autonomous cars will help them out a lot.',
           'default': 'Yeah, that could be a benefit to many people.'
           }

exp_field = {'farm': 'increase efficiency',
             'agriculture': 'increase efficiency',
             'irrigat': 'increase efficiency',
             'deliver': 'save human labor cost',
             'tractor': 'increase efficiency',
             'taxi': 'save human labor cost',
             'mining': 'avoid human injuries caused by mining accidents',
             'drill': 'avoid human injuries caused by drilling accidents',
             'industrial': 'increase efficiency and save human labor cost',
             'forklift': 'increase efficiency and save human labor cost',
             'test': 'be safer',
             'experiment': 'be safer'}

comp_char_dict = {'gm': 'is working on superhuman sensors',
                  'general motor': 'is working on superhuman sensors',
                  'generalmotor': 'is working on superhuman sensors',
                  'cruise': 'is working on superhuman sensors',
                  'argo ai': 'is improving the safety of driverless vehicles',
                  'argoai': 'is improving the safety of driverless vehicles',
                  'zoox': 'is trying to complete automation in complex environments',
                  'tesla':'is the most famous autonomous vehicle company',
                  'ford': 'will have a fully autonomous vehicle in operation by 2021',
                  'aptiv': 'is working on commercializing autonomous vehicles',
                  'toyota': 'is working on commercializing autonomous vehicles',
                  'intel': 'is the leading supplier of software that supports autonomous driving',
                  'volkswagen': 'has a Level 5, fully autonomous vehicle, Sedric',
                  'bosch': 'focus on communication between car and passenger',
                  'nissan':'plans to build commercially viable autonomous vehicles on the road by 2020',
                  'nvidia':'provides autonomous driving software and hardware',
                  'amazon':'provides tons of services to support the development of autonomous driving',
                  'nuro':'designs autonomous vehicles specialized in delivery'}

class elabPro(Macro):
    def run(self, ngrams, vars, args):
        if 'more_safety' in vars:
            return exp_pro['more_safety']
        elif 'less_crash' in vars:
            return exp_pro['less_crash']
        elif 'less_traffic' in vars:
            return exp_pro['less_traffic']
        elif 'good_disable' in vars:
            return exp_pro['good_disable']
        elif 'good_environment' in vars:
            return exp_pro['good_environment']
        elif 'free_attention' in vars:
            return exp_pro['free_attention']
        else:
            return exp_pro['default']

class elabCon(Macro):
    def run(self, ngrams, vars, args):
        if 'less_safety' in vars:
            return exp_con['less_safety']
        elif 'more_crash' in vars:
            return exp_con['more_crash']
        elif 'more_traffic' in vars:
            return exp_con['more_traffic']
        elif 'hackers' in vars:
            return exp_con['hackers']
        elif 'morals' in vars:
            return exp_con['morals']
        elif 'expensive' in vars:
            return exp_con['expensive']
        elif 'less_jobs' in vars:
            return exp_con['less_jobs']
        elif 'enjoy_drive' in vars:
            return exp_con['enjoy_drive']
        elif 'laws' in vars:
            return exp_con['laws']
        else:
            return exp_con['default']

class EXPLfield(Macro):
    def run(self, ngrams, vars, args):
        a = ""
        if 'field' in vars:
            for key in exp_field:
                if key in vars['field']:
                    a = exp_field[key]
        return a

class YEAR(Macro):
    def run(self, ngrams, vars, args):
        curr_year = 2020
        d, s = 0, ""
        if 'year' in vars:
            d = int(vars['year']) - curr_year
            s = str(d) + " years from now"
            vars['n'] = 'test'
        elif 'duration' in vars:
            vars['new'] = 'new'
            d = curr_year + int(vars['duration'])
            s = "around " + str(d)
        return s


class company(Macro):
    def run(self, ngrams, vars, args):
        return 'Waymo, General Motors, and Tesla'


class chooseComp(Macro):
    def run(self, ngrams, vars, args):
        google = ['waymo', 'google', 'alphabet']
        comps = ["ford", "tesla", "zoox"]
        result = ""
        if 'comp' in vars:
            if vars['comp'] not in google:
                for elem in comps:
                    if vars['comp'] in elem:
                        comps.remove(elem)
        for elem in comps[:-1]:
            result += elem + ', '
        return result + "and " + comps[-1]

class COMPCHAR(Macro):
    def run(self, ngrams, vars, args):
        a = ""
        if 'notchosen' in vars:
            for key in comp_char_dict:
                if key in vars['notchosen']:
                    a = comp_char_dict[key]
        return a

ont = {
    "ontology": {
        "other_fields":
            [
                "delivery",
                "deliveries",
                "taxi",
                "taxis",
                "farm",
                "farming",
                "agriculture",
                "irrigator",
                "irrigators",
                "irrigate",
                "irrigation",
                "tractor",
                "tractors",
                "mining",
                "drill",
                "drilling",
                "drillings",
                "industrial",
                "forklift",
                "forklifts",
                "test",
                "tests",
                "testing",
                "experiment",
                "experiments",
                "experimenting"],
        "car_company":[
            "waymo",
            "google",
            "alphabet",
            "gmcruise",
            "gm cruise",
            "gm",
            "cruise",
            "generalmotors",
            "general motors",
            "argoai",
            "argo ai",
            "zoox",
            "tesla",
            "ford",
            "aptiv",
            "intel",
            "mobileye",
            "volkswagen",
            "bosch",
            "toyota",
            "nissan",
            "nvidia",
            "amazon",
            "nuro"
            ],
        "often_qualifier": [
            "most of the time",
            "often",
            "usually",
            "most times",
            "frequently",
            "all the time",
            "all of the time",
            "every day",
            "everyday",
            "most days",
            "every other day",
            "every few days"
        ],
        "sometimes_qualifier": [
            "some of the time",
            "sometimes",
            "every so often",
            "every once in a while",
            "i guess",
            "occasionally",
            "a little"
        ]
    }
}
kb = KnowledgeBase()
kb.load_json(ont)

macros = {"ELABCON": elabCon(),
          "ELABPRO": elabPro(),
          "EXPLFIELD": EXPLfield(),
          "YEAR": YEAR(),
          "COMPANY": company(),
          "CHOOSECOMP": chooseComp(),
          "COMPCHAR": COMPCHAR()}
df = DialogueFlow(State.S1, initial_speaker=DialogueFlow.Speaker.SYSTEM, kb=kb, macros=macros)

pro = "[" \
      "#NOT(not,isnt,[doesnt, seem])," \
      "{" \
      "$more_safety=[#NOT(less), {secure,security,safe,safety}], " \
      "$less_crash={" \
                    "[{#LEM(few),#LEM(reduce),#LEM(decrease),#LEM(low),#LEM(less),down,small}, {#LEM(accident),#LEM(crash),#LEM(death),#LEM(injury),#LEM(fatality)}]" \
                    "[{#LEM(accident),#LEM(crash),#LEM(death),#LEM(injury),#LEM(fatality)}, {#LEM(few),#LEM(reduce),#LEM(decrease),#LEM(low),#LEM(less),down,small}]" \
                    "}," \
      "$less_traffic={" \
                    "[{#LEM(few),#LEM(reduce),#LEM(decrease),#LEM(low),#LEM(less),down,small}, {#LEM(car),#LEM(vehicle),#LEM(automobile),#LEM(traffic),congestion,driving,drivers}, #NOT(#LEM(crash),#LEM(accident))]," \
                    "[{#LEM(car),#LEM(vehicle),#LEM(automobile),#LEM(traffic),congestion,driving,drivers}, {#LEM(few),#LEM(reduce),#LEM(decrease),#LEM(low),#LEM(less),down,small}, #NOT(#LEM(crash),#LEM(accident))]" \
                    "}," \
      "$good_disable={#LEM(disable),disability}, " \
      "$good_environment={#LEM(environment),environmental,environmentally}," \
      "$free_attention=[free,#LEM(attention)]" \
      "}" \
      "]"

con = "[" \
      "{" \
      "$more_traffic={" \
                    "[{more,#LEM(increase),#LEM(large),#LEM(big),up,a lot,many,lots,#LEM(high)}, {#LEM(car),#LEM(vehicle),#LEM(automobile),#LEM(traffic),congestion,driving,drivers}]," \
                    "[{#LEM(car),#LEM(vehicle),#LEM(automobile),#LEM(traffic),congestion,driving,drivers}, {more,#LEM(increase),#LEM(large),#LEM(big),up,a lot,many,lots,#LEM(high)}]" \
                    "}," \
      "$more_crash={" \
                    "[{more,#LEM(increase),#LEM(large),#LEM(big),up,a lot,many,lots,#LEM(high)}, {#LEM(accident),#LEM(crash),#LEM(death),#LEM(injury),#LEM(fatality)}]," \
                    "[{#LEM(accident),#LEM(crash),#LEM(death),#LEM(injury),#LEM(fatality)}, {more,#LEM(increase),#LEM(large),#LEM(big),up,a lot,many,lots,#LEM(high)}]" \
                    "}," \
      "$hackers=#LEM(hack)," \
      "$morals={morals,moral,morality,immoral,immorality,ethic,ethics}, " \
      "$expensive=[#NOT(down,#LEM(decrease),#LEM(low),#LEM(reduce),#LEM(less)), {expensive,price,costly,cost,#LEM(bill),#LEM(expense)}]" \
      "$less_jobs={" \
                    "[{#LEM(few),#LEM(reduce),#LEM(decrease),#LEM(low),#LEM(less),down,small,away,#LEM(replace)}, #LEM(job)], " \
                    "[#LEM(job), {#LEM(few),#LEM(reduce),#LEM(decrease),#LEM(low),#LEM(less),down,small,away,#LEM(replace)}], " \
                    "#LEM(unemployed)" \
                    "}," \
      "$enjoy_drive=[{like,#LEM(enjoy),prefer,love,pleasure,fun}, #LEM(drive)], " \
      "$laws={#LEM(regulate),#LEM(law),#LEM(act)}," \
      "$less_safety={insecure,insecurity,danger,dangerous,scary,#LEM(frighten),#LEM(scare),uncomfortable,[{dont,not,less},{safe,secure,trust,trustworthy}]}" \
      "}" \
      "]"

disagree = '{' + ', '.join([
    '[{no, nay, nah, nope}]',
    '[{absolutely, surely, definitely, certainly, i think} {not}]',
    '[!i, {dont, "don\'t", do not}, think, so]',
    '[i, {dont, "don\'t", do not}]'
]) + '}'

df.add_system_transition(State.CORONAENTRY, State.U1, '"Did you drive often?"')
df.update_state_settings(State.CORONAENTRY, system_multi_hop=True)

df.add_system_transition(State.S1, State.U1, '"I cannot drive, for obvious reasons, but it fascinates me. Do you drive often?"')

df.add_user_transition(State.U1, State.S2a,
                       '[#NOT(not), {#ONT(often_qualifier,sometimes_qualifier), %s}]'%natex_common.agree)
df.add_user_transition(State.U1, State.S2b,
                       '[{%s, [not,{really,all,much,#ONT(often_qualifier),#ONT(sometimes_qualifier)}]}]'%disagree)

df.add_system_transition(State.S2a, State.U2a, '"Cool! What car do you drive?"')
df.add_system_transition(State.S2b, State.U2b, '"No? Well, do you plan to drive more at some point in the future?"')

df.add_user_transition(State.U2a, State.S3b, '[tesla]')
df.set_error_successor(State.U2a, State.S3a)
df.add_user_transition(State.U2b, State.S3c, '[%s]'%natex_common.agree)
df.add_user_transition(State.U2b, State.S3d, '[{%s, maybe, [not,{really,all,much}]}]'%disagree)


df.add_system_transition(State.S3a, State.U3a, '"Nice! So many people drive all the time nowadays. Even after working long hours at work, or going out late with friends.'
                                               'Have you ever felt very tired when you drive?"')
df.add_system_transition(State.S3b, State.U3b, '"Wow, a Tesla? That is so awesome. What model do you have?"')
df.add_system_transition(State.S3c, State.U3a,
                         '"That\'s great! With so much driving nowadays, it may seem like the most intuitive thing '
                         'in the world. But you have to be careful. Sometimes you may feel so tired when you need to '
                         'drive, which is really dangerous. Wouldn\'t it be nice if '
                         'our cars could drive themselves?"')
df.add_system_transition(State.S3d, State.U3a,
                         '"Well, that\'s totally reasonable actually. Maybe you don\'t need to in the future! '
                         'Wouldn\'t it be nice if cars could drive themselves?"')

df.add_user_transition(State.U3a, State.S4a,
                       '[#NOT(not), {#ONT(often_qualifier,sometimes_qualifier), %s}]'%natex_common.agree)
df.add_user_transition(State.U3a, State.S4b,
                       '[{%s, [not,{really,all,much,#ONT(often_qualifier),#ONT(sometimes_qualifier)}]}]'%disagree)
df.add_user_transition(State.U3a, State.S4c, con, score=2)
df.add_user_transition(State.U3b, State.S4d, '[{models, model s, model s three, model three, model x}]')
df.add_user_transition(State.U3b, State.S4e, '[{model y, model why}]')

df.add_system_transition(State.S4a, State.U4a, '"Yeah, it would be great! People are already working on it too, calling'
                                               ' it autonomous vehicles. '
                                               'Do you think it is a good idea to have them become a part of our '
                                               'transportation system?"')
df.add_system_transition(State.S4b, State.U4b, '"You don\'t like the idea of autonomous cars? Why not?"')
df.add_system_transition(State.S4c, State.U4c, '[!#ELABCON However, do you think that there are any '
                                               'potential advantages of autonomous cars"?"]')
df.add_system_transition(State.S4d, State.U4a, '"Cool! This model is capable of autonomous driving, where the cars '
                                               'drive themselves. '
                                               'Do you think it is a good idea to have autonomous cars as a part of our '
                                               'transportation system?"')
df.add_system_transition(State.S4e, State.U4a, '"I do not know much about this model but I know that some Tesla vehicles'
                                               ' are capable of autonomous driving, where the cars can drive themselves. '
                                               'Do you think it is a good idea to have cars that can drive themselves in'
                                               ' our transportation system?"')

df.add_user_transition(State.U4a, State.S5a, pro, score=2)
df.add_user_transition(State.U4a, State.S5b, con, score=2)
df.add_user_transition(State.U4a, State.S5d, 
                       '[#NOT(not), {#ONT(often_qualifier,sometimes_qualifier), %s}]'%natex_common.agree)
df.add_user_transition(State.U4a, State.S4b,
                       '[{%s, [not,{really,all,much,#ONT(often_qualifier),#ONT(sometimes_qualifier)}]}]'%disagree)

df.add_user_transition(State.U4b, State.S5b, con)

df.add_user_transition(State.U4c, State.S5c, pro)

df.add_system_transition(State.S5d, State.U5a, '"Yeah, I think it is a good idea too. '
                                               'Even so, do you think there are any potential risks of '
                                               'autonomous cars?"')

df.add_system_transition(State.S5a, State.U5a, '[!#ELABPRO() However, do you think there are any potential risks of '
                                               'autonomous cars"?"]')
df.add_system_transition(State.S5b, State.U5b, '[!#ELABCON() Can you think of any potential advantages of'
                                               ' autonomous cars"?"]')
df.add_system_transition(State.S5c, State.U6a, '[!#ELABPRO() Since autonomy provides a lot of potential benefits"," '
                                               'can you think of any other activities that could be improved by '
                                               'autonomous machines"?"]')

df.add_user_transition(State.U5a, State.S6a, con, score=2)
df.add_user_transition(State.U5a, State.S6c, 
                       '[#NOT(not), {#ONT(often_qualifier,sometimes_qualifier), %s}]'%natex_common.agree)
df.add_user_transition(State.U5a, State.S6f, 
                       '[{%s, [not,{really,all,much,#ONT(often_qualifier),#ONT(sometimes_qualifier)}]}]'%disagree)
df.add_system_transition(State.S6c, State.U5a, '"You do think there are risks? I would love to hear more about '
                                               'your thoughts on them."')
df.add_system_transition(State.S6f, State.U6a, '"You cannot think of any risks? Yeah, it does seem to be a pretty good '
                                               'idea overall. I have heard, though, that one downside '
                                               'is that autonomous cars will replace a large amount of '
                                               'jobs, such as truck drivers. Even so, there are a lot of potential '
                                               'benefits, like improving safety and reducing costs. '
                                               'Can you think of any other activities that could be improved by '
                                               'autonomous machines for similar reasons?"')

df.add_user_transition(State.U5b, State.S6b, pro, score=2)
df.add_user_transition(State.U5b, State.S6d, 
                       '[#NOT(not), {#ONT(often_qualifier,sometimes_qualifier), %s}]'%natex_common.agree)
df.add_user_transition(State.U5b, State.S6e, 
                       '[{%s, [not,{really,all,much,#ONT(often_qualifier),#ONT(sometimes_qualifier)}]}]'%disagree)
df.add_system_transition(State.S6d, State.U5b, 
                         '"Yeah, there are probably many advantages. What comes to mind for you?"')
df.add_system_transition(State.S6e, State.U6a, '"Yeah, the thought might be kind of scary when you first think of it.'
                                               'But I do think one advantage is that autonomous cars are '
                                               'actually safer. 90% of car '
                                               'accidents are due to human errors, such as speeding and drunk driving. '
                                               'Since autonomy provides a lot of potential benefits, '
                                               'can you think of any other activities that could be improved by '
                                               'autonomous machines?"')

# elaborate and ask field
df.add_system_transition(State.S6a, State.U6a, '[!#ELABCON() Even though there might be some issues at first '
                                               'using this technology"," can you think of any other activities that '
                                               'could be improved by autonomous machines"?"]')
df.add_system_transition(State.S6b, State.U6a, '[!#ELABPRO() Since autonomy provides a lot of potential benefits"," '
                                               'can you think of any other activities that could be improved by '
                                               'autonomous machines"?"]')


df.add_user_transition(State.U6a, State.S7a, "[$field=#ONT(other_fields)]")
df.set_error_successor(State.U6a, State.S7b)
df.add_user_transition(State.U6a, State.S7c, 
                        '[{%s, [not,{really,all,much,#ONT(often_qualifier),#ONT(sometimes_qualifier)}]}]'%disagree, 
                       score=2)

# if answer in our list of field, give explanation to the field and go to question
df.add_system_transition(State.S7a, State.U7a, '[!$field is a great way to apply the Autonomous techniques"!" '
                                               'It can #EXPLFIELD()"." Anyway"," do you think autonomous cars will be widely '
                                               'used around the world"?"]')
df.add_system_transition(State.S7b, State.U7a, '"That is a good idea! Anyway"," Do you think autonomous cars will be widely '
                                               'used around the world?"')
df.add_system_transition(State.S7c, State.U7a,
                         '"You cannot think of any? That\'s ok. I have only just recently heard that '
                         'one application is autonomous mining vehicles, which could reduce human injuries caused by '
                         'mining accidents. Anyway"," Do you think autonomous cars will be widely used around the world?"')

df.add_user_transition(State.U7a, State.S8a, 
                       '[#NOT(not), {#ONT(often_qualifier,sometimes_qualifier), %s}]'%natex_common.agree)
df.add_user_transition(State.U7a, State.S8b, 
                       '[{%s, [not,{really,all,much,#ONT(often_qualifier),#ONT(sometimes_qualifier)}]}]'%disagree)

df.add_system_transition(State.S8a, State.U8a, '"I think so too! When do you think it will happen?"')
df.add_system_transition(State.S8b, State.U9a, '"You don\'t? Yeah, many other people hold the same opinion as you do. '
                                               'Even so, companies are hard at work bringing it to production. '
                                               'Can you think of any companies that are currently '
                                               'developing autonomous vehicles?"')

df.add_user_transition(State.U8a, State.S9a, '[{$year=/\d{4}/,[!/[in]?/, $duration=/\d{1,3}/, /year[s]?/]}]')
df.add_system_transition(State.S9a, State.U9a, '[!That is #YEAR"." I think it will take a few decades, maybe by "2050," since companies are '
                                               'hard at work bringing it to production, but it has not been widely deployed yet. '
                                               'What companies do you think are currently working on '
                                               'autonomous vehicles "?"]')


complist = "[$comp=#ONT(car_company)]"
df.add_user_transition(State.U9a, State.S10a, complist, score=3)
df.add_user_transition(State.U9a, State.S10b, '[$compnotinlist=#NER(ORG)]',score=2)
df.add_user_transition(State.U9a, State.S10c,
                       '[{%s, [not,{really,all,much,#ONT(often_qualifier),#ONT(sometimes_qualifier)}]}]'%disagree)

df.add_system_transition(State.S10a, State.U10a, '[!Definitely"!" #CHOOSECOMP are also working on Autonomous Vehicles"."'
                                                 ' Which company do you think will contribute '
                                                 'most to making this technology affordable and popular"?"]')
df.add_system_transition(State.S10b, State.U10a, '[!Oh, I did not know $compnotinlist is also working on Autonomous '
                                                 'Vehicles"." But I do know #COMPANY() are doing this"." '
                                                 'Which company do you think will contribute '
                                                 'most to making this technology affordable and popular"?"]')
df.add_system_transition(State.S10c, State.U10a, '[!You cannot think of any"?" That is okay"." '
                                                 'I know that #COMPANY() are doing this"." '
                                                 'Which company do you think will contribute '
                                                 'most to making this technology affordable and popular"?"]')

df.add_user_transition(State.U10a, State.S11a, '[$chosen={waymo, google, alphabet}]')
df.add_user_transition(State.U10a, State.S11b, '[$notchosen={gmcruise,gm cruise,gm,cruise,generalmotors,general motor,general motors,argoai,argo ai,zoox,tesla,ford,aptiv,intel,mobileye,volkswagen,bosch,toyota,nissan,nvidia,amazon,nuro}]', score = 2)
df.add_user_transition(State.U10a, State.S11c, '[$userchosen=#NER(ORG)]')

df.add_system_transition(State.S11a, State.U11a,
                         '[!I also think $chosen is the pioneer in Autonomous Vehicles. It has an advanced '
                         'development process that lets its autonomous cars learn from the worlds longest and '
                         'toughest driving test"," including millions of miles on public roads and billions of miles '
                         'in simulation.]')
df.add_system_transition(State.S11b, State.U11b,
                         '[!I know $notchosen #COMPCHAR"." However I think Waymo"," which is owned by Google"," is '
                         'the most successful firm in this field. It has an advanced development process that'
                         ' lets its autonomous cars learn from the worlds longest and toughest driving test"," '
                         'including millions of miles on public roads and billions of miles in simulation.]')
df.add_system_transition(State.S11c, State.U11c,
                         '[!I am not very familiar with $userchosen"," could you tell me more about it"?"]')

df.add_user_transition(State.U11a, State.END, "/.*/")
df.add_user_transition(State.U11b, State.END, "/.*/")
df.add_user_transition(State.U11c, State.END, "/.*/")

df.set_error_successor(State.U1, error_successor=State.ERR1)
df.add_system_transition(State.ERR1, State.U3a, '"I see. But would you like to have cars to drive '
                                                'themselves and take you to the destination?"')
df.set_error_successor(State.U2a, error_successor=State.ERR2)
df.add_system_transition(State.ERR2, State.U3a, '"Okay, good to know. With so much driving nowadays, it may seem like '
                                                'the most intuitive thing in the world. '
                                                'But you have to be careful. Sometimes you may feel so tired when you '
                                                'need to drive, which is really dangerous. Wouldn\'t it be nice if '
                                                'our cars could drive themselves?"')
df.set_error_successor(State.U2b, error_successor=State.ERR3)
df.add_system_transition(State.ERR3, State.U3a, '"Well, that is interesting. With so much driving nowadays, it may seem '
                                                'like the most intuitive thing in the world. '
                                                'But you have to be careful. Sometimes you may feel so tired when you '
                                                'need to drive, which is really dangerous. Wouldn\'t it be nice if '
                                                'our cars could drive themselves?"')
df.set_error_successor(State.U3a, error_successor=State.S4a)
df.set_error_successor(State.U3b, error_successor=State.S4e)
df.set_error_successor(State.U4a, error_successor=State.ERR4)
df.add_system_transition(State.ERR4, State.U6a, '"I think it is a good way to significantly reduce the amount of car '
                                                'accidents as it is much safer than humans driving cars. Are there any'
                                                ' other fields that you think we can apply automation to?"')
df.set_error_successor(State.U4b, error_successor=State.ERR5)
df.add_system_transition(State.ERR5, State.U5b, '"Maybe. However, do you think there are any potential advantages '
                                                'of autonomous cars?"')
df.set_error_successor(State.U4c, error_successor=State.ERR6)
df.add_system_transition(State.ERR6, State.U6a, '"I think so too. Even though there might be some issues at first'
                                                ' using this technology, are there any other field that you think we can '
                                                'apply automation to?"')
df.set_error_successor(State.U5a, error_successor=State.ERR7)
df.add_system_transition(State.ERR7, State.U6a, '"For sure! One downside is that autonomous cars will replace a '
                                                'large amount of jobs, such as truck drivers. Even so, it has '
                                                'many potential benefits. Are there any other fields you think we would '
                                                'benefit by applying automation to?"')
df.set_error_successor(State.U5b, error_successor=State.ERR8)
df.add_system_transition(State.ERR8, State.U6a, '"For sure! One advantage is that autonomous cars are actually safer. '
                                                '90% of car accidents are due to human errors, such as speeding and '
                                                'drunk driving. Are there any other fields you think we would '
                                                'benefit by applying automation to?"')
df.set_error_successor(State.U7a, error_successor=State.ERR9)
df.add_system_transition(State.ERR9, State.U9a, '"I think it will eventually happen but might still take a while. '
                                                'By the way, do you know what companies are now developing this '
                                                'technology?"')
df.set_error_successor(State.U8a, error_successor=State.ERR10)
df.add_system_transition(State.ERR10, State.U9a, '"Okay, sure. But I think it will happen by "2050." '
                                                 'By the way, do you know what companies are now developing '
                                                 'this technology?"')
df.set_error_successor(State.U10a, error_successor=State.ERR11)
df.add_system_transition(State.ERR11, State.U11c, '[!I am not very familiar with that one"," '
                                                  'could you tell me more about it"?"]')
df.set_error_successor(State.U9a, error_successor=State.ERR12)
df.add_system_transition(State.ERR12, State.U10a, '[!That is okay"." I know that #COMPANY() are doing this"." Which '
                                                  'company do you think will contribute the most to making '
                                                  'autonomous vehicles affordable and popular"?"]')


df.add_system_transition(State.END, State.END2, '"Well, I for one am excited to see how autonomous vehicles turn out!"')
df.update_state_settings(State.END2, system_multi_hop=True)

if __name__ == '__main__':
    df.precache_transitions()
    df.run(debugging=True)