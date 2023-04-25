import concurrent.futures
import requests
from bs4 import BeautifulSoup


def get_video_player_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
        'Accept': '*/*',
        'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://kodekloud.com',
        'Referer': 'https://kodekloud.com/courses/12-factor-app/',
        'Connection': 'keep-alive',
    }
    cookies = {
        'PHPSESSID': 'a59a6befed3fe8a8c7f074482d529d41',
    }

    r_ = requests.post(url=url, headers=headers, cookies=cookies)

    soup = BeautifulSoup(r_.content, "html.parser")
    href_list = []
    for a_tag in soup.find_all('a', href=True):
        if a_tag['href'].startswith('https://kodekloud.com/topic/'):
            href_list.append(a_tag['href'])

    vimeo_srcs = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_link = {executor.submit(get_vimeo_src, link, headers, cookies): link for link in href_list}
        for future in concurrent.futures.as_completed(future_to_link):
            link = future_to_link[future]
            try:
                vimeo_src = future.result()
                if vimeo_src:
                    vimeo_srcs.append(vimeo_src)
            except Exception as exc:
                print('%r generated an exception: %s' % (link, exc))
    print("Cantidad de videos del curso: ", str(len(vimeo_srcs)))

    return vimeo_srcs


def get_vimeo_src(link, headers, cookies):
    headers['Referer'] = link
    r_ = requests.get(url=link, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r_.content, "html.parser")
    vimeo_iframe = None
    try:
        vimeo_iframe = soup.find("iframe", src=lambda src: src and "player.vimeo.com" in src)
    except:
        pass
    if vimeo_iframe:
        vimeo_src = vimeo_iframe.get("src").split("?h")
        return vimeo_src
    return None
