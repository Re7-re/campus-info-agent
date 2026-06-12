"""
知识库模块
提供校园信息知识库管理功能
"""

from typing import List, Dict, Any, Optional
import json
import os
from dataclasses import dataclass, asdict


@dataclass
class KnowledgeItem:
    """知识条目"""
    question: str
    answer: str
    category: str
    keywords: List[str]
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeBase:
    """
    知识库类，用于存储和检索校园信息知识
    """
    
    def __init__(self, data_file: str = "data/knowledge_base.json"):
        """
        初始化知识库
        
        Args:
            data_file: 知识库数据文件路径
        """
        self.data_file = data_file
        self.knowledge_items: List[KnowledgeItem] = []
        self._load_knowledge()
    
    def _load_knowledge(self):
        """从文件加载知识库"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.knowledge_items = [
                        KnowledgeItem(**item) for item in data.get("knowledge_items", [])
                    ]
            except Exception as e:
                print(f"加载知识库失败: {e}")
                self._init_default_knowledge()
        else:
            self._init_default_knowledge()
    
    def _init_default_knowledge(self):
        """初始化默认知识库"""
        default_knowledge = [
            {
                "question": "如何查询成绩？",
                "answer": "你可以直接问我'查询成绩'或'我的成绩是多少'，我会帮你查询所有学期的成绩。你也可以指定学期，比如'查询2025-2026-1学期的成绩'。",
                "category": "成绩查询",
                "keywords": ["成绩", "分数", "查询", "考试结果"]
            },
            {
                "question": "如何查询课表？",
                "answer": "你可以问我'今天的课表'或'周一的课表'，我会帮你查询具体的课程安排。你也可以询问'本周课表'获取完整的周课程安排。",
                "category": "课表查询",
                "keywords": ["课表", "课程", "上课", "时间表"]
            },
            {
                "question": "如何查询空教室？",
                "answer": "你可以直接问我'有哪些空教室'或'查询可用教室'，我会为你提供当前可用的空教室列表。",
                "category": "教室查询",
                "keywords": ["空教室", "可用教室", "自习室", "空闲教室"]
            },
            {
                "question": "如何查询考试安排？",
                "answer": "你可以问我'考试安排'或'期末考试时间'，我会为你提供所有科目的考试时间、地点等详细信息。",
                "category": "考试查询",
                "keywords": ["考试", "期末", "考试安排", "考试时间"]
            },
            {
                "question": "如何查询校园通知？",
                "answer": "你可以问我'最新通知'或'校园通知'，我会为你提供最新的校园通知和公告信息。",
                "category": "通知查询",
                "keywords": ["通知", "公告", "消息", "校园动态"]
            },
            {
                "question": "学校的选课时间是什么时候？",
                "answer": "选课时间通常在每学期结束前2-3周开始，具体时间请关注教务处发布的选课通知。你可以通过查询校园通知获取最新的选课安排信息。",
                "category": "选课信息",
                "keywords": ["选课", "选课时间", "课程选择", "选课安排"]
            }
        ]
        
        self.knowledge_items = [KnowledgeItem(**item) for item in default_knowledge]
        self._save_knowledge()
    
    def _save_knowledge(self):
        """保存知识库到文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({
                "knowledge_items": [asdict(item) for item in self.knowledge_items]
            }, f, ensure_ascii=False, indent=2)
    
    def add_knowledge(
        self,
        question: str,
        answer: str,
        category: str,
        keywords: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        添加知识条目
        
        Args:
            question: 问题
            answer: 答案
            category: 分类
            keywords: 关键词列表
            metadata: 额外元数据
        """
        knowledge_item = KnowledgeItem(
            question=question,
            answer=answer,
            category=category,
            keywords=keywords,
            metadata=metadata
        )
        self.knowledge_items.append(knowledge_item)
        self._save_knowledge()
    
    def search(self, query: str, top_k: int = 3) -> List[KnowledgeItem]:
        """
        搜索相关知识
        
        Args:
            query: 查询文本
            top_k: 返回前k个结果
        
        Returns:
            匹配的知识条目列表
        """
        query_lower = query.lower()
        scored_items = []
        
        for item in self.knowledge_items:
            score = 0
            
            # 问题匹配
            if query_lower in item.question.lower():
                score += 10
            
            # 关键词匹配
            for keyword in item.keywords:
                if keyword.lower() in query_lower:
                    score += 5
            
            # 分类匹配
            if item.category.lower() in query_lower:
                score += 3
            
            # 答案匹配
            if query_lower in item.answer.lower():
                score += 2
            
            if score > 0:
                scored_items.append((score, item))
        
        # 按分数排序并返回前k个
        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored_items[:top_k]]
    
    def get_by_category(self, category: str) -> List[KnowledgeItem]:
        """
        按分类获取知识
        
        Args:
            category: 分类名称
        
        Returns:
            该分类下的所有知识条目
        """
        return [
            item for item in self.knowledge_items
            if item.category.lower() == category.lower()
        ]
    
    def get_all_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set()
        for item in self.knowledge_items:
            categories.add(item.category)
        return sorted(list(categories))
    
    def update_knowledge(
        self,
        index: int,
        question: Optional[str] = None,
        answer: Optional[str] = None,
        category: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ):
        """
        更新知识条目
        
        Args:
            index: 知识条目索引
            question: 新问题
            answer: 新答案
            category: 新分类
            keywords: 新关键词列表
        """
        if 0 <= index < len(self.knowledge_items):
            item = self.knowledge_items[index]
            if question is not None:
                item.question = question
            if answer is not None:
                item.answer = answer
            if category is not None:
                item.category = category
            if keywords is not None:
                item.keywords = keywords
            self._save_knowledge()
    
    def delete_knowledge(self, index: int):
        """
        删除知识条目
        
        Args:
            index: 知识条目索引
        """
        if 0 <= index < len(self.knowledge_items):
            self.knowledge_items.pop(index)
            self._save_knowledge()
    
    def get_knowledge_count(self) -> int:
        """获取知识条目数量"""
        return len(self.knowledge_items)