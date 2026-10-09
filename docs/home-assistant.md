# QobuzProxy on Home Assistant OS and Docker

This fork packages [QobuzProxy](https://github.com/leolobato/qobuz-proxy) as a
**Home Assistant add-on** and as a **ready-to-run container image**, both
automatically kept on the latest upstream release.

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

- **Sync upstream** (daily, `.github/workflows/sync-upstream.yml`) merges the
  upstream `main` branch, sets the add-on `version` in `ha-addon/config.yaml` to
  the upstream version from `pyproject.toml`, and starts the image build.
- **Home Assistant add-on** (`.github/workflows/ha-addon.yml`) builds both images
  for amd64 and arm64 and pushes them to GHCR with the version tag and `latest`.
- Home Assistant shows the update as soon as the new `version` is on `main`
  and the image exists.

## Maintainer notes

One-time setup for this fork:

1. **Actions → enable workflows** (GitHub disables workflows on new forks,
   including scheduled ones).
2. Run **Home Assistant add-on** once via **Run workflow**.
3. Make both packages public: profile → **Packages** → `qobuz-proxy-ha` and
   `qobuz-proxy` → **Package settings** → **Change visibility → Public**.
   Without this, Home Assistant cannot pull the image.
4. Repository **About** (gear icon): set a description and topics so people
   can find the fork, e.g. description
   *"Qobuz Connect for Sonos & DLNA speakers – Home Assistant add-on and Docker image (QobuzProxy)"*
   and topics `qobuz`, `qobuz-connect`, `home-assistant`, `home-assistant-addon`,
   `hassio`, `hassio-addon`, `sonos`, `dlna`, `upnp`, `docker`, `hi-res-audio`.

If **Sync upstream** fails (merge conflict, or upstream changed files under
`.github/workflows/`, which `GITHUB_TOKEN` may not push), click **Sync fork** on
the repository page, fix conflicts if any, and run **Sync upstream** again to
bump the version.

Packaging-only changes (no new upstream version) need a manual `version` bump
in `ha-addon/config.yaml`, e.g. `1.7.6` → `1.7.6.1`, plus a changelog entry.

## Files

| Path                                  | Purpose                                   |
|---------------------------------------|-------------------------------------------|
| `repository.yaml`                     | Marks the repo as an add-on repository    |
| `ha-addon/config.yaml`                | Add-on manifest (version, ports, options) |
| `ha-addon/Dockerfile`, `ha-addon/run.sh` | Add-on image and entry point           |
| `ha-addon/README.md`, `ha-addon/DOCS.md`, `ha-addon/CHANGELOG.md` | Texts shown in the add-on store |
| `.github/workflows/ha-addon.yml`      | Builds and pushes both images             |
| `.github/workflows/sync-upstream.yml` | Daily upstream sync and version bump      |
