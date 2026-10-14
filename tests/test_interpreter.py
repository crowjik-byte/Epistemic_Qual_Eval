"""Offline checks of input boundaries, validation, and the complete run workflow."""

import copy
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
spec = importlib.util.spec_from_file_location('task_interpreter', ROOT / 'src/task_interpreter.py')
interpreter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(interpreter)

QUESTION = 'Explain the distinction.'
RESULT = {
    'requested_judgment': 'Explain a distinction.',
    'scope': 'The requested distinction.',
    'requirements': [
        {
            'id': 'R1',
            'description': 'Explain.',
            'basis': 'explicit',
            'question_quote': 'Explain',
            'justification': 'Requested directly.',
        }
    ],
    'not_required': [],
    'relevant_support': [],
    'ambiguities': [],
    'candidate_checks': [
        {
            'id': 'F1',
            'requirement_ids': ['R1'],
            'check': 'Failure to explain.',
            'relevance': 'Addresses R1.',
            'failure_evidence': 'No distinction provided.',
            'legitimate_countercase': 'A concise explanation.',
        }
    ],
    'format_requirements': [],
    'application_context_needed': ['What distinction is meant?'],
    'framing_concerns': [],
}


class InterpreterTests(unittest.TestCase):
    def test_api_error_is_saved_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'question.json'
            path.write_text(json.dumps({'question': QUESTION}))
            output = Path(tmp) / 'failed'
            with (
                patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-only'}),
                patch.object(
                    interpreter.epistemic_judge,
                    'call_api',
                    side_effect=TimeoutError('private detail'),
                ) as api,
            ):
                code = interpreter.main(
                    [
                        '--input',
                        str(path),
                        '--output-dir',
                        str(output),
                        '--model',
                        'mock-model',
                        '--execute',
                    ]
                )
            self.assertEqual(code, 1)
            self.assertEqual(api.call_count, 1)
            raw = (output / 'results.jsonl').read_text()
            self.assertNotIn('private detail', raw)
            self.assertEqual(json.loads(raw)['status'], 'api_error')

    def test_question_only_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'
            for extra in ['account_text', 'rating', 'reason', 'reference', 'model']:
                path.write_text(json.dumps({'question': QUESTION, extra: 'SENTINEL'}))
                with self.assertRaises(ValueError):
                    interpreter.load_question(path)
            path.write_text(json.dumps({'question': QUESTION}))
            self.assertEqual(interpreter.load_question(path), QUESTION)
            self.assertEqual(json.loads(interpreter.user_prompt(QUESTION)), {'question': QUESTION})

    def test_grounding_references_and_malformed_shapes(self):
        self.assertEqual(interpreter.validate(RESULT, QUESTION), [])
        variants = []
        for key, value in [('question_quote', 'Invented'), ('basis', 'ground_truth')]:
            result = copy.deepcopy(RESULT)
            result['requirements'][0][key] = value
            variants.append(result)
        result = copy.deepcopy(RESULT)
        result['candidate_checks'][0]['requirement_ids'] = ['R999']
        variants.append(result)
        result = copy.deepcopy(RESULT)
        result['requirements'] *= 2
        variants.append(result)
        result = copy.deepcopy(RESULT)
        result['requirements'] = None
        variants.extend([result, [], None])
        for result in variants:
            self.assertTrue(interpreter.validate(result, QUESTION))

    def run_fixture(self, tmp, name, execute=False, response=None):
        path = Path(tmp) / 'question.json'
        path.write_text(json.dumps({'question': QUESTION}))
        output = Path(tmp) / name
        args = ['--input', str(path), '--output-dir', str(output)]
        if execute:
            args += ['--execute', '--model', 'mock-model']
        with (
            patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-only'}),
            patch.object(
                interpreter.epistemic_judge,
                'call_api',
                return_value=response or ({'usage': {'test': True}}, json.dumps(RESULT), True),
            ) as api,
        ):
            code = interpreter.main(args)
        return code, output, api

    def test_dry_run_repeats_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, output, api = self.run_fixture(tmp, 'dry')
            self.assertEqual(code, 0)
            api.assert_not_called()
            requests = [
                json.loads(line) for line in (output / 'requests.jsonl').read_text().splitlines()
            ]
            self.assertEqual(len(requests), 2)
            self.assertEqual(requests[0]['user'], requests[1]['user'])
            self.assertEqual(json.loads(requests[0]['user']), {'question': QUESTION})
            self.assertFalse((output / 'results.jsonl').exists())
            with self.assertRaises(FileExistsError):
                self.run_fixture(tmp, 'dry')

    def test_two_independent_calls_and_saved_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, output, api = self.run_fixture(tmp, 'mock', execute=True)
            self.assertEqual(code, 0)
            self.assertEqual(api.call_count, 2)
            self.assertEqual(api.call_args_list[0], api.call_args_list[1])
            records = [
                json.loads(line) for line in (output / 'results.jsonl').read_text().splitlines()
            ]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]['raw_response']['usage'], {'test': True})
            self.assertIn('Attempt 2', (output / 'review.md').read_text())

    def test_invalid_or_truncated_response_stops_and_retains_raw(self):
        for response in [
            ({'raw': True}, '{bad json', True),
            ({'raw': True}, json.dumps(RESULT), False),
            ({'raw': True}, '{}', True),
        ]:
            with self.subTest(response=response), tempfile.TemporaryDirectory() as tmp:
                code, output, api = self.run_fixture(tmp, 'bad', True, response)
                self.assertEqual(code, 1)
                self.assertEqual(api.call_count, 1)
                record = json.loads((output / 'results.jsonl').read_text())
                self.assertEqual(record['status'], 'invalid_output')
                self.assertEqual(record['raw_response'], {'raw': True})


if __name__ == '__main__':
    unittest.main()
