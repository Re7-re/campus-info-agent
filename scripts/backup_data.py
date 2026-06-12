# scripts/backup_data.py
import shutil
import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from utils.logger import get_logger

logger = get_logger("backup")


def backup_data():
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    data_dirs = [
        Path(Config.DATABASE_PATH).parent,
        Path(Config.SESSION_DIR),
        Path(Config.KNOWLEDGE_BASE_PATH).parent,
        Path(Config.USERS_FILE).parent,
    ]

    for src in set(data_dirs):
        if src.exists():
            dst = backup_dir / f"{src.name}_{timestamp}"
            shutil.copytree(src, dst, dirs_exist_ok=True)
            logger.info(f"备份 {src} -> {dst}")

    logger.info("数据备份完成")


if __name__ == "__main__":
    backup_data()