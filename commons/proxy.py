import random

# List of proxies
PROXY_LIST = [
    "http://173.208.213.170:15002",
    "http://173.208.150.242:15002",
    "http://173.208.239.10:15002",
    "http://173.208.136.2:15002"
]


def get_random_proxy():
    """
    Returns a random proxy from the PROXY_LIST
    """
    proxy = random.choice(PROXY_LIST)
    return {
        "http": proxy,
        "https": proxy
    }