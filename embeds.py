import discord
from matplotlib import pyplot
import matplotlib as mpl
import io
import copy

import api
from cache import cache


COLOUR = 0x000000
ERROR_COL = 0xFF0000


def error(text):
    e = discord.Embed(title='Error', description=text, colour=ERROR_COL)
    return {'embed': e}


def clear():
    pyplot.clf()
    cols = [
        '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a',
        '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94',
        '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d',
        '#17becf', '#9edae5'
    ]
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=cols) 
    ax = pyplot.subplot(111)
    for spine in ('right', 'top', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)


def graph(embed):
    file = io.BytesIO()
    pyplot.savefig(file, format='png', bbox_inches='tight')
    file.seek(0)
    cf = copy.deepcopy(file)
    dfile = discord.File(file, filename='graph.png')
    embed.set_image(url='attachment://graph.png')
    return dfile, cf


@cache
def affected():
    countries, time = api.affected()
    desc = ', '.join(countries)
    title = f'{len(countries)} Affected Countries'
    e = discord.Embed(
        title=title, description=desc, timestamp=time, colour=COLOUR
    )
    return {'embed': e}


@cache
def country_history(country):
    try:
        points, time = api.country_history(country)
    except ValueError as exc:
        return error(exc)
    clear()
    times = [point['time'] for point in points]
    for label in points[0]:
        if label == 'time':
            continue
        lbl = label.replace('_', ' ').title()
        pyplot.plot(times, [point[label] for point in points], label=lbl)
    pyplot.legend()
    title = f'History for {country}'
    e = discord.Embed(title=title, timestamp=time)
    file, bio = graph(e)
    return {'embed': e, 'file': file, 'b_io': bio}


@cache
def by_country():
    points, time = api.by_country()
    points = points[:15]
    clear()
    pyplot.figure(figsize=(15, 5))
    labels = [label for label in points[0] if label != 'country']
    countries = [point['country'] for point in points]

    def ind():
        return range(0, len(points)*2, 2)
    bars = []
    for label in points[0]:
        if label == 'country':
            continue
        bars.append(
            pyplot.bar(ind(), [point[label] for point in points], 1.5)[0]
        )
    pyplot.xticks(ind(), countries)
    pyplot.legend(bars, [label.replace('_', ' ').title() for label in labels])
    desc = (
        'Only the top 15 countries are shown in order to make the image a '
        'reasonable size.'
    )
    e = discord.Embed(
        title='Country Stats', description=desc, timestamp=time, colour=COLOUR
    )
    file, bio = graph(e)
    return {'embed': e, 'file': file, 'b_io': bio}


@cache
def usa():
    data, time = api.usa()
    text = (
        'There are currently {} cases in the USA, {} of which are due to '
        'foreign travel, and {} of which are due to person to person spread. '
        'The remaining {} cases have unkown cause. There have been {} deaths '
        'in the USA and {} have been affected.'
    ).format(
        data['cases'], data['travel_related'], data['person_to_person'],
        data['unknown'], data['deaths'], data['states']
    )
    e = discord.Embed(
        title='USA Stats', description=text, timestamp=time, colour=COLOUR
    )
    return {'embed': e}


@cache
def by_state():
    points = api.by_state()
    data = [list(point.values()) for point in points if point['cases']]
    headers = list(points[0].keys())
    clear()
    pyplot.table(cellText=data, colLabels=headers, loc='center')
    pyplot.axis('off')
    e = discord.Embed(title='USA Cases', colour=COLOUR)
    file, bio = graph(e)
    return {'embed': e, 'file': file, 'b_io': bio}


@cache
def country_latest(country):
    try:
        data, time = api.country_latest(country)
    except ValueError as exc:
        return error(exc)
    clear()
    pyplot.figure(figsize=(9, 5))

    def ind():
        return [i*1.5 for i in range(len(data))]
    pyplot.bar(ind(), list(data.values()), align='center')
    pyplot.xticks(ind(), [k.replace('_', ' ').title() for k in data])
    e = discord.Embed(title=f'{country} Stats', timestamp=time, colour=COLOUR)
    file, bio = graph(e)
    return {'embed': e, 'file': file, 'b_io': bio}


@cache
def world():
    data, time = api.world()
    clear()
    pyplot.bar(range(len(data)), list(data.values()), align='center')
    pyplot.xticks(
        range(len(data)), [k.replace('_', ' ').title() for k in data]
    )
    e = discord.Embed(title='World Stats', timestamp=time, colour=COLOUR)
    file, bio = graph(e)
    return {'embed': e, 'file': file, 'b_io': bio}
