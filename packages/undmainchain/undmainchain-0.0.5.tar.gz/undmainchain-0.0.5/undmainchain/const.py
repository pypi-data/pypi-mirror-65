import os
from pathlib import Path

GENESIS = 'https://raw.githubusercontent.com/unification-com/testnet/master' \
          '/latest/genesis.json'

MACHINES = {
    'default': {
        'service': 'und',
        'home': Path(os.path.expanduser("~")) / '.und_mainchain',
        'und_user': 'root'
    },
    'shark': {
        'service': 'und',
        'home': Path('/home/deploy/.und_mainchain'),
        'und_user': 'deploy'
    },
    'node1': {
        'service': 'node1',
        'home': Path('/home/deploy/node1/.und_mainchain'),
        'und_user': 'deploy'
    },
    'node2': {
        'service': 'node2',
        'home': Path('/home/deploy/node2/.und_mainchain'),
        'und_user': 'deploy'
    },
    'node3': {
        'service': 'node3',
        'home': Path('/home/deploy/node3/.und_mainchain'),
        'und_user': 'deploy'
    },
    'sentinel1': {
        'service': 'sentinel1',
        'home': Path('/home/deploy/sentinel1/.und_mainchain'),
        'und_user': 'deploy'
    }
}
