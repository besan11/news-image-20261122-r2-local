# Sunday 22 November 2026 — World news in one front page, 35 stories

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/besan11/news-image-20261122-r2-local/rank.svg)](https://make.fun/c/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/besan11/news-image-20261122-r2-local/reward.svg)](https://make.fun/c/news-image-20261122)

One 1024×1024 front page that sums up Sunday 22 November 2026: three
leads (two tankers hit leaving Hormuz, COP31 nears a deal in Antalya, the
Russian cargo ship Sparta II ablaze in the Baltic), ten illustrated panels,
a numbered world map, 22 more stories in brief, and a boxed DATE CHECK
that names what was left out as earlier news. Every story is drawn in
code — no photos, no downloaded art.

This is round 2. Round 1 scored 98.2336% (rank #70), just 0.11 points
below the paid zone. The gap study for this round
(`news-image-20261122-r2-gap-study.md`, kept outside this repo) found
round 1 lost on story selection, not on craft: it led with Eisenkot's
Israeli domestic politics, missed nine of the day's biggest stories
(Ukraine's 400-drone barrage, the Chapo Isidro capture, the FBI crime
database breach, the Las Vegas pole, the Belgian strike, the Gaza aid
van, Iran's power rationing, Rutte's Warsaw pledge, the Bayelsa boat),
and put 13 of 31 stories in the Middle East with one in Asia-Pacific
and none in Oceania. Round 2 fixes exactly that: the #1 entry's lead
trio (Hormuz + COP31 + Sparta II), all nine missing stories as panels,
and a balanced 35-story set across six regions.

## How it works

- `render.py` draws `entry.png` with Pillow from the story list in the
  same file: masthead, six-number ticker, coloured region chips, three
  leads with a fact pill inside each scene, ten panels with a red
  kicker banner and a number badge, a simplified world map with
  numbered pins, 22 briefs, a DATE CHECK box, and a footer.
- `main.py` (standard library only) copies `entry.png` into
  `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the bytes. It never
  deletes the output directory or anything in it — in the grader the
  output directory is a bind mount, and deleting it fails.
- `check_entry.py` verifies the PNG (magic, ≤ 1 MiB, 1024×1024) and
  runs `main.py` twice, checking the two outputs are byte-identical
  and that a pre-existing file in the output directory survives.
- `fonts/` holds the DejaVu TTF files the renderer uses, as files —
  never base64.

## How to run

```sh
python3 render.py        # draws entry.png
python3 check_entry.py   # verifies entry.png + two-run reproducibility
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

Each story names its source beside it on the page (Reuters, AP, AFP,
UKMTO, Formula 1, and others). The full verification notes, including
what was checked fresh, what was carried from round 1, and what was
deliberately left out, are in `NOTES.md`.

Referral code: `jpgk45b3` — https://make.fun/r/jpgk45b3
