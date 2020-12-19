from matterhook import Webhook
import os
from is_travel_log import is_travel_log
from url_generator import get_kibana_url


def send_message(log_path, server, urls, count, code, top5_urls):
    api_key = os.environ['MATTERMOST_API_KEY']
    kibana_url = get_kibana_url(server, log_path)
    message = f'**@channel :warning: [Смотреть в Kibana]({kibana_url})\nБольшое количество {code} ошибок за последние 15 минут на {server} - {log_path} ({count})**\n'
    top_message = f'\n**TOP 5**\n\n'
    channel = 'rsmon-notifications'
    if code == '4xx':
        message = f'**@channel :warning: \nБольшое количество {code} ошибок за последние 15 минут на {server} - {log_path} ({count})**\n'
        channel = 'http-4xx-errors'
    if server == 'travelask' or is_travel_log(log_path):
        api_key = os.environ['MATTERMOST_API_KEY_TRAVEL']
        message = f'**:warning: [Смотреть в Kibana]({kibana_url}) \nБольшое количество {code} ошибок за последние 15 минут на {server} - {log_path} ({count})**\n'
        if code == '4xx':
            message = f'**:warning: \nБольшое количество {code} ошибок за последние 15 минут на {server} - {log_path} ({count})**\n'
        channel = 'travelask-bugs'
    if log_path == '/data/logs/cdn.vashurok.access.log' or log_path == '/data/logs/vashurok.access.log':
        api_key = os.environ['MATTERMOST_API_KEY_TRAVEL']
        channel = 'shkolniki'
        message = f'**:warning: [Смотреть в Kibana]({kibana_url}) \nБольшое количество {code} ошибок за последние 15 минут на {server} - {log_path} ({count})**\n'
        if code == '4xx':
            message = f'**:warning: \nБольшое количество {code} ошибок за последние 15 минут на {server} - {log_path} ({count})**\n'

    mwh = Webhook('https://bfchat.ru', api_key)
    mwh.username = 'Log checker'
    mwh.icon_url = 'http://rsmon-api.r6s.ru/focus-512.png'
    markdown_msg = message
    markdown_msg += '\n| CODE | URL | USER | REF | IP |\n'
    markdown_msg += '| :----| :---- | :---- | :---- | :---- |\n'
    for url in urls:
        u = list(url.keys())
        ai = list(url.values())
        markdown_msg += f'| {ai[0][0]} | {u[0]} | {ai[0][1]} | {ai[0][2]} | {ai[0][3]} |\n'
    if code == '4xx':
        markdown_msg += ' '
        markdown_msg += top_message
        markdown_msg += '| URL | COUNT |\n'
        markdown_msg += '| :---- | :---- |\n'
        for top_url in top5_urls:
            c = list(top_url.values())
            markdown_msg += f'| {c[0]} | {c[1]} |\n'
    mwh.send(markdown_msg, channel=channel)