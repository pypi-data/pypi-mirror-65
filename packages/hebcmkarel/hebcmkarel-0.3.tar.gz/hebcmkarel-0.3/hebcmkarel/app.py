import tkinter
import threading
from  hebcmkarel.settings import SettingsDialog
from hebcmkarel.karelmain import Orientation, Point, Wall, Cell, World, KarelMain, KarelError
import tkinter.filedialog
import tkinter.messagebox
import configparser
import hebcmkarel.superkarel as superkarel
import os

iconspath = os.path.dirname(os.path.abspath(__file__)) + "/icons"

class ConfigIni:
    def __init__(self):
        self.m_FileName = 'config.ini'
    

    def Get(self,key,default):
        config = configparser.ConfigParser()
        config.read(self.m_FileName)
        return config.get('default',key, fallback=default)
    

    def Set(self,key,value):
        config = configparser.ConfigParser()
        config.add_section("default")
        config.set('default',key, value)
        config.write(open(self.m_FileName, "w"))


class KarelUI:
    def __init__(self,window,canvas):
        self.m_mainWindow =window
        self.m_Canvas=canvas
        self.m_CanvasHeight= 0
        self.m_CanvasWidth = 0
        self.m_EditMode =False
        self.m_Buttons = None
        self.m_IsRunning =False
        self.m_FileName =''
        self.m_Config = ConfigIni()
        self.InitKarel()

    def InitKarel(self):
        self.m_FileName = self.m_Config.Get('LastFile','')
        if(self.m_FileName!=''):
            self.LoadMap(self.m_FileName)
        else:
            self.NewKarel()
        

    def SetFile(self,fileName):
        self.m_FileName = fileName
        if self.m_FileName!='':
            self.m_mainWindow.title("KarelRobot -" +  self.m_FileName)
        else:
            self.m_mainWindow.title("KarelRobot")
        self.m_Config.Set('LastFile',self.m_FileName)

    def SetKarel(self,karel):
        self.m_Karel=karel
        self.m_Karel.CallBack = self.ReDrawPartial
        superkarel.g_Karel = self.m_Karel
        self.ReDraw()

    def NewKarel(self):
        world = World(5,8)
        karel = KarelMain(world, Point(1, 1), Orientation.EAST)
        self.SetKarel(karel)
        self.SetFile('')


    def Clear(self):
        for p in (self.m_Canvas.find_all()):
            self.m_Canvas.delete(p)

    def OnResize(self,event):
        #if self.CanvasHeight!=event.height  or self.CanvasWidth!=event.width:
        self.m_CanvasHeight=event.height
        self.m_CanvasWidth =event.width
        self.ReDraw()

    def ReDrawPartial(self):
        karelX = self.m_Karel.Position.X
        karelY = self.m_Karel.Position.Y  
        #定义绘图坐标范围 startX,startY,endX,endY
        startX,startY,endX,endY, marginX,marginY, cellSize,  rows,columns = self.GetRange()      

        #清除墙，beepers,karel
        for p in (self.m_Canvas.find_withtag("karel")):
            self.m_Canvas.delete(p)
        for p in (self.m_Canvas.find_withtag('cell'+str(karelX)+'_'+str(karelY))):
            self.m_Canvas.delete(p)
        #画所在格子的墙
        self.RedrawWalls(startX, marginX, karelX, cellSize, startY, marginY, rows, karelY)
        #画所在格子的beepers
        self.RedrawBeepers(startX, marginX, karelX, cellSize, startY, marginY, rows, karelY)
        #画Karel
        self.RedrawKarel(startX, marginX, cellSize, startY, marginY, rows)

    def GetRange(self):
        #定义绘图坐标范围 startX,startY,endX,endY
        startX=0
        startY=0
        endX=self.m_CanvasWidth
        endY=self.m_CanvasHeight
        #确定绘图边缘，注意格子必须是方的,上边缘为0.5个格子大小
        columns = self.m_Karel.World.Columns
        rows=self.m_Karel.World.Rows
        cellSize = 0
        if (endX-startX)/columns > (endY-startY)/rows:
            cellSize = (endY-startY) / (rows+1.5)
        else:
            cellSize = (endX-startX) / (columns+2)

        marginX = (endX-startX - (columns+2) * cellSize)/2
        marginY = (endY-startY - (rows+1.5) * cellSize)/2

        startX=startX+cellSize
        endX=endX-cellSize
        startY =startY+0.5*cellSize
        endY =endY-cellSize

        return startX,startY,endX,endY, marginX,marginY, cellSize,  rows,columns


    def ReDraw(self):
        self.Clear()
        #定义绘图坐标范围 startX,startY,endX,endY
        startX,startY,endX,endY, marginX,marginY, cellSize,rows,columns = self.GetRange()

        #画内侧虚线
        if  self.m_EditMode:
            for x in range(1,columns):
                self.m_Canvas.create_line(startX+marginX+x*cellSize,startY+marginY,startX+marginX+x*cellSize,endY-marginY,fill='Gainsboro')
            for y in range(1,rows):
                self.m_Canvas.create_line(startX+marginX,startY+marginY+y*cellSize,endX-marginX,startY+marginY+y*cellSize,fill='Gainsboro')

        #画坐标
        for x in range(1,rows+1):
            textx  = startX+marginX-0.3*cellSize
            texty = endY-marginY+0.5*cellSize
            self.m_Canvas.create_text(textx,texty-cellSize*x,text=str(x),font=('Times',int(cellSize/4)))
        for y in range(1,columns+1):
            textx  = startX+marginX-0.5*cellSize
            texty = endY-marginY+0.3*cellSize
            self.m_Canvas.create_text(textx+y*cellSize,texty,text=str(y),font=('Times',int(cellSize/4)))


        #画边框实线
        self.m_Canvas.create_line(startX+marginX,startY+marginY,endX-marginX,startY+marginY,width=2)
        self.m_Canvas.create_line(endX-marginX,startY+marginY,endX-marginX,endY-marginY,width=2)
        self.m_Canvas.create_line(endX-marginX,endY-marginY,startX+marginX,endY-marginY,width=2)
        self.m_Canvas.create_line(startX+marginX,endY-marginY,startX+marginX,startY+marginY,width=2)

        #绘制定位点
        if not self.m_EditMode:
            for x in range(1,columns+1):
                for y in range(1,rows+1):
                    topleftX = startX+marginX+(x-1)*cellSize
                    topleftY = startY+marginY+(rows-y)*cellSize
                    beeperlist = []
                    self.AppendCoordinate(beeperlist,topleftX + 0.5*cellSize,topleftY + 0.4*cellSize)
                    self.AppendCoordinate(beeperlist,topleftX + 0.6*cellSize,topleftY + 0.5*cellSize)
                    self.AppendCoordinate(beeperlist,topleftX + 0.5*cellSize,topleftY + 0.6*cellSize)
                    self.AppendCoordinate(beeperlist,topleftX + 0.4*cellSize,topleftY + 0.5*cellSize)
                    self.m_Canvas.create_polygon(beeperlist,fill='Gainsboro')

        #绘制墙和beepers
        for x in range(1,columns+1):
            for y in range(1,rows+1):
                self.RedrawWalls(startX, marginX, x, cellSize, startY, marginY, rows, y)
                self.RedrawBeepers(startX, marginX, x, cellSize, startY, marginY, rows, y)                

        #画Karel
        if not self.m_EditMode:
            self.RedrawKarel(startX, marginX, cellSize, startY, marginY, rows)

    def RedrawWalls(self, startX, marginX, x, cellSize, startY, marginY, rows, y):
        topleftX = startX+marginX+(x-1)*cellSize
        topleftY = startY+marginY+(rows-y)*cellSize
        if self.m_Karel.World.GetCell(Point(x,y)).Wall.Right:
            self.m_Canvas.create_line(topleftX+cellSize,topleftY,topleftX+cellSize,topleftY+cellSize,tag='cell'+str(x)+'_'+str(y))
        if self.m_Karel.World.GetCell(Point(x,y)).Wall.Top:
            self.m_Canvas.create_line(topleftX,topleftY,topleftX+cellSize,topleftY,tag='cell'+str(x)+'_'+str(y))

    def RedrawBeepers(self, startX, marginX, x, cellSize, startY, marginY, rows, y):
        topleftX = startX+marginX+(x-1)*cellSize
        topleftY = startY+marginY+(rows-y)*cellSize
        if self.m_Karel.World.GetCell(Point(x,y)).Beepers>0:
            beeperlist = []
            self.AppendCoordinate(beeperlist,topleftX + 0.5*cellSize,topleftY + 0.2*cellSize)
            self.AppendCoordinate(beeperlist,topleftX + 0.8*cellSize,topleftY + 0.5*cellSize)
            self.AppendCoordinate(beeperlist,topleftX + 0.5*cellSize,topleftY + 0.8*cellSize)
            self.AppendCoordinate(beeperlist,topleftX + 0.2*cellSize,topleftY + 0.5*cellSize)
            self.m_Canvas.create_polygon(beeperlist,fill='Gainsboro',tag='cell'+str(x)+'_'+str(y))

        if self.m_Karel.World.GetCell(Point(x,y)).Beepers>1:
            textx  = topleftX+0.5*cellSize
            texty = topleftY+0.5*cellSize
            self.m_Canvas.create_text(textx,texty,text=self.m_Karel.World.GetCell(Point(x,y)).Beepers,font=('Times',int(cellSize/6)),tag='cell'+str(x)+'_'+str(y))

    def RedrawKarel(self, startX, marginX, cellSize, startY, marginY, rows):
        karelX = startX+marginX+(self.m_Karel.Position.X-1)*cellSize 
        karelY = startY+marginY+(rows-self.m_Karel.Position.Y)*cellSize
        karelVector = []
        
        self.AppendVector(karelVector,karelX,karelY,0.3,0.1,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.75,0.1,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.9,0.25,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.9,0.8,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.45,0.8,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.3,0.65,cellSize,self.m_Karel.Orientation)
        self.m_Canvas.create_polygon(karelVector,fill='Gainsboro',tag='karel')
        karelVector.clear()
        self.AppendVector(karelVector,karelX,karelY,0.6,0.8,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.68,0.8,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.68,0.88,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.76,0.88,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.76,0.96,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.6,0.96,cellSize,self.m_Karel.Orientation)
        self.m_Canvas.create_polygon(karelVector,tag='karel')
        karelVector.clear()
        self.AppendVector(karelVector,karelX,karelY,0.14,0.49,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.3,0.49,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.3,0.57,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.22,0.57,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.22,0.65,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.14,0.65,cellSize,self.m_Karel.Orientation)
        self.m_Canvas.create_polygon(karelVector,tag='karel')
        karelVector.clear()
        self.AppendVector(karelVector,karelX,karelY,0.4,0.2,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.7,0.6,cellSize,self.m_Karel.Orientation)
        self.m_Canvas.create_rectangle(karelVector,tag='karel')
        karelVector.clear()
        self.AppendVector(karelVector,karelX,karelY,0.55,0.65,cellSize,self.m_Karel.Orientation)
        self.AppendVector(karelVector,karelX,karelY,0.7,0.65,cellSize,self.m_Karel.Orientation)
        self.m_Canvas.create_line(karelVector,tag='karel')



    def AppendCoordinate(self,vector,x,y):
        vector.append(x)
        vector.append(y)

    def AppendVector(self,vector,baseX,baseY,xRation,yRation,size,faceTo):
        centerX = baseX+0.5*size
        centerY = baseY+0.5*size
        relativeX=baseX+xRation*size-centerX
        relativeY=baseY+yRation*size-centerY
        if faceTo==Orientation.EAST:
            newRelativeX = relativeX
            newRelationY = relativeY
        if faceTo==Orientation.NORTH:
            newRelativeX = relativeY
            newRelationY = -relativeX
        if faceTo==Orientation.WEST:
            newRelativeX = -relativeX
            newRelationY = -relativeY
        if faceTo==Orientation.SOUTH:
            newRelativeX = -relativeY
            newRelationY = relativeX
        vector.append(newRelativeX+centerX)
        vector.append(newRelationY+centerY)
     
        

    def Exec(self, callback):
        thread1 = ProcessThread(self, callback)
        thread1.start()

    def CreatePolygon(self,*args,**kw):
        self.m_Canvas.create_polygon(args,kw)

    def SetEditMode(self):
        self.m_EditMode =True
        self.UpdateButtonsState()
        self.ReDraw()
    def SetRunningMode(self):
        self.m_EditMode =False
        self.UpdateButtonsState()
        self.ReDraw()

    def UpdateButtonsState(self):

        if self.m_IsRunning: 
            self.m_Buttons['run'].config(state='disabled')
            self.m_Buttons['reload'].config(state='disabled')
            self.m_Buttons['runningMode'].config(state='disabled')
            self.m_Buttons['editMode'].config(state='disabled')
            self.m_Buttons['settings'].config(state='disabled')
            self.m_Buttons['open'].config(state='disabled')
            self.m_Buttons['new'].config(state='disabled')
            self.m_Buttons['save'].config(state='disabled')
            self.m_Buttons['saveAs'].config(state='disabled')
        else:
            self.m_Buttons['open'].config(state='normal')
            self.m_Buttons['new'].config(state='normal')
            if self.m_EditMode:
                self.m_Buttons['editMode'].config(state='disabled')
                self.m_Buttons['runningMode'].config(state='normal')
                self.m_Buttons['settings'].config(state='normal')
                self.m_Buttons['save'].config(state='normal')
                self.m_Buttons['saveAs'].config(state='normal')
                self.m_Buttons['run'].config(state='disabled')
                self.m_Buttons['reload'].config(state='disabled')
            else:
                self.m_Buttons['runningMode'].config(state='disabled')
                self.m_Buttons['editMode'].config(state='normal')
                self.m_Buttons['settings'].config(state='disabled')
                self.m_Buttons['save'].config(state='disabled')
                self.m_Buttons['saveAs'].config(state='disabled')
                self.m_Buttons['run'].config(state='normal')
                self.m_Buttons['reload'].config(state='normal')

        

    def SetWallOrBeeper(self,event):
        if self.m_EditMode:
            action="set"
            self.EditWallOrBeepers(event, action)

    def RemoveWallOrBeeper(self,event):
        if self.m_EditMode:
            action="remove"
            self.EditWallOrBeepers(event, action)

    def EditWallOrBeepers(self, event, action):
        #定义绘图坐标范围 startX,startY,endX,endY
        startX,startY,endX,endY, marginX,marginY, cellSize,rows,columns = self.GetRange()
        #右墙的横坐标，在正负一定范围内
        rightWallX = round((event.x-startX-marginX)/cellSize)
        wallY = int((event.y-startY-marginY)/cellSize)
        diff=4
        if event.x >= startX+marginX+(rightWallX *cellSize)-diff  and event.x <= startX+marginX+(rightWallX *cellSize)+diff:
            if self.validate(rightWallX,rows-wallY,rows,columns):
                self.EditRightWall(rightWallX,rows-wallY,action)
        #上墙的纵坐标，在正负一定范围内
        TopWallY = round((event.y-startY-marginY)/cellSize)
        wallX = int((event.x-startX-marginX)/cellSize)
        if event.y >= startY+marginY+(TopWallY *cellSize)-diff  and event.y <= startY+marginY+(TopWallY *cellSize)+diff:
            if self.validate(wallX+1,rows-TopWallY,rows,columns):
                self.EditTopWall(wallX+1,rows-TopWallY,action)
        #beeper的坐标
        if event.y >= startY+marginY+(wallY *cellSize)+diff  and event.y <= startY+marginY+((wallY+1) *cellSize)-diff \
          and event.x >= startX+marginX+(wallX *cellSize)+diff  and event.x <= startX+marginX+((wallX+1) *cellSize)-diff :
            if self.validate(wallX+1,rows-wallY,rows,columns):
                self.EditBeepers(wallX+1,rows-wallY,action)
    
    
    def validate(self,x,y,rows,columns):
        if x<=columns and y<=rows and x>0 and y>0 :
            return True
        else:
            return False
        

    def EditRightWall(self,x,y,action):
        if action=="set":
            self.m_Karel.World.GetCell(Point(x,y)).SetRightWall()
        else:
            self.m_Karel.World.GetCell(Point(x,y)).RemoveRightWall()
        self.ReDraw()

    def EditTopWall(self,x,y,action):
        if action=="set":
            self.m_Karel.World.GetCell(Point(x,y)).SetTopWall()
        else:
            self.m_Karel.World.GetCell(Point(x,y)).RemoveTopWall()
        self.ReDraw()

    def EditBeepers(self,x,y,action):
        if action=="set":
            self.m_Karel.World.GetCell(Point(x,y)).IncreaseBeeper()
        else:
            self.m_Karel.World.GetCell(Point(x,y)).DecreaseBeeper()
        self.ReDraw()
    def ConfigWorld(self):
        settings  = SettingsDialog(self.m_mainWindow, title='settings') 
        if settings.result=="ID_OK":
            world = World(settings.m_Data['rows'],settings.m_Data['columns'])
            karel = KarelMain(world, Point(settings.m_Data['x'], settings.m_Data['y']), Orientation.EAST,settings.m_Data['beepers'])
            self.SetKarel(karel)

    def SaveMap(self):
        if self.m_FileName=='':
            fileName = tkinter.filedialog.asksaveasfilename(title=u'保存地图文件',defaultextension=".kw",filetypes=[("Karel World File",".kw")])
            if len(fileName)==0:
                return
            self.SetFile(str(fileName))
        self.m_Karel.Serialize(self.m_FileName)
    
    def SaveMapAs(self):
        fileName = tkinter.filedialog.asksaveasfilename(title=u'保存地图文件',defaultextension=".kw",filetypes=[("Karel World File",".kw")])
        if len(fileName)!=0:
            return
        self.SetFile(str(fileName))
        self.m_Karel.Serialize(self.m_FileName)

    def LoadMap(self,fileName):
        karel = Karel.Derialize(fileName)
        if karel!=None:
            self.SetKarel(karel)
            self.SetFile(fileName)
        else:
            self.NewKarel()
    
    def OpenMap(self):
        fileName =  tkinter.filedialog.askopenfilename(title=u'打开地图文件',defaultextension=".kw",filetypes=[("Karel World File",".kw")])
        if len(fileName)!=0:
            self.LoadMap(str(fileName))

    def ReLoad(self):
        self.m_Karel.ReLoad()
        self.ReDraw()



class ProcessThread (threading.Thread):
    def __init__(self, karelUI, callback):
        threading.Thread.__init__(self)
        self.m_KarelUI = karelUI
        self.m_callback = callback
    def run(self):
        self.m_KarelUI.m_Karel.Snapshot()
        self.m_KarelUI.m_IsRunning = True
        self.m_KarelUI.UpdateButtonsState()

        try:
            self.m_callback()
        except KarelError as e:
            print (e)
            tkinter.messagebox.showerror("error",e)
        finally:
            self.m_KarelUI.m_IsRunning=False
            self.m_KarelUI.UpdateButtonsState()


# karel UI窗口
class Application(tkinter.Frame):
    def __init__(self,callback,master=None):
        tkinter.Frame.__init__(self,master)
        self.pack()
        self.master.title("Karel Robot")
        self.master.geometry('640x480')
        self.callback = callback
        self.createWidgets()

    def createWidgets(self):
        cv = tkinter.Canvas(self.master, width=65535, height=65535, bg="white")
        cv.pack()
        self.pack(side="bottom", padx=2, pady=2)

        self.karelUI = KarelUI(self.master,cv)
        #使用成员变量，避免被回收
        self.iconOpen = tkinter.PhotoImage(file=iconspath + "/open.png")
        self.iconNew = tkinter.PhotoImage(file=iconspath + "/new.png")
        self.iconSave = tkinter.PhotoImage(file=iconspath + "/save.png")
        self.iconSaveAs = tkinter.PhotoImage(file=iconspath + "/saveas.png")
        self.iconEditMode = tkinter.PhotoImage(file=iconspath + "/edit.png")
        self.iconRunMode = tkinter.PhotoImage(file=iconspath + "/running.png")
        self.iconStart = tkinter.PhotoImage(file=iconspath + "/play.png")
        #iconStop = tkinter.PhotoImage(file=iconspath + "/stop.png")
        self.iconReload = tkinter.PhotoImage(file=iconspath + "/reload.png")
        self.iconSettings = tkinter.PhotoImage(file=iconspath + "/settings.png")
        buttons = {}
        buttons['new'] =  tkinter.Button(self, text='新建',image=self.iconNew,command=self.karelUI.NewKarel)
        buttons['new'].pack(  side='left',anchor='w',padx=4)
        buttons['open']= tkinter.Button(self, text='打开',image=self.iconOpen,command=self.karelUI.OpenMap)
        buttons['open'].pack( side='left',anchor='w',padx=4)
        buttons['save'] = tkinter.Button(self, text='保存',image=self.iconSave,command=self.karelUI.SaveMap)
        buttons['save'].pack( side='left',anchor='w',padx=4)
        buttons['saveAs'] = tkinter.Button(self, text='另存为',image=self.iconSaveAs,command=self.karelUI.SaveMapAs)
        buttons['saveAs'].pack( side='left',anchor='w',padx=4)
        buttons['runningMode'] = tkinter.Button(self, text='运行',image=self.iconRunMode,command=self.karelUI.SetRunningMode)
        buttons['runningMode'].pack( side='left',anchor='w',padx=4)
        buttons['editMode'] = tkinter.Button(self, text='编辑',image=self.iconEditMode,command=self.karelUI.SetEditMode)
        buttons['editMode'].pack( side='left',anchor='w',padx=4)
        buttons['settings'] = tkinter.Button(self, text='设置',image=self.iconSettings,command=self.karelUI.ConfigWorld)
        buttons['settings'].pack( side='left',anchor='w',padx=4)
        # buttons['run'] = tkinter.Button(self, text='执行',image=self.iconStart,command=self.karelUI.Exec)
        buttons['run'] = tkinter.Button(
            self, text='执行', image=self.iconStart, command=lambda: self.karelUI.Exec(self.callback))
        buttons['run'].pack(side='left',anchor='w',padx=4)
        # buttons['stop'] = tkinter.Button(self, text='停止',image=iconStop)
        # buttons['stop'].pack( side='left',anchor='w',padx=4)
        buttons['reload'] = tkinter.Button(self, text='重置',image=self.iconReload,command = self.karelUI.ReLoad)
        buttons['reload'].pack(side='left',anchor='w',padx=4)

        self.karelUI.m_Buttons=buttons
        self.karelUI.UpdateButtonsState()
        cv.bind("<Configure>", self.karelUI.OnResize)
        cv.bind("<Button-1>", self.karelUI.SetWallOrBeeper)
        cv.bind("<Button-3>", self.karelUI.RemoveWallOrBeeper)


# 显示karel程序
def run(callback) :
    Application(callback).mainloop()
