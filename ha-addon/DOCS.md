# Qobuz Proxy

QobuzProxy turns any DLNA/UPnP player (moOde audio, Volumio, upmpdcli,
network speakers and receivers, ...) into a Qobuz Connect device that you
control from the official Qobuz app.

## Setup

1. Start the add-on.
2. Click **Open Web UI** (port 8689 on your Home Assistant host).
3. Click **Log in to Qobuz** and sign in with your Qobuz account.
4. Click **+ Add Speaker**, pick a discovered DLNA device (or enter its IP) and save.
5. In the Qobuz app, open the output picker and select the speaker by its name.

The Qobuz login and speaker configuration are stored in the add-on's persistent
storage (`/data/credentials.json`, `/data/config.yaml`). They survive restarts
and updates and are included in Home Assistant backups.

## Options

| Option      | Description                                       |
|-------------|---------------------------------------------------|
| `log_level` | `debug`, `info` (default), `warning` or `error`   |

## Audio quality

With `auto` (default), QobuzProxy asks each speaker which formats it supports
and picks the best one: MP3 320 kbps, FLAC CD (16-bit/44.1 kHz), FLAC Hi-Res
(24-bit/96 kHz) or FLAC Hi-Res (24-bit/192 kHz). You can override it per
speaker in the web UI.

## Networking

- The add-on uses the host network. The Qobuz app finds it via mDNS, so your
  phone and Home Assistant must be on the same network (or mDNS must be
  forwarded between VLANs).
- Ports 8689 (web UI + Qobuz Connect discovery) and 7120 (audio proxy for the
  speakers) must be free on the host. Additional speakers use the next ports
  (8690, 7121, ...).
- Open the web UI via your host's IP, not through a reverse proxy path:
  the Qobuz login redirects back to the address you opened it from.

## Troubleshooting

- **Speaker does not show up in the Qobuz app**: check that phone and Home
  Assistant are on the same network, then set `log_level` to `debug` and
  check the add-on log.
- **Plays, but no sound**: make sure the speaker can reach port 7120 on your
  Home Assistant host (firewall/VLAN rules).
- **Bugs in QobuzProxy itself**: report them upstream at
  https://github.com/leolobato/qobuz-proxy/issues
