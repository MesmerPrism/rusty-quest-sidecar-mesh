# Termux Capability Map

This map records how the Termux profile fits the sidecar architecture.

## Known Useful Capabilities

- Python and shell-friendly Linux userland for small local tools.
- App-private and shared-storage file access under Android constraints.
- Localhost services for bounded status, dashboards, or file exchange.
- Optional Termux:X11 or Proot for desktop-style lab workflows.
- Optional ADB client use after a user or external operator has authorized a
  wireless debugging session.
- Low-rate status generation and diagnostic processing while another app is
  foregrounded.

## Plausible But Not Proven Here

- Reliable long-running background operation across headset sleep, app
  lifecycle changes, and battery management.
- Fleet-scale peer status exchange across many headsets on a noisy LAN.
- Repeatable remote desktop control that remains ergonomic in headset panels.
- Reboot-surviving WiFi ADB readiness from normal-app helpers.
- Clean import of private live mesh evidence into public-safe derivatives.

## Rejected As Architecture Authority

- Termux as Manifold broker authority.
- Termux as Android recovery authority.
- Termux as a cross-headset ADB router.
- Termux as an unattended root or device-owner lane.
- Peer mesh as a command bus.
- Remote desktop as the primary operational control plane.

## Recommended Default

Use Termux as a headless Linux sidecar that writes observations and pulls or
submits bounded status through explicit, approved routes. Keep desktop GUI,
VNC, and X11 as lab/inspection tools rather than core fleet control surfaces.

