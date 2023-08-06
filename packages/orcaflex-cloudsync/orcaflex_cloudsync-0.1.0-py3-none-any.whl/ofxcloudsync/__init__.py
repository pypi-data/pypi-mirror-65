import os

import yaml
from appdirs import AppDirs

dirs = AppDirs("ofx-cloudsync", "AgileTek")

SYNC_OFX = os.path.join(dirs.user_data_dir, "sync.ofx")
def load_sync_ofx():
    if os.path.exists(SYNC_OFX):
        with open(SYNC_OFX, "r") as ymlfile:
            return yaml.safe_load(ymlfile)
    else:
        return None


def write_sync_ofx(data):
    with open(SYNC_OFX, "w") as wf:
        yaml.dump(data, wf)