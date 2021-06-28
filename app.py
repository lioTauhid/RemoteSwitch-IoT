from firebase_admin import db
import firebase_admin
from firebase_admin import credentials

from config import Config


def initFirebase():
    credential = credentials.Certificate(Config.firebaseSdk)
    firebase_admin.initialize_app(credential, {
        'databaseURL': 'https://cloud-remote-switch-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })


if __name__ == '__main__':
    initFirebase()

    rootRef = db.reference("/")
    rootRef.child("liot").set("ttt")
