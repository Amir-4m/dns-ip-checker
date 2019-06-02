import requests

def domain_updater(domain, ip):
    """
    zone_id and dns record needed
    :param domain:
    :param ip:
    :return:
    """
    url = "https://api.cloudflare.com/client/v4/zones/023e105f4ecef8ad9ca31a8372d0c353/dns_records/372e67954025e0ba6aaa6d586b9e0b59"

    headers = {
        'X-Auth-Email': 'user@example.com',
        'X-Auth-Key': 'c2547eb745079dac9320b638f5e225cf483cc5cfdda41',
        'Content-Type': 'application/json',
    }

    data = f'{"type":"A","name":"{domain}","content":"127.0.0.1","ttl":{},"proxied":false}'

    try:
        req = requests.put(url, headers=headers, data=data)

        if req.status_code != 200:
            print(req.text)
            raise Exception('Recieved non 200 response while sending response to Cloudflare.')
        return 'ip set'

    except requests.exceptions.RequestException as e:
        print(e)
