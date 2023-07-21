from __future__ import annotations

import signal
import subprocess
import time
from types import TracebackType


class TunnelNotStartedException(Exception):
    """Raised when trying to stop a tunnel that was not started"""


class IAPTunnel:
    """GCP IAP SSH Tunnel to Druid SQL Proxy

    This class represents a SSH Tunnel to Google cloud SQL Proxy in the GCP
    environment. It can be used as a context manager to automatically manage
    the lifecycle of the tunnel.

    Examples
    --------
    >>> with IAPTunnel() as tunnel:
    ...     print(tunnel.is_running())
    True

    Notes
    -----
    The tunnel is created using the gcloud CLI tool. It is assumed that the
    tool is installed and configured in the system. The tunnel is created
    using the following command:

    $ gcloud compute ssh <server> \
        --project=<project> \
        --zone=<zone> \
        --tunnel-through-iap \
        -- <local_port>:<endpoint> *<args>
    """

    def __init__(
        self: IAPTunnel,
        server: str,
        local_port: int,
        endpoint: str,
        zone: str,
        project: str,
        *ssh_args: str,
        sleep: int = 3,
    ) -> None:
        """
        Initialize IAPTunnel.

        Parameters
        ----------
        server : str
            The server to be connected to.
        port : int
            The local port to be used for the tunnel. Eg. 8888
        endpoint : str
            The endpoint to be connected to. Eg. localhost:8888
        project : str
            The GCP project name.
        zone : str
            The GCP zone.
        *args :
            Additional arguments to be passed to the SSH command.

        """
        self.server = server
        self.local_port = local_port
        self.endpoint = endpoint
        self.zone = zone
        self.project = project
        self.ssh_args = ssh_args
        self.sleep = sleep
        self.process: None | subprocess.Popen = None  # type: ignore[type-arg]
        self.cmd: None | list[str] = None

    def build_cmd(self) -> list[str]:
        """Build the command to be create tunnel.

        Returns
        -------
        out : list
            The command to be executed.
        """
        server = self.server
        zone = self.zone
        local_port = self.local_port
        project = self.project
        args = self.ssh_args
        endpoint = self.endpoint

        cmd = [
            "gcloud",
            "compute",
            "ssh",
            server,
            f"--project={project}",
            f"--zone={zone}",
            "--tunnel-through-iap",
            "--",
            f"{local_port}:{endpoint}",
            *args,
        ]
        self.cmd = cmd
        return cmd

    def __enter__(self) -> IAPTunnel:
        """
        Start the tunnel when entering the context.

        Returns
        -------
        IAPTunnel
            The instance of the IAPTunnel.
        """
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Stop the tunnel when exiting the context.
        """
        self.close(force=True)

    def open(self) -> None:
        """
        Start the tunnel process.
        """
        cmd = self.build_cmd()
        self.process = subprocess.Popen(cmd)  # pylint: disable=R1732

    def close(self, force: bool = False) -> bool:
        """
        Close the tunnel process.

        Parameters
        ----------
        force : bool, optional
            If True, the process will be forcefully killed if it does not stop
            after a short period, by default False
        """
        process = self.process
        if process is None:
            msg = "Tunnel is not started yet."
            raise TunnelNotStartedException(msg)
        process.send_signal(signal.SIGINT)  # same as Ctrl-C
        time.sleep(self.sleep)
        is_closed = not self.is_running()
        if force and not is_closed:
            process.kill()
            is_closed = not self.is_running()
        return is_closed

    def is_running(self) -> bool:
        """
        Check if the tunnel process is running.

        Returns
        -------
        bool
            True if the process is running, False otherwise.
        """
        process = self.process
        if process is None:
            return False
        return process.poll() is None
