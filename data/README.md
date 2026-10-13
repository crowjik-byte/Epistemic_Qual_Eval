# Judge-facing data

| File | Rows | Use |
| --- | ---: | --- |
| `judge_development.csv` | 1,040 | Initial judge development and review. |
| `judge_reserved.csv` | 269 | Later check after freezing a judge version. |

The files are not included in the public repository. Copy the prepared judge-facing CSVs into this folder locally. Their publication is pending explicit approval.

Both have exactly `case_id`, `question`, `account_text`, `rating`, and `reason`. The original text and rating strings are preserved; rows were shuffled with seed 20261013 and assigned neutral IDs. Model identity, experimental labels, old codes, evidence notes, and resolution history were removed from judge inputs.

The split reserves the entire question variant containing `This holds for established research terms too:`. Identical question/account combinations remain together. It does not separate all similar reasoning across the two files: underlying accounts and related wording recur, and some examples were discussed before splitting. This is a preliminary wording-transfer check, not a secret or independent new-domain benchmark.

These files derive from the user's 1,309-row `merged_coded.csv`. The original and the ID-to-metadata lookup remain outside the public repository. Keep them in a separate private location; `private/`, `data/raw/`, `merged_coded.csv`, and `private_case_lookup.csv` are ignored. Removing metadata does not hide the traditions named in the account or all stylistic clues about the responding model.

Treat these base files as stable inputs. Keep annotations in the relevant review round. If cases or splits change, make a deliberate versioned update and record why. Do not include the reserved file in routine tuning runs.
