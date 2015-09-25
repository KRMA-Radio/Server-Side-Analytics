from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from urllib.parse import urlencode
from Access import Access

session = FuturesSession(executor=ThreadPoolExecutor(max_workers=100))
__author__ = 'Isaac'


def hit_from_access(access: Access, tracking_id: str, client_id:str=None):
    if client_id is None:
        client_id = access.ip

    print(access.time)
    return send(tracking_id, client_id, hostname=access.host, page=access.page, title=access.page, ip=access.ip,
                referer=access.http_referer, user_agent=access.user_agent)


def send(tracking_id, client_id, hit_type="pageview", hostname: str=None, page: str=None, title: str=None, ip: str=None,
         referer: str=None, user_agent: str=None, queue_time: int=None):
    data = dict()
    data['v'] = 1
    data['tid'] = tracking_id
    data['cid'] = client_id

    data['t'] = hit_type
    if hostname is not None:
        data['dh='] = hostname
    if page is not None:
        data['dp'] = page
    if title is not None:
        data['dt'] = title
    if ip is not None:
        data['uip'] = ip
    if user_agent is not None:
        data['ua'] = user_agent
    if referer is not None:
        data['dr'] = referer
    if queue_time is not None:
        data['qt'] = queue_time

    return session.post("https://www.google-analytics.com/debug/collect?", data=urlencode(data))