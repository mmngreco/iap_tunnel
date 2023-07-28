# IAP tunnel

[![Actions Status][actions-badge]][actions-link]
<!-- [![Documentation Status][rtd-badge]][rtd-link] -->

<!-- [![PyPI version][pypi-version]][pypi-link] -->
<!-- [![Conda-Forge][conda-badge]][conda-link] -->
<!-- [![PyPI platforms][pypi-platforms]][pypi-link] -->

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/mmngreco/iap_tunnel/workflows/CI/badge.svg
[actions-link]:             https://github.com/mmngreco/iap_tunnel/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/iap_tunnel
[conda-link]:               https://github.com/conda-forge/iap_tunnel-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/mmngreco/iap_tunnel/discussions
[pypi-link]:                https://pypi.org/project/iap_tunnel/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/iap_tunnel
[pypi-version]:             https://img.shields.io/pypi/v/iap_tunnel
[rtd-badge]:                https://readthedocs.org/projects/iap_tunnel/badge/?version=latest
[rtd-link]:                 https://iap_tunnel.readthedocs.io/en/latest/?badge=latest

<!-- prettier-ignore-end -->

> ⚠️ NOTE: This is a work in progress. Use it at your own risk.

Imagine a scenario where you need to create an IAP tunnel. The conventional
method would be to run `gcloud compute ssh ...` in a shell, forward the ports
you need, and execute the code. This process can be cumbersome and inefficient.
What if there was a way to create the tunnel exactly where you need it and
close it immediately after use? That's where IAP Tunnel Manager comes in.

## Project Overview

IAP Tunnel Manager is a project designed to streamline the process of creating
and managing IAP tunnels. It allows you to create a tunnel at your point of
need and automatically closes it once you're done. This not only simplifies the
process but also enhances security by minimizing the tunnel's open time. With
IAP Tunnel Manager, you no longer have to manually manage your IAP tunnels. The
project does it for you, saving you time and effort, and allowing you to focus
on what truly matters - your code. Stay tuned for more updates and features
that will further enhance your IAP tunnel management experience.


### Example

```python
from iap_tunnel import IAPTunnel

with IAPTunnel(
        server="server",
        local_port=1234,
        endpoint="endpoint",
        zone="zone",
        project="project",
    ) as tunnel:
    print(tunnel.is_running())   # True
    # your code here

print(tunnel.is_running())   # False
```
