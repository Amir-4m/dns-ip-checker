import subprocess
import re


class PingCheck:
    def __init__(self, input_string):
        self.input_string = input_string
        self.is_ping = False
        self.ip = None
        self.time = None
        self.success = None
        self.domain = None
        self.status = 0
        self.ping()

    def ping(self):
        ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        is_ip = ip_pattern.match(self.input_string)
        if is_ip is None:
            self.domain = self.input_string
        else:
            self.ip = self.input_string
            self.domain = 'You Entered IP'

        try:
            p = subprocess.check_output(f'ping -c 6 -s 1 -q {self.input_string}', shell=True)
            p = p.decode('utf-8')
            self.ip = p.split('\n')[0].split('(')[1][:-3]
            self.time = p.split('\n')[-3].split()[-1]
            self.success = 100 - float(p.split('\n')[-3].split(',')[2].rstrip('% packet loss'))

            if self.success >= 50.0:
                self.is_ping = True

        except Exception as e:
            self.success = 0
            self.status = str(e).split()[-1].rstrip('.')




# def ping_check(input_string):
#     ping = os.system(f'ping {input_string} -c 6 -s 1 > result.tmp')
#     result = open('result.tmp').read()
#
#     ip = result.split('\n')[0].split()[2][1:-1]
#     time = result.split('\n')[-3].split()[-1][:-2]
#     packet_lost = result.split('\n')[-3].split()[5][:-1]
#     statistics = result.split('\n')[-3].split()[0: 4]
#     logger.info(f"domain: {input_string} "
#                 f"ping_code: {ping}, ip: {ip}, time: {time}ms, "
#                 f"packet lost: {packet_lost}%, "
#                 f"statistics: {' '.join(statistics)}")
