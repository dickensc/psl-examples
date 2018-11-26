#!/usr/bin/env python3

import os

from pslpython.model import Model
from pslpython.partition import Partition
from pslpython.predicate import Predicate
from pslpython.rule import Rule

MODEL_NAME = 'simple-acquaintances'
ADDITIONAL_PSL_OPTIONS = {}

DATA_DIR = os.path.join('..', 'data')

def main():
    model = Model(MODEL_NAME)

    # Add Predicates

    knows_predicate = Predicate('Knows', closed = False, size = 2)
    model.add_predicate(knows_predicate)

    likes_predicate = Predicate('Likes', closed = True, size = 2)
    model.add_predicate(likes_predicate)

    lived_predicate = Predicate('Lived', closed = True, size = 2)
    model.add_predicate(lived_predicate)

    # Add Data

    path = os.path.join(DATA_DIR, 'knows_obs.txt')
    knows_predicate.add_data_file(Partition.OBSERVATIONS, path)

    path = os.path.join(DATA_DIR, 'lived_obs.txt')
    lived_predicate.add_data_file(Partition.OBSERVATIONS, path)

    path = os.path.join(DATA_DIR, 'likes_obs.txt')
    likes_predicate.add_data_file(Partition.OBSERVATIONS, path)

    path = os.path.join(DATA_DIR, 'knows_targets.txt')
    knows_predicate.add_data_file(Partition.TARGETS, path)

    path = os.path.join(DATA_DIR, 'knows_truth.txt')
    knows_predicate.add_data_file(Partition.TRUTH, path)

    # Add Rules
    model.add_rule(Rule('20: Lived(P1, L) & Lived(P2, L) & (P1 != P2) -> Knows(P1, P2) ^2'))
    model.add_rule(Rule('5: Lived(P1, L1) & Lived(P2, L2) & (P1 != P2) & (L1 != L2) -> !Knows(P1, P2) ^2'))
    model.add_rule(Rule('10: Likes(P1, L) & Likes(P2, L) & (P1 != P2) -> Knows(P1, P2) ^2'))
    model.add_rule(Rule('5: Knows(P1, P2) & Knows(P2, P3) & (P1 != P3) -> Knows(P1, P3) ^2'))
    model.add_rule(Rule('Knows(P1, P2) = Knows(P2, P1) .'))
    model.add_rule(Rule('5: !Knows(P1, P2) ^2'))

    # Run Inference
    results = model.infer(psl_config = ADDITIONAL_PSL_OPTIONS)

    # Write out the results.
    out_dir = 'inferred-predicates'
    out_path = os.path.join(out_dir, 'KNOWS.txt')

    os.makedirs(out_dir, exist_ok = True)
    results[knows_predicate].to_csv(out_path, sep = "\t", header = False, index = False)

    # Print thr results as well.
    print(results[knows_predicate])

if (__name__ == '__main__'):
    main()
