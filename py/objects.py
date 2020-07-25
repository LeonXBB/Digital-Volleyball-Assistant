import os
import time
import traceback

import requests

import gfx
import py.core
from meta.app_config import *

# log_id + time + request type + request method + data + response text + event_id


class Log:
    type = ''
    # log = [] Moved to self.__init__
    array_file = ''
    current_id = -1

    def __init__(self, log_name, mode='NEW', save_to_file=True):

        self.log = []
        self.deep_log = []

        self.name = log_name
        self.save_to_file = save_to_file

        if save_to_file:
            if mode == 'NEW':
                f = open(os.getcwd() + '/logs/' + self.name + '.txt', 'w+', encoding='utf-8')
                f.close()
            self.array_file = os.getcwd() + '/logs/' + self.name + '.txt'

    def add(self, data, caller='', mode='NEW'):

        self.current_id += 1

        if mode == 'NEW':
            self.log.append(str(self.current_id) + str(data))

            if self.save_to_file:
                f = open(self.array_file, 'a', encoding='utf-8')
                f.write(str(self.current_id) + str(data) + '\n')
                f.close()

            caller.id = self.current_id

        else:
            self.log.append(str(self.current_id) + str(data)) # self.log.append(data)

    def deep_add(self, __object__):

        self.deep_log.append(__object__)

    def get(self, indexes, values, detailed=False, backwards=False):

        if type(indexes) != list: indexes = [indexes]
        if type(values) != list: values = [values]

        range_indexes = [0, len(self.log), 1]

        if backwards and len(self.log) > 1:
            range_indexes = [len(self.log) - 1, -len(self.log) - 1, -1]

        for i in range(range_indexes[0], range_indexes[1], range_indexes[2]):
            for index in indexes:
                for value in values:
                    if not detailed:
                        if self.log[i].split('#')[index] == value:
                            return {"exists": True, "id": i, "record": self.log[i]}
                    else:
                        if value in str(self.log[i].split('#')[index]):
                            return {"exists": True, "id": i, "record": self.log[i]}

        return {"exists": False, "id": None, "record": None}

    def get_all(self, indexes, values, detailed=False):

        if type(indexes) != list: indexes = [indexes]
        if type(values) != list: values = [values]

        return_list = []

        for i in range(len(self.log)):
            for index in indexes:
                for value in values:
                    if not detailed:
                        if self.log[i].split('#')[index] == value:
                            return_list.append([i, self.log[i]])
                    else:
                        if value in str(self.log[i].split('#')[index]):
                            return_list.append([i, self.log[i]])

        return return_list

    def delete(self):

        from DVA import logs

        logs.pop(self)
        if self.save_to_file:
            os.remove(os.getcwd() + '/' + self.name)


class Request:
    id = 0
    # data = [] Moved to self.__init__
    request_time = 0
    type = ''
    event_id = 0
    request_method = ''
    request_body = ''
    reply_body = ''

    no_internet = False

    def __init__(self, data, mode='NEW'):  # data = (type, event_id, (vars))

        from DVA import logs
        
        from meta.localization import internet_requests

        if mode == 'RESTORED':
            variables = ['id', 'request_time', 'type', 'request_method', 'request_body', 'reply_body', 'event_id']
            for i in range(len(variables)):
                setattr(self, variables[i], data[i])
            logs[1].add(str(data[0]) + self.__dir__(), mode='RESTORED')
            logs[1].deep_add(self)

        else:

            self.data = data
            self.request_time = time.time()
            self.type = data[0]
            self.event_id = data[1]

            self.send()

            if self.no_internet is False:
                self.process()
            else:
                if no_internet_method == 'popup':
                    i = gfx.frontend.PopUpWindow()
                    i.show_pop_up(internet_requests[language_code][0])
                elif no_internet_method == 'loop': #TODO actually you need to change requests' code for this
                    #to work (they currently won't proceed if there's no Internet)
                    while self.no_internet != True:
                        self.send()
                        if self.no_internet is False: self.process()

            logs[1].add(self.__dir__(), self)

    def send(self):

        request_file = ''

        address = os.getcwd()
        try:
            address = address.split('\\')
            string = ''
            for element in address:
                string += (element + '/')
            address = string[:-1]
        except:
            pass

        try:
            with open(address + '/py/requests/' + self.type + '__init__.py', encoding='utf-8') as f:
                request_file = request_file + f.read()
            f.close()
            exec(request_file)
            self.no_internet = False
        except:
            self.no_internet = True

    def process(self):

        import DVA

        from meta.localization import internet_requests

        process_file = ''

        address = os.getcwd()
        try:
            address = address.split('\\')
            string = ''
            for element in address:
                string += (element + '/')
            address = string[:-1]
        except:
            pass

        with open(address + '/py/requests/' + self.type + '__process__.py', encoding='utf-8') as f:
            process_file = process_file + f.read()
        f.close()
        exec(process_file)

    def __dir__(self):
        return ('#' + str(self.request_time) + '#' + str(self.type) + '#' + str(self.request_method) + '#' +
                str(self.request_body) + '#' + str(self.reply_body) + '#' + str(self.event_id))
