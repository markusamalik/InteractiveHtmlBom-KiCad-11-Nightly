#!/usr/bin/env python3
"""Entry point for KiCad's IPC plugin system.

KiCad launches this script in its own process (inside the plugin's
virtual environment) when the user clicks the iBOM action button.
Connection parameters are passed via the KICAD_API_SOCKET and
KICAD_API_TOKEN environment variables, which kipy picks up
automatically.

With wxPython available the regular settings dialog is shown;
otherwise the BOM is generated headlessly with the saved
(or default) settings.
"""

import os
import sys
import traceback
from datetime import datetime


def _log_path():
    local_app_data = os.environ.get('LOCALAPPDATA')
    if local_app_data:
        log_dir = os.path.join(local_app_data, 'KiCad', '10.99')
    else:
        log_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, 'interactive-html-bom.log')


def _write_log(message):
    try:
        with open(_log_path(), 'a', encoding='utf-8') as log_file:
            log_file.write('%s %s\n' %
                           (datetime.now().isoformat(timespec='seconds'),
                            message))
    except Exception:
        # Logging must never hide the original plugin error.
        pass


def _unhandled_exception(exc_type, exc_value, exc_traceback):
    _write_log('Unhandled exception:\n' + ''.join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = _unhandled_exception

# Prevent InteractiveHtmlBom/__init__.py from trying to register the
# legacy SWIG action plugin when the package is imported.
os.environ['INTERACTIVE_HTML_BOM_CLI_MODE'] = '1'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from InteractiveHtmlBom.core import ibom  # noqa: E402
from InteractiveHtmlBom.core.config import Config  # noqa: E402
from InteractiveHtmlBom.ecad import get_kicad_ipc_parser  # noqa: E402
from InteractiveHtmlBom.errors import ParsingException  # noqa: E402
from InteractiveHtmlBom.version import version  # noqa: E402
from InteractiveHtmlBom.compat import get_wx, should_create_wx_app  # noqa: E402


def main():
    _write_log('Starting Interactive HTML BOM IPC action')
    # Keep the regular dialog for KiCad actions, but allow deterministic
    # headless generation for kicad-cli and automated smoke tests.
    wx = get_wx() if should_create_wx_app() else None
    app = None
    if wx is not None:
        app = wx.App()
        if hasattr(wx, "APP_ASSERT_SUPPRESS"):
            app.SetAssertMode(wx.APP_ASSERT_SUPPRESS)

    logger = ibom.Logger(cli=(wx is None))

    try:
        from kipy import KiCad
        kicad = KiCad()
        board = kicad.get_board()
    except Exception as e:
        _write_log('Cannot connect to KiCad via the IPC API:\n' +
                   traceback.format_exc())
        logger.error("Cannot connect to KiCad via the IPC API: %s" % e)
        return 1

    file_name = board.name
    if not file_name:
        logger.error('Please save the board file before generating BOM.')
        return 1

    try:
        project = board.get_project()
        pcb_file_name = os.path.join(project.path, file_name)

        config = Config(version, os.path.dirname(pcb_file_name))
        parser = get_kicad_ipc_parser(
            pcb_file_name, config, logger, kicad, board)

        if wx is not None:
            ibom.run_with_dialog(parser, config, logger)
        else:
            config.load_from_ini()
            ibom.main(parser, config, logger)
    except ParsingException as e:
        _write_log('Board parsing failed:\n' + traceback.format_exc())
        logger.error(str(e))
        return 1
    except Exception as e:
        _write_log('Interactive HTML BOM failed:\n' +
                   traceback.format_exc())
        if wx is not None:
            wx.MessageBox(
                'Interactive HTML BOM konnte nicht gestartet werden.\n\n'
                '%s\n\nDetails: %s' % (e, _log_path()),
                'Interactive HTML BOM', wx.OK | wx.ICON_ERROR)
        else:
            logger.error(str(e))
        return 1

    _write_log('Interactive HTML BOM action finished successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
