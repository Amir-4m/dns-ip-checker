from .models import DomainList
import socket
import os


def ping_and_log():
    """
    ping the domains and log the result as log.txt
    :return:
    """
    list_of_domains_to_ping = [objc.domain for objc in DomainList.objects.all()]

    for domain in list_of_domains_to_ping:
        ping = os.system("ping -c 4 " + domain)
        result = 'Successful' if ping == 0 else 'Unsuccessful'
        with open('domain_checker/log.txt', 'a+') as file:
            try:
                file.write(f"{domain} ip: {socket.gethostbyname(domain)} -------------- result: {result}\n")
            except socket.gaierror:
                file.write(f"{domain} ip: Temporary failure in name resolution -------------- result: {result}\n")
