#!/usr/bin/env python3
"""
    Alternative train loop that might be more explicit.
    It does use the same Teacher and Agent
"""
import argparse
from parlai.core.dict import DictionaryAgent
from parlai_internal.agents.comment_battle.agents import CommentBattleUruAgent
from parlai_internal.tasks.comment_battle.agents import DefaultTeacher
from parlai.scripts.train_model import setup_args
import random
import json
import time

# parse arguments
argparser = setup_args()
DefaultTeacher.add_cmdline_args(argparser)
CommentBattleUruAgent.add_cmdline_args(argparser)
opt = argparser.parse_args()
opt_valid = argparser.parse_args()
opt_valid["datatype"] = "valid"


# create teacher and agent
train_teacher = DefaultTeacher(opt)
valid_teacher = DefaultTeacher(opt_valid)
agent = CommentBattleUruAgent(opt)
batch_size = opt["batchsize"]

def get_batches(teacher, seed, eval=False):
    """
        Create a list of batches from a teacher
    """
    all_observations = [teacher.get(i) for i in range(teacher.num_examples())]
    # for evaluation we change labels to eval_labels
    if eval:
        for o in all_observations:
            o["eval_labels"] = o["labels"]
            del(o["labels"])
    random.Random(seed).shuffle(all_observations)
    return [all_observations[i:i+batch_size] for i in range(0, len(all_observations), batch_size)]


def swallow_batches(agent, batches, datatype, epoch):
    """
        calls batch act on all the elements of the batch.
        Output report.
    """
    start = time.time()
    agent.reset_metrics()
    for batch in batches:
        agent.batch_act(batch)
    report = agent.report()
    report["datatype"] = datatype
    report["epoch"] = epoch
    report["duration"] = round(time.time()-start, 2)
    return report

class EarlyStopper:

    def __init__(self, direction, patience):
        self.multiplier = 1 if direction == "max" else -1
        self.impatience =0
        self.best_metric = -1000000000.0
        self.patience = patience

    def update(self, value):
        """ return true if we just observed the best value """
        if value * self.multiplier > self.best_metric:
            self.best_metric = value * self.multiplier
            self.impatience = 0
            return True
        self.impatience += 1
        return False

    def is_ended(self):
        return self.impatience >= self.patience



valid_batches = get_batches(valid_teacher, 0, True)
early_stopper = EarlyStopper(opt["validation_metric_mode"], opt["validation_patience"])
for epoch in range(500):
    train_batches = get_batches(teacher=train_teacher, seed=epoch)
    print(json.dumps(swallow_batches(agent, train_batches, "train", epoch)))
    valid_report = swallow_batches(agent, valid_batches, "valid", epoch)
    print(json.dumps(valid_report))
    agent.receive_metrics(valid_report)
    best = early_stopper.update(valid_report[opt["validation_metric"]])
    if best:
        agent.save()
    if early_stopper.is_ended():
        break

#reload the best model for the final evaluation
agent = CommentBattleUruAgent(opt)
# The final evaluation is computed with the candidates provided by Kurt Shuster.
opt_test = argparser.parse_args()
opt_test["datatype"] = "test"
opt_test["use_provided_candidates"] = True
test_teacher = DefaultTeacher(opt_test)

opt_valid = argparser.parse_args()
opt_valid["datatype"] = "valid"
opt_valid["use_provided_candidates"] = True
valid_teacher = DefaultTeacher(opt_valid)

valid_batches = get_batches(valid_teacher, 0, True)
test_batches = get_batches(test_teacher, 0, True)

valid_report = swallow_batches(agent, valid_batches, "valid", -1)
print(json.dumps(valid_report))
test_report = swallow_batches(agent, test_batches, "test", -1)
print(json.dumps(test_report))
