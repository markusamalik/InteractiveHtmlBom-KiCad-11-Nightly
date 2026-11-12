import os

from .xmlparser import XmlParser
from .netlistparser import NetlistParser

PARSERS = {
    '.xml': XmlParser,
    '.net': NetlistParser,
}


if os.environ.get('KICAD_API_SOCKET'):
    # Never import pcbnew in the external IPC process.  On Windows the chosen
    # interpreter may expose an older KiCad's SWIG module through system site
    # packages; loading it alongside KiCad 11 IPC can crash Python at exit.
    _pcb_fields_supported = True
else:
    try:
        import pcbnew
        _pcb_fields_supported = hasattr(pcbnew, 'FOOTPRINT')
    except ImportError:
        _pcb_fields_supported = True


if _pcb_fields_supported:
    PARSERS['.kicad_pcb'] = None


def parse_schematic_data(file_name):
    if not os.path.isfile(file_name):
        return None
    extension = os.path.splitext(file_name)[1]
    if extension not in PARSERS:
        return None
    else:
        parser_cls = PARSERS[extension]
        if parser_cls is None:
            return None
        parser = parser_cls(file_name)
        return parser.get_extra_field_data()


def find_latest_schematic_data(base_name, directories):
    """
    :param base_name: base name of pcb file
    :param directories: list of directories to search
    :return: last modified parsable file path or None if not found
    """
    files = []
    for d in directories:
        files.extend(_find_in_dir(d))
    # sort by decreasing modification time
    files = sorted(files, reverse=True)
    if files:
        # try to find first (last modified) file that has name matching pcb file
        for _, f in files:
            if os.path.splitext(os.path.basename(f))[0] == base_name:
                return f
        # if no such file is found just return last modified
        return files[0][1]
    else:
        return None


def _find_in_dir(dir):
    _, _, files = next(os.walk(dir), (None, None, []))
    # filter out files that we can not parse
    files = [f for f in files if os.path.splitext(f)[1] in PARSERS.keys()]
    files = [os.path.join(dir, f) for f in files]
    # get their modification time and sort in descending order
    return [(os.path.getmtime(f), f) for f in files]
