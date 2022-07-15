import asyncio
import configparser
import os
import sys
# import logging
# logging.basicConfig(level=logging.DEBUG)

import simpleobsws

config = configparser.ConfigParser()
home = os.path.expanduser("~")
config.read(os.path.join(home, ".obspycli.conf"))
passwd = config["DEFAULT"].get('password', os.environ.get("OBS_PASSWORD", ''))
port = config["DEFAULT"].get('port', '4455')
host = config["DEFAULT"].get('host', 'localhost')
parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False)
ws = simpleobsws.WebSocketClient(url = 'ws://{}:{}'.format(host, port),
                                 password = passwd,
                                 identification_parameters = parameters)

async def make_request(verb):
    await ws.connect()
    await ws.wait_until_identified()

    req = simpleobsws.Request(verb)
    ret = await ws.call(req)

    await ws.disconnect()
    return ret

def request(myloop, req):
    ret = myloop.run_until_complete(make_request(req))
    if ret.ok():
        return ret.responseData
    return None

loop = asyncio.get_event_loop_policy().get_event_loop()
if len(sys.argv) != 2:
    print("Run ./{} <command>".format(sys.argv[0]))
    print("commands can be:")
    print("  start_recording")
    print("  stop_recording")
    sys.exit(1)

commands = {
    'start_recording': 'StartRecord',
    'stop_recording': 'StopRecord',
}
command = sys.argv[1]
if command in commands:
    request(loop, commands[command])
else:
    print("Error command %s not implemented" % command)
    sys.exit(1)
