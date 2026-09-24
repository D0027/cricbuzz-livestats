import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ["DB_TYPE"] = "sqlite"
os.environ["DB_PATH"] = "data/test_cricbuzz.db"
