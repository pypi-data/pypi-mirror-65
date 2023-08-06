import os
import sys
import logging
import Crasa.Crasa as crasa

sys.path.append("/scratch/stimela")

utils = __import__('utils')

CONFIG = os.environ["CONFIG"]
INPUT = os.environ["INPUT"]
OUTPUT = os.environ["OUTPUT"]
MSDIR = os.environ["MSDIR"]

cab = utils.readJson(CONFIG)

makemask_args = {}
immath_args = {}
for param in cab['parameters']:
    name = param['name']
    value = param['value']

    if value is None:
        continue

    if name in ['threshold', 'inpimage', 'output']:
        if name in ['threshold']:
            im_value = ' iif( IM0 >=%s, IM0, 0.0) ' % value
            im_name = 'expr'
        if name in ['output']:
            im_value = '%s_thresh' % value
            im_name = 'outfile'
        if name in ['inpimage']:
            im_value = value
            im_name = 'imagename'
        immath_args[im_name] = im_value

    if name in ['mode', 'inpimage', 'inpmask', 'output', 'overwrite']:
        makemask_args[name] = value

if 'expr' in immath_args:
    task = crasa.CasaTask("immath", **immath_args)
    task.run()

if 'inpmask' not in makemask_args:
    makemask_args['inpmask'] = immath_args['outfile']

task = crasa.CasaTask(cab["binary"], **makemask_args)
task.run()
