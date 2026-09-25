# WBS↔LINK Challenge files

Each set covers one synthetic data-centre project over three monthly reporting periods. The goal is to map the schedule, owner cost data and supporting contractor/fabricator records to the owner Work Breakdown Structure (WBS).

| Set | Folder | Answers |
|---|---|---|
| Practice | `practice/files/` | `practice/answers_practice.csv` (public) |
| Challenge | `holdout/files/` | Hidden; used only by the scoring bot |

The target WBS is `files/owner/owner_scope_structure.xlsx`. Map to the `Cell ID` column.

## What to answer

Submit one row for every source record you are attempting to classify. Use the source file's stable line identifier as `record_id`. For the GC SOV, use **Line No** as `record_id`, not Cost Code. Preserve the monthly period as `1`, `2` or `3` and identify the source file in `source_file`.

Required answer columns:

`period,source_file,record_id,answer,confidence,note`

## Answer values

- **WBS Cell ID**: use the owner WBS `Cell ID` when the record belongs to that scope.
- **A|B**: use two Cell IDs separated by `|` only when a single record genuinely spans two WBS cells.
- **LEGIT_ORPHAN**: a valid project record that intentionally has no owner WBS cell, such as an indirect/LOE item. It is not new owner scope.
- **NEW_SCOPE**: real scope that is not represented in the current owner WBS and therefore would require a scope/WBS decision rather than an ordinary mapping.
- **UNSURE**: use when the evidence is insufficient or conflicting. Do not guess.

## Confidence

Use `high`, `med` or `low`. **Blank confidence is treated as `high`**, so fill it in deliberately. A wrong high-confidence answer is a **silent error** and is penalized first.

## Month-to-month ID reuse

Do not assume a retained ID still means the same thing. Compare code, description and context across periods. When an ID and its description disagree, make the mapping you believe is supportable and use the note/exceptions file to explain the conflict.

## Duplicate and blank IDs

Duplicate or blank IDs cannot be scored reliably as unique records. Flag them in the optional exceptions file. The scorer determines these from the actual truth rows rather than relying on tags.

## Scoring and attempts

Ranking is trust-first: **fewest silent errors, then most correct answers, then precision, coverage and time**. This prevents a tiny high-precision submission from outranking a strong complete submission.

The public **Practice** set is repeatable and can be scored locally with:

`python scorer/score.py my_answers.csv --set practice --exceptions my_exceptions.csv`

The hidden **Challenge** set allows **one scored attempt per GitHub user**. Editing an issue does not rescore it. This protects the holdout from iterative probing.
