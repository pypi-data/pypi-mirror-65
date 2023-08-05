#  MIT License
#  Copyright (C) Michael Tao-Yi Lee (taoyil AT UCI EDU)
import platform

from .callbacks import CapData

if platform.system() == "Linux":
    from .linux.sensorBoard import SensorBoard
elif platform.system() == "Darwin":
    pass
elif platform.system() == "Windows":
    from .windows.sensorBoard import SensorBoard
