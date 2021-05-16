import utils
import json
import sys
import parse

# load config
with open(sys.argv[1]) as f:
    cfg = json.load(f)

# build Mobius
utils.build_mobius()

# run experiment
for a in cfg['alpha']:
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
parsed = []
for a in cfg['alpha']:
    print("Parsing Mobius, alpha = {alpha}".format(alpha = a))
    dir = '{dir}/sprite/alpha{alpha}'.format(dir = cfg['dir'], alpha = a)
    parse.parse(dir)
    parsed += ['{dir}/tasks.csv'.format(dir = dir)]

to = '{dir}/tasks.csv'.format(dir = cfg['dir'])
parse.merge(parsed, to)

# generate plot
cmd = 'Rscript dynamic.r {dir}/tasks.csv {dir}/dynamic.pdf'.format(dir = cfg['dir'])
utils.exec(cmd)

print("Plot saved to {dir}/dynamic.pdf".format(dir = cfg['dir']))

