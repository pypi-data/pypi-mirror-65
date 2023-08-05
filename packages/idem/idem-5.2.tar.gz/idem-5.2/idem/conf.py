CLI_CONFIG = {
    "sls_sources": {"nargs": "*",},
    "test": {"options": ["-t"], "action": "store_true",},
    "tree": {"options": ["-T"],},
    "takara_unit": {"options": ["-u"],},
    "seal_raw": {},
    "cache_dir": {},
    "root_dir": {},
    "render": {},
    "runtime": {},
    "output": {},
    "sls": {"nargs": "*",},
}
CONFIG = {
    "sls_sources": {
        "default": ["file://"],
        "help": "list off the sources that should be used for gathering sls files and data",
    },
    "test": {
        "default": False,
        "help": "Set the idem run to execute in test mode. No changes will be made, idem will only detect if changes will be made in a real run.",
    },
    "tree": {"default": "", "help": "The directory containing sls files",},
    "takara_unit": {
        "default": None,
        "help": "The Takara unit to work with, This enables Takara as a backend for secret storage in your idem states",
    },
    "seal_raw": {
        "default": None,
        "help": "DO NOT USE! This option allows you to pass Takara unsealing secrets as command line arguments! This should only be used for testing!!",
    },
    "cache_dir": {
        "default": "/var/cache/idem",
        "help": "The location to use for the cache directory",
    },
    "root_dir": {
        "default": "/",
        "help": 'The root directory to run idem from. By default it will be "/", or in the case of running as non-root it is set to <HOMEDIR>/.idem',
    },
    "render": {
        "default": "jinja|yaml",
        "help": "The render pipe to use, this allows for the language to be specified",
    },
    "runtime": {"default": "serial", "help": "Select which execution runtime to use",},
    "output": {"default": "idem", "help": "The putputter to use to display data",},
    "sls": {"default": [], "help": "A space delimited list of sls refs to execute",},
}
GLOBAL = {}
SUBS = {}
DYNE = {
    "exec": ["exec"],
    "states": ["states"],
    "output": ["output"],
}
