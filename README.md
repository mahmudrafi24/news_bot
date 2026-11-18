# Tech Brief news bot

Collects new technology stories from the US English Google News feed and uses the ChatGPT-authenticated Codex CLI to draft a headline and a short summary from each story's feed metadata. Up to 12 stories are drafted per run. Drafts go to SQLite for review. The bot never publishes.

## Oracle setup

Clone this repository to `~/news_bot` and the [dashboard](https://github.com/mahmudrafi24/newspaper_dashboard) to `~/newspaper_dashboard` under the same Oracle user. The repositories share `~/news_bot/data/news.sqlite`. To use a different directory, set an absolute `TECH_NEWS_DATA_DIR` in `~/.config/tech-news/shared.env` and export it for any manual runs.

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
