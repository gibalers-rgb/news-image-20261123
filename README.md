# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/gibalers-rgb/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/gibalers-rgb/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world news of Monday, 23 November 2026: a
newspaper front page — masthead and date, a painted scene of the day's
lead story, and the six stories that defined the day. The Iran–US war
widening at the Strait of Hormuz, with a site struck in Bahrain and two
tankers hit; COP31 ending with no deal after the EU rejected a draft that
omitted fossil fuels; a Russian drone strike leaving 14 missing in the
Kyiv region; South Korea's education minister resigning over an AI
cheating scandal; thousands marching in Lisbon against the cost of living;
and a factory fire in Indonesia leaving three dead and 36 missing. The
image is drawn once (AI illustration + sharp rendered text) and the
program copies it to the output, byte for byte, every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024 PNG, under 1 MiB) — the whole entry.

## How the image was made

`compose.py` builds `entry.png`: it takes the AI-generated hero
illustration in `assets/` (a burning tanker at the Strait of Hormuz, no
text) and lays out the masthead, date, caption and six story cards with
PIL, so every word is crisp and legible. Rebuild it with
`python3 compose.py`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
