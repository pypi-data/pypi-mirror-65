from typing import List
import os
import datetime
import traceback
import functools
import json
import socket
import requests


class SlackSender(object):

    def __init__(self, webhook_url: str, channel: str, user_mentions: List[str] = []):
        super(SlackSender, self).__init__()
        self.webhook_url = webhook_url
        self.channel = channel
        self.user_mentions = user_mentions
        self.dump = {
            "username": "Knock Knock",
            "channel": channel,
            "icon_emoji": ":clapper:",
        }
        self.flag_log = {
            "info":  ":flag_green: *{}!*",
            "warning": ":flag_yellow: *{}!*",
            "error": ":flag_red: *{}!*",
            "none": ":flag_red: *{}!* log_type must be info, warning, error"
        }
        self.flag_status = {
            'info': 'COMPLETE',
            'warning': 'WARNING',
            'error': 'ERROR',
            'none': 'WRONG_LOG_TYPE'
        }
        self.flag_start = False
        self.DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            host_name = socket.gethostname()
            func_name = func.__name__
            # Handling distributed training edge case.
            # In PyTorch, the launch of `torch.distributed.launch` sets up a RANK environment variable for each process.
            # This can be used to detect the master process.
            # See https://github.com/pytorch/pytorch/blob/master/torch/distributed/launch.py#L211
            # Except for errors, only the master process will send notifications.
            if 'RANK' in os.environ:
                master_process = (int(os.environ['RANK']) == 0)
                host_name += ' - RANK: %s' % os.environ['RANK']
            else:
                master_process = True
            log_type = 'info'
            if master_process and self.flag_start == False:
                self.flag_start = True
                contents = ['{} \t {}'.format(self.flag_log[log_type].format('INFO'), host_name),
                            '\t\t Function call: %s' % func_name,
                            '\t\t Starting date: %s' % start_time.strftime(self.DATE_FORMAT)]
                contents.append(' '.join(self.user_mentions))
                self.dump['text'] = '\n'.join(contents)
                self.dump['icon_emoji'] = ':clapper:'
                requests.post(self.webhook_url, json.dumps(self.dump))
            try:
                value = func(*args, **kwargs)
                if type(value) == dict:
                    if 'log_type' in value.keys():
                        log_type = value['log_type']
                        if log_type not in ['info', 'warning', 'error']:
                            log_type = 'none'
                        del value['log_type']
                if master_process:
                    end_time = datetime.datetime.now()
                    elapsed_time = (end_time - start_time).total_seconds()
                    elapsed_time = f'{int(elapsed_time//3600)} hours {int(elapsed_time%3600//60)} minutes {int(elapsed_time%3600%60)} seconds'
                    contents = ["{} \t {}".format(self.flag_log[log_type].format(self.flag_status[log_type]), host_name),
                                '\t\tFunction call: %s' % func_name,
                                '\t\tDatetime: {}\t:arrow_right:\t{}'.format(
                                    start_time.strftime(self.DATE_FORMAT), end_time.strftime(self.DATE_FORMAT)),
                                '\t\tDuration: %s' % str(elapsed_time)]

                    try:
                        str_value = ''
                        if type(value) == dict:
                            str_value += '\n'
                            for key, value in value.items():
                                str_value += '\t\t    {:15s}: {}\n'.format(
                                    str(key), value)
                        else:
                            str_value = str(value)
                        contents.append(
                            '\t\tMain call returned value: %s' % str_value)
                    except:
                        contents.append('Main call returned value: %s' %
                                        "ERROR - Couldn't str the returned value.")

                    contents.append(' '.join(self.user_mentions))
                    self.dump['text'] = '\n'.join(contents)
                    self.dump['icon_emoji'] = ':tada:'
                    requests.post(self.webhook_url, json.dumps(self.dump))

                return value

            except Exception as ex:
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                contents = ["Your training has crashed ☠️",
                            'Machine name: %s' % host_name,
                            'Main call: %s' % func_name,
                            'Starting date: %s' % start_time.strftime(
                                self.DATE_FORMAT),
                            'Crash date: %s' % end_time.strftime(
                                self.DATE_FORMAT),
                            'Crashed training duration: %s\n\n' % str(
                                elapsed_time),
                            "Here's the error:",
                            '%s\n\n' % ex,
                            "Traceback:",
                            '%s' % traceback.format_exc()]
                contents.append(' '.join(self.user_mentions))
                self.dump['text'] = '\n'.join(contents)
                self.dump['icon_emoji'] = ':skull_and_crossbones:'
                requests.post(webhook_url, json.dumps(self.dump))
                raise ex
        return wrapper
