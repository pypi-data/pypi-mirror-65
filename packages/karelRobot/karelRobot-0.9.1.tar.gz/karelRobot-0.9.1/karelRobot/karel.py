from enum import Enum
import pickle
import time
import copy
import pathlib
import sys

class Orientation(Enum):
    NORTH=0
    EAST=1
    SOUTH=2
    WEST=3

class Point:
    def __init__(self,x,y):
        self.X=x
        self.Y=y

    def __eq__(self, other):
        if self.X != other.X:
            return False
        if self.Y != other.Y:
            return False
        return True

class Wall:
    def __init__(self):
        self.Right=False
        self.Top=False

class Cell:
    def __init__(self,wall,beepers):
        self.Wall = wall
        self.Beepers =beepers
    def SetRightWall(self):
        self.Wall.Right=True
    def SetTopWall(self):
        self.Wall.Top=True
    def RemoveRightWall(self):
        self.Wall.Right=False
    def RemoveTopWall(self):
        self.Wall.Top=False
    def IncreaseBeeper(self):
        self.Beepers=self.Beepers+1
    def DecreaseBeeper(self):
        if self.Beepers>0:
            self.Beepers=self.Beepers-1

class World:
    def __init__(self,rows,columns):
        self.Rows=rows
        self.Columns=columns
        self.Cells = [[Cell(Wall(),0) for i in range(self.Rows)] for i in range(self.Columns)]


    def GetCell(self ,location):
        return self.Cells[location.X-1][location.Y-1]


class KarelError(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self) #初始化父类
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo


class Karel:
    def __init__(self,world,position,orientation,beepers=None):
        self.World=world
        self.Position =position
        self.Orientation =orientation
        self.CallBack = None
        self.Spot = []
        if beepers==None:
            self.Beepers = sys.maxsize
        else:
            self.Beepers = beepers
    
    def Delay2(self):
        time.sleep(0.25)


    def SetKarelPosition(self,position):
        self.Position =position
    def SetKarelOrientation(self,orientation):
        self.Orientation =orientation

    def Run(self):
        self.Move()
        self.PutBeeper()
        self.Move()
        self.PutBeeper()
        self.Move()
        self.PutBeeper()
        self.Move()
        self.PutBeeper()
        self.Move()

    
    def Snapshot(self):
        self.Spot = copy.deepcopy([self.World,self.Position,self.Orientation])
        
    def ReLoad(self):
        if len(self.Spot)>0:
            self.World = self.Spot[0]
            self.Position = self.Spot[1]
            self.Orientation = self.Spot[2]
    
    def RefreshView(self):
        if self.CallBack!=None:
            self.CallBack()

    def Move(self):
        self.Delay2()
        if not self.FrontIsClear():
            raise KarelError('Karel is blocked!')
        if self.Orientation==Orientation.EAST:
            self.Position.X=self.Position.X+1
            self.RefreshView()
            return
        if self.Orientation==Orientation.NORTH:
            self.Position.Y=self.Position.Y+1
            self.RefreshView()
            return
        if self.Orientation==Orientation.WEST:
            self.Position.X=self.Position.X-1
            self.RefreshView()
            return
        if self.Orientation==Orientation.SOUTH:
            self.Position.Y=self.Position.Y-1
            self.RefreshView()
            return


    def FrontIsClear(self):
        x=self.Position.X
        y = self.Position.Y
        orientation =self.Orientation

        result = True
        if orientation==Orientation.EAST:
            if x==self.World.Columns or self.World.GetCell(Point(x,y)).Wall.Right:
                result =  False
        if orientation==Orientation.WEST:
            if x==1 or self.World.GetCell(Point(x-1,y)).Wall.Right:
                result =  False
        if orientation==Orientation.NORTH:
            if y==self.World.Rows or self.World.GetCell(Point(x,y)).Wall.Top:
                result =  False
        if orientation==Orientation.SOUTH:
            if y==1 or self.World.GetCell(Point(x,y-1)).Wall.Top:
                result =  False
        return result

    def FrontIsBlocked(self):
        return not self.FrontIsClear()

    
    def RightIsClear(self):
        x=self.Position.X
        y = self.Position.Y
        orientation =self.Orientation

        result = True
        if orientation==Orientation.EAST:
            if y==1 or self.World.GetCell(Point(x,y-1)).Wall.Top:
                result =  False
        if orientation==Orientation.WEST:
            if y==self.World.Rows or self.World.GetCell(Point(x,y)).Wall.Top:
                result =  False
        if orientation==Orientation.NORTH:
            if x==self.World.Columns or self.World.GetCell(Point(x,y)).Wall.Right:
                result =  False
        if orientation==Orientation.SOUTH:
            if x==1 or self.World.GetCell(Point(x-1,y)).Wall.Right:
                result =  False
        return result
    
    def RightIsBlocked(self):
        return not self.RightIsClear()

    
    def LeftIsClear(self):
        x=self.Position.X
        y = self.Position.Y
        orientation =self.Orientation

        result = True
        if orientation==Orientation.EAST:
            if y==self.World.Rows or self.World.GetCell(Point(x,y)).Wall.Top:
                result =  False
        if orientation==Orientation.WEST:
            if y==1 or self.World.GetCell(Point(x,y-1)).Wall.Top:
                result =  False
        if orientation==Orientation.NORTH:
            if x==1 or self.World.GetCell(Point(x-1,y)).Wall.Right:
                result =  False
        if orientation==Orientation.SOUTH:
            if x==self.World.Columns or self.World.GetCell(Point(x,y)).Wall.Right:
                result =  False
        return result
    
    def LeftIsBlocked(self):
        return not self.LeftIsClear()

    


    def PickBeeper(self):
        self.Delay2()
        x = self.Position.X
        y = self.Position.Y
        if self.BeepersPresent():
            self.World.GetCell(Point(x,y)).DecreaseBeeper()
            self.Beepers = self.Beepers+1
            self.RefreshView()
        else:
            raise KarelError('No Beepers on this corner!')

    def BeepersPresent(self):
        if self.World.GetCell(Point(self.Position.X,self.Position.Y)).Beepers > 0:
            return True
        return False
    
    def NoBeepersPresent(self):
        return not self.BeepersPresent()

    def BeepersInBag(self):
        if self.Beepers>0:
            return True
        return False
    
    def NoBeepersInBag(self):
        return not self.BeepersInBag()

    def FacingNorth(self):
        return self.Orientation==Orientation.NORTH

    def NotFacingNorth(self):
        return not self.NotFacingNorth()

    def FacingEast(self):
        return self.Orientation==Orientation.EAST

    def NotFacingEast(self):
        return not self.NotFacingEast()

    def FacingSouth(self):
        return self.Orientation==Orientation.SOUTH

    def NotFacingSouth(self):
        return not self.NotFacingSouth()

    def FacingWest(self):
        return self.Orientation==Orientation.WEST

    def NotFacingWest(self):
        return not self.NotFacingWest()

    def PutBeeper(self):
        self.Delay2()
        x = self.Position.X
        y = self.Position.Y
        if self.NoBeepersInBag():
            raise KarelError('No Beepers in bag!')
        self.Beepers = self.Beepers -1
        self.World.GetCell(Point(x,y)).IncreaseBeeper()
        self.RefreshView()

    def TurnLeft(self):
        self.Delay2()
        if self.Orientation==Orientation.EAST:
            self.Orientation=Orientation.NORTH
            self.RefreshView()
            return
        if self.Orientation==Orientation.NORTH:
            self.Orientation=Orientation.WEST
            self.RefreshView()
            return
        if self.Orientation==Orientation.WEST:
            self.Orientation=Orientation.SOUTH
            self.RefreshView()
            return
        if self.Orientation==Orientation.SOUTH:
            self.Orientation=Orientation.EAST
            self.RefreshView()
            return
        



    #序列化与反序列化
    def Serialize(self,filePath):
        file = open(filePath, 'wb+')
        pickle.dump(self, file)
        file.close()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['CallBack']  # manually delete
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        return state

    @staticmethod
    def Derialize(filePath):
        path = pathlib.Path(filePath)
        print(path)
        if not path.is_file():
            return None
        rpickle_file = open(filePath, 'rb')
        return pickle.load(rpickle_file)






