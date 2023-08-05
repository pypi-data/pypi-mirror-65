# karelRobot

Karel Robot 0.9  

参考斯坦福大学编程方法使用的Java框架
**河北中医学院计算机教研室** 用于教学用途

### 1. 使用方法

（1）使用 pip 下载karelRobot库

```python
pip install karelRobot
```

（2）建立 ***.py 文件

```python
import karelRobot.app
from karelRobot.superkarel import *

# 自定义动作
def myfun():
    Move()

# 显示karel窗口
karelRobot.app.run(myfun)
```

### 2. karel核心方法

##### （1）karel内置动作

|   动作方法    |                            解释                            |                           备注                           |
| :-----------: | :--------------------------------------------------------: | :------------------------------------------------------: |
|    Move( )    |                    卡雷尔向前方移动一步                    | 当一堵墙挡在卡雷尔面前的时候，卡雷尔不能响应 Move( )命令 |
|  TurnLeft( )  |                 卡雷尔向左转90度（逆时针）                 |                卡雷尔的面向方向会一并修改                |
| PickBeeper( ) |  卡雷尔捡起街角上的蜂鸣器，把它放到卡雷尔的蜂鸣器收藏包里  |                收藏包可容纳无限多的蜂鸣器                |
| PutBeeper( )  | 卡雷尔从蜂鸣器收藏包里拿出一个蜂鸣器，放在卡雷尔所在的位置 |                                                          |

##### （2）karel条件监测

| **判断内容**         | **测试条件**                                                 | **相反的测试条件**                                           |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 面前是否有墙         | **FrontIsClear( )**：面前无墙返回   True                     | FrontIsBlocked( )   ：面前有墙返回   True                    |
| 左面/右面是否有墙    | LeftIsClear( )、RightIsClear( )                              | LeftIsBlocked( )、RightIsBlocked( )                          |
| 当前位置是否有蜂鸣器 | **BeepersPresent( )** ：所在位置有蜂鸣器返回   True          | NoBeepersPresent( )   ：所在位置无蜂鸣器返回True             |
| 背包里是否有蜂鸣器   | **BeepersInBag( )** ：背包里有蜂鸣器返回   True              | NoBeepersInBag( )   ：背包里无蜂鸣器返回True                 |
| 判断当前朝向         | **FacingNorth**( )****、****FacingEast****( )****、****FacingSouth****( )****、****FacingWest****( )** | NotFacingNorth( )、NotFacingEast( )、NotFacingSouth( )、NotFacingWest( ) |





