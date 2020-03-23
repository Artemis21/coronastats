import requests
import datetime
import re

from config import API_KEY


URL = 'https://coronavirus-monitor.p.rapidapi.com/coronavirus/{}.php'
HEADERS = {
    'x-rapidapi-host': 'coronavirus-monitor.p.rapidapi.com',
    'x-rapidapi-key': API_KEY,
}


def to_int(val):
    if not val:
        return 0
    v = float(val.replace(',', ''))
    if int(v) == v:
        return int(v)
    return v


def to_time(val):
    return datetime.datetime.fromisoformat(val.split('.')[0])


def get_endpoint(endpoint, **params):
    res = requests.get(URL.format(endpoint), headers=HEADERS, params=params)
    return res.json()


def affected():
    raw = get_endpoint('affected')
    countries = raw['affected_countries']
    time = to_time(raw['statistic_taken_at'])
    return countries, time


def country_history(country):
    raw = get_endpoint('cases_by_particular_country', country=country)
    points = []
    for point in raw['stat_by_country']:
        points.append({
            'cases': to_int(point['total_cases']),
            'new_cases': to_int(point['new_cases']),
            'active': to_int(point['active_cases']),
            'deaths': to_int(point['total_deaths']),
            'new_deaths': to_int(point['new_deaths']),
            'recovered': to_int(point['total_recovered']),
            'critical': to_int(point['serious_critical']),
            'cases_per_million': to_int(point['total_cases_per1m']),
            'time': to_time(point['record_date'])
        })
    if not points:
        raise ValueError(f'No data found for {country}.')
    return points, points[-1]['time']


def by_country():
    raw = get_endpoint('cases_by_country')
    time = to_time(raw['statistic_taken_at'])
    points = []
    for point in raw['countries_stat']:
        points.append({
            'country': point['country_name'],
            'cases': to_int(point['cases']),
            'active': to_int(point['active_cases']),
            'deaths': to_int(point['deaths']),
            'new_deaths': to_int(point['new_deaths']),
            'recovered': to_int(point['total_recovered']),
            'critical': to_int(point['serious_critical']),
            'cases_per_million': to_int(
                point['total_cases_per_1m_population']
            ),
        })
    return points, time


def usa():
    raw = get_endpoint('united_states_stat_small')
    data = {
        'cases': to_int(raw['total_cases']),
        'deaths': to_int(raw['total_deaths']),
        'travel_related': to_int(raw['travel_related_cases']),
        'person_to_person': to_int(raw['person_to_person_spread_cases']),
        'unknown': to_int(raw['under_investigation'])
    }
    m = re.match('.*\((.*)\)', raw['state_reported_cases'])
    if m:
        data['states'] = m.group(1)
    else:
        data['states'] = raw['state_reported_cases'] + ' states'
    time = to_time(raw['statistic_taken_at'])
    return data, time


def by_state():
    raw = get_endpoint('usastates')
    points = []
    for point in raw['united_states_stat']:
        points.append({
            'state': point['state'],
            'cases': to_int(point['cases']),
            'sex': point['sex'],
            'age': point['age'],
            'date': point['date'],
            'number': point['case_number']
        })
    return points


def country_latest(country):
    raw = get_endpoint('latest_stat_by_country', country=country)
    point = raw['latest_stat_by_country'][0]
    if not point:
        raise ValueError(f'No data found for {country}.')
    data = {
        'cases': to_int(point['total_cases']),
        'new_cases': to_int(point['new_cases']),
        'active': to_int(point['active_cases']),
        'deaths': to_int(point['total_deaths']),
        'new_deaths': to_int(point['new_deaths']),
        'recovered': to_int(point['total_recovered']),
        'critical': to_int(point['serious_critical']),
        'cases_per_million': to_int(point['total_cases_per1m']),
    }
    return data, to_time(point['record_date'])


def world():
    raw = get_endpoint('worldstat')
    data = {
        'cases': to_int(raw['total_cases']),
        'new_cases': to_int(raw['new_cases']),
        'deaths': to_int(raw['total_deaths']),
        'new_deaths': to_int(raw['new_deaths']),
        'recovered': to_int(raw['total_recovered']),
    }
    time = to_time(raw['statistic_taken_at'])
    return data, time
