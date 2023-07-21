from __future__ import annotations

import signal
import subprocess
from unittest.mock import Mock, call, patch

import pytest

from iap_tunnel import IAPTunnel


def build_tunnel() -> IAPTunnel:
    return IAPTunnel(
        server="server",
        local_port=1234,
        endpoint="endpoint",
        zone="zone",
        project="project",
        sleep=0,
    )


@pytest.mark.skip(reason="Requires google CLI installed.")
def test_druid_tunnel_cm_running():
    expected = True
    with build_tunnel() as tunnel:
        obtained = tunnel.is_running()
    assert expected == obtained


@pytest.mark.skip(reason="Requires google CLI installed.")
def test_druid_tunnel_cm_running_false():
    expected = False
    with build_tunnel() as tunnel:
        pass
    obtained = tunnel.is_running()
    assert expected == obtained


@pytest.mark.skip(reason="Requires google CLI installed.")
def test_druid_tunnel_obj_running():
    expected = True
    tunnel = build_tunnel()
    tunnel.open()
    obtained = tunnel.is_running()
    assert expected == obtained


@pytest.mark.skip(reason="Requires google CLI installed.")
def test_druid_tunnel_obj_is_running():
    expected = False
    tunnel = build_tunnel()
    obtained = tunnel.is_running()
    assert expected == obtained


@pytest.mark.skip(reason="Requires google CLI installed.")
def test_druid_tunnel_obj_start_stop():
    expected = False
    tunnel = build_tunnel()
    tunnel.open()
    tunnel.close()
    obtained = tunnel.is_running()
    assert expected == obtained


def test_tunnel_mock():
    # Create mock subprocess.Popen object
    mock_popen = Mock()
    mock_popen.poll.return_value = None

    # Suplanta subprocess.Popen con el mock
    with patch("subprocess.Popen", return_value=mock_popen):
        tunnel = build_tunnel()
        # Check tunnel is not running
        assert tunnel.is_running() is False

        tunnel.open()

        # check subprocess.Popen is called with the right arguments
        subprocess.Popen.assert_called_once_with(tunnel.cmd)  # type: ignore[attr-defined]

        # Check tunnel is running
        assert tunnel.is_running() is True

        # Close tunnel
        tunnel.close()
        mock_popen.poll.return_value = 0

        # Check close signal
        mock_popen.send_signal.assert_has_calls([call(signal.SIGINT)])

        # Check tunnel is not running
        assert tunnel.is_running() is False
