# THE WORLD TODAY — 21 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Sipalingtesnet/news-image-20261121-entry-ris/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Sipalingtesnet/news-image-20261121-entry-ris/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image summing up the world news of Saturday 21 November 2026, rendered as a
newspaper front page for the [make.fun bounty](https://make.fun/bounty/news-image-20261121).
`entry.png` is a 1024x1024 picture showing the day's six biggest stories plus a
news ticker along the bottom.

## The six stories in the image

1. **Russian missiles land in Poland** — the lead story: two Russian missiles and
   a suspected drone came down in Poland; a schematic map marks the impact sites.
2. **US stocks fall about 3.7%** — an AI-share sell-off pushes the S&P 500 into
   correction (the Nasdaq loses more than 5%), drawn as a falling red chart.
3. **Cyclone Akvan crosses the Odisha coast** — landfall near Gopalpur with
   strong winds and heavy rain, drawn as a cyclone spiral.
4. **Coalition-of-the-willing Berlin summit on Ukraine** — leaders meet in
   Berlin with President Zelenskyy and US negotiators, drawn as a summit table
   with Ukrainian, German and US flags.
5. **GTA 6 passes $2.36 billion in launch revenue** — more than 24.5 million
   copies sold, drawn as a game controller.
6. **Daraxonrasib cancer-pill trial breakthrough** — tumours stopped growing in
   nearly all patients and cancer became undetectable in one in 12, drawn as a
   capsule in the bottom strip.

The bottom ticker adds: UK and EU sign food, carbon and youth-mobility deals —
Trump-Xi-Putin summit ends with few results — World Court: Myanmar committed
genocide against Rohingya — India 159 for 1 at stumps in the Wellington Test.

## How to run

- `python3 main.py` — copies `entry.png` byte-for-byte to `/output/entry.png`
  (creating `/output` if needed) and exits 0.
- `python3 generate_image.py` — regenerates `entry.png` from scratch using
  Pillow (DejaVu fonts); requires no input files.

## Determinism

The program is fully deterministic: the same bytes are produced on every run.
It uses no network, no randomness and no timestamps.
