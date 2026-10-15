#!/usr/bin/env python3
"""Freeze the first two fresh interpreter outputs for the four-case follow-up."""

import argparse
import json
from pathlib import Path

import interpreted_judge as judge
import task_interpreter as interpreter

CASE_IDS = ['C000915', 'C000071', 'C000756', 'C000570']


def prepare(results_path, manifest_path, output):
    root = Path(__file__).resolve().parents[1]
    plan = json.loads((root / 'inputs/judge_pilot.json').read_text(encoding='utf-8'))
    meta = json.loads(manifest_path.read_text(encoding='utf-8'))
    if (
        meta.get('question_sha256') != plan['question_sha256']
        or meta.get('instructions_sha256') != interpreter.sha(interpreter.INSTRUCTIONS.encode())
        or meta.get('interpreter_version') != interpreter.VERSION
    ):
        raise ValueError('Use a fresh run of the current interpreter on the initial question')
    records = [
        json.loads(line)
        for line in results_path.read_text(encoding='utf-8').splitlines()
        if line.strip()
    ]
    if len(records) != 2 or [r.get('attempt') for r in records] != [1, 2]:
        raise ValueError('Use exactly two attempts, in original order, without selection')
    hashes = {str(r['attempt']): judge.fingerprint(r.get('interpretation')) for r in records}
    question = interpreter.load_question(root / 'inputs/initial_question.json')
    judge.load_interpretations(results_path, question, hashes)
    plan.update(
        layout='followup',
        case_ids=CASE_IDS,
        comparison_ids=CASE_IDS,
        repeat_ids=[],
        order_seed=20261016,
        interpretation_sha256=hashes,
    )
    plan['case_sha256'] = {cid: plan['case_sha256'][cid] for cid in CASE_IDS}
    plan['source_results_sha256'] = interpreter.sha(results_path.read_bytes())
    plan['source_manifest_sha256'] = interpreter.sha(manifest_path.read_bytes())
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(plan, indent=2) + '\n')
    print('Frozen both interpretations unchanged for eight evaluations on four cases.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--interpreter-results', type=Path, required=True)
    parser.add_argument('--interpreter-manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.interpreter_results, args.interpreter_manifest, args.output)


if __name__ == '__main__':
    main()
