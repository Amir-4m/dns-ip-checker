import json

import requests

from ip_updater.management.commands.configs import EMAIL, ZONE_ID, API_KEY


def domain_updater(domain, ip, dns_record):
    """
    :param domain:
    :param ip:
    :return:
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{dns_record}"

    headers = {
        'X-Auth-Email': EMAIL,
        'X-Auth-Key': API_KEY,
        'Content-Type': 'application/json',
    }

    data = {"type": "A", "name": domain, "content": ip, "ttl": 1, "proxied": False}

    try:
        req = requests.put(url, headers=headers, data=json.dumps(data))

        if req.status_code != 200:
            print(req.text)
            raise Exception('Recieved non 200 response while sending response to Cloudflare.')
        return (f"ip:{ip} set for {domain} successfully")

    except requests.exceptions.RequestException as error:
        print(error)
