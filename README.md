# lichess-exporter

Simple prometheus exporter for lichess user metrics.

**Example sample**
```
# HELP puzzle_daily_count puzzle_daily_count
# TYPE puzzle_daily_count gauge
puzzle_daily_count 12.0
# HELP ...
puzzle_weekly_count 22.0
puzzle_monthly_count 43.0
puzzle_total_count 938.0
perfs_rapid_games 31.0
perfs_rapid_rating 1117.0
perfs_rapid_rd 98.0
perfs_rapid_prog 65.0
perfs_puzzle_games 194.0
perfs_puzzle_rating 1651.0
perfs_puzzle_rd 80.0
perfs_puzzle_prog 0.0
```

## Contribute

```
pipenv sync --dev
pipenv run -- black --color --diff --check .
pipenv run -- ruff check .
```

Pre-push git hooks are available using [`lefthook install`](https://github.com/evilmartians/lefthook/tree/master).
