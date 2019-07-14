import os
import re


class PingCheck:
    __slots__ = ['input_string', 'is_ping', 'ip', 'time', 'success', 'domain']

    def __init__(self, input_string):
        self.input_string = input_string
        self.is_ping = False
        self.ip = None
        self.time = None
        self.success = 0
        self.domain = None
        self.ping()

    def ping(self):
        ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        is_ip = ip_pattern.match(self.input_string)

        if is_ip is None:
            self.domain = self.input_string
        else:
            self.ip = self.input_string
            self.domain = ''

        ping = os.popen(f'ping -c 6 -q -s 1 {self.input_string}').read()
        self.ip = ping.split('\n')[0].split()[2][1:-1]
        self.time = ping.split('\n')[-3].split()[-1].lstrip('time')
        self.success = 100.0 - float(ping.split('\n')[-3].split(',')[2].rstrip('% packet loss'))

        if self.success >= 60.0:
            self.is_ping = True