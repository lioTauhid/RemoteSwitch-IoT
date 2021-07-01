from pathlib import Path


class Config:
    currentPath = f'{Path.home()}/PycharmProjects/RemoteSwitch-IoT/'

    firebaseSdk = f"{currentPath}firebase_admin_sdk.json"
    configFile = f"{currentPath}config.json"
