# InteractiveHtmlBom for KiCad 11 Nightly

> **Unofficial compatibility fork.** This is not an official OpenScope or
> KiCad release. It preserves the familiar InteractiveHtmlBom workflow while
> adding support for KiCad 11 development builds, currently identified as
> KiCad 10.99 nightlies.

InteractiveHtmlBom generates a self-contained HTML bill of materials with an
interactive PCB view. Components can be searched, grouped and highlighted on
the board, which is especially useful for hand assembly and troubleshooting.

This fork is based on InteractiveHtmlBom 2.12.0 and the KiCad IPC API work from
[upstream pull request #555](https://github.com/openscopeproject/InteractiveHtmlBom/pull/555).
It adds a narrow compatibility fix for the `ReferencePoint` objects emitted by
newer KiCad nightlies, as well as persistent error logging for plugin startup
and generation failures.

## Current status

- Tested on Windows with KiCad Nightly 10.99.0.
- Keeps the existing toolbar action, settings dialog and generated HTML layout.
- Successfully generated a BOM from a real board with 141 footprints.
- The generated HTML opened successfully in a browser.
- The legacy SWIG backend remains present for older KiCad installations.

Nightly APIs can change without notice. See [NIGHTLY_PATCH.md](NIGHTLY_PATCH.md)
for implementation details, limitations and the exact compatibility changes.

## Installation

1. Download the latest release ZIP, or use GitHub's **Code → Download ZIP**.
2. Extract it into your KiCad user plugin directory. For KiCad 10.99 on
   Windows, the usual location is:

   ```text
   %USERPROFILE%\Documents\KiCad\10.99\plugins\InteractiveHtmlBom-KiCad-11-Nightly
   ```

3. Verify that `plugin.json` is directly inside that folder.
4. In KiCad, enable the API server under **Preferences → Plugins**.
5. Restart the PCB Editor.

KiCad creates a per-plugin Python environment and installs the dependencies
listed in `requirements.txt`.

## Usage

Open a board in the PCB Editor and click **Generate Interactive HTML BOM** in
the toolbar, or start it from the external plugins menu. The normal iBOM
settings dialog opens and the generated HTML file is written to the selected
output folder.

The output is a single, self-contained HTML file and does not need an internet
connection.

## Troubleshooting

If the window appears briefly and closes, inspect the persistent log file:

```text
%LOCALAPPDATA%\KiCad\10.99\interactive-html-bom.log
```

Also verify that the KiCad API server is enabled and restart the PCB Editor
after installing or updating the plugin. When reporting a problem, include the
exact KiCad nightly build and the relevant log excerpt. Do not publish private
board files unless you intend to share them.

## Upstream project and documentation

- [Original InteractiveHtmlBom repository](https://github.com/openscopeproject/InteractiveHtmlBom)
- [Original project wiki](https://github.com/openscopeproject/InteractiveHtmlBom/wiki)
- [Installation documentation](https://github.com/openscopeproject/InteractiveHtmlBom/wiki/Installation)
- [Interactive demo](https://openscopeproject.org/InteractiveHtmlBomDemo/)

## Credits and license

- Original project and copyright: `qu1ck` / OpenScope Project
- KiCad IPC backend: [mikelemo, pull request #555](https://github.com/openscopeproject/InteractiveHtmlBom/pull/555)
- KiCad IPC bindings: [kicad-python](https://gitlab.com/kicad/code/kicad-python)

The project remains available under the MIT License. The original copyright
and license notice are preserved in [LICENSE](LICENSE).
