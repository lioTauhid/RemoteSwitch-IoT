import json
from time import sleep
from getmac import get_mac_address as mac
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from config import Config
from gpiozero import LED


def initFirebase():
    credential = credentials.Certificate(Config.firebaseSdk)
    firebase_admin.initialize_app(credential, {
        'databaseURL': 'https://cloud-remote-switch-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })


def onOffLed(pin, value):
    if value == "on":
        pin.on()
    else:
        pin.off()


def updatePin(key, value):
    print(key, '\t', value)
    if key == "s1":
        s1 = LED(4)
        onOffLed(s1, value)
        print(value)
        return
    elif key == "s2":
        s2 = LED(17)
        onOffLed(s2, value)
        print(value)
        return
    elif key == "s3":
        s3 = LED(27)
        onOffLed(s3, value)
        print(value)
        return
    elif key == "s4":
        s4 = LED(22)
        onOffLed(s4, value)
        print(value)
        return


def listenSwitch(event):
    rootRef = db.reference("/")
    # print(event.path)  # relative to the reference, it seems
    # print(event.data)  # new data at /reference/event.path. None if deleted
    if event.path == "/":
        """update all pins"""
        for key, value in event.data.items():
            updatePin(key, value)
    else:
        """update a pin"""
        updatePin(event.path.replace('/', ''), event.data)

    dbData = rootRef.child("devices").child(mac()).get()
    with open(Config.configFile, "w") as config: json.dump(dbData, config)
    config.close()


def connectToFirebase():
    try:
        rootRef = db.reference("/")
        if rootRef.child(f"devices/{mac()}/s1").get() is None:
            """First time launch"""
            with open(Config.configFile) as file: data = json.load(file)
            # update gpio pin
            rootRef.child("devices").child(mac()).set(data)
        else:
            dbData = rootRef.child("devices").child(mac()).get()
            # update gpio pin
            with open(Config.configFile, "w") as config: json.dump(dbData, config)
            config.close()

        print("Firebase alive")
        rootRef.child(f"devices").child(mac()).listen(listenSwitch)
    except Exception as e:
        print(f"{e} connection failed, retrying!!!")
        sleep(5)
        connectToFirebase()


def runFirebaseSyncer():
    initFirebase()
    connectToFirebase()
