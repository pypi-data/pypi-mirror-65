from emora_stdm import Macro
import pandas as pd
import os, json, random

class Dataset():
    def __init__(self):
        self.confirmed = pd.read_csv(os.path.join('modules','time_series_19-covid-Confirmed.csv'))
        self.deaths = pd.read_csv(os.path.join('modules','time_series_19-covid-Deaths.csv'))
        self.recovered = pd.read_csv(os.path.join('modules','time_series_19-covid-Recovered.csv'))
        self.states = json.load(open(os.path.join('modules','states.json')))

        # variables
        self.stats = dict()
        self.total_confirmed_lastweek, self.total_confirmed_today = 0.0, 0.0
        self.total_deaths_lastweek, self.total_deaths_today = 0.0, 0.0
        self.total_recovered_lastweek, self.total_recovered_today = 0.0, 0.0

        # read last k days of data
        self.read(dataset=self.confirmed, type='confirmed', k=7)
        self.read(dataset=self.deaths, type='deaths', k=7)
        self.read(dataset=self.recovered, type='recovered', k=7)
        self.locations = list(self.stats.keys()) + ['united states', 'usa']
        self.locations = set(self.locations)

        # process statistics
        self.process_stats()
        return

    def read(self, dataset, type, k=7):
        stats = self.stats
        base = [0.0] * k

        for i, row in dataset.iterrows():
            city, country, state = str(row['Province/State']).lower().strip(), str(row['Country/Region']).lower().strip(), None
            city = city.replace('county', '')
            recent_values = row.tolist()[-k:]

            if country == 'nan':
                continue
            if 'diamond princess' in city or 'georgia' in country:
                continue
            if 'china' in country:
                country = 'china'

            # split city and state
            if ',' in city:
                temp = city.split(',')
                city, state = temp[0].strip(), temp[1].strip()
                if state.upper() in self.states:
                    state = self.states[state.upper()].lower()

            if country not in stats and country != 'nan':
                stats[country] = {'confirmed': base, 'deaths': base, 'recovered': base}
            if city not in stats and city != 'nan':
                stats[city] = {'confirmed': base, 'deaths': base, 'recovered': base}
            if state not in stats and state != 'nan' and state != None:
                stats[state] = {'confirmed': base, 'deaths': base, 'recovered': base}

            # parser
            if country != 'nan':
                stats[country][type] = [float(sum(x)) for x in zip(stats[country][type], recent_values)]
            if city != 'nan':
                stats[city][type] = [float(sum(x)) for x in zip(stats[city][type], recent_values)]
            if state != 'nan' and state != None:
                stats[state][type] = [float(sum(x)) for x in zip(stats[state][type], recent_values)]

            if type == 'confirmed':
                self.total_confirmed_lastweek += recent_values[0]
                self.total_confirmed_today += recent_values[-1]
            if type == 'deaths':
                self.total_deaths_lastweek += recent_values[0]
                self.total_deaths_today += recent_values[-1]
            if type == 'recovered':
                self.total_recovered_lastweek += recent_values[0]
                self.total_recovered_today += recent_values[-1]
        return

    def process_stats(self):
        # global stats
        self.total_death_rate = (self.total_deaths_today / self.total_confirmed_today) * 100.0
        self.avg_confirmed = (self.total_confirmed_today - self.total_confirmed_lastweek) / len(self.confirmed)
        self.avg_deaths = (self.total_deaths_today - self.total_deaths_lastweek) / len(self.confirmed)
        self.avg_recovered = (self.total_recovered_today - self.total_recovered_lastweek) / len(self.confirmed)

        stats = self.stats
        for k, v in stats.items():
            diff_confirmed = v['confirmed'][-1] - v['confirmed'][0]
            diff_deaths = v['deaths'][-1] - v['deaths'][0]
            diff_recovered = v['recovered'][-1] - v['recovered'][0]
            p_increase = (diff_confirmed / (v['confirmed'][0] + 1.0)) * 100.0

            if v['deaths'][-1] == 0:
                death_rate = 0.0
            else:
                death_rate = round((v['deaths'][-1] / v['confirmed'][-1]) * 100.0, 3)

            new_feats = {'diff_confirmed': diff_confirmed, 'diff_deaths': diff_deaths, 'diff_recovered': diff_recovered, 'death_rate': death_rate, 'p_increase': p_increase,
                         'global_death_rate': self.total_death_rate}
            v.update(new_feats)
            stats[k] = v
        return


# detect location
class DetectLocation(Macro):
    def __init__(self, locations, stats):
        self.locations = locations
        self.stats = stats

    def run(self, ngrams, vars, args):
        match = ngrams & self.locations
        return ngrams & self.locations


# location stats
class SummaryLocation(Macro):
    def __init__(self, stats):
        self.stats = stats

    def run(self, ngrams, vars, args):
        location = vars[args[0]]
        if location in ['united states', 'usa']:
            location = 'us'

        stats = self.stats[location]

        # response generation
        response_1 = 'Compared to last week, there are {} new confirmed cases in {} with {} additional deaths. '.format(int(stats['diff_confirmed']), location, int(stats['diff_deaths']))

        if stats['p_increase'] > 100.0:
            response_2 = 'You should be extra careful since the approximate percent increase of confirmed case in the last 7 days is {} percent. '.format(round(stats['p_increase'], 2))
        elif stats['death_rate'] > stats['global_death_rate']:
            response_2 = 'The death rate in your region is {} percent higher than the nation average of {}. '.format(round(stats['death_rate'] - stats['global_death_rate'], 2), round(stats['global_death_rate'], 2))
        else:
            response_2 = ' '

        # followup
        response = response_1 + response_2 + 'Are you interested in hearing official CDC facts for coronavirus prevention'
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