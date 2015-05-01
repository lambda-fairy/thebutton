#!/usr/bin/env python3

import asyncio
from functools import partial
import json
import re
import websockets

import praw
praw.Config.API_PATHS['press_button'] = 'api/press_button'

import warnings
warnings.simplefilter('ignore', ResourceWarning)


USER_AGENT = 'Button Presser by /u/lfairy'

TARGET = 1


@asyncio.coroutine
def the_button(r, url):
    socket = yield from websockets.connect(url)
    minimum = 60
    while True:
        payload = yield from next_tick(socket.recv)
        seconds = int(payload['seconds_left'])
        tick_time = payload['now_str']
        tick_mac = payload['tick_mac']
        minimum = min(minimum, seconds)
        print('[{}] tick {} (min {})'.format(tick_time, seconds, minimum))
        if seconds == TARGET:
            click(r, seconds, tick_time, tick_mac)


@asyncio.coroutine
def next_tick(recv):
    while True:
        frame = yield from recv()
        message = json.loads(frame)
        payload, message_type = message['payload'], message['type']
        if message_type == 'ticking':
            return payload


def discover_websocket_url(r):
    page = r.request('https://www.reddit.com/r/thebutton/').text
    return re.search('wss://[^"]+', page).group(0)


def click(r, seconds, tick_time, tick_mac):
    response = r.request(r.config['press_button'], data={
        'seconds': seconds,
        'prev_seconds': seconds,
        'tick_time': tick_time,
        'tick_mac': tick_mac,
        'r': 'thebutton',
        })
    print(response)
    raise SystemExit('Clicked at {}'.format(seconds))


if __name__ == '__main__':
    print('Logging in...')
    r = praw.Reddit(user_agent=USER_AGENT)
    r.login()
    print('Requesting socket token...')
    url = discover_websocket_url(r)
    print('Connecting to {}...'.format(url))
    try:
        asyncio.get_event_loop().run_until_complete(the_button(r, url))
    except KeyboardInterrupt:
        pass
