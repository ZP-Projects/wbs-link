# Product Owner corrections — issue 73

References: findings 6118310918; previous Engineering handoff 6118031705;
assurance reconciliation 6118143806. Product Owner visual acceptance is pending.

The website branch is based on the unchanged Fresh Eyes candidate
4826baa68a51834d7609b5170f9b41f04cbaa7f6. Product and marketing source heads remain
9ae7df438da5968b5d5ca3d7dbd1e7fc4291d9c1 and
c7e0858270b259526413b689551cc722cad61d00.

The new integration diagram connects every source through Owner WBS, exposes an
illustrative missing-evidence link and ends at management insight. No direct
source-to-source authority or health score is asserted. The proof section uses
deliberate actual-document excerpts, readable exact Action text, links to complete
page images and four native chart images. Images use natural aspect ratios and
containment. Before/after evidence is retained at 1440 and 390 pixels.

Video 1's supplied MP4 has an AAC stream, but its mean/peak levels were
-47.0/-40.6 dBFS. The correction applies 26 dB gain: -21.0/-14.6 dBFS. The original
file is preserved; extracted H.264 streams are byte-identical, SHA-256
0af1e65bef96661b63cf9ab357502ede9d0b27eb9810aa93eda3fbdcdbec3b59.
There are no separately supplied audio stems in the current repository. Historical
generation scripts describe older synthesized audio, not the supplied film's stems.

Video 2 is an 80-second 1920×1080 H.264/yuv420p MP4 with 48 kHz stereo AAC,
an original harmonic/percussion score, descriptive English captions and actual
HarbourLink candidate UI. It includes genuine browser interactions: WBS perspective
selection, source Why disclosure, professional-decision/approval history scrolling
and Cycle 2 revisions. Edited recordings are combined with magnified actual PDF,
workbook and chart evidence, icons, quiet transitions and a navigation trail. It is
an edited demonstration of the approved synthetic Cycle 2 position and Version 1/2
history, not a continuous ingestion/approval recording. No approval action is
simulated. `docs/videos/source/HARBOURLINK_STORYBOARD.txt` records the sequence;
the contact sheet samples the actual final encoded MP4.

TEST: all existing commercial static/asset/claim/link/film checks pass; additive
Product Owner correction checks pass. No existing regression was removed or weakened.
Four browser playback cases pass (two films × desktop/phone emulation): trusted
Play-with-sound click, advancing playback, muted=false, volume=1, running Web Audio
context and nonzero decoded waveform; captions load. Both widths have no horizontal
overflow. Full final MP4 decode and whitespace checks pass. Product code/tests and
governed intelligence are unchanged, so the prior complete baseline/source suites
were not rebuilt or rerun for this presentation-only change.

LIMITS: fetching the actual hosted Video 1 is blocked by the configured proxy:
CONNECT tunnel failed, HTTP 403, server envoy. No policy/proxy/security changes were
made. Candidate-source audio is corrected and locally verified; the hosted service
has not received it. Browser emulation/decoded waveform is not a physical-phone,
Safari/native mobile, speaker/listening or native Microsoft Office acceptance test.
Soundtrack is instrumental; captions describe the demonstration rather than
transcribe spoken narration. Creative acceptance remains with the Product Owner.

The already validated 16-file ZIP was not rebuilt. It was independently verified on
private delivery commit ae6093017398afa54576b0c50f138dbfc041b716, with SHA-256
9bd9342fb086b3820ffde5a6d6e8eee91d842d4edc0e4076da6ea112c01558b5,
8,486,808 bytes. Product Owner confirmed “Download succeeded” in Codex; GitHub
confirmation comment 6118489625. No merge, deployment, approval or external release.
