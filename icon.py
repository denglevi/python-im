#!/usr/bin/python  
# _*_ coding: utf-8 _*_  
  
import wx  
import winapi
class TaskBarIcon(wx.TaskBarIcon):  
    ID_Hello = wx.NewId()  
    def __init__(self, frame):  
        wx.TaskBarIcon.__init__(self)  
        self.frame = frame  
        self.SetIcon(wx.Icon(name='images/char.ico', type=wx.BITMAP_TYPE_ICO), 'TaskBarIcon!')  
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)  
        self.Bind(wx.EVT_MENU, self.OnHello, id=self.ID_Hello)  
  
    def OnTaskBarLeftDClick(self, event):  
        if self.frame.IsIconized():  
           self.frame.Iconize(False)  
        if not self.frame.IsShown():  
           self.frame.Show(True)  
        self.frame.Raise()  
  
    def OnHello(self, event):  
        wx.MessageBox('Hello From TaskBarIcon!', 'Prompt')  
  
    # override  
    def CreatePopupMenu(self):  
        menu = wx.Menu()  
        menu.Append(self.ID_Hello, 'Hello')  
        return menu  
  
class Frame(wx.Frame):  
    def __init__(  
            self, parent=None, id=wx.ID_ANY, title='TaskBarIcon', pos=wx.DefaultPosition,  
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE  
            ):  
        wx.Frame.__init__(self, parent, id, title, pos, size, style)    
        # create a welcome screen  
        #screen = wx.Image(self.screenIm).ConvertToBitmap()  
        #wx.SplashScreen(screen, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,1000, None, -1)  
        #wx.Yield()  
         
        self.SetIcon(wx.Icon('images/char.ico', wx.BITMAP_TYPE_ICO))  
        panel = wx.Panel(self, wx.ID_ANY)  
        button = wx.Button(panel, wx.ID_ANY, 'Hide Frame', pos=(60, 60))  
         
        sizer = wx.BoxSizer()  
        sizer.Add(button, 0)  
        panel.SetSizer(sizer)  
        self.taskBarIcon = TaskBarIcon(self)          
         
        # bind event  
        self.Bind(wx.EVT_BUTTON, self.OnHide, button)  
        self.Bind(wx.EVT_CLOSE, self.OnClose)  
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy) # 最小化事件绑定  
    def OnHide(self, event):  
        self.Hide()  
    def OnIconfiy(self, event):  
        wx.MessageBox('Frame has been iconized!', 'Prompt')  
        event.Skip()  
    def OnClose(self, event):  
        self.taskBarIcon.Destroy()  
        self.Destroy()  
  
def TestFrame():  
    app = wx.PySimpleApp()  
    frame = Frame(size=(640, 480))  
    frame.Centre()  
    frame.Show()  
    app.MainLoop()  
if __name__ == '__main__':  
    TestFrame() 