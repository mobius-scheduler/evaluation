import utils
import json
import sys
import parse

MOBIUS_PATH = './mobius'

# load config
with open(sys.argv[1]) as f:
    cfg = json.load(f)

# build Mobius
utils.build_mobius()

# run experiment
a = cfg['alpha'][0]
print("Running Mobius, alpha = {alpha}".format(alpha = a))
mobius_cfg = {
    "mode": cfg['mode'],
    "apps": cfg['apps'],
    "alpha": a,
    "horizon": cfg['horizon'],
    "capacity": cfg['capacity'],
    "rth": cfg['rth'],
    "replan_sec": cfg['replan_sec'],
    "hull": cfg['hull'],
    "dir": cfg['dir'],
    "num_vehicles": cfg['num_vehicles'],
    "cfg_vehicles": cfg['cfg_vehicles']
}
utils.run_mobius(mobius_cfg)

# parse logs
print("Parsing Mobius, alpha = {alpha}".format(alpha = a))
dir = '{dir}/sprite/alpha{alpha}'.format(dir = cfg['dir'], alpha = a)
parse.parse_hull(dir)

# generate plot
cmd = 'Rscript hull.r {dir}/sprite/alpha{alpha}/hull.csv {dir}/hull.pdf'.format(dir = cfg['dir'], alpha = a)
utils.exec(cmd)

print("Plot saved to {dir}/hull.pdf".format(dir = cfg['dir']))

