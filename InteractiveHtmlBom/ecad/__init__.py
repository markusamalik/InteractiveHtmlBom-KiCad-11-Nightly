import os


def get_parser_by_extension(file_name, config, logger):
    ext = os.path.splitext(file_name)[1]
    if ext == '.kicad_pcb':
        # KiCad 11/nightly removed the embedded SWIG pcbnew module.  IPC
        # plugin actions provide the socket in the environment, so use the
        # stable kicad-python backend there.  Standalone CLI invocations keep
        # using the legacy parser because it can load a board from disk.
        if os.environ.get('KICAD_API_SOCKET'):
            try:
                return get_kicad_ipc_parser(file_name, config, logger)
            except Exception as e:
                logger.info("IPC API unavailable (%s), "
                            "falling back to the legacy parser." % e)
        return get_kicad_parser(file_name, config, logger)
    elif ext == '.json':
        """.json file may be from EasyEDA or a generic json format"""
        import io
        import json
        with io.open(file_name, 'r', encoding='utf-8') as f:
            obj = json.load(f)
        if 'pcbdata' in obj:
            return get_generic_json_parser(file_name, config, logger)
        else:
            return get_easyeda_parser(file_name, config, logger)
    elif ext in ['.fbrd', '.brd']:
        return get_fusion_eagle_parser(file_name, config, logger)
    else:
        return None


def get_kicad_parser(file_name, config, logger, board=None):
    from .kicad import PcbnewParser
    return PcbnewParser(file_name, config, logger, board)


def get_kicad_ipc_parser(file_name, config, logger, kicad=None, board=None):
    """Create the KiCad IPC parser without importing legacy pcbnew."""
    from .kicad_ipc import IpcApiParser
    return IpcApiParser(file_name, config, logger, kicad, board)


def get_easyeda_parser(file_name, config, logger):
    from .easyeda import EasyEdaParser
    return EasyEdaParser(file_name, config, logger)


def get_generic_json_parser(file_name, config, logger):
    from .genericjson import GenericJsonParser
    return GenericJsonParser(file_name, config, logger)


def get_fusion_eagle_parser(file_name, config, logger):
    from .fusion_eagle import FusionEagleParser
    return FusionEagleParser(file_name, config, logger)
