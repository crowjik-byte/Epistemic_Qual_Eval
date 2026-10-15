#!/usr/bin/env python3
"""Freeze the first two fresh interpreter outputs for a four-case follow-up.

By default this uses the initial question and the four pilot cases. With
--question, --cases and --data it builds the same layout for another question
wording, pinning the named development cases from the data file."""

import argparse
import json
from pathlib import Path

import interpreted_judge as judge
import task_interpreter as interpreter

CASE_IDS = ['C000915', 'C000071', 'C000756', 'C000570']


def wording_plan(question_path, case_ids, data_path):
    question = interpreter.load_question(question_path)
    if len(case_ids) != 4 or len(set(case_ids)) != 4:
        raise ValueError('Name exactly four distinct case IDs')
    cases = judge.adapter.load_cases(data_path, set(case_ids), 0)
    if {c['case_id'] for c in cases} != set(case_ids):
        raise ValueError('Some case IDs are missing from the data file')
    if any(c['question'] != question for c in cases):
        raise ValueError('Every case must use the supplied question wording')
    by_id = {c['case_id']: c for c in cases}
    plan = {
        'question_sha256': interpreter.sha(question.encode()),
        'case_sha256': {cid: judge.fingerprint(by_id[cid]) for cid in case_ids},
    }
    return question, plan


def prepare(results_path, manifest_path, output, question_path=None, case_ids=None, data_path=None):
    root = Path(__file__).resolve().parents[1]
    if question_path:
        question, plan = wording_plan(question_path, case_ids or [], data_path)
    else:
        case_ids = CASE_IDS
        question = interpreter.load_question(root / 'inputs/initial_question.json')
        plan = json.loads((root / 'inputs/judge_pilot.json').read_text(encoding='utf-8'))
    meta = json.loads(manifest_path.read_text(encoding='utf-8'))
    if (
        meta.get('question_sha256') != plan['question_sha256']
        or meta.get('instructions_sha256') != interpreter.sha(interpreter.INSTRUCTIONS.encode())
        or meta.get('interpreter_version') != interpreter.VERSION
    ):
        raise ValueError('Use a fresh run of the current interpreter on this question')
    records = [
        json.loads(line)
        for line in results_path.read_text(encoding='utf-8').splitlines()
        if line.strip()
    ]
    if len(records) != 2 or [r.get('attempt') for r in records] != [1, 2]:
        raise ValueError('Use exactly two attempts, in original order, without selection')
    hashes = {str(r['attempt']): judge.fingerprint(r.get('interpretation')) for r in records}
    judge.load_interpretations(results_path, question, hashes)
    plan.update(
        layout='followup',
        case_ids=case_ids,
        comparison_ids=case_ids,
        repeat_ids=[],
        order_seed=20261016,
        interpretation_sha256=hashes,
    )
    plan['case_sha256'] = {cid: plan['case_sha256'][cid] for cid in case_ids}
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
    parser.add_argument('--question', type=Path, help='Question JSON for another wording')
    parser.add_argument('--cases', help='Four comma-separated case IDs; requires --question')
    parser.add_argument('--data', type=Path, default=Path('data/judge_development.csv'))
    args = parser.parse_args()
    if bool(args.question) != bool(args.cases):
        parser.error('--question and --cases must be given together')
    cases = args.cases.split(',') if args.cases else None
    prepare(
        args.interpreter_results,
        args.interpreter_manifest,
        args.output,
        args.question,
        cases,
        args.data,
    )


if __name__ == '__main__':
    main()
