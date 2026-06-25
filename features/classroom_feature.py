"""
教室查询功能模块
支持解析教室编号（如H1101表示第一教学楼一楼1101教室）
"""

from typing import Dict, Any, List
from .base_feature import BaseFeature
from data.mock_data import MOCK_STUDENT, update_student_with_cuit_data
from config import Config
import json
import os
import re


class ClassroomFeature(BaseFeature):
    """
    教室查询功能模块
    支持查询空教室、教室状态等
    教室编号解析规则：
    - H1101: 第一教学楼一楼1101教室
    - H4101: 第四教学楼一楼4101教室
    - 第一个数字代表教学楼号
    - 第二个数字代表楼层
    - 第三和第四代表该楼层教室排序
    """
    
    def __init__(self):
        super().__init__(
            name="教室查询",
            description="查询可用空教室信息，支持教学楼筛选"
        )
        # 根据配置选择数据源
        if Config.DATA_SOURCE == "cuit" and Config.ENABLE_CUIT_SPIDER:
            # 使用真实教务数据
            student_data = update_student_with_cuit_data(
                username=Config.CUIT_USERNAME,
                password=Config.CUIT_PASSWORD,
                cookies=Config.CUIT_COOKIES
            )
            self.classroom_data = student_data["classroom"]
        elif Config.DATA_SOURCE == "manual":
            # 使用手动导入数据
            manual_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "manual_data.json")
            try:
                with open(manual_data_path, "r", encoding="utf-8") as f:
                    manual_data = json.load(f)
                    self.classroom_data = manual_data.get("classroom", MOCK_STUDENT["classroom"])
            except:
                self.classroom_data = MOCK_STUDENT["classroom"]
        else:
            # 使用模拟数据
            self.classroom_data = MOCK_STUDENT["classroom"]
    
    def execute(self, building: str = None, floor: str = None, room: str = None, **kwargs) -> Dict[str, Any]:
        """
        执行教室查询
        
        Args:
            building: 教学楼编号，如"1"、"2"、"3"、"4"或"第一教学楼"、"第四教学楼"
            floor: 楼层，如"1"、"一楼"
            room: 教室编号，如"H4101"
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            if room:
                return self.get_classroom_info(room)
            
            available_rooms = self.classroom_data
            
            # 根据教学楼筛选
            if building:
                building_num = self._parse_building_number(building)
                if building_num:
                    available_rooms = [room for room in available_rooms 
                                      if self._get_building_number(room) == building_num]
            
            # 根据楼层筛选
            if floor:
                floor_num = self._parse_floor_number(floor)
                if floor_num:
                    available_rooms = [room for room in available_rooms 
                                      if self._get_floor_number(room) == floor_num]
            
            # 转换为列表格式，包含详细信息
            rooms_list = []
            for room in available_rooms:
                room_info = self._parse_room_number(room)
                rooms_list.append({
                    "room": room,
                    "building": room_info["building_name"],
                    "building_num": room_info["building_num"],
                    "floor": room_info["floor_name"],
                    "floor_num": room_info["floor_num"],
                    "room_num": room_info["room_num"],
                    "status": "空闲"
                })
            
            # 按教学楼和楼层分组
            grouped_rooms = self._group_rooms_by_building(rooms_list)
            
            result = {
                "success": True,
                "classrooms": rooms_list,
                "grouped": grouped_rooms,
                "count": len(rooms_list),
                "message": f"找到 {len(rooms_list)} 间可用教室"
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"查询教室时出错: {str(e)}"
            }
    
    def _parse_room_number(self, room: str) -> Dict[str, Any]:
        """
        解析教室编号
        
        Args:
            room: 教室编号，如"H1101"
        
        Returns:
            教室信息字典
        """
        # 提取教室编号中的数字部分
        match = re.search(r'H(\d{4})', room)
        if match:
            room_code = match.group(1)
            building_num = int(room_code[0])  # 第一个数字代表教学楼号
            floor_num = int(room_code[1])     # 第二个数字代表楼层
            room_num = room_code[2:4]         # 第三和第四代表教室编号
            
            return {
                "building_num": building_num,
                "building_name": f"第{building_num}教学楼",
                "floor_num": floor_num,
                "floor_name": f"{floor_num}楼",
                "room_num": room_num,
                "full_name": f"第{building_num}教学楼{floor_num}楼{room_code}教室"
            }
        else:
            # 无法解析的教室编号
            return {
                "building_num": 0,
                "building_name": "其他",
                "floor_num": 0,
                "floor_name": "未知",
                "room_num": room,
                "full_name": room
            }
    
    def _get_building_number(self, room: str) -> int:
        """获取教学楼编号"""
        room_info = self._parse_room_number(room)
        return room_info["building_num"]
    
    def _get_floor_number(self, room: str) -> int:
        """获取楼层编号"""
        room_info = self._parse_room_number(room)
        return room_info["floor_num"]
    
    def _parse_building_number(self, building: str) -> int:
        """解析教学楼编号"""
        if building.isdigit():
            return int(building)
        
        # 中文教学楼名称转换
        building_mapping = {
            "第一教学楼": 1, "一教": 1, "教学楼1": 1,
            "第二教学楼": 2, "二教": 2, "教学楼2": 2,
            "第三教学楼": 3, "三教": 3, "教学楼3": 3,
            "第四教学楼": 4, "四教": 4, "教学楼4": 4,
        }
        return building_mapping.get(building, 0)
    
    def _parse_floor_number(self, floor: str) -> int:
        """解析楼层编号"""
        if floor.isdigit():
            return int(floor)
        
        # 中文楼层名称转换
        floor_mapping = {
            "一楼": 1, "一层": 1, "1楼": 1,
            "二楼": 2, "二层": 2, "2楼": 2,
            "三楼": 3, "三层": 3, "3楼": 3,
            "四楼": 4, "四层": 4, "4楼": 4,
            "五楼": 5, "五层": 5, "5楼": 5,
            "六楼": 6, "六层": 6, "6楼": 6,
        }
        return floor_mapping.get(floor, 0)
    
    def _group_rooms_by_building(self, rooms_list: List[Dict]) -> Dict[str, Dict]:
        """按教学楼和楼层分组教室"""
        grouped = {}
        for room in rooms_list:
            building = room["building"]
            floor = room["floor"]
            
            if building not in grouped:
                grouped[building] = {}
            
            if floor not in grouped[building]:
                grouped[building][floor] = []
            
            grouped[building][floor].append(room)
        
        return grouped
    
    def get_building_map(self, building_num: int) -> Dict[str, Any]:
        """
        获取教学楼地图
        
        Args:
            building_num: 教学楼编号
        
        Returns:
            教学楼地图信息
        """
        # 获取该教学楼的所有教室
        building_rooms = [room for room in self.classroom_data 
                         if self._get_building_number(room) == building_num]
        
        # 按楼层分组
        floors = {}
        for room in building_rooms:
            floor_num = self._get_floor_number(room)
            if floor_num not in floors:
                floors[floor_num] = []
            floors[floor_num].append(room)
        
        return {
            "building_num": building_num,
            "building_name": f"第{building_num}教学楼",
            "floors": floors,
            "total_rooms": len(building_rooms)
        }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """
        获取UI组件配置
        
        Returns:
            UI组件配置字典
        """
        return {
            "type": "classroom_query",
            "title": "教室查询",
            "description": "查询当前可用空教室",
            "components": [
                {
                    "type": "button",
                    "label": "查询空教室",
                    "action": "query_classroom"
                },
                {
                    "type": "textbox",
                    "label": "查询结果",
                    "key": "result",
                    "readonly": True
                }
            ]
        }
    
    def get_available_classrooms(self) -> List[str]:
        """获取可用教室列表"""
        return self.classroom_data.copy()
    
    def search_classroom(self, keyword: str) -> List[str]:
        """
        搜索教室
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的教室列表
        """
        return [
            room for room in self.classroom_data
            if keyword in room
        ]
    
    def get_classroom_heatmap(self) -> dict:
        """获取教室空闲热力图数据"""
        heatmap = {}
        for room in self.classroom_data[:10]:
            heatmap[room] = {i: 0 for i in range(1, 13)}
        return heatmap
    
    def get_classroom_info(self, room_number: str) -> Dict[str, Any]:
        """
        获取教室详细信息
        
        Args:
            room_number: 教室编号
        
        Returns:
            教室信息
        """
        room_info = self._parse_room_number(room_number)
        
        if room_number in self.classroom_data:
            return {
                "success": True,
                "room_number": room_number,
                "building": room_info["building_name"],
                "floor": room_info["floor_name"],
                "status": "可用",
                "message": f"教室 {room_number} ({room_info['full_name']}) 当前可用"
            }
        else:
            return {
                "success": False,
                "room_number": room_number,
                "building": room_info["building_name"],
                "floor": room_info["floor_name"],
                "message": f"教室 {room_number} ({room_info['full_name']}) 不存在或不可用"
            }