import logging
import subprocess

import requests

from undmainchain.const import GENESIS

log = logging.getLogger(__name__)


def run_shell(cmd):
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, shell=True,
        stderr=subprocess.PIPE, universal_newlines=True)

    log.debug(cmd)

    if result.returncode != 0:
        log.error(result.stdout)
        log.error(result.stderr)
        exit(1)

    return result.stdout


def get_height():
    r = requests.get('http://localhost:26660/status')
    d = r.json()

    height = int(d['result']['sync_info']['latest_block_height'])
    return height


def fetch_genesis(machine_d):
    target = machine_d['home'] / 'config/genesis.json'
    user = machine_d['und_user']

    r = requests.get(GENESIS)
    target.write_text(r.text)
    run_shell(f'chown {user}:{user} {str(target)}')
