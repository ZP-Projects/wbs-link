# WBS↔LINK Challenge

**Schedule. WBS. Cost. Connected.**

Major projects often describe the same work differently across schedule and cost systems:

| Structure | Example |
|---|---|
| Schedule activity | `ST3-ELEC-SWG` |
| WBS element | `STN3 / ELECTRICAL / SWITCHGEAR` |
| Cost code | `4600.31.07` |

Same work. Different structures. **WBS↔LINK** maps schedule activities and cost structures to a common Work Breakdown Structure, and surfaces the links that need review. This repository is its open challenge: a synthetic project for testing how well *any* method can rebuild those links.

> ⚠️ **Early beta. Synthetic data only.** See [DISCLAIMER.md](DISCLAIMER.md). Never upload real project, client or employer data.

## Take the challenge (about 1–4 hours)
1. **Download** the [challenge set or practice set](https://zp-projects.github.io/wbs-link/#challenge), or use the `challenge/` folder here.
2. **Map** each schedule activity and cost line (plus supporting contractor records) to a WBS element in `files/owner/owner_scope_structure.xlsx` (the `Cell ID` column). Or mark it `LEGIT_ORPHAN`, `NEW_SCOPE` or `UNSURE`. Use Excel, SQL, Python, AI, or your own method. Template: `challenge/ANSWER_TEMPLATE.csv`.
3. **Don't guess.** `UNSURE` is an honest answer.
4. **Submit:** open [Issues → New issue → Submit results](../../issues/new/choose), drag in your CSV, and note your minutes. Practice is repeatable; the hidden Challenge set allows one scored attempt per GitHub user. A bot replies with your score.

## Scoring
**A missing mapping creates a question. A confident wrong mapping creates a reporting risk.**

| Measure | Meaning |
|---|---|
| **Silent errors** | Wrong answers marked high confidence. Counts most |
| **Correct answers** | More correct answers rank next, preventing strategic abstention |
| Precision | Correct ÷ answered |
| Coverage | Answered ÷ scored records |
| Time | Your reported minutes |

## What's here and what isn't
- **Here:** synthetic data, the scorer, the submission bot, and the challenge website (`docs/`).
- **Not here:** the WBS↔LINK engine. It's proprietary and not open source; see [NOTICE](NOTICE).

## Licences
- Code: [Apache-2.0](LICENSE).
- Data and documentation: [CC BY-NC 4.0](LICENSE-DATA.md).

