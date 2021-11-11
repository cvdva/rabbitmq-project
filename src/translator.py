import pika, sys, os
import json
import src.init_queue


def check_translate(body):
    form = body['format']
    translations = []
    for line in translation_list:
        if form == line[0]:
            translations.append(line[1])
    return translations


def announce_listen(new_format, body):
    body['format'] = new_format



if __name__ == "__main__":
    translation_list = [('txt', 'csv'), ('txt', 'word'), ('word', 'txt')]
    body = {}
    body['format'] = 'txt'
    print(check_translate(body))