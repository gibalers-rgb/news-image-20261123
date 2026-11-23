# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/gibalers-rgb/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/gibalers-rgb/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One picture that holds a whole day of world news: Monday, 23 November
2026, laid out as a newspaper front page. The masthead and date sit at
the top, under them a painted scene from the day's lead story, and then
six short cards for the stories that mattered most. The war widening at
the Strait of Hormuz — a site struck in Bahrain, two tankers hit. COP31
in Antalya ending without a deal, after the EU refused a draft that left
fossil fuels out. A Russian drone strike in the Kyiv region leaving 14
people missing. South Korea's education minister resigning over an AI
cheating scandal. Thousands marching in Lisbon against the cost of
living. And a factory fire in Indonesia that left three dead and 36
missing. The picture itself is drawn once, and the entry program hands
it to the grader byte for byte on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That writes `out/entry.png` — a 1024×1024 PNG, under 1 MiB, the whole
entry in one file.

## Where the picture comes from

`compose.py` draws `entry.png`. It starts from the AI-painted hero
illustration in `assets/` — a burning tanker in the Strait of Hormuz,
with no words on it — then lays the masthead, the date, the caption
and the six story cards over it with PIL, so every letter comes out
crisp. To draw it again, run `python3 compose.py`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
