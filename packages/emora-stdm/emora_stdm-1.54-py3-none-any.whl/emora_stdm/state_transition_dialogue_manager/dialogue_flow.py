
from enum import Enum, auto
from emora_stdm.state_transition_dialogue_manager.memory import Memory
from emora_stdm.state_transition_dialogue_manager.natex_nlu import NatexNLU
from emora_stdm.state_transition_dialogue_manager.natex_nlg import NatexNLG
from emora_stdm.state_transition_dialogue_manager.database import GraphDatabase
from structpy.graph.labeled_digraph import MapMultidigraph
from typing import Union, Set, List, Dict, Callable, Tuple, NoReturn
from emora_stdm.state_transition_dialogue_manager.utilities import AlterationTrackingDict
from emora_stdm.state_transition_dialogue_manager.ngrams import Ngrams
from emora_stdm.state_transition_dialogue_manager.settings import Settings
from emora_stdm.state_transition_dialogue_manager.stochastic_options import StochasticOptions
from emora_stdm.state_transition_dialogue_manager.utilities import HashableDict
from emora_stdm.state_transition_dialogue_manager.macro import Macro
from emora_stdm.state_transition_dialogue_manager.knowledge_base import KnowledgeBase
from emora_stdm.state_transition_dialogue_manager.macros_common import *
from emora_stdm.state_transition_dialogue_manager.state import State
from emora_stdm.state_transition_dialogue_manager.update_rules import UpdateRules
from emora_stdm.state_transition_dialogue_manager.utilities import random_max
from time import time
import dill
from pathos.multiprocessing import ProcessingPool as Pool

def module_source_target(source, target):
    if isinstance(source, str) and ':' in source:
        source = tuple(source.split(':'))
    if isinstance(target, str) and ':' in target:
        target = tuple(target.split(':'))
    return source, target

def module_state(state):
    if isinstance(state, str) and ':' in state:
        state = tuple(state.split(':'))
    return state

def precache(transition_datas):
    for tran_datas in transition_datas:
        tran_datas['natex'].precache()
    parsed_trees = [x['natex']._compiler._parsed_tree for x in transition_datas]
    return parsed_trees

_autostate = '-1'

class EnumByName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class Speaker(EnumByName):
    SYSTEM = auto()
    USER = auto()

class DialogueFlow:

    Speaker = Speaker

    @classmethod
    def autostate(cls):
        global _autostate
        _autostate = str(int(_autostate) + 1)
        return _autostate

    def __init__(self, initial_state: Union[Enum, str, tuple], initial_speaker = Speaker.SYSTEM,
                 macros: Dict[str, Macro] =None, kb: Union[KnowledgeBase, str, List[str]] =None, default_system_state=None):
        self._graph = GraphDatabase()
        self._initial_state = State(initial_state)
        self._potential_transition = None
        self._initial_speaker = initial_speaker
        self._speaker = self._initial_speaker
        self._response = None
        self._vars = HashableDict()
        self.set_state(self._initial_state)
        self._gate_requirements = defaultdict(dict)
        self._gates = defaultdict(set)
        self._gate_buffer = {}
        self._prepends = {}
        self._var_dependencies = defaultdict(set)
        self._error_transitioned = False
        self._is_module = False
        self._default_state = default_system_state
        self.vars()['__stack__'] = []
        if kb is None:
            self._kb = KnowledgeBase()
        elif isinstance(kb, str):
            self._kb = KnowledgeBase()
            self._kb.load_json_file(kb)
        elif isinstance(kb, list):
            self._kb = KnowledgeBase()
            for filename in kb:
                self._kb.load_json_file(filename)
        else:
            self._kb = kb
        onte = ONTE(self._kb)
        kbe = KBE(self._kb)
        self._macros = {
            'WN': WN(),
            'ONT': onte, 'ONTE': onte,
            'KBQ': kbe, 'KBE': kbe,
            'ONTN': ONTN(self._kb),
            'EXP': EXP(self._kb),
            'ONT_NEG': ONT_NEG(self._kb),
            'NOT': NOT(),
            'U': UnionMacro(),
            'I': Intersection(),
            'DIF': Difference(),
            'SET': SetVars(),
            'ALL': CheckVarsConjunction(),
            'ANY': CheckVarsDisjunction(),
            'ISP': IsPlural(),
            'FPP': FirstPersonPronoun(self._kb),
            'TPP': ThirdPersonPronoun(self._kb),
            'PSP': PossessivePronoun(self._kb),
            'EQ': Equal(),
            'GATE': Gate(self),
            'CLR': Clear(),
            'NER': NamedEntity(),
            'POS': PartOfSpeech(),
            'LEM': Lemma(),
            'SCORE': Score(),
            'TOKLIMIT': TokLimit(),
            'AGREE': Agree(),
            'DISAGREE': Disagree(),
            'QUESTION': Question(),
            'NEGATION': Negation(),
            'IDK': DontKnow(),
            'MAYBE': Maybe(),
            'TRANSITION': Transition(),
            'UNX': Unexpected()
        }
        if macros:
            self._macros.update(macros)
        self._rules = UpdateRules(vars=self._vars, macros=self._macros)

    # TOP LEVEL: SYSTEM-LEVEL USE CASES

    def run(self, debugging=False):
        """
        test in interactive mode
        :return: None
        """
        t1 = time()
        while True:
            if self.speaker() == Speaker.SYSTEM:
                system_response = self.system_turn(debugging=debugging)
                if debugging:
                    print('Time delta: {:.5f}'.format(time() - t1))
                print("S:", system_response)
            else:
                user_input = input("U: ")
                t1 = time()
                self.user_turn(user_input, debugging=debugging)

    def system_turn(self, debugging=False):
        """
        an entire system turn comprising a single system utterance and
        one or more system transitions
        :return: the natural language system response
        """
        t1 = time()
        visited = {self.state()}
        responses = []
        while self.speaker() is Speaker.SYSTEM:
            response, next_state = self.system_transition(self.state(), debugging=debugging)
            self.take_transition(next_state)
            responses.append(response)
            if next_state in visited and self._speaker is Speaker.SYSTEM:
                self.change_speaker()
                break
            visited.add(next_state)
        t2 = time()
        if debugging:
            print('System turn in {:.5f}'.format(t2-t1))
        return  ' '.join(responses)

    def user_turn(self, natural_language, debugging=False):
        """
        an entire user turn comprising one user utterance and
        one or more user transitions
        :param natural_language:
        :param debugging:
        :return: None
        """
        t1 = time()
        self.state_update(natural_language, debugging)
        visited = {self.state()}
        while self.speaker() is Speaker.USER:
            next_state = self.user_transition(natural_language, self.state(), debugging=debugging)
            if self._error_transitioned and next_state != self.state():
                try:
                    nns = self.user_transition(natural_language, next_state, debugging=debugging)
                    if nns not in visited:
                        next_state = nns
                except RuntimeError:
                    if debugging:
                        print("Couldn't error hop")
            self.take_transition(next_state)
            if next_state in visited and self._speaker is Speaker.USER:
                self.change_speaker()
                break
            visited.add(next_state)
        self.set_speaker(Speaker.SYSTEM)
        t2 = time()
        if debugging:
            print('User turn in {:.5f}'.format(t2 - t1))


    def load_transitions(self, json_dict, speaker=None, root=None):
        """
        wheeeeeeee!
        """
        if speaker is None:
            speaker = self._initial_speaker
        if 'state' in json_dict:
            source = json_dict['state']
        else:
            source = DialogueFlow.autostate()
        if root is None:
            root = self._initial_state

        hop = None
        switch = False

        # read settings and transitions for state
        transitions = []
        for key, value in json_dict.items():
            if key == 'transitions':
                assert isinstance(value, list)
                transitions = value
            elif key == 'root':
                root = json_dict['root']
            elif key == 'hop':
                hop = json_dict['hop']
            elif key == 'prepend':
                prepend = json_dict['prepend']
                self.set_state_prepend(source, prepend)
            elif key == 'switch':
                switch = json_dict['switch']
            elif key not in {'state', 'hop', 'score', 'switch'}:
                transitions.append((key, value))

        # set up state settings
        if not self.has_state(source):
            self.add_state(source)
            self.set_error_successor(source, root)
        if hop:
            if speaker == Speaker.USER:
                speaker = Speaker.SYSTEM
                self.state_settings(source).update(system_multi_hop=True)
            elif speaker == Speaker.SYSTEM:
                speaker = Speaker.USER
                self.state_settings(source).update(user_multi_hop=True)
        if switch:
            self.update_state_settings(source, switch=True)

        # set up transitions
        expanded_transitions = []
        for natex, target in transitions:
            natex_with_leading_digits_stripped = ''
            i = 0
            c = natex[i] if natex else ''
            while c and c.isnumeric():
                natex_with_leading_digits_stripped += c
                i += 1
                c = natex[i] if i < len(natex) else ''
            if natex == 'error':
                if isinstance(target, dict):
                    if 'state' not in target:
                        target['state'] = DialogueFlow.autostate()
                    expanded_transitions.append(target)
                    target = target['state']
                    if not self.has_state(target):
                        self.add_state(target)
                        self.set_error_successor(target, root)
                self.set_error_successor(source, target)

            else:
                score = 1.0
                if isinstance(target, dict):
                    if 'state' not in target:
                        target['state'] = DialogueFlow.autostate()
                    if 'score' in target:
                        score = target['score']
                    expanded_transitions.append(target)
                    target = target['state']
                    if not self.has_state(target):
                        self.add_state(target)
                        self.set_error_successor(target, root)
                if speaker == Speaker.USER:
                    if self.has_transition(source, target, Speaker.USER):
                        intermediate = self.autostate()
                        self.add_state(intermediate, target, user_multi_hop=True)
                        self.add_user_transition(source, intermediate, natex, score=score)
                    else:
                        self.add_user_transition(source, target, natex, score=score)
                elif speaker == Speaker.SYSTEM:
                    if self.has_transition(source, target, Speaker.SYSTEM):
                        intermediate = self.autostate()
                        self.add_state(intermediate, system_multi_hop=True)
                        self.add_system_transition(intermediate, target, '')
                        self.add_system_transition(source, intermediate, natex, score=score)
                    else:
                        self.add_system_transition(source, target, natex, score=score)

        # switch turn (will be switched back if multi hop detected on next recursive call)
        if speaker == Speaker.USER:
            speaker = Speaker.SYSTEM
        elif speaker == Speaker.SYSTEM:
            speaker = Speaker.USER

        # recurse to load nested turns
        for transition in expanded_transitions:
            self.load_transitions(transition, speaker)

    # HIGH LEVEL

    def system_transition(self, state: Union[Enum, str, tuple], debugging=False):
        """
        :param state:
        :param debugging:
        :return: a <state, response> tuple representing the successor state and response
        """
        state = module_state(state)
        ti = time()
        if state is None:
            state = self.state()
        else:
            state = State(state)
        transition_options = {}
        if self._response is not None:
            response, vars, dest, score = self._response
            transition_options[(response, (self.state(), dest, self._speaker), vars)] = score
        self._gate_buffer.clear()
        transitions = list(self.transitions(state, Speaker.SYSTEM))
        for transition in transitions:
            self._potential_transition = transition
            if not self._is_module and isinstance(transition[1], tuple):
                continue
            t1 = time()
            natex = self.transition_natex(*transition)
            if '->' in transition[1]:
                transition = (transition[1].split('->')[0], transition[1].split('->')[1], Speaker.SYSTEM)
                natex = natex + self.transition_natex(*transition)
            settings = self.transition_settings(*transition)
            vars = HashableDict(self._vars)
            try:
                generation = natex.generate(vars=vars, macros=self._macros, debugging=debugging)
            except Exception as e:
                print()
                print(e)
                print('Transition {}: {} failed'.format(str(transition), natex))
                print()
                generation = None
            if generation is not None:
                if '__score__' in vars:
                    score = vars['__score__']
                    del vars['__score__']
                else:
                    score = settings.score
                transition_options[(generation, transition, vars)] = score
            t2 = time()
            if debugging:
                print('Transition {} evaluated in {:.5f}'.format(transition, t2-t1))
        if transition_options:
            remaining = list(transition_options)
            memory = self.state_settings(state).memory
            for item in memory:
                if len(transition_options) > 1:
                    key = None
                    for k in transition_options:
                        if k[1] == item:
                            key = k
                            break
                    if key:
                        del transition_options[key]
                else:
                    break
            response, transition, vars = random_max(transition_options, key=lambda x: transition_options[x])
            if self.is_switch(state):
                to_add_to_stack = [x[1] for x in remaining if x != (response, transition, vars)]
                for trans in to_add_to_stack:
                    src, tgt, natex = trans[0], trans[1], self.transition_natex(*trans)
                    if isinstance(src, tuple):
                        src = ':'.join(src)
                    if isinstance(tgt, tuple):
                        tgt = ':'.join(tgt)
                    if src != state:
                        tgt = src + '->' + tgt
                    self.vars()['__stack__'].append(tgt)
            if debugging:
                updates = {}
                for k, v in vars.items():
                    if k not in self._vars or v != self._vars[k]:
                        updates[k] = v
                if updates:
                    print('Updating vars:')
                    for k, v in updates.items():
                        if k in self._vars:
                            print('  {} = {} -> {}'.format(k, self._vars[k], v))
                        else:
                            print('  {} = None -> {}'.format(k, v))
            if transition in self.gate_buffer():
                self.gates()[transition].add(self.gate_buffer()[transition])
            self.update_vars(vars)
            next_state = transition[1]
            if debugging:
                tf = time()
                print('System transition in {:.5f}'.format(tf-ti))
                print('Transitioning {} -> {}'.format(self.state(), next_state))
            if self._response is not None:
                self._response = None
            if '__response_prefix__' in self.vars() and self.vars()['__response_prefix__'] != 'None':
                response = self.vars()['__response_prefix__'] + ' ' + response
                self.vars()['__response_prefix__'] = 'None'
            if self.is_switch(state):
                switch_response, switch_next_state = self.system_transition(next_state)
                return response + ' ' + switch_response, switch_next_state
            return response, next_state
        else:
            while self.is_switch(state) and self.vars()['__stack__']:
                target = self.vars()['__stack__'].pop()
                if '->' in target:
                    source, target = target.split('->')
                    transition = source, target, Speaker.SYSTEM
                    natex = self.transition_natex(*transition)
                    vars = HashableDict(self._vars)
                    try:
                        response = natex.generate(vars=vars, macros=self._macros, debugging=debugging)
                    except Exception as e:
                        print()
                        print(e)
                        print('Stack transition to {}: {} failed'.format(str(target), natex))
                        print()
                        response = None
                    if response is not None:
                        if transition in self.gate_buffer():
                            self.gates()[transition].add(self.gate_buffer()[transition])
                        self.update_vars(vars)
                        next_state = transition[1]
                        if debugging:
                            tf = time()
                            print('System transition in {:.5f}'.format(tf - ti))
                            print('Transitioning {} -> {}'.format(self.state(), next_state))
                        if self._response is not None:
                            self._response = None
                        if '__response_prefix__' in self.vars() and self.vars()['__response_prefix__'] != 'None':
                            response = self.vars()['__response_prefix__'] + ' ' + response
                            self.vars()['__response_prefix__'] = 'None'
                        return response, next_state
                else:
                    return self.system_transition(target, debugging=debugging)
            else:
                if self._default_state is not None:
                    self.set_state(self._default_state)
                    if debugging:
                        print('No valid system transitions found, going to default state...')
                    return self.system_transition(self.state(), debugging=debugging)
                raise AssertionError('dialogue flow system transition found no valid options')


    def user_transition(self, natural_language: str, state: Union[Enum, str, tuple], debugging=False):
        """
        :param state:
        :param natural_language:
        :param debugging:
        :return: the successor state representing the highest score user transition
                 that matches natural_language, or None if none match
        """
        state = module_state(state)
        self._error_transitioned = False
        ti = time()
        if state is None:
            state = self.state()
        else:
            state = State(state)
        transition_options = []
        if '__transition__' in self.vars() and self.vars()['__transition__']:
            transition_options.append(
                (self.vars()['__transition_score__'],
                 ('__global__', self.vars()['__transition__'], Speaker.USER),
                 self.vars()))
        ngrams = Ngrams(natural_language, n=10)
        self._gate_buffer.clear()
        for transition in self.transitions(state, Speaker.USER):
            self._potential_transition = transition
            if not self._is_module and isinstance(transition[1], tuple):
                continue
            t1 = time()
            if debugging:
                print('Evaluating transition {}'.format(transition[:2]))
            natex = self.transition_natex(*transition)
            settings = self.transition_settings(*transition)
            vars = HashableDict(self._vars)
            try:
                match = natex.match(natural_language, vars, self._macros, ngrams, debugging)
            except Exception as e:
                print()
                print(e)
                print('Transition {}: {} failed'.format(str(transition), natex))
                print()
                match = None
            if match:
                if debugging:
                    print('Transition {} matched "{}"'.format(transition[:2], natural_language))
                if '__score__' in vars:
                    score = vars['__score__']
                    del vars['__score__']
                else:
                    score = settings.score
                transition_options.append((score, transition, vars))
            t2 = time()
            if debugging:
                print('Transition {} evaluated in {:.5f}'.format(transition, t2-t1))
        if transition_options:
            score, transition, vars = random_max(transition_options, key=lambda x: x[0])
            if debugging:
                updates = {}
                for k, v in vars.items():
                    if k not in self._vars or v != self._vars[k]:
                        updates[k] = v
                if updates:
                    print('Updating vars:')
                    for k, v in updates.items():
                        if k in self._vars:
                            print('  {} = {} -> {}'.format(k, self._vars[k], v))
                        else:
                            print('  {} = None -> {}'.format(k, v))
            if transition in self.gate_buffer():
                self.gates()[transition].add(self.gate_buffer()[transition])
            self.update_vars(vars)
            next_state = transition[1]
            if debugging:
                print('User transition in {:.5f}'.format(time() - ti))
                print('Transitioning {} -> {}'.format(self.state(), next_state))
            return next_state
        else:
            self._error_transitioned = True
            next_state = self.error_successor(self.state())
            if debugging:
                print('User transition in {:.5f}'.format(time() - ti))
                print('Error transition {} -> {}'.format(self.state(), next_state))
            return next_state

    def precache_transitions(self, process_num=1):
        """
        Make DialogueFlow fast from the start with the power of precache!
        """
        if process_num == 1:
            for transition in self._graph.arcs():
                data = self._graph.arc_data(*transition)
                data['natex'].precache()
            for rule in self.update_rules().rules:
                rule.precondition.precache()
                rule.postcondition.precache()
        else:
            # transition_data_sets = []
            # for i in range(process_num):
            #     transition_data_sets.append([])
            # count = 0
            # for transition in self._graph.arcs():
            #     transition_data_sets[count].append(self._graph.arc_data(*transition))
            #     count = (count + 1) % process_num
            #
            # print("multiprocessing...")
            # p = Pool(process_num)
            # results = p.map(precache, transition_data_sets)
            # for i in range(len(results)):
            #     result_list = results[i]
            #     t_list = transition_data_sets[i]
            #     for j in range(len(result_list)):
            #         parsed_tree = result_list[j]
            #         t = t_list[j]
            #         t['natex']._compiler._parsed_tree = parsed_tree
            raise NotImplementedError()


    def check(self, debugging=False):
        all_good = True
        for state in self._graph.nodes():
            has_system_fallback = False
            has_user_fallback = False
            for source, target, speaker in self._graph.arcs_out(state):
                if speaker == Speaker.SYSTEM:
                    if self.transition_natex(source, target, speaker).is_complete():
                        has_system_fallback = True
            if self.error_successor(state) is not None:
                has_user_fallback = True
            in_labels = {x[2] for x in self.incoming_transitions(state)}
            if Speaker.SYSTEM in in_labels:
                if not has_user_fallback:
                    if debugging:
                        print('WARNING: Turn-taking dead end: state {} has no fallback user transition'.format(state))
                    all_good = False
            if Speaker.USER in in_labels:
                if not has_system_fallback:
                    if debugging:
                        print('WARNING: Turn-taking dead end: state {} may have no fallback system transitions'.format(state))
                    all_good = False
        return all_good

    def add_user_transition(self, source: Union[Enum, str, tuple], target: Union[Enum, str, tuple],
                            natex_nlu: Union[str, NatexNLU, List[str]], **settings):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        if self.has_transition(source, target, Speaker.USER):
            raise ValueError('user transition {} -> {} already exists'.format(source, target))
        natex_nlu = NatexNLU(natex_nlu, macros=self._macros)
        if not self.has_state(source):
            self.add_state(source)
        if not self.has_state(target):
            self.add_state(target)
        self._graph.add_arc(source, target, Speaker.USER)
        self.set_transition_natex(source, target, Speaker.USER, natex_nlu)
        transition_settings = Settings(score=1.0)
        transition_settings.update(**settings)
        self.set_transition_settings(source, target, Speaker.USER, transition_settings)
        if target in self._prepends:
            prepend = self._prepends[target]
            natex = self.transition_natex(source, target, Speaker.USER)
            self.set_transition_natex(source, target, Speaker.USER, prepend + natex)

    def add_system_transition(self, source: Union[Enum, str, tuple], target: Union[Enum, str, tuple],
                              natex_nlg: Union[str, NatexNLG, List[str]], **settings):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        if self.has_transition(source, target, Speaker.SYSTEM):
            raise ValueError('system transition {} -> {} already exists'.format(source, target))
        natex_nlg = NatexNLG(natex_nlg, macros=self._macros)
        if not self.has_state(source):
            self.add_state(source)
        if not self.has_state(target):
            self.add_state(target)
        self._graph.add_arc(source, target, Speaker.SYSTEM)
        self.set_transition_natex(source, target, Speaker.SYSTEM, natex_nlg)
        transition_settings = Settings(score=1.0)
        transition_settings.update(**settings)
        self.set_transition_settings(source, target, Speaker.SYSTEM, transition_settings)
        if target in self._prepends:
            prepend = self._prepends[target]
            natex = self.transition_natex(source, target, Speaker.SYSTEM)
            self.set_transition_natex(source, target, Speaker.SYSTEM, prepend + natex)

    def add_state(self, state: Union[Enum, str, tuple], error_successor: Union[Union[Enum, str, tuple], None] =None, **settings):
        state = module_state(state)
        state = State(state)
        if self.has_state(state):
            raise ValueError('state {} already exists'.format(state))
        state_settings = Settings(user_multi_hop=False, system_multi_hop=False, switch=False, memory=10)
        state_settings.update(**settings)
        self._graph.add_node(state)
        self.update_state_settings(state, **state_settings)
        if error_successor is not None:
            error_successor = State(error_successor)
            self.set_error_successor(state, error_successor)


    # MID LEVEL

    def take_transition(self, target):
        target = module_state(target)
        if self.speaker() is Speaker.SYSTEM:
            transition = (self.state(), target, self.speaker())
            self.state_settings(self.state()).memory.add(transition)
        self.set_state(target)
        if self.speaker() is Speaker.SYSTEM:
            if not self.state_settings(self.state()).system_multi_hop:
                self.set_speaker(Speaker.USER)
        else:
            if not self.state_settings(self.state()).user_multi_hop:
                self.set_speaker(Speaker.SYSTEM)

    # LOW LEVEL: PROPERTIES, GETTERS, SETTERS

    def transition_natex(self, source: Union[Enum, str, tuple], target: Union[Enum, str, tuple], speaker: Enum):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        return self._graph.arc_data(source, target, speaker)['natex']

    def set_transition_natex(self, source, target, speaker, natex):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        self._graph.arc_data(source, target, speaker)['natex'] = natex

    def transition_settings(self, source: Union[Enum, str, tuple], target: Union[Enum, str, tuple], speaker: Enum):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        return self._graph.arc_data(source, target, speaker)['settings']

    def set_transition_settings(self, source, target, speaker, settings):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        self._graph.arc_data(source, target, speaker)['settings'] = settings

    def update_transition_settings(self, source, target, speaker, **settings):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        self.transition_settings(source, target, speaker).update(**settings)

    def state_settings(self, state):
        state = module_state(state)
        state = State(state)
        return self._graph.data(state)['settings']

    def add_global_nlu(self, state, nlu, score=0.5):
        state = module_state(state)
        state = State(state)
        if not self.has_state(state):
            self.add_state(state)
        if isinstance(state, tuple):
            state = ':'.join(state)
        if isinstance(nlu, list) or isinstance(nlu, set):
            nlu = '{' + ', '.join(nlu) + '}'
        self._rules.add('{} ({})'.format(nlu, score), '#TRANSITION({}, {})'.format(state, score))

    def update_state_settings(self, state, **settings):
        state = module_state(state)
        state = State(state)
        if 'settings' not in self._graph.data(state):
            self._graph.data(state)['settings'] = Settings()
        if 'memory' in settings:
            settings['memory'] = Memory(settings['memory'])
        if 'global_nlu' in settings:
            self.add_global_nlu(state, settings['global_nlu'])
        self.state_settings(state).update(**settings)

    def remove_transition(self, source, target, speaker):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        MapMultidigraph.remove_arc(self.graph(), source, target, speaker)

    def states(self):
        return self.graph().nodes()

    def state(self):
        return self._vars['__state__']

    def set_state(self, state: Union[Enum, str, tuple]):
        state = module_state(state)
        state = State(state)
        self._vars['__state__'] = state

    def has_state(self, state):
        state = module_state(state)
        state = State(state)
        return self._graph.has_node(state)

    def error_successor(self, state):
        state = module_state(state)
        state = State(state)
        data = self._graph.data(state)
        if 'error' in data:
            return data['error']
        else:
            return None

    def set_error_successor(self, state, error_successor):
        state, error_successor = module_source_target(state, error_successor)
        state = State(state)
        error_successor = State(error_successor)
        self._graph.data(state)['error'] = error_successor

    def speaker(self):
        return self._speaker

    def set_speaker(self, speaker: Enum):
        self._speaker = speaker

    def graph(self):
        return self._graph

    def vars(self):
        return self._vars

    def set_vars(self, vars):
        self._vars = vars
        self.update_rules().set_vars(vars)

    def transitions(self, source_state, speaker=None):
        """
        get (source, target, speaker) transition tuples for the entire state machine
        (default) or that lead out from a given source_state
        :param source_state: optionally, filter returned transitions by source state
        :param speaker: optionally, filter returned transitions by speaker
        :return: a generator over (source, target, speaker) 3-tuples
        """
        source_state = module_state(source_state)
        source_state = State(source_state)
        if speaker is None:
            yield from self._graph.arcs_out(source_state)
        elif self._graph.has_arc_label(source_state, speaker):
            yield from self._graph.arcs_out(source_state, label=speaker)
        else:
            return

    def has_transition(self, source, target, speaker):
        source, target = module_source_target(source, target)
        source = State(source)
        target = State(target)
        return self._graph.has_arc(source, target, speaker)

    def incoming_transitions(self, target_state):
        target_state = module_state(target_state)
        target_state = State(target_state)
        yield from self._graph.arcs_in(target_state)

    def change_speaker(self):
        if self.speaker() is Speaker.USER:
            self.set_speaker(Speaker.SYSTEM)
        elif self.Speaker is Speaker.SYSTEM:
            self.set_speaker(Speaker.USER)

    def reset(self):
        self._speaker = self._initial_speaker
        self._vars = HashableDict()
        self.set_state(self._initial_state)
        self._rules.set_vars(self._vars)
        self._gates = defaultdict(set)
        for state in self.graph().nodes():
            self.state_settings(state).memory.clear()

    def update_vars(self, variables: HashableDict):
        if not isinstance(variables, HashableDict):
            variables = HashableDict(variables)
        for k in variables.altered():
            if k in self._var_dependencies:
                dependencies = self._var_dependencies[k]
                for dependency in dependencies:
                    if dependency in self._vars:
                        self._vars[dependency] = None
        self._vars.update({k: variables[k] for k in variables.altered()})

    def potential_transition(self):
        return self._potential_transition

    def gates(self):
        return self._gates

    def gate_buffer(self):
        return self._gate_buffer

    def buffer_configuration(self, configuration):
        self._gate_buffer[self._potential_transition] = configuration

    def gate_requirements(self):
        return self._gate_requirements

    def set_gate_requirements(self, requirements):
        self._gate_requirements[self._potential_transition] = requirements

    def var_dependencies(self):
        return self._var_dependencies

    def set_state_prepend(self, state, prepend):
        state = module_state(state)
        self._prepends[state] = prepend
        if self.has_state(state):
            for transition in self._graph.arcs_in(state):
                natex = self.transition_natex(*transition)
                self.set_transition_natex(*transition, prepend + natex)

    def passes_gate(self, var_config):
        if var_config in self._gates[self._potential_transition]:
            return False
        for k, v in self._gate_requirements[self._potential_transition].items():
            if k not in var_config:
                if v is not None:
                    return False
            else:
                if v != var_config[k]:
                    return False
        for k, v in var_config.items():
            if v is None:
                if k not in self._gate_requirements[self._potential_transition] \
                    or self._gate_requirements[self._potential_transition][k] is not None:
                    return False
        return True

    def add_update_rule(self, precondition, postcondition=None):
        self._rules.add(precondition, postcondition)

    def state_update(self, user_input, debugging=False):
        result = self._rules.update(user_input, debugging)
        if result is not None:
            response, score = result
            self._response = response, self._vars, self.state(), score
            self.set_speaker(Speaker.SYSTEM)

    def knowledge_base(self):
        return self._kb

    def set_is_module(self):
        self._is_module = True

    def is_switch(self, state):
        return self.state_settings(state)['switch']

    def update_rules(self):
        return self._rules