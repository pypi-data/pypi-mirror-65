from emora_stdm import DialogueFlow

df = DialogueFlow('root')

transitions = {
    'state': 'root',

    '#SET($topic=school)'
    '"I\'m really glad I get a chance to talk with you. I\'m actually a student right now, but I think my school is pretty different than what most people are used to. '
    'Are you a student too?"':{
        '#SET($is_student=True)'
        '#AGREE':{
            'state': 'ask_like_school',
            '"Honestly, I think taking classes is pretty boring, even though I know they are important. I would much rather spend time talking to my friends and being outside. '
            'What about you? Do you like school?"':{
                '#SET($likes_school=True)'
                '#AGREE':{
                    '"I think that\'s great. I mean, who doesn\'t like learning new things? "': {
                        'error': 'root'
                    }
                },
                '#SET($likes_school=False)'
                '#DISAGREE':{
                    '"I kind of get that. But to be fair, learning new things can sometimes be a lot of fun."':{
                        'error': 'root'
                    }
                },
                '#UNX':{
                    'score': 0.9,
                    '"I understand that. "': 'root'
                }
            }
        },
        '#SET($is_student=False)'
        '#DISAGREE':{
            '"Oh, really? I cannot even imagine not waking up everyday and going to class. This one teacher of mine is hilarious. He never talks in class about the material, '
            'he just rants the entire time about the economy and social issues."':{
                '#UNX':{
                    '"So, what do you remember most about school?"':{
                        'error':{
                            '"Sounds about right. "': 'root'
                        },
                        '#IDK': {
                            '"Has it been a while then?"':{
                                'error': {
                                    '"I see. "': 'root'
                                }
                            }
                        }
                    }
                }
            }
        },
        '#UNX':{
            'score': 0.9,
            '"Gotcha. "': 'ask_like_school'
        }
    }
}


df.load_transitions(transitions, speaker=DialogueFlow.Speaker.SYSTEM)

df.update_state_settings('root', system_multi_hop=True)

if __name__ == '__main__':
    df.run(debugging=True)
