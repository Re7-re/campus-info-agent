"""
校园信息智能查询系统 - 主程序
多功能模块化校园服务平台
"""

import sys
import os
import argparse
from typing import Optional

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.gradio_ui import create_ui, create_auth_ui
from ui.integrated_ui import create_integrated_ui
from config import Config
from utils.logger import setup_logger


def validate_environment() -> bool:
    """
    验证运行环境
    
    Returns:
        环境是否有效
    """
    logger = setup_logger("main")
    
    # 验证配置
    if not Config.validate():
        logger.error("配置验证失败")
        return False
    
    # 检查必要的依赖包
    required_packages = [
        'gradio',
        'langchain',
        'langgraph',
        'langchain_openai'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"缺少必要的依赖包: {', '.join(missing_packages)}")
        logger.error("请运行: pip install -r requirements.txt")
        return False
    
    logger.info("环境验证通过")
    return True


def start_auth_server():
    """启动登录注册服务器"""
    logger = setup_logger("main")
    
    try:
        # 创建登录注册UI界面
        logger.info("正在创建登录注册界面...")
        demo = create_auth_ui()
        
        # 启动服务器
        server_config = Config.get_server_config()
        logger.info(f"启动登录服务器: {server_config['host']}:{server_config['ui_port']}")
        
        print(f"[OK] 登录注册服务启动成功!")
        print(f"访问地址: http://{server_config['host']}:{server_config['ui_port']}")
        print(f"\n按 Ctrl+C 停止服务器\n")
        
        # 启动Gradio服务器（不指定固定端口，让Gradio自动选择可用端口）
        demo.launch(
            server_name=server_config['host'],
            inbrowser=True,
            show_error=True,
            quiet=False,
            favicon_path=None
        )
        
    except KeyboardInterrupt:
        logger.info("用户中断，程序退出")
        print("\n系统已停止")
        
    except Exception as e:
        logger.error(f"系统启动失败: {str(e)}")
        print(f"系统启动失败: {str(e)}")
        sys.exit(1)


def start_integrated_server():
    """启动集成服务器（登录+主系统）"""
    logger = setup_logger("main")
    
    try:
        # 创建集成UI界面
        logger.info("正在创建集成界面...")
        demo = create_integrated_ui()
        
        # 启动服务器
        server_config = Config.get_server_config()
        logger.info(f"启动集成服务器: {server_config['host']}:{server_config['ui_port']}")
        
        print(f"[OK] 集成服务启动成功!")
        print(f"访问地址: http://{server_config['host']}:{server_config['ui_port']}")
        print(f"日志目录: {Config.LOG_DIR}")
        print(f"数据目录: {Config.DATA_DIR}")
        print(f"记忆目录: {Config.MEMORY_DIR}")
        print(f"\n按 Ctrl+C 停止服务器\n")
        
        # 启动Gradio服务器（不指定固定端口，让Gradio自动选择可用端口）
        demo.launch(
            server_name=server_config['host'],
            inbrowser=True,
            show_error=True,
            quiet=False,
            favicon_path=None
        )
        
    except KeyboardInterrupt:
        logger.info("用户中断，程序退出")
        print("\n系统已停止")
        
    except Exception as e:
        logger.error(f"系统启动失败: {str(e)}")
        print(f"系统启动失败: {str(e)}")
        sys.exit(1)


def start_main_server():
    """启动主应用服务器"""
    logger = setup_logger("main")
    
    try:
        # 创建UI界面
        logger.info("正在创建主应用界面...")
        demo = create_ui()
        
        # 启动服务器
        server_config = Config.get_server_config()
        logger.info(f"启动主服务器: {server_config['host']}:{server_config['ui_port']}")
        
        print(f"[OK] 主应用服务启动成功!")
        print(f"访问地址: http://{server_config['host']}:{server_config['ui_port']}")
        print(f"日志目录: {Config.LOG_DIR}")
        print(f"数据目录: {Config.DATA_DIR}")
        print(f"记忆目录: {Config.MEMORY_DIR}")
        print(f"\n按 Ctrl+C 停止服务器\n")
        
        # 启动Gradio服务器（不指定固定端口，让Gradio自动选择可用端口）
        demo.launch(
            server_name=server_config['host'],
            inbrowser=True,
            show_error=True,
            quiet=False,
            favicon_path=None
        )
        
    except KeyboardInterrupt:
        logger.info("用户中断，程序退出")
        print("\n系统已停止")
        
    except Exception as e:
        logger.error(f"系统启动失败: {str(e)}")
        print(f"系统启动失败: {str(e)}")
        sys.exit(1)


def main():
    """主函数"""
    # 设置日志
    logger = setup_logger("main")
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="校园信息智能查询系统")
    parser.add_argument(
        '--mode',
        type=str,
        choices=['auth', 'main', 'integrated', 'full'],
        default='integrated',
        help="运行模式: auth(仅登录注册), main(仅主应用), integrated(集成模式), full(完整模式)"
    )
    args = parser.parse_args()
    
    # 打印欢迎信息
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          校园信息智能查询系统 v{Config.VERSION}                    ║
    ║                                                              ║
    ║          多功能模块化智能服务平台                              ║
    ║                                                              ║
    ║          功能模块:                                            ║
    ║          AI智能助手  成绩查询  课表查询               ║
    ║          教室查询    考试查询  通知查询               ║
    ║                                                              ║
    ║          用户认证:                                            ║
    ║          登录 / 注册                                         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 验证环境
    if not validate_environment():
        logger.error("环境验证失败，程序退出")
        sys.exit(1)
    
    # 根据模式启动服务
    if args.mode == 'auth':
        start_auth_server()
    elif args.mode == 'main':
        start_main_server()
    elif args.mode == 'integrated':
        start_integrated_server()
    elif args.mode == 'full':
        # 完整模式：启动集成模式
        start_integrated_server()


if __name__ == "__main__":
    main()