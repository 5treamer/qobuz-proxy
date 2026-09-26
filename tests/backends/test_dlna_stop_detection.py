"""How the DLNA poll loop reads a renderer that stopped.

Covers a GitHub #33 follow-up: another controller stopping the renderer must not
look like a natural track end (the queue auto-advanced and took the renderer
back).
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from qobuz_proxy.backends.dlna.backend import DLNABackend
from qobuz_proxy.backends.dlna.client import DLNAClient
from qobuz_proxy.backends.types import PlaybackState

QOBUZ_URI = "http://proxy:7120/audio/123.flac"


@pytest.fixture
def backend():
    backend = DLNABackend("192.0.2.1", name="Kitchen")
    backend._current_proxy_url = QOBUZ_URI
    backend._state = PlaybackState.PLAYING
    backend._duration_ms = 200_000
    backend._playback_started_at = 0.0  # well past the start grace period
    client = AsyncMock(spec=DLNAClient)
    client.get_media_info.return_value = QOBUZ_URI
    client.get_transport_info.return_value = "STOPPED"
    client.get_position_info.return_value = 0
    backend._client = client
    backend.ended = MagicMock()
    backend.interrupted = MagicMock()
    backend.on_track_ended(backend.ended)
    backend.on_playback_interrupted(backend.interrupted)
    return backend


async def poll(backend, monkeypatch, times: int = 1) -> None:
    backend._is_connected = True
    ticks = 0

    async def tick(_):
        nonlocal ticks
        ticks += 1
        if ticks > times:
            backend._is_connected = False

    monkeypatch.setattr("qobuz_proxy.backends.dlna.backend.asyncio.sleep", tick)
    await backend._poll_state_loop()


async def test_stop_mid_track_is_not_a_track_end(backend, monkeypatch):
    backend._furthest_position_ms = 20_000
    await poll(backend, monkeypatch)
    backend.ended.assert_not_called()
    backend.interrupted.assert_called_once_with(20_000)


async def test_position_read_after_the_stop_does_not_hide_an_early_stop(backend, monkeypatch):
    """The player's monitor reads RelTime 0 right after a foreign Stop."""
    backend._furthest_position_ms = 20_000
    await backend.get_position()  # renderer now reports 0:00:00
    assert backend._position_ms == 0
    await poll(backend, monkeypatch)
    backend.interrupted.assert_called_once_with(20_000)
    backend.ended.assert_not_called()


async def test_stop_near_the_end_is_a_track_end(backend, monkeypatch):
    backend._furthest_position_ms = 198_000
    await poll(backend, monkeypatch)
    backend.ended.assert_called_once()
    backend.interrupted.assert_not_called()


async def test_stop_without_a_known_position_is_a_track_end(backend, monkeypatch):
    """Renderers that never report a position must keep advancing."""
    backend._furthest_position_ms = 0
    await poll(backend, monkeypatch)
    backend.ended.assert_called_once()
