#+
# Example WebSocket server, intended to be invoked via ASGI.
# See accompanying README for an explanation.
#
# Copyright 2022 by Lawrence D'Oliveiro <ldo@geek-central.gen.nz>. This
# script is licensed CC0
# <https://creativecommons.org/publicdomain/zero/1.0/>; do with it
# what you will.
#-

import sys
import os
import enum
import socket
import subprocess
import asyncio
import logging

LOGGING_NAME = "ping_server"
  # identifies my messages in the logging module

class WEBSOCK_CLOSE(enum.IntEnum) :
    "some useful WebSocket codes to use on connection close."
    # codes come from RFC6455 <https://www.rfc-editor.org/rfc/rfc6455>
    NORMAL = 1000
    PROTOCOL_ERROR = 1002
    DATA_ERROR = 1003
    WTF = 1011 # Weird Technical Failure
#end WEBSOCK_CLOSE

SUPPORTED_PROTOCOL = "pingu.example.com"

def get_logger() :
    logger = logging.getLogger(LOGGING_NAME)
    try :
        loglevel = int(os.getenv("LOGLEVEL", ""))
        if loglevel < 0 :
            raise ValueError("invalid loglevel")
        #end if
    except ValueError :
        loglevel = None
    #end try
    if loglevel != None :
        logger.setLevel(loglevel)
    #end if
    if not logger.hasHandlers() :
        # uvicorn CLI command seems to quietly ignore my log messages,
        # so I insert my own logging setup to get around this.
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setFormatter(logging.Formatter(fmt = "%(levelname)-8s: %(message)s"))
        logger.addHandler(stderr_handler)
        logger.propagate = False
    #end if
    return \
        logger
#end get_logger

async def ping(scope, receive, send) :
    assert scope["type"] == "websocket" # avoid accepting lifespan events
    logger = get_logger()
    logger.debug("connection scope = %s" % repr(scope))
    while True :
        event = await receive()
        logger.debug("got event %s" % repr(event))
        if event["type"] == "websocket.connect" :
            if SUPPORTED_PROTOCOL in scope.get("subprotocols", []) :
                await send({"type" : "websocket.accept", "subprotocol" : SUPPORTED_PROTOCOL})
            else :
                await send({"type" : "websocket.close", "code" : WEBSOCK_CLOSE.PROTOCOL_ERROR})
            #end if
        elif event["type"] == "websocket.receive" :
            data = event.get("text")
            logger.info("request to ping %s" % repr(data))
            try :
                target = socket.gethostbyname(data)
                  # note: blocking call
            except (UnicodeError, OSError) as err :
                logger.info("error translating target %s: %s" % (repr(data), repr(err)))
                target = None
            #end try
            if target != None :
                child = await asyncio.create_subprocess_exec \
                  (
                    "ping", "-c", "10", "-i", "2", target,
                    stdin = subprocess.DEVNULL,
                    stdout = subprocess.PIPE
                  )
                nextline = asyncio.create_task(child.stdout.readline())
                child_done = asyncio.create_task(child.wait())
                while True :
                    await asyncio.wait \
                      (
                        [nextline, child_done],
                        return_when = asyncio.FIRST_COMPLETED
                      )
                    if nextline.done() :
                        failure = nextline.exception()
                        if failure != None :
                            result = str(failure)
                        else :
                            line = nextline.result()
                            result = line.decode()
                        #end if
                        await send({"type" : "websocket.send", "text" : result})
                        nextline = None
                    #end if
                    if child_done.done() :
                        sts = child.returncode
                        if sts != 0 :
                            logger.warning("child terminated with status %d" % sts)
                            closecode = WEBSOCK_CLOSE.WTF
                        else :
                            closecode = WEBSOCK_CLOSE.NORMAL
                        #end if
                        await send({"type" : "websocket.close", "code" : closecode})
                        break
                    #end if
                    assert nextline == None
                    nextline = asyncio.create_task(child.stdout.readline())
                #end while
            else :
                await send({"type" : "websocket.close", "code" : WEBSOCK_CLOSE.DATA_ERROR})
            #end if
        elif event["type"] == "websocket.disconnect" :
            logger.debug("disconnect code %d" % event["code"])
            break
        else :
            logger.warning("unexpected websocket event type %s" % repr(event["type"]))
        #end if
    #end while
#end ping
