from .base_feature import BaseFeature
from data.mock_data import get_exam_data
from typing import Dict, Any, List
from datetime import datetime

class ExamFeature(BaseFeature):
    def __init__(self):
        super().__init__(
            name="考试查询",
            description="查询各科期末考试时间、地点，即将开考提醒"
        )
        self.exam_data = get_exam_data()

    def execute(self, subject: str = None) -> Dict[str, Any]:
        res_list = []
        data = get_exam_data(subject)
        for item in data:
            res_list.append(f"{item['name']} | {item['time']} | {item['location']}")
        msg = "\n".join(res_list) if res_list else "暂无考试数据"
        return {"message": msg}

    def get_upcoming_exams(self) -> List[Dict[str, Any]]:
        today = datetime.now()
        upcoming = []
        for item in self.exam_data:
            try:
                exam_day_str = item["time"].split(" ")[0]
                # 适配6月XX日格式
                month, day = int(exam_day_str.replace("月","")), int(exam_day_str.replace("日",""))
                from datetime import date
                exam_day = date(2026, month, day)
                diff = (exam_day - date.today()).days
                if 0 <= diff <= 30:
                    upcoming.append({"name":item["name"], "days_until":diff})
            except:
                continue
        return upcoming

    def get_exam_summary(self) -> Dict[str, Any]:
        total = len(self.exam_data)
        return {"message": f"本学期共{total}门期末考试"}

    def get_ui_components(self):
        return {}