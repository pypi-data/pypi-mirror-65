from urllib.request import Request, urlopen

def idl(url):
    return urlopen(url).read().decode(urlopen(url).headers.get_content_charset('utf-8'))
