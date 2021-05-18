import subprocess as sh
import os
import json

MOBIUS_PATH = './mobius'

MOBIUS_CMD = './{path}/main \
        --mode {mode} --alpha {alpha} --horizon {horizon} \
        --capacity {capacity} --rth {rth} --replan {replan} --dir {dir} \
        --cfg_vehicles {cfg_vehicles}'

def exec(cmd, cwd = None):
    sh.run(cmd.split(), cwd = cwd)

def build_mobius():
    if os.path.exists(MOBIUS_PATH + '/main'):
        os.remove(MOBIUS_PATH + '/main')
    cmd = 'go build main.go'
    exec(cmd, cwd = MOBIUS_PATH)
    print('Built Mobius!')

def run_mobius(cfg):
    cmd = MOBIUS_CMD.format(
            path = MOBIUS_PATH,
            mode = cfg['mode'],
            alpha = cfg['alpha'],
            horizon = cfg['horizon'],
            capacity = cfg['capacity'],
            rth = cfg['rth'],
            replan = cfg['replan_sec'],
            dir = cfg['dir'],
            cfg_vehicles = cfg['cfg_vehicles'])
    if 'num_vehicles' in cfg:
        cmd += ' --num_vehicles {num_vehicles}'.format(\
                num_vehicles = cfg['num_vehicles'])
    if 'duration_sec' in cfg:
        cmd += ' --duration {duration}'.format(duration = cfg['duration_sec'])
    if 'ttpath' in cfg:
        cmd += ' --ttpath {ttpath}'.format(ttpath = cfg['ttpath'])
    if 'solver' in cfg:
        cmd += ' --solver {solver}'.format(solver = cfg['solver'])
    if 'discount' in cfg:
        cmd += ' --discount {discount}'.format(discount = cfg['discount'])
    if cfg['hull']:
        cmd += ' --hull'
    for a in cfg['apps']:
        cmd += ' --app {}'.format(a)
    print(cmd)
    exec(cmd)

def get_app_ids(apps):
    ids = []
    for a in apps:
        with open(a) as f:
            data = json.load(f)
            ids += [data['app_id']]
    return ids

