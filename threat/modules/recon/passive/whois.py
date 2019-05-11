from core.colors import color
import requests
def whois(target):
    for t in target:
        site = t.name.replace('http://','').replace('https://','')
        text = requests.get('http://api.hackertarget.com/whois/?q=' + site).text
        nping = str(text)
        if 'error' not in nping:
            print(color.custom(nping, white=True))
        else:
            print(color.red(' [-] Outbound Query Exception!'))