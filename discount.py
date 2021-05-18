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
a = cfg['alpha'][0]
for d in cfg['discount']:
    print("Running Mobius, discount = {discount}".format(discount = d))
    mobius_cfg = {
        "mode": cfg['mode'],
        "apps": cfg['apps'],
        "alpha": a,
        "discount": d,
        "horizon": cfg['horizon'],
        "capacity": cfg['capacity'],
        "rth": cfg['rth'],
        "replan_sec": cfg['replan_sec'],
        "duration_sec": cfg['duration_sec'],
        "hull": cfg['hull'],
        "dir": cfg['dir'] + '/discount-{discount}'.format(discount = d),
        "num_vehicles": cfg['num_vehicles'],
        "cfg_vehicles": cfg['cfg_vehicles']
    }
    utils.run_mobius(mobius_cfg)

# get app ids
ids = utils.get_app_ids(cfg['apps'])

# parse logs
parsed = []
for d in cfg['discount']:
    print("Parsing Mobius, discount = {discount}".format(discount = d))
    dir = '{dir}/discount-{discount}/sprite/alpha{alpha}'.format(\
            dir = cfg['dir'], discount = d, alpha = a)
    parse.parse(dir, ids)
    parse.add_col('{dir}/tasks.csv'.format(dir = dir), 'discount', d)
    parsed += ['{dir}/tasks.csv'.format(dir = dir)]

to = '{dir}/tasks.csv'.format(dir = cfg['dir'])
parse.merge(parsed, to)

# generate plots
cmd = 'Rscript discount.r {dir}/tasks.csv {dir}/discount.pdf'.format(dir = cfg['dir'])
utils.exec(cmd)

print("Plot saved to {dir}/discount.pdf".format(dir = cfg['dir']))

