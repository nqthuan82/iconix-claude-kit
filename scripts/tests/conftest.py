"""pytest configuration for the ICONIX `.claude/scripts/` test suite.

Puts the scripts directory (the parent of tests/) on sys.path so tests can
`import _common`, `import checkpoint`, etc. — the same module-resolution the scripts
get at runtime when invoked as `python3 .claude/scripts/<name>.py`.
"""

import os
import sys

SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
