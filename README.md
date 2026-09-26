# WBS↔LINK Challenge

**Schedule. WBS. Cost. Connected.**

The schedule is developed, structured and coded one way. The cost system another. The owner has a Work Breakdown Structure (WBS). Contractors bring their own coding structures into the mix.

**Same project. Different structures. Somebody has to build the crosswalk.**

## Think you can?

WBS↔LINK is an early-stage idea being pressure-tested with the project controls community.

We've built a fictional capital project across three monthly reporting cycles. Your challenge is to map its schedule, cost and supporting contractor records back to the owner WBS.

**Excel. Power Query. SQL. Python. AI. Whatever you use.**

**Map it → Submit it → See how your approach scores**

Start with the **Practice set**, then take the hidden **WBS↔LINK Challenge** when you're ready.

And don't just give us a score. Tell us what the benchmark misses about real projects. Your experience will help shape future versions of both the challenge and WBS↔LINK.

> ⚠️ **Early beta. Fictional project data only.** See [DISCLAIMER.md](DISCLAIMER.md). Never upload real project, client or employer data.

## Take the challenge (about 1–4 hours)

1. Read the plain-language [How-to guide](challenge/HOW_TO.md).
2. **Download** the [challenge set or practice set](https://zp-projects.github.io/wbs-link/#challenge), or use the `challenge/` folder here.
3. **Map** each schedule activity and cost line (plus supporting contractor records) to a WBS `Cell ID`, or use `NO_WBS`, `NEW_SCOPE` or `UNSURE`. Use Excel, Power Query, SQL, Python, AI, or your own method.
4. **Don't guess.** `UNSURE` is an honest answer.
5. **Submit:** open Issues → New issue → Submit results, drag in your CSV, and complete the short professional debrief.

## Scoring

**A missing mapping creates a question. A confident wrong mapping creates a reporting risk.**

The leaderboard uses a published trust-weighted score:

| Result | Score |
|---|---:|
| High-confidence mapping matches reference | +1.0 |
| Medium/low-confidence mapping matches reference | +0.5 |
| High-confidence mapping differs from reference | -5.0 |
| Medium/low-confidence mapping differs from reference | -0.5 |
| `UNSURE` / unresolved | 0 |

Higher score ranks first. Ties are broken by fewer silent errors, higher precision, higher coverage and earlier submission. Self-reported time is shown for context but does not break ties.

Confidence must be exactly `high`, `med` or `low` for an answered mapping. Invalid or blank confidence is rejected rather than silently changing the score.

## What happens after the mapping

The submission includes a short professional debrief. We are asking practitioners what evidence they relied on, how they think mapping risk should be treated, what makes reconciliation harder on real projects, and how much effort it consumes today. Feedback will help shape future versions of the benchmark and WBS↔LINK.

## What's here and what isn't

- **Here:** fictional project data, the scorer, the submission bot, the challenge website and the public benchmark.
- **Not here:** the private WBS↔LINK mapping engine. It is proprietary and not open source; see [NOTICE](NOTICE).

The longer-term concept is a secure web workflow to connect schedule, cost, WBS and contractor records; propose mappings; surface uncertainty for review; reuse approved relationships; and export standard Excel/CSV crosswalks. That product workflow is still being developed and should not be read as a shipped capability.

## Licences

- Code: [Apache-2.0](LICENSE).
- Data and documentation: [CC BY-NC 4.0](LICENSE-DATA.md).
