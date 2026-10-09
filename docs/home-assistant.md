# QobuzProxy on Home Assistant OS and Docker

This fork is a version of [QobuzProxy](https://github.com/leolobato/qobuz-proxy)
packaged with Claude Code as a **Home Assistant add-on** and as a
**ready-to-run container image**.

QobuzProxy turns any DLNA/UPnP player into a fully featured Qobuz Connect
device: for example a free moOde audio player on a Raspberry Pi, Volumio,
upmpdcli, or network speakers and receivers. You control it from the official
Qobuz app, in up to 24-bit/192 kHz hi-res quality.

| What                       | Where                                         |
|----------------------------|-----------------------------------------------|
| Home Assistant add-on repo | `https://github.com/5treamer/qobuz-proxy`     |
| Add-on image               | `ghcr.io/5treamer/qobuz-proxy-ha:<version>`   |
| Standalone container image | `ghcr.io/5treamer/qobuz-proxy:<version>` / `:latest` |
| Platforms                  | `amd64`, `aarch64` / `arm64` (Raspberry Pi 4/5) |

## Install on Home Assistant OS

[![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2F5treamer%2Fqobuz-proxy)

Or manually:

1. **Settings → Add-ons → Add-on Store** → **⋮** (top right) → **Repositories**.
2. Add `https://github.com/5treamer/qobuz-proxy` and close the dialog.
3. Reload the page, find **Qobuz Proxy** and click **Install**.
4. Enable **Start on boot** and **Watchdog**, then **Start**.
5. **Open Web UI**, click **Log in to Qobuz**, then **+ Add Speaker**.
6. Select the speaker in the Qobuz app's output picker.

Works on Home Assistant OS and Supervised installations. Home Assistant
Container/Core have no add-ons; use the container image below instead.

## Run as a container (Docker, Portainer, Unraid, Synology, ...)

```bash
docker run -d --name qobuz-proxy --network host --restart unless-stopped \
  -v ./data:/data \
  ghcr.io/5treamer/qobuz-proxy:latest
```

Or with Docker Compose:

```yaml
services:
  qobuz-proxy:
    image: ghcr.io/5treamer/qobuz-proxy:latest
    container_name: qobuz-proxy
    network_mode: host   # required for mDNS discovery
    volumes:
      - ./data:/data
    restart: unless-stopped
```

Then open `http://<host-ip>:8689`, log in to Qobuz and add your speakers.

## How updates work

Updates are done by hand, so nothing from the original project reaches this
fork (or your Home Assistant) without review:

1. On the repository page, click **Sync fork → Update branch** to merge the
   latest upstream changes into `main` (or merge them locally with git).
2. Set `version` in `ha-addon/config.yaml` to the new version from
   `pyproject.toml` and add an entry to `ha-addon/CHANGELOG.md`.
3. Push to `main`. The **Home Assistant add-on** workflow
   (`.github/workflows/ha-addon.yml`) builds both images for amd64 and arm64
   and pushes them to GHCR with the version tag and `latest`.
4. Home Assistant shows the update once the new `version` is on `main`
   and the image exists.

Packaging-only changes (no new upstream version) use a fourth version part,
e.g. `1.7.6` → `1.7.6.1`.

## Maintainer notes

One-time setup for this fork:

1. **Actions → enable workflows** (GitHub disables workflows on new forks).
2. Run **Home Assistant add-on** once via **Run workflow**.
3. Make both packages public: profile → **Packages** → `qobuz-proxy-ha` and
   `qobuz-proxy` → **Package settings** → **Change visibility → Public**.
   Without this, Home Assistant cannot pull the image.
4. Repository **About** (gear icon): set a description and topics so people
   can find the fork, e.g. description
   *"QobuzProxy 1.7.6, packaged with Claude Code: turns any DLNA/UPnP player (moOde, Volumio, ...) into a Qobuz Connect device. Home Assistant add-on + Docker image."*
   and topics `qobuz`, `qobuz-connect`, `dlna`, `upnp`, `moode`, `moode-audio`,
   `volumio`, `home-assistant`, `home-assistant-addon`, `hassio-addon`,
   `docker`, `raspberry-pi`, `hi-res-audio`.

## Files

| Path                                  | Purpose                                   |
|---------------------------------------|-------------------------------------------|
| `repository.yaml`                     | Marks the repo as an add-on repository    |
| `ha-addon/config.yaml`                | Add-on manifest (version, ports, options) |
| `ha-addon/Dockerfile`, `ha-addon/run.sh` | Add-on image and entry point           |
| `ha-addon/README.md`, `ha-addon/DOCS.md`, `ha-addon/CHANGELOG.md` | Texts shown in the add-on store |
| `.github/workflows/ha-addon.yml`      | Builds and pushes both images             |
