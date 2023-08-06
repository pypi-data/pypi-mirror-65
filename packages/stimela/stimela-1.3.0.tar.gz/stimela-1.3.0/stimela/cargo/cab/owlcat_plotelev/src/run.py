import os
import sys

sys.path.append('/scratch/stimela')

utils = __import__('utils')

CONFIG = os.environ["CONFIG"]
INPUT = os.environ["INPUT"]
MSDIR = os.environ["MSDIR"]

cab = utils.readJson(CONFIG)
args = []

for param in cab['parameters']:
    name = param['name']
    value = param['value']
    if value is None:
        continue
    elif value is False:
        continue

    if name in ['msname']:
        args += ['{0}'.format(value)]
    elif type(value) is bool:
        args += ['{0}{1}'.format(cab['prefix'], name)]
    else:
        args += ['{0}{1} {2}'.format(cab['prefix'], name, value)]

utils.xrun(cab['binary'], args)
