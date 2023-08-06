###################################
# Import your DialogueFlow object
###################################
from general_activity import df as component

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

    sequences = [
        ["i cleaned my room"],
        ["i shouldve done some cleaning but i didnt"],
        ["just some chores"],
        ["i went to the grocery store", "yeah"],
        ["i went to the grocery store", "i am"],
        ["i went to the grocery store", "i am not"],
        ["i went to the grocery store", "no"],
        ["i went to the grocery store", "i hate doing errands"],
        ["i went shopping", "its alright i kind of like going to the store"],
        ["i had to run to the bank", "it wasnt fun"],
        ["i did some homework", "yeah"],
        ["i worked on a project", "i should still be working on it"],
        ["i finished my homework", "sort of"],
        ["i had a test", "no"],
        ["homework", "yeah"],
        ["schoolwork", 'sure'],
        ["i had class"],
        ["i went to classes"],
        ["had to go to a lecture"],
        ["worked"],
        ["went to work"],
        ["had to work"],
        ["went to the store"],
        ["went to the park"],
        ["travelled to the gardens"],
        ["i am going to the museum later"],
        ["played some video games", "yeah"],
        ["played on the switch", "not really"],
        ["played pokemon", "maybe a little bit more"],
        ["i worked out","no its normal"],
        ["i lifted some weights", "yes"],
        ["went for a run", "i am trying"],
        ["had a dance class", "no"],
        ["went on a walk", "maybe"],
        ["went on a walk", "im not"],
        ["watched tv"],
        ["netflix and chill"],
        ["watching movies mostly"],
        ["i did nothing"],
        ["not much"],
        ["i dont know"],
        ["just trying to relax at home"],
        ["taking a break from the madness"],
        ["i dont want to tell you that"],
        ["that is none of your business"],
        ["im not interested in sharing my life with you"],
        ["stuck at home because of the virus"],
        ["quarantined"],
        ["trying to stock up on necessities"],
        ["took a shit"],
        ["farted"],
        ["i pooped earlier"],
        ["had sex with my girlfriend"],
        ["fucked hard"],
        ["sucked dick"],
        ["eat my pussy"],
        ["jerked myself off"],
        ["masturbated my girlfriend"],
        ["i gardened a bit today"],
        ["played house with my sister"],
        ["colored"],
        ["cooked mostly all day"]
    ]

    #######################################################################################################
    # Uses your utterances to conduct a conversation with your component.
    #######################################################################################################
    turn = 0
    for sequence in sequences:
        print()
        print("-"*20)
        component.reset()
        start = component.system_turn(debugging=debug)
        print("E: %s (%s)" % (start, component.state()))
        for utter in sequence:
            component.user_turn(utter, debugging=debug)
            print("U: %s (%s)"%(utter,component.state()))
            response = component.system_turn(debugging=debug)
            print("E: %s (%s)"%(response,component.state()))
            turn += 1
