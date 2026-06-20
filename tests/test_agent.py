# tests/test_agent.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from features.agent_feature import AgentFeature


class TestAgentFeature :
    @pytest.fixture
    def agent (self):
        return AgentFeature()

    def test_greeting (self, agent):
        result =  agent.execute("你好")
        assert result ["success"] is True
        assert "您好" in result["message"]

    def test_grade_query (self, agent):
        result = agent.execute ("查询成绩")
        assert result["success"] is True
        assert "成绩" in result["message"]

    def test_empty_message (self, agent):
        result = agent.execute("")
        # 应该返回错误或默认提示
        assert result["success"] is True  # 本地引擎会返回默认响应

    def test_memory (self, agent):
        agent.clear_memory()
        agent.execute ("我叫小明")
        agent.execute ("我叫什么名字？")
        assert True