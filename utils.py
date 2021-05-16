import subprocess as sh
import os

MOBIUS_PATH = './mobius'

MOBIUS_CMD = './{path}/main \
        --mode {mode} --alpha {alpha} --horizon {horizon} \
        --capacity {capacity} --rth {rth} --replan {replan} --dir {dir} \
        --cfg_vehicles {cfg_vehicles} --num_vehicles {num_vehicles}'

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
            cfg_vehicles = cfg['cfg_vehicles'],
            num_vehicles = cfg['num_vehicles'])
    if cfg['hull']:
        cmd += ' --hull'
    for a in cfg['apps']:
        cmd += ' --app {}'.format(a)
    print(cmd)
    exec(cmd)

