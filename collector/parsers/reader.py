import requests


def website_content(url):
    """
    Get website contents

    :return: given website html code
    """
    # headers = requests.utils.default_headers()
    # headers.update({
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
    #     'From': 'http://rozklady.mpk.krakow.pl'
    # })
    # cookie = {
    #     'ROZKLADY_WIZYTA': '20',
    #     'ROZKLADY_WIDTH': '1920',
    #     'ROZKLADY_JEZYK': 'PL',
    #     '__utma': '174679166.1956832196.1504264753.1504264753.1504264753.1',
    #     '__utmz': '174679166.1504264753.1.1.utmcsr = google | utmccn = (organic) | utmcmd = organic | utmctr = (not % 20provided)',
    #     'ROZKLADY_OSTATNIA': '1505207038',
    #     'ROZKLADY_LWT': '142__2__50'
    # }
    # first request - to get cookies
    r_first = requests.get(url)
    r = requests.get(url, cookies=r_first.cookies)
    return r.text
