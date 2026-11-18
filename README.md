# Market Ledger news bot

Collects new market stories from five US English Google News search feeds for equities, the economy, currencies, commodities and crypto and uses the ChatGPT-authenticated Codex CLI to draft a headline and a short summary from each story's feed metadata. The hourly service targets at least 10 distinct fresh reports when available and collects up to 25 per run. It automatically publishes new stories. A direct run of the collector without `--publish` still creates drafts for manual review.

## Oracle setup

Clone this repository to `~/news_bot` and the [dashboard](https://github.com/mahmudrafi24/newspaper_dashboard) to `~/newspaper_dashboard` under the same Oracle user. The repositories share `~/news_bot/data/markets.sqlite`. To use a different directory, set an absolute `TECH_NEWS_DATA_DIR` in `~/.config/tech-news/shared.env` and export it for any manual runs.

Python 3.9 or newer and outbound connectivity to Google News and Codex are required. Sign in to Codex with ChatGPT as the service user. If Codex is installed outside `~/.local/bin/codex`, adjust `CODEX_BIN` in the service or set it when running manually. ChatGPT usage limits apply.

```sh
cd ~/news_bot
codex login status
python3 collector.py
mkdir -p ~/.config/systemd/user
cp systemd/* ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now tech-news-ingest.timer
journalctl --user -u tech-news-ingest.service -n 30
```

The timer runs at the start of each hour. The dashboard reports the most recent run. To keep user services running across logout and reboot, the Oracle administrator can run `sudo loginctl enable-linger opc` (replace `opc` with the service username if different). If you already scheduled the earlier combined version, stop its scheduler before enabling this one.

## Public frontend

This repository owns the Market Ledger public frontend in `site/`, including
the October market review. The private editor lives in
[newspaper_dashboard](https://github.com/mahmudrafi24/newspaper_dashboard)
and reads these same frontend files on Oracle when exporting published stories.

- **Cloudflare Workers** — connect this repository in Workers Builds and use
  `npx wrangler deploy`. The committed Wrangler config targets the existing
  `notasmuchhyped` Worker and deploys only `site/`.
- **Cloudflare Pages** — use `sh build-pages.sh` and set the output directory
  to `public`.

These builds serve the static edition. If Oracle manages story publishing,
disable automatic production deployments after the initial deployment. Use the
editor’s Cloudflare deployment settings to publish future exports from Oracle.

## Hourly publishing

Set `CLOUDFLARE_WORKER_NAME=notasmuchhyped`, the absolute `WRANGLER_BIN`
path, and authorized Cloudflare credentials in the private
`~/.config/tech-news/pages.env` file. Use the dashboard setup guide for Pages
instead. Update both repositories on Oracle, then install the updated service.

```sh
cp ~/news_bot/systemd/tech-news-ingest.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user restart tech-news-dashboard.service
systemctl --user start tech-news-ingest.service
```

The hourly timer invokes the service. Codex prepares new stories from source
metadata, SQLite commits them, and the service uploads the public export.
The editor still lets you correct or unpublish a story. Previously saved
drafts require your approval. A failed upload is reported in the editor and
can be retried there or on the next successful hourly run. Disable automatic
production builds when Oracle takes over the public Worker so Git builds
cannot overwrite its published stories.
