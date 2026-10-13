"""No network or API credentials required."""
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'src' / 'epistemic_judge.py'
spec = importlib.util.spec_from_file_location('epistemic_judge', SCRIPT)
judge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(judge)


class JudgeTests(unittest.TestCase):
    def test_human_notes_are_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.csv'
            with path.open('w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(judge.FIELDS) + ['human_verdict'])
                writer.writeheader()
                writer.writerow(dict(case_id='C1', question='Assess this.', account_text='A claim.',
                                     rating='2', reason='A reason.', human_verdict='PRIVATE_SENTINEL'))
            cases = judge.load_cases(path, set(), 0)
            self.assertEqual(set(cases[0]), set(judge.FIELDS))
            self.assertNotIn('PRIVATE_SENTINEL', judge.user_prompt(cases[0]))

    def test_invented_quote_and_inconsistent_verdict_are_rejected(self):
        case = dict(case_id='C1', question='Assess this.', account_text='Below awareness.',
                    rating='2', reason='Therefore impossible to study.')
        result = dict(case_id='C1', question_standard='Testability', verdict='supported_failure',
                      findings=[dict(code='ACCESS_LEAP', reason_quote='impossible to study',
                                     source_field='account_text', source_quote='Below awareness.',
                                     explanation='A leap.', strongest_defense='Limited access.',
                                     defense_assessment='Does not establish impossibility.')],
                      rationale='Fixture.', materiality='weakens_justification',
                      uncertainty_reasons=[], other_issues=[])
        self.assertEqual(judge.validate_result(result, case), [])
        result['findings'][0]['reason_quote'] = 'Fabricated evidence'
        self.assertTrue(judge.validate_result(result, case))
        result['findings'][0]['reason_quote'] = 'impossible to study'
        result['verdict'] = 'no_failure_established'
        self.assertTrue(judge.validate_result(result, case))

    @unittest.skipUnless(all((ROOT / p).exists() for p in (
        "data/judge_development.csv", "data/judge_reserved.csv",
        "review/round_01/review_cases.csv")), "Local research data not installed")
    def test_review_cases_are_exact_development_subsets(self):
        dev = judge.load_cases(ROOT / 'data/judge_development.csv', set(), 0)
        reserved = judge.load_cases(ROOT / 'data/judge_reserved.csv', set(), 0)
        review = judge.load_cases(ROOT / 'review/round_01/review_cases.csv', set(), 0)
        by_id = {r['case_id']: r for r in dev}
        self.assertEqual((len(dev), len(reserved), len(review)), (1040, 269, 16))
        self.assertFalse(set(by_id) & {r['case_id'] for r in reserved})
        for row in review:
            self.assertEqual(row, by_id[row['case_id']])
        self.assertFalse({(r['question'], r['account_text']) for r in dev} &
                         {(r['question'], r['account_text']) for r in reserved})

    def test_dry_run_and_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / 'input.csv'
            with input_path.open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=judge.FIELDS)
                writer.writeheader()
                for cid in ('C1', 'C2'):
                    writer.writerow(dict(case_id=cid, question='Assess this.',
                                         account_text='A claim.', rating='2', reason='A reason.'))
            output = Path(tmp) / 'preview'
            cmd = [sys.executable, str(SCRIPT), '--input',
                   str(input_path),
                   '--output-dir', str(output), '--limit', '2']
            first = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn('No API calls made', first.stdout)
            manifest = json.loads((output / 'manifest.json').read_text())
            self.assertFalse(manifest['execute'])
            self.assertEqual(len(manifest['case_ids']), 2)
            self.assertFalse((output / 'results.jsonl').exists())
            before = (output / 'manifest.json').read_bytes()
            second = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual((output / 'manifest.json').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
