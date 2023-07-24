# misc
DAY = 86400
HOUR = 3600

# canvas chunk info, assumed correct. 
CANVAS_IDS     = [   0,    1,    2,    3,    4,    5]
CANVAS_XOFFSET = [   0, 1000, 2000,    0, 1000, 2000]
CANVAS_YOFFSET = [   0,    0,    0, 1000, 1000, 1000]
CANVAS_XSIZE   = [1000, 1000, 1000, 1000, 1000, 1000]
CANVAS_YSIZE   = [1000, 1000, 1000, 1000, 1000, 1000]
CanvasIdMap = None

SET_PIXEL_QUERY = \
    """mutation setPixel($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetUserCooldownResponseMessageData {\n            nextAvailablePixelTimestamp\n            __typename\n          }\n          ... on SetPixelResponseMessageData {\n            timestamp\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"""


# color
COLOR_MAP_FULL = {
    "#6D001AFF":  0,
    "#BE0039FF":  1,
    "#FF4500FF":  2,
    "#FFA800FF":  3,
    "#FFD635FF":  4,
    "#FFF8B8FF":  5,
    "#00A368FF":  6,
    "#00CC78FF":  7,
    "#7EED56FF":  8,
    "#00756FFF":  9,
    "#009EAAFF": 10,
    "#00CCC0FF": 11,
    "#2450A4FF": 12,
    "#3690EAFF": 13,
    "#51E9F4FF": 14,
    "#493AC1FF": 15,
    "#6A5CFFFF": 16,
    "#94B3FFFF": 17,
    "#811E9FFF": 18,
    "#B44AC0FF": 19,
    "#E4ABFFFF": 20,
    "#DE107FFF": 21,
    "#FF3881FF": 22,
    "#FF99AAFF": 23,
    "#6D482FFF": 24,
    "#9C6926FF": 25,
    "#FFB470FF": 26,
    "#000000FF": 27,
    "#515252FF": 28,
    "#898D90FF": 29,
    "#D4D7D9FF": 30,
    "#FFFFFFFF": 31,
    "#FFF34FFF": 32
}

COLOR_NAMES_MAP = {
    "#6D001AFF": 'Burgundy',
    "#BE0039FF": 'Dark Red',
    "#FF4500FF": 'Red',
    "#FFA800FF": 'Orange',
    "#FFD635FF": 'Yellow',
    "#FFF8B8FF": 'Pale Yellow',
    "#00A368FF": 'Dark Green',
    "#00CC78FF": 'Green',
    "#7EED56FF": 'Light Green',
    "#00756FFF": 'Dark Teal',
    "#009EAAFF": 'Teal',
    "#00CCC0FF": 'Light Teal',
    "#2450A4FF": 'Dark Blue',
    "#3690EAFF": 'Blue',
    "#51E9F4FF": 'Light Blue',
    "#493AC1FF": 'Indigo',
    "#6A5CFFFF": 'Periwinkle',
    "#94B3FFFF": 'Lavender',
    "#811E9FFF": 'Dark Purple',
    "#B44AC0FF": 'Purple',
    "#E4ABFFFF": 'Pale Purple',
    "#DE107FFF": 'Magenta',
    "#FF3881FF": 'Pink',
    "#FF99AAFF": 'Light Pink',
    "#6D482FFF": 'Dark Brown',
    "#9C6926FF": 'Brown',
    "#FFB470FF": 'Biege',
    "#000000FF": 'Black',
    "#515252FF": 'Dark Grey',
    "#898D90FF": 'Grey',
    "#D4D7D9FF": 'Light Grey',
    "#FFFFFFFF": 'White',
    "#FFF34FFF": 'this is a fucking hack and a half'
}