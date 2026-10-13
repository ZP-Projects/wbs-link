# Audio sources

The runtime audio files in this folder are edited excerpts of public-domain /
CC0 recordings. They are layered with the procedural WebAudio sweeteners in
`src/audio/audio.ts`; none of the source recordings is shipped unedited.

## Firearms

- `p226-report-0.wav` through `p226-report-2.wav`
  - Source: **Walther PPQ, 9 mm, near-field gunshots**
  - Collection: The Free Firearm Sound Library
  - License: CC0 1.0
  - Edit: three genuine takes isolated from the 96 kHz/24-bit near microphone.
- `p226-tail-0.mp3` and `p226-tail-1.mp3`
  - Source: the matching PPQ mid-distance microphone takes
  - Edit: direct 90 ms removed; natural field returns trimmed and level-matched.
- `mp5-report-0.wav` through `mp5-report-2.wav`
  - Source: **Carl Gustav M45 / Swedish K, 9 mm SMG, near-field single shots**
  - Collection: The Free Firearm Sound Library
  - License: CC0 1.0
  - Edit: three genuine takes cut to compact direct reports for cyclic playback.
- `mp5-tail-0.mp3` through `mp5-tail-2.mp3`
  - Source: the matching M45 mid-distance microphone takes
  - Edit: late returns level-matched; runtime debounce lets only a burst's final
    round bloom like a standalone shot.
- `sg-report-0.wav` and `sg-report-1.wav`
  - Source: **Benelli Nova, 12 gauge, near-field gunshots**
  - Collection: The Free Firearm Sound Library
  - License: CC0 1.0
  - Edit: two genuine 96 kHz/24-bit takes isolated and browser-mastered.
- `sg-tail-0.mp3` and `sg-tail-1.mp3`
  - Source: the matching Benelli mid-distance microphone takes
  - Edit: direct 90 ms removed; natural outdoor returns trimmed and matched.

Firearm collection and license:
https://opengameart.org/content/the-free-firearm-sound-library

Original recordists: Ben Jaszczak, Brian Nelson, Kevin Heras, and Matthew Nanney.

## Foley

- `step-hard-0.wav` through `step-hard-3.wav`
  - Source: **Footsteps — shoe on concrete**
  - Creator: Joseph Sardin / BigSoundBank (LaSonothèque)
  - Source page: https://bigsoundbank.com/footsteps-shoe-on-concrete-s0514.html
  - License: CC0 1.0
  - Edit: four steps isolated, level-matched, band-limited, and faded.

Ragdoll body drops are procedural (`bodyDrop*` in `src/audio/audio.ts`) — no
recordings. Footstep lands stay on the shoe samples above; corpses never share them.

BigSoundBank license: https://bigsoundbank.com/licenses.html

CC0 does not require attribution; the source record is retained here anyway.
Good provenance costs twelve lines. Bad provenance costs a lawsuit and several
meetings.
