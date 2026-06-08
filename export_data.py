# scripts/export_data.py
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import db
from data.mock_data import MOCK_STUDENT


def export_to_json():
    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)

    # 导出模拟数据
    with open(export_dir / "mock_data.json", "w", encoding="utf-8") as f:
        json.dump(MOCK_STUDENT, f, ensure_ascii=False, indent=2)

    # 导出数据库中的用户（示例）
    users = db.execute_query("SELECT id, username, role, created_at FROM users")
    with open(export_dir / "users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2, default=str)

    print("数据导出完成，目录: exports/")


if __name__ == "__main__":
    export_to_json()