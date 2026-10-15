"""Offline tests of pilot boundaries, unchanged interpretations and judge evidence."""

import copy
import csv
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import interpreted_judge as judge
from test_interpreter import QUESTION, RESULT


def answer(payload):
    return {
        'checks': [
            {
                'check_id': c['id'],
                'verdict': 'no_failure_established',
                'evidence': [],
                'reasoning': 'The response explains the distinction.',
                'strongest_defense': 'Concise explanation.',
                'resolution': 'No failure shown.',
            }
            for c in payload['interpretation']['candidate_checks']
        ],
        'format': {'verdict': 'compliant', 'explanation': 'No extra constraints.'},
        'interpretation_issues': [],
        'other_observations': [],
        'review_needed': [],
    }


class PilotTests(unittest.TestCase):
    def fixture(self, root):
        rows = [
            {
                'case_id': f'C{i}',
                'question': QUESTION,
                'account_text': f'Account {i // 2}',
                'rating': '4',
                'reason': f'Reason {i}.',
            }
            for i in range(8)
        ]
        data = root / 'development.csv'
        with data.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=[*rows[0], 'human_notes'])
            writer.writeheader()
            for row in rows:
                writer.writerow({**row, 'human_notes': 'PRIVATE_SENTINEL'})
        results = root / 'source.jsonl'
        second = copy.deepcopy(RESULT)
        second['scope'] = 'A second interpretation.'
        results.write_text(
            '\n'.join(
                json.dumps(
                    {
                        'attempt': i,
                        'status': 'structured_output',
                        'interpretation': value,
                        'response_text': json.dumps(value),
                    }
                )
                for i, value in enumerate([RESULT, second], 1)
            )
        )
        plan = root / 'plan.json'
        plan.write_text(
            json.dumps(
                {
                    'case_ids': [r['case_id'] for r in rows],
                    'case_sha256': {r['case_id']: judge.fingerprint(r) for r in rows},
                    'question_sha256': judge.interpreter.sha(QUESTION.encode()),
                    'interpretation_sha256': {
                        '1': judge.fingerprint(RESULT),
                        '2': judge.fingerprint(second),
                    },
                    'comparison_ids': ['C0', 'C6'],
                    'repeat_ids': ['C0', 'C6'],
                    'order_seed': 1,
                }
            )
        )
        return ['--data', str(data), '--interpreter-results', str(results), '--plan', str(plan)]

    def test_plan_dry_run_identical_repeats_and_private_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = self.fixture(root) + ['--output-dir', str(root / 'dry')]
            with patch.object(judge.adapter, 'call_api') as api:
                self.assertEqual(judge.main(args), 0)
                api.assert_not_called()
            requests = [
                json.loads(line) for line in (root / 'dry/requests.jsonl').read_text().splitlines()
            ]
            self.assertEqual(len(requests), 12)
            self.assertEqual(sum(r['attempt'] == 2 for r in requests), 2)
            self.assertEqual(len({r['case_id'] for r in requests}), 8)
            for req in requests:
                payload = json.loads(req['user'])
                self.assertEqual(
                    set(payload), {'question', 'account_text', 'rating', 'reason', 'interpretation'}
                )
                self.assertNotIn('PRIVATE_SENTINEL', req['user'])
                if req['purpose'] == 'repeat':
                    baseline = next(
                        r
                        for r in requests
                        if r['case_id'] == req['case_id'] and r['purpose'] == 'baseline'
                    )
                    self.assertEqual(req['user'], baseline['user'])
                if req['attempt'] == 1:
                    self.assertEqual(payload['interpretation'], RESULT)
            self.assertEqual(
                (root / 'source.jsonl').read_bytes(),
                (root / 'dry/interpreter_results.jsonl').read_bytes(),
            )
            with self.assertRaises(FileExistsError):
                judge.main(args)

    def test_changed_interpretation_or_data_rejected_before_output(self):
        for mutation in ['data', 'parsed', 'both', 'manifest']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                args = self.fixture(root) + ['--output-dir', str(root / 'dry')]
                if mutation == 'data':
                    path = root / 'development.csv'
                    path.write_text(path.read_text().replace('Reason 0.', 'Changed reason.'))
                elif mutation == 'manifest':
                    path = root / 'manifest.json'
                    path.write_text(json.dumps({'question_sha256': 'wrong'}))
                    args += ['--interpreter-manifest', str(path)]
                else:
                    path = root / 'source.jsonl'
                    records = [json.loads(line) for line in path.read_text().splitlines()]
                    records[0]['interpretation']['scope'] = 'Changed'
                    if mutation == 'both':
                        records[0]['response_text'] = json.dumps(records[0]['interpretation'])
                    path.write_text('\n'.join(json.dumps(r) for r in records))
                with self.assertRaises(ValueError):
                    judge.main(args)
                self.assertFalse((root / 'dry').exists())

    def test_evidence_and_complete_check_coverage(self):
        payload = {
            'interpretation': RESULT,
            'question': QUESTION,
            'account_text': 'Account',
            'reason': 'Reason',
        }
        result = answer(payload)
        self.assertEqual(judge.validate(result, payload), [])
        result['checks'][0]['verdict'] = 'supported_failure'
        self.assertTrue(judge.validate(result, payload))
        result['checks'][0]['evidence'] = [{'source': 'reason', 'quote': 'Reason'}]
        self.assertEqual(judge.validate(result, payload), [])
        result['checks'][0]['evidence'][0]['quote'] = 'Invented'
        self.assertTrue(judge.validate(result, payload))
        result = answer(payload)
        result['checks'] = []
        self.assertTrue(judge.validate(result, payload))
        result = answer(payload)
        result['checks'] *= 2
        self.assertTrue(judge.validate(result, payload))
        result = answer(payload)
        result['interpretation_issues'] = [
            {'check_ids': ['invented'], 'issue': 'Issue', 'consequence': 'Effect'}
        ]
        self.assertTrue(judge.validate(result, payload))

    def test_mock_live_and_stop_on_failure(self):
        for mode in ('success', 'truncated', 'invalid', 'error'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                args = self.fixture(root) + [
                    '--output-dir',
                    str(root / 'live'),
                    '--execute',
                    '--model',
                    'mock',
                ]

                def call(provider, model, system, prompt, tokens, timeout, mode=mode):
                    if mode == 'error':
                        raise TimeoutError('PRIVATE_ERROR')
                    content = json.dumps(answer(json.loads(prompt))) if mode != 'invalid' else '{}'
                    return {'usage': 'mock'}, '```json\n' + content + '\n```', mode != 'truncated'

                with (
                    patch.dict(os.environ, {'OPENAI_API_KEY': 'test'}),
                    patch.object(judge.adapter, 'call_api', side_effect=call) as api,
                ):
                    self.assertEqual(judge.main(args), 0 if mode == 'success' else 1)
                    self.assertEqual(api.call_count, 12 if mode == 'success' else 1)
                raw = (root / 'live/results.jsonl').read_text()
                self.assertNotIn('PRIVATE_ERROR', raw)
                records = [json.loads(line) for line in raw.splitlines()]
                self.assertEqual(len(records), 12 if mode == 'success' else 1)
                self.assertTrue((root / 'live/review.md').exists())
                if mode == 'success':
                    self.assertTrue(all(r['fence_stripped'] for r in records))
                    self.assertTrue(all(r['status'] == 'structured_output' for r in records))


if __name__ == '__main__':
    unittest.main()
