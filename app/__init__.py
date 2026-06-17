import logging
import sys
from pathlib import Path


# Setup logging
def setup_logging(level: str = "INFO"):
    # Create logs directory if it doesn't exist
    # log_dir = Path(__file__).parent.parent / "logs"
    # log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="[%(asctime)s %(levelname)s %(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),  # Console
            # logging.FileHandler(log_dir / "app.log"),  # File
        ],
    )


# Add proto/agen to sys.path so generated code can find zservice module
proto_gen_path = (
    Path(__file__).parent.parent
    / "proto"
    / "agen"  # intended to use "a" + "gen" to take advantage of the alphabetical arrangement
)

# -- initialize
if str(proto_gen_path) not in sys.path:
    sys.path.insert(0, str(proto_gen_path))
setup_logging(level="INFO")  # Call once at startup
