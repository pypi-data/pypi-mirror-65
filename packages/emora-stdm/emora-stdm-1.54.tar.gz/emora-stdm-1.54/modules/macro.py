from emora_stdm import Macro
from emora_stdm import NatexNLU

class DetectTravel(Macro):
    def __init__(self, keywords):
        self.keywords = keywords

    def run(self, ngrams, vars, args):
        match = ngrams & self.keywords
        return match


class DetectFamily(Macro):
    def __init__(self, keywords):
        self.keywords = keywords

    def run(self, ngrams, vars, args):
        match = ngrams & self.keywords
        return match


class DetectWork(Macro):
    def __init__(self, keywords):
        self.keywords = keywords

    def run(self, ngrams, vars, args):
        match = ngrams & self.keywords
        return match


class DetectSocial(Macro):
    def __init__(self, keywords):
        self.keywords = keywords

    def run(self, ngrams, vars, args):
        match = ngrams & self.keywords
        return match


# detect location
class DetectLocation(Macro):
    def __init__(self, locations):
        self.locations = locations

    def run(self, ngrams, vars, args):
        match = ngrams & self.locations
        return match


class DummyTrue(Macro):
    def __init__(self):
        pass

    def run(self, ngrams, vars, args):
        return True


class TravelSummary(Macro):
    def __init__(self, stats):
        self.stats = stats

    def run(self, ngrams, vars, args):
        location = vars[args[0]]
        stats = self.stats[location]

        # response generation
        response = 'I believe you made the right decision. Compared to yesterday, there are {} new confirmed cases in {} with total of {} positive cases.' \
                   ' I hope travel businesses to come back to normal states soon.'.format(stats['diff_confirmed'], location, stats['confirmed_today'])
        return response


class InfoSummary(Macro):
    def __init__(self, stats):
        self.stats = stats

    def run(self, ngrams, vars, args):
        location = vars[args[0]]
        stats = self.stats[location]

        # response generation
        if stats['diff_confirmed'] > 1 or stats['diff_confirmed'] == 1:
            response = 'At {}, there are about {} confirmed and {} deaths so far. Compared to yesterday, there are {} more positive cases. '.format(location, stats['confirmed_today'], stats['deaths_today'], stats['diff_confirmed'])
        else:
            response = 'At {}, there are about {} confirmed and {} deaths so far. Compared to yesterday, there is {} more positive case. '.format(location, stats['confirmed_today'], stats['deaths_today'], stats['diff_confirmed'])
        return response



# facts
class RandomFact(Macro):
    def __init__(self):
        pass

    def run(self, ngrams, vars, args):
        facts = ['Corona virus can infect anyone regardless of race or ethnicity. Help stop fear by letting people know that being of Asian descent does not increase the chance of getting or spreading coronavirus.',
                 'Wash your hands often with soap and water for at least 20 seconds. Avoid touching your eyes, nose and mouth with unwashed hands',
                 'Health experts said that the vaccine will be ready in the next 12 to 18 months. As of now, prevention is the best practice against coronavirus',
                 'Coronavirus is a type of RNA virus, which is well known for its frequent mutations.',
                 'According to W H O, coronavirus may survive on non-organic surfaces ranging from few hours to several days']
        return random.choice(facts)