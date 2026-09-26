# WBS↔LINK Challenge files

Each set covers one synthetic data-centre project over three monthly reporting periods. The goal is to map the schedule, owner cost data and supporting contractor/fabricator records to the owner Work Breakdown Structure (WBS).

| Set | Folder | Reference |
|---|---|---|
| Practice | `practice/files/` | `practice/answers_practice.csv` (public) |
| Challenge | `holdout/files/` | Hidden; used only by the scoring bot |

The target WBS is `files/owner/owner_scope_structure.xlsx`. Map to the `Cell ID` column.

## What you are trying to do

For each source record, decide whether it belongs to an owner WBS element. The end goal is a reviewable crosswalk between structures that describe the same project differently.

Submit one row for every source record you are attempting to classify. Use the source file's stable line identifier as `record_id`. For the GC SOV, use **Line No** as `record_id`, not Cost Code. Preserve the monthly period as `1`, `2` or `3` and identify the source file in `source_file`.

Required columns:

`period,source_file,record_id,answer,confidence,note`

## Answer values, in plain language

- **WBS Cell ID**: the owner WBS `Cell ID` when the record belongs to that scope.
- **A|B**: two Cell IDs separated by `|` only when one record genuinely spans two WBS cells.
- **NO_WBS**: a valid project record with no applicable owner WBS element, such as an indirect or level-of-effort item. This does **not** mean the record is bad data.
- **NEW_SCOPE**: real scope that is not represented in the current owner WBS and may need a scope/WBS decision rather than an ordinary mapping.
- **UNSURE**: the available evidence is insufficient or conflicting. Do not guess.


## Confidence

For every answered mapping, use exactly `high`, `med` or `low`. Invalid or blank confidence on an answered mapping is rejected. With `UNSURE`, use blank or `low` confidence.

A confident wrong mapping matters because it can pass through a reporting process without being challenged. The benchmark therefore penalizes a wrong `high` answer much more heavily than a wrong `med` or `low` answer.

## Month-to-month ID reuse

Do not assume a retained ID still means the same thing. Compare code, description and context across periods. When an ID and its description disagree, make the mapping you believe is supportable and use the note/exceptions file to explain the conflict.

## Duplicate and blank IDs

Duplicate or blank IDs cannot be scored reliably as unique records. Flag them in the optional exceptions file. The scorer identifies them from the reference records rather than relying on descriptive tags.

## Scoring

The leaderboard uses a published trust-weighted score:

- `+1.0` high-confidence mapping that matches the reference
- `+0.5` medium/low-confidence mapping that matches the reference
- `-5.0` high-confidence mapping that differs from the reference (a **silent error**)
- `-0.5` medium/low-confidence mapping that differs from the reference
- `0` for `UNSURE` / unresolved

Higher trust-weighted score ranks first. Ties are then broken by fewer silent errors, higher precision, higher coverage and earlier submission. Self-reported time is shown for context but is not a ranking tiebreaker.

The public **Practice** set is repeatable. In the repository, score it with:

`python scorer/score.py my_answers.csv --set practice --exceptions my_exceptions.csv`

The downloaded Practice package contains the same scorer and can be run from the extracted folder with the same command.

The hidden **Challenge** set allows **one scored attempt per GitHub user**. Editing an issue does not rescore it. This protects the hidden reference mapping from iterative probing.

## After you finish

The submission form includes a short professional debrief. The questions are there for a reason: the benchmark is intentionally early, and practitioner feedback will help determine what future versions should represent.

Please describe real-world conditions generally and do not post client, employer or confidential project information.
