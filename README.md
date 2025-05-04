# Archiver – Twitch backup toolkit **v2**  
*A cleaned-up, config-first rewrite of the original v1 archiver.*

The v2 Twitch Archiver pulls down **VODs, thumbnails, chat (upcoming)** and core metadata for every channel you list in a single `.config` file.  Secrets stay in `.env`, and each job writes its own colourised log so you always know what happened.

---

## Key features

| Feature | Script / module | Notes |
|---------|-----------------|-------|
| Download **one VOD** on demand | `download_vods.py` → `video_utils.download_vod()` (`yt-dlp`) | `--channel` and `--vod-id` CLI flags |
| **Background VOD watcher** (poller) | `start_download_vods.py` | Reads `.config`, checks Helix every _N_ minutes, runs `download_vods.py` for anything new |
| Lightweight **SQLite catalogue** | `modules/db_utils.py` | Table `vods` stores id, folder, title, timestamp – handy for dashboards |
| **Modular helpers** | `modules/*.py` | OAuth calls, yt-dlp/ffmpeg wrappers, JSON I/O, duration parsing, structured logging |
| **Token guide** | `refresh_env.instruct.md` | Step-by-step OAuth flow: URL → `curl` exchange → validation |

---

## Repository layout (abridged)

```

Archiver/
├─ archiver.scripts/
│  └─ Archiver-twitch-v2/      ← v2 code
│     ├─ .env
│     ├─ .config               # channels + poll interval
│     ├─ download\_vods.py
│     ├─ start\_download\_vods.py
│     ├─ modules/
│     └─ logs/
└─ persons/                     ← all archived media appears here

````

---

## ⚙Requirements

* **Python 3.11+** (sample venv targets 3.12.8)  
* **yt-dlp** 2025.02+  
* **ffmpeg / ffprobe** (bundled for Windows in `.dependencies/` or on `$PATH`)  
* **Twitch OAuth** scopes:  
`user:read:email user:read:broadcast channel:read:subscriptions chat:read chat:edit user_subscriptions`

All Python packages live in `requirements.txt`.

---

## First-time setup

1. **Install dependencies**
```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
````

2. **Create `.env`**
```ini
   CLIENT_ID=xxxxxxxxxxxx
   CLIENT_SECRET=xxxxxxxxxxxx
   ACCESS_TOKEN=…
   REFRESH_TOKEN=…
   REDIRECT_URI=http://localhost
```
> Need tokens?  See `refresh_env.instruct.md`.

3. **Create `.config`**
```jsonc
   {
     "channels": ["MichiMochievee"],
     "vod_check_interval_minutes": 15
   }
```

4. Ensure `yt-dlp.exe`, `ffmpeg.exe`, `ffprobe.exe` are in `.dependencies/` or on `%PATH%`.

---

## Usage

### Download a single VOD

```bash
python download_vods.py --channel MichiMochievee --vod-id 2388768765
```

Each run creates:

```
persons/MichiMochievee/twitch/vods/2025-02-23T03-11-53Z_v2388768765_Example-Title/
├─ thumbnails/thumbnail_[number/main].jpg
├─ vod.mp4
├─ chat.vod.sqlite
└─ metadata.vod.json
```

> **Save-path format:** `[date]_[id]_[title]` (ISO date with `:` replaced by `-`).

### Run the automatic poller

```bash
python start_download_vods.py
```

* Loops over every channel in `.config["channels"]`.
* Every *vod\_check\_interval\_minutes* it asks the Helix API for new VOD IDs and spawns `download_vods.py`.

Stop the script with **Ctrl-C** or run it in a tmux/session manager.

---

## Logs & debugging

Log files live in `archiver.scripts/twitch_archiver/logs/` (e.g. `download_vods.log`).
Console shows **INFO** messages; files receive full **DEBUG** detail.  Adjust in `modules/logging_setup.py`.
