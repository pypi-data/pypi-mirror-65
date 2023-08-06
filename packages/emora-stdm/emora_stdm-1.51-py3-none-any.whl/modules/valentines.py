from emora_stdm import DialogueFlow, KnowledgeBase, Macro
component = DialogueFlow('prestart', initial_speaker=DialogueFlow.Speaker.USER)

component.add_system_transition('opening_chat_choices', 'valentines response',
                                '"I hope you had a good Valentine\'s Day on Friday! Did you do anything special for it?"', score=100.0)
component.add_user_transition('valentines response', 'valentines no person',
                              "[#ONT(ont_negation), {[have, {#ONT(partner)}],[married],[dating],[relationship],[[!{seeing,with,have} {anyone,anybody,someone,somebody}]]}]")
component.add_user_transition('valentines response', 'valentines person',
                              "[!#ONT_NEG(ont_negation), -{wish, want} [$valentine={#ONT(partner)}]]", score=2.0)
component.add_user_transition('valentines response', 'valentines broke up',
                              '[{divorce, divorced, broke up, split up, left me}]', score=2.0)
component.set_error_successor('valentines response', 'valentines appreciation')
component.add_user_transition('valentines response', 'valentines yes',
                              '{[!#ONT_NEG(ont_negation), [{yes, yeah, yep, yup, yea, sure}]],[!#ONT_NEG(ont_negation), [{i do,i did, we do, we did}]]}',
                              score=0.9)
component.add_user_transition('valentines response', 'valentines no',
                              '{[{no,nah,not really,not at all,not much,nothing,nope}],[{i dont, i do not, no i dont, no i do not, we dont, we do not, i didnt, i did not, no i didnt, no i did not, we didnt, we did not}]}',
                              score=0.9)
component.add_system_transition('valentines yes', 'valentines response', '"Thats exciting! What did you do?"')
component.add_user_transition('valentines response', 'valentines plans with a',
                              '[$activity={dinner, date, movie, dancing, trip}]')
component.add_user_transition('valentines response', 'valentines plans without a',
                              '[$activity={movies, bowling, theatre, dance}]')
component.add_user_transition('valentines response', 'valentines plans go out', '[{going out, go out, went out}]')
component.add_system_transition('valentines plans with a', 'valentines plans reaction',
                                '[!a, $activity, sounds like a lot of, "fun. Hope you had a good time."]')
component.add_system_transition('valentines plans without a', 'valentines plans reaction',
                                '[!$activity, sounds like a lot of, "fun. Hope you had a good time."]')
component.add_system_transition('valentines plans go out', 'valentines plans reaction',
                                '"going out sounds like a lot of fun. Hope you had a good time."')
component.set_error_successor('valentines plans reaction', 'valentines appreciation')
component.add_system_transition('valentines broke up', 'valentines broke up reaction',
                                '"Oh. I am really sorry to hear that. Being apart from someone who used to be in your life can be hard."')
component.add_system_transition('valentines person', 'valentines person reaction',
                                '[!Well I hope you and your $valentine have a good time"."]')
component.add_system_transition('valentines no person', 'valentines no person reaction',
                                '[!Even if you are not in a relationship"," you could have still done something fun for yourself"." I think it is good to treat yourself too"."]')
component.set_error_successor('valentines broke up reaction', 'valentines appreciation')
component.set_error_successor('valentines person reaction', 'valentines appreciation')
component.set_error_successor('valentines no person reaction', 'valentines appreciation')
component.add_system_transition('valentines no', 'transition_out',
                                '"Yeah, not everyone had special plans. I did not do anything either. So, "')
component.add_system_transition('valentines appreciation', 'transition_out',
                                '"Yeah, Valentine\'s Day is just one of many days to do something nice for yourself or others. So, "')