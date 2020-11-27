import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init()


def correct_url(url):
    print(url)
    return '.' in url


def get_parsed(response):
    data = response.content
    parser = 'html.parser'
    soup = BeautifulSoup(data, parser)
    tags = soup.find_all(['p', 'div', 'a', 'ul', 'ol', 'li',
                          'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                          'span'])
    s = ''
    for tag in tags:
        if tag.string is not None:
            if tag.name == "a":
                s += Fore.BLUE + tag.string + '\n'
                s += Style.RESET_ALL
            else:
                s += tag.string + '\n'
    return s


dir_for_files = sys.argv[1]
if not os.path.exists(dir_for_files):
    os.mkdir(dir_for_files)

history = deque()
cur_page = None

while (user_input := input()) != "exit":
    if os.path.exists(user_input):
        with open(user_input, 'r') as f:
            for line in f.readlines():
                print(line.strip())
        cur_page = user_input
    elif user_input == "back":
        if len(history) != 1:
            history.pop()
            print(history)
            with open(dir_for_files + '/' + history[-1], 'r') as f:
                for line in f.readlines():
                    print(line.strip())
    elif correct_url(user_input):
        headers = {'user-agent': 'Mozilla/5.0'}
        url = 'https://' + user_input
        response = requests.Session().get(url, headers=headers)
        if response.status_code != 404:
            text = get_parsed(response)
            print(text)
            file_name = user_input[:user_input.rfind('.')]
            with open(dir_for_files + "/" + file_name, 'w') as f:
                f.write(text)
            cur_page = file_name
        else:
            print("Error: Incorrect URL")
    else:
        print("Error: Incorrect URL")
    history.append(cur_page)
