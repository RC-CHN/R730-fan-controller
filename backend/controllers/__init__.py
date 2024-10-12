# controllers/__init__.py

# 导入 fan_controller 模块
from .fan_controller import start_fan_controller

# 公开的模块
__all__ = ['start_fan_controller']
