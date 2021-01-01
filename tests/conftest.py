import sys
from pathlib import Path
# add template/lib to path, we'll be testing those files
root = Path(__file__).parent.parent
sys.path.append(str(root / 'src' / 'ploomber_scaffold' / 'template' / 'lib'))
