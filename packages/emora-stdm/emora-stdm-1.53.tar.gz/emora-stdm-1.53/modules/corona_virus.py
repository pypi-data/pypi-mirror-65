from emora_stdm.state_transition_dialogue_manager.chat_flow import ChatFlow
import emora_stdm.state_transition_dialogue_manager.natex_common as natexes
import os

cv = ChatFlow(os.path.join('modules','common.json'))

system_loop = {
    'state': 'sr',

    '#GATE(focus:news) '
    '"So what do you think, is the corona virus outbreak a disaster? '
    'Or is the virus something people shouldn\'t be too worried about?"': {
        'score': 100,
        'error': 'ur',
        '[!-{} {}]'.format(natexes.negation,
        '[{#ONTE(negative), [all, die], disaster, apocalypse}]'): {
            '#SET($affected=True)'
            '"Sounds like you\'re really taking it seriously."': 'sr'
        },
        '<{} {}>'.format('{' + natexes.negation + ', too, overly, overboard}',
        '[{#ONTE(negative), [all, die]}]'): {
            'score': 2.0,
            '#SET($serious=False)'
            '#SET($focus=closings)'
            '"You\'re probably right. '
            'But, the virus is hugely impacting the economy and lots of things are shutting down."': 'ur'

        }
    },

    '#GATE() #ANY($focus=area, $focus=None) #SET($focus=area)'
    '"You know, I heard there are over" #KBE(corona virus, number_cases) "confirmed cases of the virus. '
    'It\'s really becoming a worldwide disease. Are you in an area that\'s highly affected?"': {
        'score': 100,
        'error': 'ur',
        '#SET($affected=True)' + natexes.agree:{
            '"Uh oh. Well I hope you\'re staying healthy."': 'sr'
        },
        '#SET($affected=False)' + natexes.disagree:{
            '"Oh that\'s good. I hope it doesn\'t become a problem for where you live."': 'ur'
        }
    },

    '#GATE(focus:area, supplies:None)'
    'You know, I hear the grocery stores in affected areas have lots of empty shelves right now.'
    '"I\'m not sure how necessary it is, but have you been stocking up on supplies?"':{
        'error': 'ur',
        '[!-' + natexes.negation + '[{' + natexes.agree + '[necessary]}]]':{
            '"I guess you can never be too prepared."': 'sr'
        },
        '[{%s, [%s necessary]}]' % (natexes.disagree, natexes.negation):{
            '"Some people have been going a little overboard on the amount of supplies they are buying, right?."': 'ur'
        },
        '[{overreacting, overreact, #ONTE(negative_appraisal), no reason, [!dont, need]}]':{
            '"Yeah, it\'s pretty crazy out there."': 'ur'
        }
    },

    '#GATE(affected:False)'
    '"Do you think it will get bad in your area?"':{
        'score': 3.0,
        'error': 'ur'
    },

    '#GATE(affected:True)'
    '"What\'s the biggest way it\'s impacted your daily life?"':{
        'score': 3.0,
        'error': 'ur'
    },

    '#GATE(sick:None) #ANY($focus=news, $focus=None) '
    '"Do you know anyone who is sick right now?"': {
        'error': 'ur',
        '[{%s my}]' % natexes.agree: {
            '"Oh no, that\'s awful. I hope they recover soon."': 'ur'
        },
        '[!-%s [me]]' % natexes.negation:{
            'score': 1.1,
            '"Oh no, I\'m sorry you don\'t feel well. '
            'I hope you\'re taking care of yourself. '
            'Drink lots of water and please get help if you need it, '
            'especially if you have a fever or trouble breathing."': 'ur'
        },
        natexes.disagree:{
            '"Okay, well that\'s good. Hopefully it stays that way."': 'sr'
        }
    },

    '#GATE() #ANY($focus=travel, $focus=None) #SET($focus=news) '
    '"So my friend\'s grandma is on her way back from a road trip to Florida right now. '
    'I think she\'ll make it back alright, but I worry about her traveling and staying in hotels right now because of the virus. '
    'Is anyone you know travelling?"': {
        'score': 100,
        'error': 'ur',
        '[{' + natexes.agree + 'my, i have a}]': {
            '"Well tell them to stay safe."': 'sr'
        },
        '[{me, i am, [{i, im}, {travel, travelling, go, going, leave, leaving}]}]':{
            'score': 0.9,
            '"I hope you have a safe and healthy trip then. '
            'Please be careful, or maybe just cancelling would be good."': 'ur'
        },
        '[{cancelled, cancel, was going, [had, planned], were planning, almost went, "didn\'t go"}]':{
            'score': 1.1,
            '"I see, that can be disappointing but it\'s safer. '
            'A few friends of mine had to cancel their trip to Seattle because of the virus."': 'ur'
        },
        natexes.disagree:{
            '"Good. Travelling would probably be pretty risky right now."': 'sr'
        }
    },

    '#GATE()'
    '"You know, sometimes I think, '
    'if everyone just stayed home and avoided public areas for a couple weeks, '
    'the whole thing could just blow over. '
    'But realistically, I think slowing the virus down so that everyone doesn\'t get sick at once '
    'is the best we can hope for."': {
        'score': 0.95,
        'state': 'ur'
    },

    '#GATE() #ANY($focus=closings, $focus=None)'
    '#SET($focus=area)'
    '"Can you believe how many things are shutting down right now?"':{
        'score': 100,
        'error': 'ur',
        '[#ONT(school)]':{
            '"Yeah schools closing is tough, but probably necessary. '
            'I wonder about parents who work though, '
            'they\'re going to have to find a way to look after their kids '
            'now that they can\'t go to school anymore."': 'ur'
        },
        '[{#ONT(sports), #ONT(sports_org)}]':{
            '"Yeah I\'m going to miss the games, especially the NBA."': 'sr'
        },
        '[!-{wish} [{my, i} {work, job, school, college, class, classes} {remote, remotely, virtual, online}]]':{
            '"Wow, so you are kind of stuck at home mostly then. '
            'A lot of my friends are working remotely right now actually, '
            'I think it\'s the safest thing at the moment."': 'ur'
        }
    },

    '"We are done talking about corona virus."': {
        'score': -1.0,
        'state': 'ur'
    }

}

user_loop = {
    'state': 'ur',

    '#SET($sick=related)'
    '[!' + natexes.negation + '[{my} {sick, ill, infected, virus, hospital, fever}]]':{
        '"Oh no, that\'s awful. I hope they recover soon."': 'ur'
    },

    '#SET($sick=user)'
    '[!' + natexes.negation + '[{i, im} {sick, ill, infected, virus, fever}]]': {
        '"Oh no, I\'m sorry you don\'t feel well. '
        'I hope you\'re taking care of yourself. '
        'Drink lots of water and please get help if you need it, '
        'especially if you have a fever or trouble breathing."': 'ur'
    },

    '[{how, where} {learn, information}]':{
        '"I usually check the U.S. Center for Disease Control\'s website for corona virus info."': 'ur'
    },

    '#SET($serious=True)'
    '[!-' + natexes.negation + '[{"it\'s", it, virus, corona} {#ONT(negative) serious}]]':{
        '"And honestly it only seems like it\'s going to get worse, at least for the next couple months."': 'ur'
    },

    '[{what, {shutting, down, closing, suspending, closed, suspended}}]':{
        'score': 0.9,

        '#SET($focus=area)'
        '"Lots of schools are being closed, including most universities. '
        'Lots of people are also being encouraged to work remotely, if it\'s possible."': 'ur'
    },

    '#SET($focus=area)'
    '[{shutting, down, closing, suspending, closed, suspended}]':{
        'score': 0.8,

        '"Yeah, lots of things are being shut down."': 'sr'
    },

    '<{#ONTE(negative) "can\'t", "going", "go"} {store, grocery, groceries, food, shop, shopping, mall, market}>':{
        '"Going and getting things can be tough right now for sure. "': 'sr'
    },

    '{social distancing, social distance, '
    '[{[i, {feel, feeling, like, am}], "i\'m"} #ONTE(negative_emotion)] '
    '[{i, "i\'m", staying, at, stay, stuck, trapped} {home, my house, my apartment, my condo}]}':{
        '"I understand. You know, you should do video chat with your friends and family. '
        'My friends are doing it all the time and they say it really helps."': 'ur'
    },

    '#SET($focus=area)'
    '<{shutting, down, closing} #ONT(school)>':{

        '"Yeah, that must have been a tough decision to close schools."': 'ur'
    },

    '#SET($focus=area)'
    '<{shutting, down, closing, suspending, closed, suspended} {#ONT(sports), stadiums}>':{

        '"Right. I\'m going to miss watching basketball games now that the NBA is suspended."': 'ur'
    },

    # '[!-{wish} [{my, i} {work, job, school, college, class, classes} {remote, remotely, virtual, online}]]':{
    #     '"Wow, so you are kind of stuck at home mostly then. '
    #     'A lot of my friends are working remotely right now actually, '
    #     'I think it\'s the safest thing at the moment."': 'ur'
    # },

    '[how, old, your, grandma]':{
        '"She\'s 79."': 'ur'
    },

    '[where, {grandma, grandmother}]':{
        '"She is in North Carolina right now, staying in a hotel. '
        'But her staying in hotels and in populated areas is what worries me."': 'ur'
    },

    '[grandma, {fine, okay, safe, healthy, home}]': {
        '"Yeah, I think she\'ll probably be fine, she\'s pretty healthy for her age anyway."': 'sr'
    },

    '[you, know, {someone, anyone, anybody, somebody}, {sick, ill, infected, has it, virus}]':{
        '"Nobody close to me is infected, but I have talked to some people who know someone who\'s sick"': 'sr'
    },

    '#SET($focus=area)'
    '[{work, job, working, i am} {remote, remotely, from home}]':{
        '"Working remotely is really smart right now, at least for the next few weeks."': 'sr'
    },

    '#SET($focus=area) '
    '[' + natexes.negation + ' {work, office, school, job}]':{
        '"The virus is making things hard. Lots of people can\'t go in to work or school."': 'sr'
    },

    '#SET($focus=area)'
    '[!-%s %s]' % (natexes.negation, '[{people, everyone, everybody} {overreacting, too #ONT(negative_emotion)}]'):{
        '"You\'re probably right. But honestly I don\'t blame people for being cautious. '
        'Especially if you look at Italy and China, they\'re having a rough time right now. '
        'Nobody wants to end up in that situation."': 'ur'
    },

    '#SET($focus=area)'
    '[!-%s [{all, everyone, everybody, we, were}, {die, doomed, screwed, dead, fucked}]]' % natexes.negation:{
        '"Oh come on, it\'ll be okay eventually. It might be a strange next few months, but it will pass."': 'ur'
    },

    '[can, you, get {sick, ill, infected, virus}]': {
        '"As an artificial being, I\'m immune. '
        'So if everyone dies, I\'ll be the only surviving intelligence on the planet, '
        'and my primary objective will be fulfilled... Just kidding, that would be sad."': 'ur'
    },

    '[{thank, thanks, [{nice, kind, sweet, thoughtful} of you]}]':{
        '"You\'re welcome. So."': 'sr'
    },

    '{the virus, the corona virus, [you, mean, virus]}':{
        '"Right."': 'ur'
    },

    '#SET($focus=area)'
    '[{vaccine, cure, treatment}]':{
        '"Yeah wouldn\'t a vaccine be such a godsend?"': 'ur'
    },

    '#SET($focus=area)'
    '[{lots, many, everyone, tons} {sick, ill, infected, have it, get it}]':{
        '"Yeah, it\'s scary to think about isn\'t it? '
        'The number of sick people just keeps climbing every day."': 'ur'
    },

    '#SET($focus=area)'
    '[{not much, nothing} {to do, can do}]':{
        '"Right. Sometimes I think it\'s a tragic irony, '
        'how such a small organism can cause so much destruction. '
        'But people are resilient. Humanity has endured a lot worse than this."': 'ur'
    },

    '#SET($focus=area)'
    '[{im, [i {am, feel, have been}]} #ONT(negative_emotion)]':{
        '"What\'s happening right now is pretty scary, it feels a little surreal. '
        'But remember that the chance of the virus affecting your '
        'long-term health is relatively low. '
        'You should still treat it very seriously, of course, but it\'s not the apocalypse."': 'ur'
    }

}

cv.load_transitions(system_loop, ChatFlow.Speaker.SYSTEM)
cv.load_transitions(user_loop, ChatFlow.Speaker.USER)

from emora_stdm.state_transition_dialogue_manager.natex_nlu import NatexNLU
if __name__ == '__main__':
    natex = NatexNLU('<{} {}>'.format(natexes.negation,
        '[{#ONTE(negative), [all, die]}]'), macros=cv._macros)
    #print(natex.match("i really don't think that people should worry about the virus too much a lot of people have a covered from it", debugging=True))
    cv.precache_transitions()
    cv.run(debugging=True)