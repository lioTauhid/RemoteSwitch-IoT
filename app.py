from time import sleep

from listen_firebase import runFirebaseSyncer
from utils import is_internet_alive


def automateInternetConnection():

    if is_internet_alive():
        runFirebaseSyncer()
    else:
        sleep(5)
        automateInternetConnection()


if __name__ == '__main__':
    automateInternetConnection()
