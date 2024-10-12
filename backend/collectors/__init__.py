# collectors/__init__.py

# 这里可以导入本模块内的功能，方便在其他地方导入时直接使用。
from .ipmi_collector import start_ipmi_collector

# 公开的模块
__all__ = ['start_ipmi_collector']
