import os
import sys

sys.path.append("/scratch/stimela")

utils = __import__('utils')


CONFIG = os.environ["CONFIG"]
INPUT = os.environ["INPUT"]
MSDIR = os.environ["MSDIR"]
OUTDIR = os.environ["OUTPUT"]
HOME = os.environ["HOME"]

cab = utils.readJson(CONFIG)
args = []
overwrite = False

for param in cab['parameters']:
    value = param['value']
    name = param['name']

    if value in [None, False]:
        continue
    elif name == "overwrite":
        overwrite = value
        continue
    elif value is True:
        value = ""
    elif name == 'mvffiles':
        files = value
        continue
    elif name == "output-ms" and value:
        ms = value
    elif name == "credentials_dir" and value:
        os.system("cp -rf {0:s} {1:s}/.aws".format(value, HOME))
        continue
    elif name == "archive-url":
        files = value
        continue

    args += ['{0}{1} {2}'.format(cab['prefix'], name, value)]

if overwrite:
    os.system("rm -fr {0:s}".format(ms))

utils.xrun(cab["binary"], args+files)
