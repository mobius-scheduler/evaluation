import json
import sys
import pandas as pd
import glob

COLS = ['env', 'alpha', 'time', 'round', 'app_id', 'tasks_requested', 'tasks_fulfilled']

def parse_im(y, req_prev):
    # open file
    with open(y) as f:
        im = json.load(f)

    ids = [1, 2]
    req = {id: 0 for id in ids}
    for t in im:
        req[t['app_id']] += t['interest']
    return req

def parse_schedule(x, req, rnd, time, env):
    # open file
    with open(x) as f:
        s = json.load(f)

    df = pd.DataFrame(columns = COLS)
    ids = [1, 2]
    for app in ids:
        if str(app) in s['allocation']:
            alloc = s['allocation'][str(app)]
        else:
            alloc = 0

        assert(req[app] >= alloc)
        df = df.append(
                {
                    'env': env,
                    'alpha': s['stats']['alpha'],
                    'time': time,
                    'round': rnd,
                    'app_id': app,
                    'tasks_requested': req[app],
                    'tasks_fulfilled': alloc,
                },
                ignore_index = 1
        )
    df = df.append(
            {
                'env': env,
                'alpha': s['stats']['alpha'],
                'time': time,
                'round': rnd,
                'app_id': -1,
                'tasks_requested': sum(req[app] for app in ids),
                'tasks_fulfilled': sum(s['allocation'][str(app)] for app in ids),
            },
            ignore_index = 1
    )
    return df

def merge(parsed, to):
    x = []
    for i in range(len(parsed)):
        x += [pd.read_csv(parsed[i])]
    df = pd.concat(x)
    df.to_csv(to, index = False)

def parse(dir):
    with open(dir + '/config.cfg') as f:
        cfg = json.load(f)
        horizon = cfg['replan_sec']
    
    df = pd.DataFrame(columns = COLS)
    sched = sorted(glob.glob(dir + '/schedule_round*.json'))
    im = sorted(glob.glob(dir + '/im_round*.json'))
    req_prev = None
    for x,y in zip(sched, im):
        env = dir.split('/')[-4]
        rnd = int(x.split('round')[-1].split('.json')[0]) + 1
        req = parse_im(y, req_prev)
        s = parse_schedule(x, req, rnd, horizon * rnd, env)
        df = df.append(s)
        req_prev = req
    df.to_csv(dir + '/tasks.csv', index = False)

def parse_hull(dir):
    cols = ['round', 'app1', 'app2']
    df = pd.DataFrame(columns = cols)
    for f in sorted(glob.glob(dir + '/hull_round*.json')):
        rnd = int(f.split('round')[1].split('.json')[0])
        with open(f) as x:
            h = json.load(x)
            if h is None:
                continue
            for s in h:
                df = df.append(
                        {
                            'round': rnd,
                            'app1': s['allocation']['1'],
                            'app2': s['allocation']['2'],
                        },
                        ignore_index = 1
                )
    
    df.to_csv(dir + '/hull.csv', index = False)

