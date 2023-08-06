import pandas as pd
import numpy as np
import os, json, random

class CovidDataset():
    def __init__(self):
        self.confirmed_global = pd.read_csv(os.path.join('modules','time_series_covid19_confirmed_global.csv'))
        self.confirmed_us = pd.read_csv(os.path.join('modules','time_series_covid19_confirmed_US.csv'))
        self.deaths_global = pd.read_csv(os.path.join('modules','time_series_covid19_deaths_global.csv'))
        self.deaths_us = pd.read_csv(os.path.join('modules','time_series_covid19_deaths_US.csv'))
        self.states = json.load(open(os.path.join('modules','states.json')))

        # keywords
        self.keywords = json.load(open(os.path.join('modules','keywords.json')))
        self.travel_keywords = set(self.keywords['travel'])
        self.family_keywords = set(self.keywords['family'])
        self.work_keywords = set(self.keywords['work'])
        self.social_keywords = set(self.keywords['social'])

        # variables
        self.stats = dict()
        self.total_confirmed_lastweek, self.total_confirmed_today = 0.0, 0.0
        self.total_deaths_lastweek, self.total_deaths_today = 0.0, 0.0
        self.total_recovered_lastweek, self.total_recovered_today = 0.0, 0.0

        self.read_us(confirmed=self.confirmed_us, deaths=self.deaths_us)
        self.read_global(confirmed=self.confirmed_global, deaths=self.deaths_global)
        self.process_stats()
        self.locations = set(list(self.stats.keys()) + ['united states', 'usa', 'america'])
        return

    def read_us(self, confirmed, deaths):
        stats = self.stats
        us_confirmed, us_deaths, us_dr = 0.0, 0.0, 0.0

        for x in list(self.states.values()):
            stats[x.lower()] = {'confirmed_yesterday': 0.0, 'confirmed_today': 0.0, 'deaths_yesterday': 0.0, 'deaths_today': 0.0}

        for i, x in confirmed.groupby(['Province_State']):
            if i.lower() not in stats:
                continue
            else:
                today, yesterday = x.iloc[:, -1], x.iloc[:, -2]
                stats[i.lower()]['confirmed_yesterday'] = yesterday.sum()
                stats[i.lower()]['confirmed_today'] = today.sum()
                us_confirmed += today.sum()

        for i, x in deaths.groupby(['Province_State']):
            if i.lower() not in stats:
                continue
            else:
                today, yesterday = x.iloc[:, -1], x.iloc[:, -2]
                stats[i.lower()]['deaths_yesterday'] = yesterday.sum()
                stats[i.lower()]['deaths_today'] = today.sum()
                us_deaths += today.sum()

        self.us_confirmed = int(us_confirmed)
        self.us_deaths = int(us_deaths)
        self.us_dr = round((us_deaths / us_confirmed) * 100.0, 3)
        return

    def read_global(self, confirmed, deaths):
        stats = self.stats
        global_confirmed, global_deaths, global_dr = 0.0, 0.0, 0.0

        for x in list(confirmed['Country/Region'].unique()):
            if x.lower() in ['georgia']:
                continue
            stats[x.lower()] = {'confirmed_yesterday': 0.0, 'confirmed_today': 0.0, 'deaths_yesterday': 0.0, 'deaths_today': 0.0}

        for i, x in confirmed.groupby(['Country/Region']):
            if i.lower() not in stats or i.lower() in ['georgia']:
                continue
            else:
                today, yesterday = x.iloc[:, -1], x.iloc[:, -2]
                stats[i.lower()]['confirmed_yesterday'] = yesterday.sum()
                stats[i.lower()]['confirmed_today'] = today.sum()
                global_confirmed += today.sum()

        for i, x in deaths.groupby(['Country/Region']):
            if i.lower() not in stats or i.lower() in ['georgia']:
                continue
            else:
                today, yesterday = x.iloc[:, -1], x.iloc[:, -2]
                stats[i.lower()]['deaths_yesterday'] = yesterday.sum()
                stats[i.lower()]['deaths_today'] = today.sum()
                global_deaths += today.sum()

        # special case
        stats['usa'] = stats['us']
        stats['united states'] = stats['us']
        stats['america'] = stats['us']

        self.global_confirmed = int(global_confirmed)
        self.global_deaths = int(global_deaths)
        self.global_dr = round((global_deaths / global_confirmed) * 100.0, 1)

        # print ()
        # print ('confirmed-{} \t deaths-{} \t dr-{}'.format(self.global_confirmed, self.global_deaths, self.global_dr))
        return


    def process_stats(self):
        stats = self.stats

        for k, v in stats.items():
            diff_confirmed = v['confirmed_today'] - v['confirmed_yesterday']
            diff_deaths = v['deaths_today'] - v['deaths_yesterday']

            if v['deaths_today'] == 0:
                death_rate = 0.0
            else:
                death_rate = round((v['deaths_today'] / v['confirmed_today']) * 100.0, 1)

            v.update({'diff_confirmed': diff_confirmed, 'diff_deaths': diff_deaths, 'death_rate': death_rate})
            stats[k] = v
        return