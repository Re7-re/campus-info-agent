from .base_feature import BaseFeature
from data.mock_data import get_notice_data
from typing import Dict, Any

class NoticeFeature(BaseFeature):
    def __init__(self):
        super().__init__(
            name="通知查询",
            description="查看校园最新通知、重要公告分类筛选"
        )

    def execute(self, count: int = 5) -> Dict[str, Any]:
        show = get_notice_data(count)
        text = "\n".join([f"{i+1}.{n}" for i,n in enumerate(show)])
        return {"message": text}

    def get_important_notices(self):
        imp = [x for x in get_notice_data() if "重要" in x or "考试" in x]
        return imp

    def get_notice_categories(self) -> Dict[str, list]:
        cate_dict = {"教务":[], "后勤":[], "学工":[]}
        all_notice = get_notice_data()
        for item in all_notice:
            if "考试" in item or "选课" in item or "成绩" in item:
                cate_dict["教务"].append(item)
            elif "校园网" in item or "暑假" in item:
                cate_dict["学工"].append(item)
            else:
                cate_dict["后勤"].append(item)
        return cate_dict

    def get_ui_components(self):
        return {}