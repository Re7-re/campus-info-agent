# tests/test_features.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from features.grade_feature import GradeFeature
from features.schedule_feature import ScheduleFeature
from features.classroom_feature import ClassroomFeature
from features.exam_feature import ExamFeature
from features.notice_feature import NoticeFeature


class TestFeatures:
    def test_grade(self):
        g = GradeFeature ()
        res = g.execute (term="2025-2026-1")
        assert res ["success"] is True
        assert "高等数学" in  res["message"]

    def test_schedule (self):
        s =ScheduleFeature()
        res = s.execute (day="周一")
        assert res["success"] is True
        assert "高等数学" in res["message"]

    def test_classroom (self):
        c = ClassroomFeature()
        res = c.execute ()
        assert res["success"] is True
        assert "空教室" in res["message"]

    def test_exam(self):
        e = ExamFeature()
        res = e.execute()
        assert res["success"] is True
        assert "考试安排" in res["message"]

    def test_notice (self):
        n = NoticeFeature()
        res = n.execute (count=3)
        assert  res["success"] is True
        assert  len(res["notices"]) <= 3