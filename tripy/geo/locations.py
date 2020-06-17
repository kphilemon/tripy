KUALA_LUMPUR = 0
JAKARTA = 1
BANGKOK = 2
TAIPEI = 3
HONG_KONG = 4
TOKYO = 5
BEIJING = 6
SEOUL = 7

INDEX_BY_NAME = {
    'KualaLumpur': KUALA_LUMPUR,
    'Jakarta': JAKARTA,
    'Bangkok': BANGKOK,
    'Taipei': TAIPEI,
    'HongKong': HONG_KONG,
    'Tokyo': TOKYO,
    'Beijing': BEIJING,
    'Seoul': SEOUL
}

NAME_BY_INDEX = {
    KUALA_LUMPUR: 'KualaLumpur',
    JAKARTA: 'Jakarta',
    BANGKOK: 'Bangkok',
    TAIPEI: 'Taipei',
    HONG_KONG: 'HongKong',
    TOKYO: 'Tokyo',
    BEIJING: 'Beijing',
    SEOUL: 'Seoul'
}

COORDINATES_BY_INDEX = {
    KUALA_LUMPUR: (3.15972, 101.7),
    JAKARTA: (-6.16667, 106.8),
    BANGKOK: (13.75, 100.51667),
    TAIPEI: (25.03333, 121.63333),
    HONG_KONG: (22.27833, 114.15861),
    TOKYO: (35.6652065, 139.7263785),
    BEIJING: (39.905, 116.39139),
    SEOUL: (37.58333, 127)
}

ALL_LOCATIONS = [KUALA_LUMPUR, JAKARTA, BANGKOK, TAIPEI, HONG_KONG, TOKYO, BEIJING, SEOUL]


def indices_to_names(*args: int, sep: str = ', ') -> str:
    names = [NAME_BY_INDEX[i] for i in args if i in NAME_BY_INDEX]
    return sep.join(names)
