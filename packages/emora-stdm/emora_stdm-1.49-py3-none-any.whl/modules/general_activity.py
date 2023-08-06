"""
### (SYSTEM) ASK ABOUT DAY ACTIVITIES
ask_plans_nlg = ['"What are your plans for today?"',
                 '"What are you looking forward to doing today?"',
                 '"What is happening in your life today?"']
ask_recap_nlg = ['"What did you do today?"',
                 '"What was something fun that you did today?"',
                 '"What did you get up to today?"']


### (USER) ANSWER ABOUT DAY ACTIVITIES
decline_share = "{" \
                "[#ONT(ont_negation), {talk, talking, discuss, discussing, share, sharing, tell, telling, say, saying}]," \
                "[#ONT(ont_fillers), #ONT(ont_negative)]," \
                "[#ONT(ont_negative)]," \
                "[none,your,business]," \
                "[!{[!that,is],thats},private]" \
                "}"
dont_know = '[{' \
            'dont know,do not know,unsure,[not,{sure,certain}],hard to say,no idea,uncertain,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[{dont,do not}, have, {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[!{cant,cannot,dont} {think,remember,recall}]' \
            '}]'
relax_plans_nlu = '[{relax,relaxing,chill,chilling,fun,enjoy,enjoying}]'
no_plans_nlu = '{' + decline_share + ', [{nothing,none,have not decided,havent decided, up in the air, undecided, not much}]}'
component.add_user_transition('rec_plans_for_day', 'ack_relax_plans', relax_plans_nlu)
component.add_user_transition('rec_plans_for_day', 'ack_no_plans', no_plans_nlu)
component.set_error_successor('rec_plans_for_day', 'ack_gen_plans')

component.add_user_transition('rec_plans_for_rest_day', 'ack_relax_plans', relax_plans_nlu)
component.add_user_transition('rec_plans_for_rest_day', 'ack_no_plans', no_plans_nlu)
component.set_error_successor('rec_plans_for_rest_day', 'ack_gen_plans')

component.add_user_transition('rec_recap_for_day', 'ack_relax_plans', relax_plans_nlu)
component.add_user_transition('rec_recap_for_day', 'ack_no_plans', no_plans_nlu)
component.set_error_successor('rec_recap_for_day', 'ack_gen_plans')

### (SYSTEM) ACK ABOUT DAY ACTIVITIES
ack_plans_relax_nlg = ['"Its always good to take some time to relax."',
                       '"I think having some time to breath is so important."',
                       '"You can never underappreciate the value of taking some time for yourself."']
ack_plans_no_nlg = ['"Yeah, sometimes it is hard to decide what to do."',
                    '"Sure, I know the feeling of not really doing too much."',
                    '"I see. I think some days are just meant to be more relaxed!"']
ack_plans_gen_nlg = ['"Interesting. Thanks for telling me about it."',
                     '"Cool, I am glad to hear more about what you do."',
                     '"Gotcha. That sounds interesting."']
component.add_system_transition('ack_relax_plans', 'transition_out', ack_plans_relax_nlg)
component.add_system_transition('ack_no_plans', 'transition_out', ack_plans_no_nlg)
component.add_system_transition('ack_gen_plans', 'transition_out', ack_plans_gen_nlg)
"""