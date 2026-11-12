# KiCad 11 Nightly compatibility patch

## Why this fork exists

KiCad 11 removes the legacy embedded SWIG `pcbnew` interface used by older
versions of InteractiveHtmlBom. The replacement is KiCad's IPC API, where the
plugin runs as a separate Python process and communicates with the open PCB
Editor.

The IPC backend in this fork is based on upstream pull request
[openscopeproject/InteractiveHtmlBom#555](https://github.com/openscopeproject/InteractiveHtmlBom/pull/555).
The upstream pull request was still open when this compatibility package was
prepared.

## Additional fixes in this fork

- Adds the KiCad IPC plugin manifest and separate-process entry point.
- Keeps InteractiveHtmlBom 2.12.0 behavior and the legacy parser intact.
- Avoids loading the obsolete `pcbnew` module inside the IPC process on
  Windows.
- Preserves polygon hole contours for even-odd rendering.
- Handles `type.googleapis.com/kiapi.board.types.ReferencePoint` objects from
  current KiCad 10.99 builds.
- Writes startup failures to
  `%LOCALAPPDATA%/KiCad/10.99/interactive-html-bom.log` and displays a visible
  error instead of closing silently.

### ReferencePoint compatibility

At the time of testing, the latest stable `kicad-python` releases 0.7.1 and
0.8.0 could not deserialize KiCad's new `ReferencePoint` footprint marker.
Support exists in the unreleased 0.9 development branch. These markers are
editor reference/snap points and are not part of BOM data or the board drawing
used by iBOM.

The compatibility layer therefore skips exactly this object type when an older
binding is detected. All other unknown IPC object types still raise an error so
that future incompatibilities are not silently hidden.

## Verification performed

- Plugin manifest validated against the schema shipped with KiCad 10.99.
- Python sources compiled and imported successfully.
- IPC connection tested with a real KiCad API server.
- Geometry regression tests passed.
- A 141-footprint production board parsed successfully after the
  `ReferencePoint` fix.
- The resulting `ibom.html` contained PCB data and opened successfully in a
  browser.

## Known limitations

The current stable IPC bindings do not expose every data item available through
the old SWIG API. Custom local board-outline clipping, barcodes, some dimensions,
and some advanced variant data may therefore differ in IPC mode. Normal
footprints, pads, tracks, vias, zones, nets, BOM fields, DNP fields, and the
interactive HTML interface are supported.

## Troubleshooting

If the toolbar action is missing:

1. Confirm that `plugin.json` is directly inside the extracted plugin folder.
2. Enable the KiCad API server under **Preferences → Plugins**.
3. Confirm that a Python interpreter with wxPython is configured there.
4. Restart the complete PCB Editor.

If the plugin window closes or generation fails, inspect:

```text
%LOCALAPPDATA%/KiCad/10.99/interactive-html-bom.log
```

Please include that log, the exact KiCad nightly version, and a minimal test
board when reporting an issue. Do not upload proprietary board files unless
you have permission to share them.
