import json
with open('network_config.json') as network_file:
    data = json.load(network_file)

#connect to network defined in network_config.json file if WLAN is not connected
def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...\n')
        sta_if.active(True)
        sta_if.connect(data['SSID'], data['password'])
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def no_debug():
    import esp
    esp.osdebug(None)

no_debug()
connect()