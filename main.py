#!/usr/bin/env python3

# adopted from https://github.com/CloudburstSys/PonyPixel :)
# Warcrimes baby

import math
from traceback import print_exc
from typing import Optional, Dict, List, Union, Tuple

import numpy
from tqdm import tqdm
import time
import json

import requests
from bs4 import BeautifulSoup

import urllib
from io import BytesIO
from websocket import create_connection
from websocket import WebSocketConnectionClosedException
from PIL import ImageColor
from PIL import Image
import numpy as np
import random

import os

from main_vars import *
from main_utils import *
from buckets import *
import bot_logger 

######## 
VERSION = "0.7.0"

# config
CURRENT_CANVASES = [0,1,2,3,4,5]
template_offset = (500, 0)
modeSetPixels = True

######## 
global start_time, pixels_placed_count, template_size
start_time = time.time()
pixels_placed_count = 0
template_size = (0,0)
rgb_colors_array = []

## load logger
global log
log = bot_logger.setupLogger(consolelevel="debug", enableLogFile=True)
##

max_x = int(max(xoffset+xsize for xoffset, xsize in zip(CANVAS_XOFFSET, CANVAS_XSIZE)))
max_y = int(max(yoffset+ysize for yoffset, ysize in zip(CANVAS_YOFFSET, CANVAS_YSIZE)))
currentData = np.zeros([max_x, max_y, 4], dtype=np.uint8) # should hold current state of canvas at all times


def init_rgb_colors_array(ref_color_map):
    global rgb_colors_array
    
    # generate array of available rgb colors we can use
    for color_hex, color_index in ref_color_map.items():
        rgb_array = ImageColor.getcolor(color_hex, "RGBA")
        rgb_colors_array.append(rgb_array)

init_rgb_colors_array(ref_color_map=COLOR_MAP_FULL)

def image_to_npy(img):
    return np.asarray(img).transpose((1, 0, 2))


#"https://github.com/r-ainbowroad/2023-minimap/blob/main/templates/mlp" 

rPlaceTemplateBaseUrl = "https://media.githubusercontent.com/media/r-ainbowroad/2023-minimap/main/templates/mlp" 

def getRPlaceTemplateUrl(ttype):
    return f'{rPlaceTemplateBaseUrl}/{ttype}.png'


rPlaceTemplateNames = []
rPlaceTemplates = {}
def addRPlaceTemplate(templateName, options):
    rPlaceTemplates[templateName] = {
        'canvasUrl': getRPlaceTemplateUrl("canvas"),
        'botUrl'   : getRPlaceTemplateUrl("bot" ) if options['bot' ] else None,
        'maskUrl'  : getRPlaceTemplateUrl("mask") if options['mask'] else None,
    }
    rPlaceTemplateNames.append(templateName)


addRPlaceTemplate("mlp"         , {'bot': False, 'mask': False}) ## TODO False for the time being


# globals
rPlaceTemplateName: Optional[str] = None
rPlaceTemplate: Optional[dict] = None
maskData: Optional[np.ndarray] = None
templateData: Optional[np.ndarray] = None
rPlaceMask: Optional[np.ndarray] = None

def setRPlaceTemplate(templateName):
    global rPlaceTemplateName
    global rPlaceTemplate
    template = rPlaceTemplates.get(templateName, None)
    if template is None:
        log.warning("Invalid /r/place template name:", templateName)
        log.warning(f"Must be one of {rPlaceTemplates.keys()}")
        return
    
    rPlaceTemplateName = templateName
    rPlaceTemplate = template

def enlargenImage(im, offset):
    # basically a botch function to enlargen the size of the template image to that of a full potential board. 
    ### MODE 1 ### (half of 1 and 4)

    full_transp_im = Image.new("RGBA", (max_x, max_y), (0,0,0,0))
    x_pos = offset[0]
    y_pos = offset[1]

    full_transp_im.paste(im, (x_pos, y_pos))
    # full_transp_im.show()

    return full_transp_im

# Fetch template, returns a Promise<Uint8Array>, on error returns the response object
def fetchTemplate(url):
    # return unsignedInt8Array[W, H, C] of the URL
    response = requests.get(url)
    # im = urllib.request.urlopen(f'{url}?t={time.time()}').read()# load raw file
    # print(type(im))
    im = BytesIO(response.content)
    im = Image.open(im)

    ### TODO Currently checks template for different size from prev, if so quits bot to avoid template-canvas mismatch
    global template_size
    if template_size == (0,0):
        # initial update
        template_size = im.size # udpate size
    elif template_size != im.size and template_offset != (0,0):
        log.critical("Template size changed. Exiting bot...")
        bot_exit(40)
    elif template_size != im.size:
        log.warning("Template size changed but not likely to affect alignment. ")
    
    im = im.convert("RGBA")

    im = enlargenImage(im, offset=template_offset)
    # print(im.size)
    im.save("template_test.png")
    
    im = image_to_npy(im)# raw -> intMatrix([W, H, (RGBA)])

    assert im.dtype == 'uint8', f'got dtype {im.dtype}, expected uint8'
    assert im.shape[2] == 4, f'got {im.shape[2]} color channels, expected 4 (RGBA)'
    return im

def updateTemplate():
    global templateData
    global maskData
    rPlaceTemplateUrl = rPlaceTemplate['botUrl'] if rPlaceTemplate['botUrl'] is not None else rPlaceTemplate['canvasUrl']
    
    try:
        templateData = fetchTemplate(rPlaceTemplateUrl)# [W, H, (RGBA)]
    except Exception as err:
        print("Error updating template")
        raise err
    
    # Also update mask if needed
    maskData = np.zeros(templateData.shape, dtype=numpy.uint8)
    if rPlaceTemplate['maskUrl'] is not None:
        try:
            submask = fetchTemplate(rPlaceTemplate['maskUrl'])# [W, H, (RGBA)]
            maskData[:submask.shape[0], :submask.shape[1]] = submask
            
            #loadMask()
        except Exception as err:
            print_exc()
            print("Error updating mask:\n", err)

def visualizeDiff(diff):
    blank_white = Image.new("RGBA", (max_x, max_y), (255,255,255,255))

    for x,y in diff:
        blank_white.putpixel((x, y), (255, 0, 0, 255)) # ff0000

    blank_white.show()

def getDiff(currentData, templateData):

    ## the image vis is flipped 90 deg
    # current_img = Image.fromarray(currentData, "RGBA")
    # current_img.show()

    # template_img = Image.fromarray(templateData, "RGBA")
    # template_img.show()

    # print(currentData.shape, templateData.shape)

    assert currentData.shape == templateData.shape, f'got {currentData.shape} and {templateData.shape} for currentData and templateData shapes'
    assert currentData.shape[2] == 4, f'got {currentData.shape[2]} color channels, expected 4'
    # [W, H, (RGBA)], [W, H, (RGBA)]
    diff = []

    # obtain opaque pixels in template
    opaque_coord = np.array(np.where(templateData[:, :, 3] == 255))
    # print(opaque_coord.shape)
    
    for i in range(opaque_coord.shape[1]):
        x = opaque_coord[0][i]
        y = opaque_coord[1][i]

        curr_pixel = currentData[x, y]# [R,G,B,A]
        temp_pixel = templateData[x, y]# [R,G,B,A]
        opacity = temp_pixel[3]
        if opacity == 0.0:
            continue
        if np.not_equal(curr_pixel[:3], temp_pixel[:3]).any():
            # print(curr_pixel[:3], temp_pixel[:3], x, y)
            diff.append([x, y])

    # visualizeDiff(diff) # for visualizing the error pixels, error pixels are marked in red. 
    
    log.info(f'Total Damage: {len(diff) / (templateData[:, :, 3] != 0.0).sum():.1%} | {len(diff)}/{(templateData[:, :, 3] != 0.0).sum()}')
    return diff

def selectRandomPixel(diff):
    if rPlaceTemplate['maskUrl'] is None or maskData is None:
        pixel = random.choice(diff)
    else:
        pixel = selectRandomPixelWeighted(diff)
    
    (x, y) = pixel
    return x, y

###########################

class CLIBotConfig:
    # I guess this is just a config class for ease of access
    username = None
    password = None
    session_token = None
    template = "mlp"
    modeSetPixels = True

    proxy = None
    duration = None

    authmethod = "token"

class Placer:
    REDDIT_URL = "https://www.reddit.com"
    LOGIN_URL = REDDIT_URL + "/login"
    INITIAL_HEADERS = {
        "accept"            :
            "*/*",
        "accept-encoding"   :
            "gzip, deflate, br",
        "accept-language"   :
            "en-US,en;q=0.9",
        "content-type"      :
            "application/x-www-form-urlencoded",
        "origin"            :
            REDDIT_URL,
        "sec-ch-ua"         :
            '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile"  :
            "?0",
        "sec-ch-ua-platform":
            '"Windows"',
        "sec-fetch-dest"    :
            "empty",
        "sec-fetch-mode"    :
            "cors",
        "sec-fetch-site"    :
            "same-origin",
        "user-agent"        :
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
    }
    
    def __init__(self, modeSetPixels):
        self.client = requests.session()
        self.client.headers.update(self.INITIAL_HEADERS)
        
        self.token = None

        self.modeSetPixels = modeSetPixels
    
    def login(self, username: str, password: str):
        # get the csrf token
        r = self.client.get(self.LOGIN_URL)
        time.sleep(1)
        
        login_get_soup = BeautifulSoup(r.content, "html.parser")
        csrf_token = login_get_soup.find("input", {"name": "csrf_token"})["value"]
        
        # log.debug(csrf_token)
        
        # authenticate
        # log.debug(username + ", " + password)

        log.info(f"Logging in with username: {username} ...")

        data = {"username":username,
                "password":password,
                "dest":self.REDDIT_URL,
                "csrf_token":csrf_token
                }
        # log.debug(data)
        r = self.client.post(self.LOGIN_URL, data=data)
        time.sleep(1)
        
        log.info("LOGIN-RESPONSE: " + str(r.content))
        assert r.status_code == 200
        
        # get the new access token
        r = self.client.get(self.REDDIT_URL)
        data_str = BeautifulSoup(r.content, features="html5lib").find(
            "script", {
                "id": "data"
            }).contents[0][len("window.__r = "):-1]
        data = json.loads(data_str)
        self.token = data["user"]["session"]["accessToken"]

        log.debug("TOKEN: " + str(self.token))

    def login_token(self, session_token: str):
        # log.debug(session_token)
        self.token = session_token
    
    def get_board(self):
        log.info("Getting r/place current status...")

        boardimg = [None, None, None, None, None, None]
        ws = create_connection("wss://gql-realtime-2.reddit.com/query", origin="https://garlic-bread.reddit.com")  # works
        
        # initialization message
        # log.info(self.token)
        ws.send(
            json.dumps({
                "type"   : "connection_init",
                "payload": {
                    "Authorization": "Bearer " + str(self.token)
                },
            }))
        ws.recv()
        
        # start message 
        ws.send(
            json.dumps({
                "id"     : "1",
                "type"   : "start",
                "payload": {
                    "variables"    : {
                        "input": {
                            "channel": {
                                "teamOwner": "GARLICBREAD",
                                "category" : "CONFIG",
                            }
                        }
                    },
                    "extensions"   : {},
                    "operationName":
                        "configuration",
                    "query"        :
                        "subscription configuration($input: SubscribeInput!) {  subscribe(input: $input) {    id    ... on BasicMessage {      data {        __typename        ... on ConfigurationMessageData {          colorPalette {            colors {              hex              index              __typename            }            __typename          }          canvasConfigurations {            index            dx            dy            __typename          }          activeZone {            topLeft {              x              y              __typename            }            bottomRight {              x              y              __typename            }            __typename          }          canvasWidth          canvasHeight          adminConfiguration {            maxAllowedCircles            maxUsersPerAdminBan            __typename          }          __typename        }      }      __typename    }    __typename  }}",
                },
            }))
        ws.recv()

        color_configured = False
        # configure colors
        while not color_configured:
            temp = json.loads(ws.recv())
            if temp["type"] == "data":
                msg = temp["payload"]["data"]["subscribe"]
                if msg["data"]["__typename"] == "ConfigurationMessageData":
                    colors = msg["data"]["colorPalette"]["colors"]
                    global rgb_colors_array
                    if len(colors) != len(rgb_colors_array):
                        global COLOR_MAP
                        current_palette_hexes = [a["hex"] + "FF" for a in colors]
                        COLOR_MAP = {key: COLOR_MAP_FULL[key] for key in current_palette_hexes if key in COLOR_MAP_FULL}

                        # hacky?
                        rgb_colors_array = []
                        init_rgb_colors_array(ref_color_map=COLOR_MAP)
                        log.info(f"Color palette is incorrect. Palette updated to current {len(COLOR_MAP)} available colors.")
                    else:
                        log.debug("Color palette is correct.")
                    
                    color_configured = True


        ### CANVASES ###
        canvas_query = "subscription replace($input: SubscribeInput!) {  subscribe(input: $input) {    id    ... on BasicMessage {      data {        __typename        ... on FullFrameMessageData {          __typename          name          timestamp        }        ... on DiffFrameMessageData {          __typename          name          currentTimestamp          previousTimestamp        }      }      __typename    }    __typename  }}"
        message_id = 1

        # iteration baby
        for c in CURRENT_CANVASES:
            message_id += 1
            ws_msg = json.dumps({
                "id"     : str(message_id),
                "type"   : "start",
                "payload": {
                    "variables"    : {
                        "input": {
                            "channel": {
                                "teamOwner": "GARLICBREAD",
                                "category" : "CANVAS",
                                "tag"      : str(c),
                            }
                        }
                    },
                    "extensions"   : {},
                    "operationName": "replace",
                    "query"        : canvas_query,
                },
            })

            ws.send(ws_msg)
        
            while boardimg[c] == None:
                temp = json.loads(ws.recv())
                if temp["type"] == "data":
                    msg = temp["payload"]["data"]["subscribe"]
                    if msg["data"]["__typename"] == "FullFrameMessageData":
                        # print("Got Canvas {}: {}".format(c, msg["data"]["name"]))
                        log.debug(f"Got Canvas {c}.")

                        boardimg[c] = BytesIO(urllib.request.urlopen(msg["data"]["name"]).read())
                        break

        log.info("Canvases obtained.")
        ws.close()
                
        return boardimg
    
    def place_tile(self, canvas: int, x: int, y: int, color: int):
        if not self.token:
            # this happened once, so here's something to catch it.
            log.critical("self.token is None.")
            bot_exit(20)

        rl_mode = 0 # hacky method of telling external code whether pixel placement is successful

        headers = self.INITIAL_HEADERS.copy()
        headers.update({
            "apollographql-client-name"   : "garlic-bread",
            "apollographql-client-version": "0.0.1",
            "content-type"                : "application/json",
            "origin"                      : "https://garlic-bread.reddit.com",
            "referer"                     : "https://garlic-bread.reddit.com/",
            "sec-fetch-site"              : "same-site",
            "authorization"               : "Bearer " + str(self.token)
        })

        # da set pixel post
        r = requests.post("https://gql-realtime-2.reddit.com/query",
                          json={
                              "operationName": "setPixel",
                              "query"        : SET_PIXEL_QUERY,
                              "variables"    : {
                                  "input": {
                                      "PixelMessageData": {
                                          "canvasIndex": canvas,
                                          "colorIndex" : color,
                                          "coordinate" : {
                                              "x": x, 
                                              "y": y
                                          }
                                      },
                                      "actionName"      : "r/replace:set_pixel"
                                  }
                              }
                          },
                          headers=headers)
        
        if r.status_code != 200:
            log.critical("Pixel placement status code not 200: " + str(r.status_code))
            bot_exit(30)

        try:
            if r.json()["data"] is None:
                try:
                    waitTimems = math.floor(
                        r.json()["errors"][0]["extensions"]["nextAvailablePixelTs"])
                    rl_mode = 1
                except IndexError:
                    waitTimems = 10000
                    rl_mode = 1
            else:
                waitTimems = math.floor(r.json()["data"]["act"]["data"][0]["data"]
                                    ["nextAvailablePixelTimestamp"])
                log.info("Placing succeeded")

        except:
            if r.json()["errors"]:
                log.critical(r.json())
                log.critical("\nOther form of error encountered while setting pixel. Exiting...")
                log.critical("Likely due to a user auth error. Please obtain a new session token. ")
                bot_exit(2)
            else:
                log.critical("\nOther form of error encountered while setting pixel. No valid error response. Exiting...")
                bot_exit(31)
        
        return waitTimems / 1000, rl_mode


def AbsCoordToCanvasCoord(x: int, y: int):
    global CanvasIdMap
    if CanvasIdMap is None:
        max_x = int(max(xoffset+xsize for xoffset, xsize in zip(CANVAS_XOFFSET, CANVAS_XSIZE)))
        max_y = int(max(yoffset+ysize for yoffset, ysize in zip(CANVAS_YOFFSET, CANVAS_YSIZE)))
        CanvasIdMap = np.zeros([max_x, max_y], dtype=np.uint8)
        for canvas_id, xoffset, yoffset, xsize, ysize in zip(CANVAS_IDS, CANVAS_XOFFSET, CANVAS_YOFFSET, CANVAS_XSIZE, CANVAS_YSIZE):
            CanvasIdMap[xoffset:xoffset + xsize, yoffset:yoffset + ysize] = canvas_id
    
    canvas_id = int(CanvasIdMap[x, y])
    cx = x - CANVAS_XOFFSET[canvas_id]
    cy = y - CANVAS_YOFFSET[canvas_id]
    return int(cx), int(cy), canvas_id

def CanvasCoordToAbsCoord(cx: int, cy: int, canvas_id: int):
    x = cx + CANVAS_XOFFSET[canvas_id]
    y = cy + CANVAS_YOFFSET[canvas_id]
    return x, y

def AttemptPlacement(place: Placer, diffcords: Optional[List[Tuple[int, int]]] = None):

    if diffcords is None:
        # Find pixels that don't match template
        diffcords = getDiff(currentData, templateData) # list([x, y], ...)
    
    if len(diffcords):# if img doesn't perfectly match template
        # Pick mismatched pixel to modify
        x, y = selectRandomPixel(diffcords) # select random pixel?
        
        # Send request to correct pixel that doesn't match template
        cx, cy, canvas_id = AbsCoordToCanvasCoord(x, y)
        log.info(f"Actual Positions: ({cx}, {cy}), canvas {canvas_id}")
        log.info(f"Global Positions: ({x}, {y})")

        hex_color = rgb_to_hex(closest_color(templateData[x, y], rgb_colors_array)) # find closest colour in colour map

        if not place.modeSetPixels:
            log.warning("Pixel not placed due to debug mode.")

            return time.time() + random.uniform(12, 43) # increased ping interval

        else:
            timestampOfSafePlace, rl_mode = place.place_tile(int(canvas_id), cx, cy, int(COLOR_MAP[hex_color])) # and convert hex_color to color ID for request
            
            # add random delay after placing tile (to reduce chance of bot detection)
            #timestampOfSafePlace += random.uniform(5, 30)
            if rl_mode == 0:
                global pixels_placed_count
                # no rate limit
                timestampOfSafePlace += random.uniform(2,10)

                log.info(f"Placed Pixel '{COLOR_NAMES_MAP.get(hex_color, hex_color)}' at [{x-1500}, {y-1000}]. Can next place in {timestampOfSafePlace - time.time():.1f} seconds\n")
                pixels_placed_count += 1

            elif rl_mode == 1:
                # rate limited
                log.warning(f"Rate limited. Pixel not placed. Can next place in {timestampOfSafePlace - time.time():.1f} seconds\n")
            
            return timestampOfSafePlace
    
    return time.time() + random.uniform(5, 30)

def init_webclient(botConfig):
    place = Placer(modeSetPixels = botConfig.modeSetPixels)

    if botConfig.authmethod == "login":
        place.login(botConfig.username, botConfig.password)
    elif botConfig.authmethod == "token":
        place.login_token(botConfig.session_token)
        log.debug(f"Set token: {botConfig.session_token}")

    return place

def updateTemplateState(templateName: str):
    setRPlaceTemplate(templateName) # set current Template to "mlp" (the default)
    # python not async so must manually call updateTemplate() periodically
    updateTemplate()

def updateCanvasState(ids: Union[int, List[int]]):
    global currentData
    if type(ids) is int:
        ids = [ids]
    
    canvases = place.get_board()

    # load current state of canvas
    for canvas_id in ids:
        xoffset = CANVAS_XOFFSET[canvas_id]
        yoffset = CANVAS_YOFFSET[canvas_id]
        xsize   = CANVAS_XSIZE[canvas_id]
        ysize   = CANVAS_YSIZE[canvas_id]

        if canvases[canvas_id]:
            # print(canvas_id)
            canvas = image_to_npy(Image.open(canvases[canvas_id]).convert("RGBA"))# raw -> intMatrix([W, H, (RGBA)])\
        else:
            empty_img = Image.new(
                "RGBA", 
                (xsize, ysize), 
                (0,0,0,0)
            )
            canvas = image_to_npy(empty_img)

        currentData[xoffset:xoffset + xsize, yoffset:yoffset + ysize] = canvas
    
    return

def bot_exit(exitcode):
    # to gracefully exit this thing.
    uptime = get_time_passed(start_time)
    log.info(f"Exit code: {exitcode}")
    log.info(f"Uptime: {uptime}")
    log.info(f"Pixels placed: {pixels_placed_count}")

    exit(exitcode)



if __name__ == '__main__':
    """
    python main.py -p [username] [password] -t [token] -am token

    """
    # manual arg input
    test_args = []

    # initialisation from commandline
    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--plain", 
                        nargs=2, help=""
                        )
    parser.add_argument("-t", "--token", 
                        nargs=1, help="Specify session token."
                        )
    parser.add_argument("-px", "--proxy", 
                        nargs=1, help="Specify proxy server address. Not in use. "
                        )
    parser.add_argument("-dt", "--duration",
                        type=int, help="Add bot duration in seconds. Will exit after duration has passed. "
                        )
    parser.add_argument("-nsp", "--nosetpixels", 
                        action="store_true", help="(Flag) Disable pixel setting."
                        )
    parser.add_argument("-am", "--authmethod", 
                        nargs="?", default="token", 
                        help="Specify the authentication method: [token (default), login]"
                        )
    parser.add_argument("--template", nargs="?", 
                        default='mlp', 
                        help="Specify the reference template to be used. Can only be set to 'mlp' (default)"
                        ) 

    args = parser.parse_args(test_args) # manual debug mode
    args = parser.parse_args()

    cliBotConfig = CLIBotConfig()

    # print(args.plain)

    if args.plain is not None:
        cliBotConfig.username = args.plain[0]
        cliBotConfig.password = args.plain[1]

    if args.token is not None:
        cliBotConfig.session_token = args.token[0]
    
    if args.plain == None and args.token == None:
        # loading from logins.txt (TEMP SOUTION)
        # loads username, pw, and optionally, a token
        if os.path.exists("logins.txt"):
            # text file loading
            log.info(f'Auth args not provided, attempting loading from file.')

            with open("logins.txt", "r") as f:
                logins = f.readlines()

            logins_parsed = [login for login in logins if not login.startswith("#")] # remove comments. 

            login1 = logins_parsed[0]
            if len(login1) == 3:
                # token given as well
                cliBotConfig.username, cliBotConfig.password, cliBotConfig.session_token = login1.split(" ")
            else:
                cliBotConfig.username, cliBotConfig.password = login1.split(" ")[:2]

        else:
            log.critical("\a-------------------------------\nNO AUTHENTICATION CREDENTIALS PROVIDED.\nPlease provide login credentials.")
            bot_exit(21)

    # auth mode
    if cliBotConfig.session_token is None:
        args.authmethod = "login"
    cliBotConfig.authmethod = args.authmethod

    # template
    cliBotConfig.template = args.template

    ## DEBUG
    if args.nosetpixels:
        modeSetPixels = False
    cliBotConfig.modeSetPixels = modeSetPixels

    if not cliBotConfig.modeSetPixels:
        log.warning("DEBUG MODE. BOT WILL NOT SET PIXELS TO AVOID UNNECESSARY API CALLS.")
    ##

    cliBotConfig.duration = args.duration


    # hmmmmm
    botConfig = cliBotConfig

    place = init_webclient(botConfig)
    updateTemplateState(botConfig.template)
    
    timestampOfPlaceAttempt = 0
    time_to_wait = 0
    need_init = False

    while True:
        try:
            if need_init:
                # this is in place
                place = init_webclient(botConfig)
            
            # checks uptime, closes if exceeded
            if botConfig.duration != None:
                if time.time() - start_time + time_to_wait > botConfig.duration:
                    log.warning(f"\nSpecified duration of {botConfig.duration} seconds is up/will be up. Exiting...")
                    bot_exit(10)

            for _ in tqdm(range(math.ceil(time_to_wait)), desc='waiting'): # fancy progress bar while waiting 
                time.sleep(1)
            
            try:
                updateTemplate() #working
                updateCanvasState(CURRENT_CANVASES)
                timestampOfPlaceAttempt = AttemptPlacement(place)

            except WebSocketConnectionClosedException:
                log.critical("\aWebSocket connection refused. Auth issue.")
                bot_exit(1)
            
            time_to_wait = timestampOfPlaceAttempt - time.time()
            if time_to_wait > DAY:
                log.critical("\a-------------------------------\nBOT BANNED FROM R/PLACE\nPlease generate a new account and rerun.")
                bot_exit(0)
            
            time.sleep(random.uniform(3, 5))

        except KeyboardInterrupt:
            log.critical('\nKeyboardInterrupt: Exiting...')
            bot_exit(11)
            break

        except Exception as err:
            print("-------------------------------")
            print_exc() # print stack trace
            log.critical("-------------------------------\nNON-TERMINAL ERROR ENCOUNTERED\nBot is reviving. Please wait 15 seconds...")
            time.sleep(15)
            need_init = True