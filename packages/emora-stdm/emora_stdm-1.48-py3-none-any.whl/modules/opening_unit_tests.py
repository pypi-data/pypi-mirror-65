###################################
# Import your DialogueFlow object
###################################
from opening import component

###################################
# Add an ending loop if
# you do not already have one
###################################
component.add_state('unit_test_end', 'unit_test_end')
component.add_system_transition('transition_out','unit_test_end','" END"')
component.add_system_transition('unit_test_end','unit_test_end','" END"')

if __name__ == '__main__':

    debug = False

    #######################################################################################################
    # If you use variables from Cobot in your logic, modify cobot_vars with your desired test cases.
    #######################################################################################################
    cobot_vars = {'request_type': 'LaunchRequest',
                 'global_user_table_name': 'GlobalUserTableBeta'}
    component._vars.update({key: val for key, val in cobot_vars.items() if val is not None})

    #######################################################################################################
    # DO NOT REMOVE - this will precompile your Natex expressions, identifying any cases where your Natex
    # is not compilable and will cause the state to throw an error.
    #######################################################################################################
    component.precache_transitions()

    #######################################################################################################
    # Add the sequence of utterances you want to test as your conversation with your component
    #######################################################################################################
    sequence = ["hi", "sarah", "i dont know"]

    #######################################################################################################
    # Uses your utterances to conduct a conversation with your component.
    #######################################################################################################
    turn = 0
    for utter in sequence:

        component.user_turn(utter, debugging=debug)
        print("U: %s (%s)"%(utter,component.state()))

        response = component.system_turn(debugging=debug)
        print("E: %s (%s)"%(response,component.state()))

        turn += 1
