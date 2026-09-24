# Challenge files

| Set | Folder | Answers |
|---|---|---|
| Practice | `practice/files/` | `practice/answers_practice.csv` (public) |
| Challenge | `holdout/files/` | Hidden (`answers_holdout.enc`, used only by the scoring bot) |

Each set covers one synthetic data-centre site over 3 monthly reporting periods: an owner, one GC, and several subcontractors and fabricators. `files/manifest.yaml` lists the files for each month. The target WBS is `files/owner/owner_scope_structure.xlsx`: each `Cell ID` is a WBS element.

**Answer values:**
- a WBS element ID (the `Cell ID`) (use `A|B` for a record that genuinely spans two cells)
- `LEGIT_ORPHAN`: valid, but no owner scope (e.g. indirect costs, LOE)
- `NEW_SCOPE`
- `UNSURE`

**Confidence:** `high`, `med` or `low`. A wrong `high` answer counts as a **silent error**.
