#!/usr/bin/env python3

# the dataset should have been built
# srun -o checkpoint/slurm-gpu-job-%j.out --error=checkpoint/slurm-gpu-job-%j.err --gres=gpu:1 python ../../../projects/graph_world2/train.py -t parlai_internal.tasks.graph_world2.agents -bs 1 --model_file tmp/0_final_model.pkl --data_agent_file tmp/0_final_data_agent.pkl --wrong_data_file tmp/0_final_wrong_data.pkl --perf_out_file tmp/0_final_out.txt --cuda True
# python run.py -nh 1 -na 2 -r 0.2 --sandbox
# python run.py -nh 1 -na 30 -r 3.0 --live
# python run.py -nc 20 -r 3.0 --live

from worlds import SimpleDataCollectionWorld as DataCollectionWorld
from parlai.agents.local_human.local_human import LocalHumanAgent
from parlai.core.params import ParlaiParser
from task_config import task_config, VERSION_NUM
import os
import time
from parlai.mturk.core.agents import MTurkAgent, MTurkManager, email_worker, pay_bonus
from joblib import Parallel, delayed
from itertools import product
import threading
from os.path import join
from subprocess import call
import pickle
from scipy import stats
import random
import shutil
from copy import copy, deepcopy
from collections import defaultdict as dd
from collections import namedtuple
import traceback
import signal

START_TASK_TIMEOUT = 10 * 60 # 10 * 60
parent_dir = os.path.dirname(os.path.abspath(__file__))
checkpoint_dir = join(parent_dir, 'checkpoint')
cur_dir = join(parent_dir, 'tmp')

if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)
if not os.path.exists(cur_dir):
    os.makedirs(cur_dir)

USE_SOCKET = True
NEW_VERSION = True

USE_CPU = False
NUM_MACHINES = 60

def pprinttable(rows):
    if len(rows) == 0: return ''
    s = ''
    # if len(rows) > 1:
    headers = rows[0]._fields
    lens = []
    for i in range(len(rows[0])):
        lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
    formats = []
    hformats = []
    for i in range(len(rows[0])):
        if isinstance(rows[0][i], int):
            formats.append("%%%dd" % lens[i])
        else:
            formats.append("%%-%ds" % lens[i])
        hformats.append("%%-%ds" % lens[i])
    pattern = " | ".join(formats)
    hpattern = " | ".join(hformats)
    separator = "-+-".join(['-' * n for n in lens])
    s += hpattern % tuple(headers) + '\n'
    s += separator + '\n'
    for line in rows:
        s += pattern % tuple(line) + '\n'
    return s

def get_output_dir(opt, round_index):
    output_dir = join(opt['datapath'], 'graph_world2_v{}_r{}'.format(VERSION_NUM, round_index))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def get_init_data(opt):
    TRAIN_DIR, VALID_DIR = join(opt['datapath'], 'graph_world2', 'train'), join(opt['datapath'], 'graph_world2', 'valid')

    def read_data(data_path):
        data = []
        for filename in os.listdir(data_path):
            if filename.endswith('pkl'):
                data.append(pickle.load(open(join(data_path, filename), 'rb')))
        return data
    train_data, valid_data = read_data(TRAIN_DIR), read_data(VALID_DIR)

    for i in range(1, opt['start_round']):
        try:
            output_dir = get_output_dir(opt, i)
            delta_train_data = pickle.load(open(join(output_dir, 'delta_train_data.pkl'), 'rb'))
            delta_valid_data = pickle.load(open(join(output_dir, 'delta_valid_data.pkl'), 'rb'))
            train_data.extend(delta_train_data)
            valid_data.extend(delta_valid_data)
        except:
            print('Error: {}'.format(traceback.format_exc()))
    return train_data, valid_data

def train(opt, round_index, train_index, train_data, valid_data, valid_weights=None, save_all=False):
    if valid_weights is not None:
        assert len(valid_data) == len(valid_weights), (len(valid_data), len(valid_weights))

    train_filename = join(cur_dir, '{}_{}_train.pkl'.format(round_index, train_index))
    valid_filename = join(cur_dir, '{}_{}_valid.pkl'.format(round_index, train_index))
    out_filename = join(cur_dir, '{}_out.txt'.format(round_index, train_index))

    pickle.dump(train_data, open(train_filename, 'wb'))
    pickle.dump(valid_data, open(valid_filename, 'wb'))

    if valid_weights is not None:
        weight_filename = join(cur_dir, '{}_{}_weights.pkl'.format(round_index, train_index))
        pickle.dump(valid_weights, open(weight_filename, 'wb'))
    else:
        weight_filename = ''

    if save_all:
        model_filename = join(cur_dir, '{}_{}_model.pkl'.format(round_index, train_index))
        data_agent_filename = join(cur_dir, '{}_{}_data_aganet.pkl'.format(round_index, train_index))
        wrong_data_filename = join(cur_dir, '{}_{}_wrong_data.pkl'.format(round_index, train_index))
    else:
        model_filename = ''
        data_agent_filename = ''
        wrong_data_filename = ''

    if USE_CPU:
        cmd = "srun -o checkpoint/slurm-gpu-job-%j.out --error=checkpoint/slurm-gpu-job-%j.err -c 16 python3 ../../../projects/graph_world2/train.py -t parlai_internal.tasks.graph_world2.agents -bs 1 --max_iter {} --num_runs {} --train_data_file {} --valid_data_file {} --perf_out_file {}".format(opt['max_iter'], opt['num_runs'], train_filename, valid_filename, out_filename)
    # else:
    #     cmd = "srun -o checkpoint/slurm-gpu-job-%j.out --error=checkpoint/slurm-gpu-job-%j.err --gres=gpu:1 python3 ../../../projects/graph_world2/train.py -t parlai_internal.tasks.graph_world2.agents -bs 1 --cuda True --max_iter {} --num_runs {} --train_data_file {} --valid_data_file {} --perf_out_file {}".format(opt['max_iter'], opt['num_runs'], train_filename, valid_filename, out_filename)
        if weight_filename != '':
            cmd += " --weight_file {}".format(weight_filename)
        if model_filename != '':
            cmd += " --model_file {}".format(model_filename)
        if data_agent_filename != '':
            cmd += " --data_agent_file {}".format(data_agent_filename)
        if wrong_data_filename != '':
            cmd += " --wrong_data_file {}".format(wrong_data_filename)

        code = call(cmd.split(), cwd=parent_dir)

        if code != 0:
            return 0.0

        try:
            f_perf = open(out_filename)
            perf = float(f_perf.readline().strip())
            f_perf.close()
            return perf
        except:
            print('Error: {}'.format(traceback.format_exc()))
            return 0.0
    else:
        new_opt = {
            'max_iter': opt['max_iter'],
            'num_runs': opt['num_runs'],
            'train_data_file': train_filename,
            'valid_data_file': valid_filename,
            'perf_out_file': out_filename,
            'task': 'parlai_internal.tasks.graph_world2.agents',
            'batchsize': 1
        }
        os.chdir(parent_dir)
        if type(train_index) != int: train_index = 0
        pickle.dump(new_opt, open('../../../projects/graph_world2/job-in-{}.pkl'.format(train_index % NUM_MACHINES), 'wb'))
        while True:
            time.sleep(5)
            if os.path.isfile('../../../projects/graph_world2/job-out-{}.txt'.format(train_index % NUM_MACHINES)):
                result = open('../../../projects/graph_world2/job-out-{}.txt'.format(train_index % NUM_MACHINES), 'r').readline().strip()
                os.remove('../../../projects/graph_world2/job-out-{}.txt'.format(train_index % NUM_MACHINES))
                if result != '0':
                    print(result)
                    return 0.0
                try:
                    f_perf = open(out_filename)
                    perf = float(f_perf.readline().strip())
                    f_perf.close()
                    return perf
                except:
                    print('Error: {}'.format(traceback.format_exc()))
                    return 0.0

def calc_bonus(rank):
    if rank == 1: return 15.0
    if rank == 2: return 10.0
    if rank == 3: return 5.0
    return 0.0

def get_saved_from_train(round_index, train_index):
    data_agent = pickle.load(open(join(cur_dir, '{}_{}_data_aganet.pkl'.format(round_index, train_index)), 'rb'))
    model_dict = pickle.load(open(join(cur_dir, '{}_{}_model.pkl'.format(round_index, train_index)), 'rb'))
    wrong_data = pickle.load(open(join(cur_dir, '{}_{}_wrong_data.pkl'.format(round_index, train_index)), 'rb'))
    return data_agent, model_dict, wrong_data

def get_email_text(perf, rank, num_part, link, hit_is_abandoned, cur_lb_text, global_lb_text):
    perf_text = '{0:.4f}'.format(perf * 100)
    s = "Your dragon has a score {} in a test by the dungeon master, ranked No. {} among {} participants.\n".format(perf_text, rank, num_part)
    bonus = calc_bonus(rank) if not hit_is_abandoned else 0.0
    if bonus > 0:
        s += "${0:.2f} dollars have been credited to you account! Congratulations!\n".format(bonus)
    if link is not None:
        s += "A new round of evolution has started! Click the following link to train a better dragon!\n{}\n".format(link)
    if cur_lb_text != '':
        s += "\n\nLEADERBOARD OF CURRENT ROUND\n{}".format(cur_lb_text)
    if global_lb_text != '':
        s += "\n\nALL TIME LEADERBOARD\n{}".format(global_lb_text)
    return s

def get_id_username_binding(opt, round_index):
    if round_index == 0:
        return {'id2name': {}, 'name2id': {}}
    output_dir = get_output_dir(opt, round_index)
    return pickle.load(open(join(output_dir, 'username_binding.pkl'), 'rb'))

def save_id_username_binding(opt, round_index, binding):
    output_dir = get_output_dir(opt, round_index)
    pickle.dump(binding, open(join(output_dir, 'username_binding.pkl'), 'wb'))

def get_leaderboard(opt, round_index):
    if round_index == 0:
        return dd(float)
    output_dir = get_output_dir(opt, round_index)
    return pickle.load(open(join(output_dir, 'leaderboard.pkl'), 'rb'))

def save_leaderboard(opt, round_index, leaderboard):
    output_dir = get_output_dir(opt, round_index)
    pickle.dump(leaderboard, open(join(output_dir, 'leaderboard.pkl'), 'wb'))

def get_showtimes(opt, round_index):
    if round_index == 0:
        return dd(float)
    output_dir = get_output_dir(opt, round_index)
    return pickle.load(open(join(output_dir, 'showtimes.pkl'), 'rb'))

def save_showtimes(opt, round_index, showtimes):
    output_dir = get_output_dir(opt, round_index)
    pickle.dump(showtimes, open(join(output_dir, 'showtimes.pkl'), 'wb'))

def get_lb_text(leaderboard):
    lb = sorted(leaderboard, key=lambda x: x[1], reverse=True)
    ret_tab = []
    Row = namedtuple('Row', ['username', 'score', 'bonus'])
    for ent in lb:
        ret_tab.append(Row(ent[0], '{0:.4f}'.format(ent[1] * 100), 'Abandoned' if ent[2] < 0 else '{0:.2f}'.format(ent[2])))
    return pprinttable(ret_tab)

def get_global_lb_text(leaderboard):
    lb = [(k, v) for k, v in leaderboard.items()]
    lb.sort(key=lambda x: x[1], reverse=True)
    lb = lb[: 10]
    ret_tab = []
    Row = namedtuple('Row', ['username', 'bonus'])
    for ent in lb:
        ret_tab.append(Row(ent[0], '{0:.2f}'.format(ent[1])))
    return pprinttable(ret_tab)

def main(opt):
    new_opt = deepcopy(opt)
    if USE_SOCKET:
        new_opt['num_conversations'] = opt['actual_num_assignments']
    else:
        new_opt['num_assignments'] = opt['actual_num_assignments']

    mturk_agent_id = 'You'
    mturk_manager = MTurkManager(opt=new_opt, mturk_agent_ids=[mturk_agent_id])
    
    if USE_SOCKET:
        mturk_manager.setup_server()
        mturk_manager.set_onboard_function(onboard_function=None)
    else:
        mturk_manager.init_aws(opt=new_opt, task_directory_path=os.path.dirname(os.path.abspath(__file__)))

    def check_worker_eligibility(worker):
        return True

    def get_worker_role(worker):
        return 'You'

    train_data, valid_data = get_init_data(opt)
    round_index = 0

    data_agent, model_dict, wrong_data = get_saved_from_train(opt['start_round'] - 1, 'final')
    binding = get_id_username_binding(opt, opt['start_round'] - 1)
    leaderboard = get_leaderboard(opt, opt['start_round'] - 1)
    showtimes = get_showtimes(opt, opt['start_round'] - 1)
    prev_perf = float(open(join(cur_dir, '{}_{}_out.txt'.format(opt['start_round'] - 1, 'final'))).readline().strip())

    mturk_agent_object_list = []
    mturk_data_list = []

    global run_hit
    def run_hit(hit_index, assignment_index, opt, mturk_manager, data_agent, model_dict, wrong_data, cur_ids):
        start_time = time.time()
        try:
            mturk_agent = MTurkAgent(id=mturk_agent_id, manager=mturk_manager, hit_index=hit_index, assignment_index=assignment_index, opt=opt)
            world = DataCollectionWorld(opt, mturk_agent, data_agent, model_dict, wrong_data, binding, cur_ids, showtimes, round_index)
            while not world.episode_done():
                world.parley()
            world.shutdown()
            return mturk_agent.get_sanitized_copy(), world.get_data()
        except:
            print('Error: {}'.format(traceback.format_exc()))
            return None, None

    def run_conversation_new(mturk_manager, opt, workers):
        start_time = time.time()
        try:
            mturk_agent = workers[0]
            world = DataCollectionWorld(opt, mturk_agent, data_agent, model_dict, wrong_data, binding, cur_ids, showtimes, round_index)
            while not world.episode_done():
                world.parley()
            world.shutdown()
            return mturk_agent.get_sanitized_copy(), world.get_data()
        except:
            print('Error: {}'.format(traceback.format_exc()))
            return None, None

    def run_conversation_old(opt, workers):
        start_time = time.time()
        try:
            mturk_agent = workers[0]
            world = DataCollectionWorld(opt, mturk_agent, data_agent, model_dict, wrong_data, binding, cur_ids, showtimes, round_index)
            while not world.episode_done():
                world.parley()
            world.shutdown()
            return mturk_agent.get_sanitized_copy(), world.get_data()
        except:
            print('Error: {}'.format(traceback.format_exc()))
            return None, None

    global run_conversation
    run_conversation = run_conversation_new if NEW_VERSION else run_conversation_old

    def filter(mturk_agent_object_list, mturk_data_list):
        filtered_mturk_agent_list, filtered_data_list = [], []
        for i in range(len(mturk_data_list)):
            if mturk_data_list[i] is None:
                continue
            filtered_mturk_agent_list.append(mturk_agent_object_list[i])
            filtered_data_list.append(mturk_data_list[i])
        return filtered_mturk_agent_list, filtered_data_list

    filtered_mturk_agent_list, perfs, ranks = [], [], None
    for i in range(opt['start_round'], opt['end_round']):
        round_index = i
        output_dir = get_output_dir(opt, round_index)

        new_opt['hit_description'] = opt['hit_description'].replace('[ROUND_NUM]', str(round_index))
        new_opt['hit_title'] = opt['hit_title'].replace('[ROUND_NUM]', str(round_index))
        if USE_SOCKET:
            mturk_manager.start_new_run()
            mturk_agent_HIT_url = mturk_manager.create_hits()
            mturk_manager.ready_to_accept_workers()
        else:
            mturk_manager.start_new_run(opt=new_opt)
            mturk_agent_HIT_url = mturk_manager.create_hits(opt=new_opt)

        if len(filtered_mturk_agent_list) > 0:
            cur_leaderboard = []
            for i, mturk_agent in enumerate(filtered_mturk_agent_list):
                my_bonus = calc_bonus(ranks[i])
                cur_leaderboard.append((mturk_agent['username'], perfs[i], my_bonus))
                if my_bonus > 0:
                    leaderboard[mturk_agent['username']] += my_bonus
            cur_lb_text = get_lb_text(cur_leaderboard)
            global_lb_text = get_global_lb_text(leaderboard)

            save_leaderboard(opt, round_index - 1, leaderboard)

            for i, mturk_agent in enumerate(filtered_mturk_agent_list):
                try:
                    if i == 0:
                        print(get_email_text(perfs[i], ranks[i], len(filtered_mturk_agent_list), mturk_agent_HIT_url, mturk_agent['hit_is_abandoned'], cur_lb_text, global_lb_text))
                    email_worker(opt, mturk_agent['worker_id'], subject="Train Your Dragon: Results for Round {}".format(round_index - 1), message_text=get_email_text(perfs[i], ranks[i], len(filtered_mturk_agent_list), mturk_agent_HIT_url, mturk_agent['hit_is_abandoned'], cur_lb_text, global_lb_text))
                except:
                    print('Error: {}'.format(traceback.format_exc()))

        filtered_mturk_agent_list, filtered_data_list, cur_ids = [], [], set()
        try_iter = 0
        while True:
            def re_start():
                print('Restarting: {} left'.format(opt['num_assignments'] - len(filtered_mturk_agent_list)))
                new_opt['hit_description'] = opt['hit_description'].replace('[ROUND_NUM]', str(round_index))
                new_opt['hit_title'] = opt['hit_title'].replace('[ROUND_NUM]', str(round_index))
                if USE_SOCKET:
                    mturk_manager.start_new_run()
                    mturk_agent_HIT_url = mturk_manager.create_hits()
                    mturk_manager.ready_to_accept_workers()
                else:
                    mturk_manager.start_new_run(opt=new_opt)
                    mturk_agent_HIT_url = mturk_manager.create_hits(opt=new_opt)
            def handler(signum, frame):
                raise Exception('Tiemout in run_hit')

            try:
                if USE_SOCKET:
                    run_hit_return_list = mturk_manager.start_task(
                        eligibility_function=check_worker_eligibility,
                        role_function=get_worker_role,
                        task_function=run_conversation,
                        timeout=START_TASK_TIMEOUT
                    )
                    mturk_manager.shutdown()
                else:
                    run_hit_return_list = Parallel(n_jobs=new_opt['num_assignments'], backend='threading') \
                            (delayed(run_hit)(1, assignment_index, new_opt, mturk_manager, data_agent, model_dict, wrong_data, cur_ids) \
                                for assignment_index in range(1, new_opt['num_assignments'] + 1))
            except:
                print('Error: {}'.format(traceback.format_exc()))
                try:
                    mturk_manager.expire_all_unassigned_hits()
                    mturk_manager.shutdown()
                except:
                    print('Error: {}'.format(traceback.format_exc()))
                re_start()
                continue
            try:
                mturk_manager.expire_all_unassigned_hits()
                mturk_manager.shutdown()
            except:
                print('Error: {}'.format(traceback.format_exc()))
            try_iter += 1
            mturk_agent_object_list = [e[0] for e in run_hit_return_list]
            mturk_data_list = [e[1] for e in run_hit_return_list]
            new_mturk_agent_object_list, new_mturk_data_list = filter(mturk_agent_object_list, mturk_data_list)
            for mturk_agent in new_mturk_agent_object_list:
                cur_ids.add(mturk_agent['worker_id'])
            filtered_mturk_agent_list.extend(new_mturk_agent_object_list)
            filtered_data_list.extend(new_mturk_data_list)

            pickle.dump(filtered_mturk_agent_list, open(join(output_dir, 'filtered_mturk_agent_list.pkl'), 'wb'))
            pickle.dump(filtered_data_list, open(join(output_dir, 'filtered_data_list.pkl'), 'wb'))
            save_id_username_binding(opt, round_index, binding)
            save_showtimes(opt, round_index, showtimes)

            if len(filtered_mturk_agent_list) >= opt['num_assignments']: break
            if try_iter >= opt['max_retry']: break
            re_start()

        min_dataset_size = None
        for dataset in filtered_data_list:
            cur_dataset_size = len(dataset)
            if min_dataset_size is None or cur_dataset_size < min_dataset_size:
                min_dataset_size = cur_dataset_size

        N = len(filtered_mturk_agent_list)

        round_train_data, round_valid_data, round_valid_weights = [], [], []
        for i in range(N):
            cur_train_data, cur_valid_data, cur_valid_weights = copy(train_data), copy(valid_data), [1.0 for _ in range(len(valid_data))]
            for j in range(N):
                cur_dataset_size = len(filtered_data_list[j])
                if i == j:
                    cur_train_data.extend(filtered_data_list[j])
                else:
                    cur_valid_data.extend(filtered_data_list[j])
                    cur_valid_weights.extend([1.0 * min_dataset_size / cur_dataset_size for _ in range(cur_dataset_size)]) # downweighing large datasets
            round_train_data.append(cur_train_data)
            round_valid_data.append(cur_valid_data)
            round_valid_weights.append(cur_valid_weights)
        for i in range(N):
            cur_train_data, cur_valid_data, cur_valid_weights = copy(train_data), copy(valid_data), [1.0 for _ in range(len(valid_data))]
            cur_train_data.extend(filtered_data_list[i])
            round_train_data.append(cur_train_data)
            round_valid_data.append(cur_valid_data)
            round_valid_weights.append(cur_valid_weights)

        print('start training {} jobs'.format(2 * N))
        perfs = []
        start, end = 0, NUM_MACHINES
        while True:
            if start >= 2 * N: break
            end = min(end, 2 * N)
            perfs_now = Parallel(n_jobs=end-start, backend='threading') \
            (delayed(train)(opt, round_index, train_index, round_train_data[train_index], round_valid_data[train_index], valid_weights=round_valid_weights[train_index]) \
                for train_index in range(start, end))
            perfs.extend(perfs_now)
            start = end
            end = start + NUM_MACHINES

        flag = True
        for perf in perfs:
            if perf == 0.0: flag = False
        
        ranks = len(perfs[: N]) + 1 - stats.rankdata(perfs[: N], method='ordinal')

        delta_train_data, delta_valid_data = [], []
        for i, dataset in enumerate(filtered_data_list):
            if perfs[i + N] < prev_perf - opt['accuracy_decrease_max']: continue
            for data_point in dataset:
                if random.random() < 0.8:
                    delta_train_data.append(data_point)
                else:
                    delta_valid_data.append(data_point)

        train_data.extend(delta_train_data)
        valid_data.extend(delta_valid_data)

        prev_perf = train(opt, round_index, 'final', train_data, valid_data, save_all=True)
        if prev_perf == 0: flag = False

        if not flag:
            input('Please manually run the training scripts. Press enter when it is finished...')
            perfs, ranks, prev_perf = tuple(pickle.load(open(join(output_dir, 'perfs.pkl'), 'rb')))
        else:
            f_log = open(join(cur_dir, 'mtd_log.txt'), 'a+')
            f_log.write('#{} perfs {} ranks {} final_perf {}\n'.format(round_index, perfs, ranks, prev_perf))
            f_log.close()

            pickle.dump([perfs, ranks, prev_perf], open(join(output_dir, 'perfs.pkl'), 'wb'))
            pickle.dump(delta_train_data, open(join(output_dir, 'delta_train_data.pkl'), 'wb'))
            pickle.dump(delta_valid_data, open(join(output_dir, 'delta_valid_data.pkl'), 'wb'))

        for i, mturk_agent in enumerate(filtered_mturk_agent_list):
            bonus = calc_bonus(ranks[i])
            if bonus > 0:
                try:
                    pay_bonus(opt, mturk_agent['worker_id'], bonus, mturk_agent['assignment_id'], 'high ranking')
                except:
                    print('Error: {}'.format(traceback.format_exc()))

        data_agent, model_dict, wrong_data = get_saved_from_train(round_index, 'final')

    if len(filtered_mturk_agent_list) > 0:
        cur_leaderboard = []
        for i, mturk_agent in enumerate(filtered_mturk_agent_list):
            my_bonus = calc_bonus(ranks[i])
            cur_leaderboard.append((mturk_agent['username'], perfs[i], my_bonus))
            if my_bonus > 0:
                leaderboard[mturk_agent['username']] += my_bonus
        cur_lb_text = get_lb_text(cur_leaderboard)
        global_lb_text = get_global_lb_text(leaderboard)

        save_leaderboard(opt, opt['end_round'] - 1, leaderboard)

        for i, mturk_agent in enumerate(filtered_mturk_agent_list):
            try:
                if i == 0:
                    print(get_email_text(perfs[i], ranks[i], len(filtered_mturk_agent_list), None, mturk_agent['hit_is_abandoned'], cur_lb_text, global_lb_text))
                email_worker(opt, mturk_agent['worker_id'], subject="Train Your Dragon: Results for Round {}".format(opt['end_round'] - 1), message_text=get_email_text(perfs[i], ranks[i], len(filtered_mturk_agent_list), None, mturk_agent['hit_is_abandoned'], cur_lb_text, global_lb_text))
            except:
                print('Error: {}'.format(traceback.format_exc()))

def test_training(opt):
    train_data, valid_data = get_init_data(opt)
    N = 60
    perfs1 = Parallel(n_jobs=N, backend='threading') \
        (delayed(train)(opt, 1, train_index, train_data, valid_data) \
            for train_index in range(N))

def resume(opt):
    train_data, valid_data = get_init_data(opt)
    prev_perf = float(open(join(cur_dir, '{}_{}_out.txt'.format(opt['start_round'] - 1, 'final'))).readline().strip())

    round_index = opt['start_round']
    output_dir = get_output_dir(opt, round_index)
    filtered_mturk_agent_list = pickle.load(open(join(output_dir, 'filtered_mturk_agent_list.pkl'), 'rb'))
    filtered_data_list = pickle.load(open(join(output_dir, 'filtered_data_list.pkl'), 'rb'))

    min_dataset_size = None
    for dataset in filtered_data_list:
        cur_dataset_size = len(dataset)
        if min_dataset_size is None or cur_dataset_size < min_dataset_size:
            min_dataset_size = cur_dataset_size

    N = len(filtered_mturk_agent_list)

    round_train_data, round_valid_data, round_valid_weights = [], [], []
    for i in range(N):
        cur_train_data, cur_valid_data, cur_valid_weights = copy(train_data), copy(valid_data), [1.0 for _ in range(len(valid_data))]
        for j in range(N):
            cur_dataset_size = len(filtered_data_list[j])
            if i == j:
                cur_train_data.extend(filtered_data_list[j])
            else:
                cur_valid_data.extend(filtered_data_list[j])
                cur_valid_weights.extend([1.0 * min_dataset_size / cur_dataset_size for _ in range(cur_dataset_size)]) # downweighing large datasets
        round_train_data.append(cur_train_data)
        round_valid_data.append(cur_valid_data)
        round_valid_weights.append(cur_valid_weights)
    for i in range(N):
        cur_train_data, cur_valid_data, cur_valid_weights = copy(train_data), copy(valid_data), [1.0 for _ in range(len(valid_data))]
        cur_train_data.extend(filtered_data_list[i])
        round_train_data.append(cur_train_data)
        round_valid_data.append(cur_valid_data)
        round_valid_weights.append(cur_valid_weights)

    print('start training {} jobs'.format(2 * N))
    perfs = []
    start, end = 0, NUM_MACHINES
    while True:
        if start >= 2 * N: break
        end = min(end, 2 * N)
        perfs_now = Parallel(n_jobs=end-start, backend='threading') \
        (delayed(train)(opt, round_index, train_index, round_train_data[train_index], round_valid_data[train_index], valid_weights=round_valid_weights[train_index]) \
            for train_index in range(start, end))
        perfs.extend(perfs_now)
        start = end
        end = start + NUM_MACHINES

    flag = True
    for perf in perfs:
        if perf == 0.0: flag = False
    
    ranks = len(perfs[: N]) + 1 - stats.rankdata(perfs[: N], method='ordinal')

    delta_train_data, delta_valid_data = [], []
    for i, dataset in enumerate(filtered_data_list):
        if perfs[i + N] < prev_perf - opt['accuracy_decrease_max']: continue
        for data_point in dataset:
            if random.random() < 0.8:
                delta_train_data.append(data_point)
            else:
                delta_valid_data.append(data_point)

    train_data.extend(delta_train_data)
    valid_data.extend(delta_valid_data)

    prev_perf = train(opt, round_index, 'final', train_data, valid_data, save_all=True)
    if prev_perf == 0: flag = False

    if not flag:
        print('Please manually run the training scripts.')
        quit()

    f_log = open(join(cur_dir, 'mtd_log.txt'), 'a+')
    f_log.write('#{} perfs {} ranks {} final_perf {}\n'.format(round_index, perfs, ranks, prev_perf))
    f_log.close()

    pickle.dump([perfs, ranks, prev_perf], open(join(output_dir, 'perfs.pkl'), 'wb'))
    pickle.dump(delta_train_data, open(join(output_dir, 'delta_train_data.pkl'), 'wb'))
    pickle.dump(delta_valid_data, open(join(output_dir, 'delta_valid_data.pkl'), 'wb'))

if __name__ == '__main__':
    argparser = ParlaiParser(False, False)
    argparser.add_argument('--resume', dest='resume', action='store_true')
    argparser.add_argument('--start_round', type=int, default=1) # 1
    argparser.add_argument('--end_round', type=int, default=10) # 10
    argparser.add_parlai_data_path()
    argparser.add_mturk_args()
    opt = argparser.parse_args()
    opt['task'] = os.path.basename(os.getcwd())
    opt.update(task_config)
    opt['seed'] = -1
    opt['edge_p'] = 0.2
    opt['max_action_len'] = 4

    opt['mtd_log'] = 'mtd_log.txt'
    # if 'data_path' not in opt:
    #     opt['data_path'] = 'data/' + opt['task'] + '_{}'.format(time.strftime("%Y%m%d-%H%M%S"))
    opt['assignment_duration_in_seconds'] = 40 * 60 # 40 * 60
    opt['accuracy_decrease_max'] = 0.03
    opt['max_retry'] = 100

    if USE_SOCKET:
        opt['num_assignments'] = opt['num_conversations']

    # if USE_SOCKET:
    #     opt['actual_num_assignments'] = min(opt['num_conversations'] * 2, 30)
    # else:
    #     opt['actual_num_assignments'] = min(opt['num_assignments'] * 2, 30)
    opt['actual_num_assignments'] = 20 # 20

    opt['max_iter'] = 100000 # 1000000
    opt['num_runs'] = 3 # 3
    opt['min_examples_per_HIT'] = 10 # 10
    opt['error_examples'] = 3
    opt['cuda'] = True

    if opt['resume']:
        resume(opt)
    else:
        main(opt)

    # test_training(opt)

    # test_lb_text()
    # test_train(opt)
