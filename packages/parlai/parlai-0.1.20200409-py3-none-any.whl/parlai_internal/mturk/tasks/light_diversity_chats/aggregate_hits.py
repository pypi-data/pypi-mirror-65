
import glob
import json
import os


def get_hits(root, run_name, print_logs=True):
    """
    Get HIT IDs for a list of workers for the purposes of sending a bonus.
    Searches through the most recent HITs first
    """
    dr = os.path.join(ROOT, run_name)
    cnt = 0
    num_turns = 0
    good_acts = []

    for file in reversed(list(glob.glob('{}/t_*/custom/data.json'.format(dr)))):
        with open(file, 'rb') as f:
            log = json.load(f)
            acts = log['acts']
            if len(acts) < 3:
                continue
            for act in acts:
                if 'text' in act:
                    num_turns += 1

            cnt += 1
            good_acts.append((acts, log['characters']))

            if print_logs:
                print(f'{cnt}.')
                chars = log['characters']
                print(f'Chars: {chars[0][0]} and {chars[1][0]}')
                print('---')
                for act in acts:
                    id = act['id']
                    txt = act['text']
                    print(f'{id}:\t{txt}\n')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
    print('=' * 50)
    print(f'Total conversations: {cnt}')
    print(f'Total dialogue turns: {num_turns}')

    return good_acts


def save_acts(root, acts):
    """
    a1: 0
    b1: 1
    a2: 2
    b2: 3
    a3: 4
    b3: 5

    # EVEN
    text = task_speech + a1 0
    label = b1 1
    text = b1 + a2 2
    label = b2 3
    text = b2 + a3 4
    label = b3, ep_done 5

    # ODD
    text = task_speech
    label = a1
    text = a1 + b1
    label = a2
    text = a2 + b2
    label = a3, ep_done = True
    """
    print('[ Formatting acts into ParlAI format ... ]')
    episodes = []
    for act_lst, chars in acts:
        act_txt = [act for act in act_lst if 'text' in act]
        char_1 = chars[0]
        char_2 = chars[1]
        ep = []
        ep_flip = []
        len_lst = len(act_txt)
        prev_a = None
        prev_b = '_task_speech'

        j = 0
        for i in range(len_lst // 2):
            a_i = act_txt[j]['text']
            b_i = act_txt[j + 1]['text']

            even_act = {}
            if prev_b is not None:
                even_text = prev_b + '\n' + '_partner_say ' + a_i + '\n'
                if prev_b != '_task_speech':
                    even_text = '_self_say ' + even_text
            else:
                even_text = a_i + '\n'
            even_label = b_i

            even_act['text'] = even_text
            even_act['labels'] = [even_label]
            even_act['self'] = char_2
            even_act['partner'] = char_1
            even_act['episode_done'] = i + 1 >= len_lst // 2
            ep.append(even_act)

            if j + 1 < len_lst:
                odd_act = {}
                if i == 0:
                    odd_text = '_task_speech\n'
                else:
                    odd_text = '_self_say ' + prev_a + '\n' + '_partner_say ' + prev_b + '\n'
                odd_label = a_i
                odd_act['text'] = odd_text
                odd_act['labels'] = [odd_label]
                odd_act['self'] = char_1
                odd_act['partner'] = char_2
                odd_act['episode_done'] = i + 1 >= len_lst // 2
                ep_flip.append(odd_act)

            prev_a = a_i
            prev_b = b_i
            j += 2

        episodes.append(ep)
        episodes.append(ep_flip)

    save_path = os.path.join(root, 'dialogue_only.json')
    print(f' [ Saving to path {save_path} ... ]')
    data = json.dumps(episodes)
    with open(save_path, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    ROOT = '/private/home/edinan/ParlAI/parlai/mturk/run_data/live/'
    acts = get_hits(ROOT, 'light_diversity_chats_*', print_logs=False)
    save_root = '/private/home/edinan/ParlAI/data/gender_bias_experiments/new_light_data/'
    #save_acts(save_root, acts)
