# Review round 01

This round uses 16 selected development cases, beginning with six initial contrasts. The packet, CSV, and human annotations are kept local pending approval to publish research data.

Copy the previously prepared files into these locations:

- `Review_Packet.md` into this folder.
- `review_cases.csv` into this folder.
- `judge_development.csv` and `judge_reserved.csv` into `data/` at the repository root.

These paths are ignored by Git. The files already supplied to the project owner remain the source for this round. The private lookup and original coded data stay separate from judge input.

Read the packet's first six cases and add notes by case ID. The script ignores human-review columns. After the review, reconcile criteria and examples before adding them to the judge prompt. Keep a new round's cases and notes in a new `round_NN` folder, rather than overwriting this round.

The script can run without any of these files using another CSV with the five required fields; see [running the judge](../../docs/running-the-judge.md). Its code-only tests use synthetic fixtures and do not require research data or API access.
