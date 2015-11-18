import wx 
import time
from threading import Thread

def test1():
    for i in range(10):
        print i
        time.sleep(1)

class TestFrame(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, -1, "Test") 
        panel = wx.Panel(self, -1) 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        panel.SetSizer(sizer) 

        self.button = wx.Button(panel, 0, "Start")
        sizer.Add(self.button, 0, wx.ALIGN_LEFT) 
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)

        self.text = wx.StaticText(panel, 0, "No test is running")
        sizer.Add(self.text, 0, wx.ALIGN_LEFT) 

        self.timer = wx.Timer(self)

    def OnButton(self, event):

        self.text.SetLabel("Running")
        self.button.Disable()
        self.Bind(wx.EVT_TIMER, self.PollThread)
        self.timer.Start(20, oneShot=True)
        self.testThread = Thread(target=test1)
        self.testThread.start()
        event.Skip()

    def PollThread(self, event):
        if self.testThread.isAlive():
            self.Bind(wx.EVT_TIMER, self.PollThread)
            self.timer.Start(200, oneShot=True)
            self.text.SetLabel(self.text.GetLabel() + ".")
        else:
            self.button.Enable()
            self.text.SetLabel("Test completed")
"""
import base64
 
with open("images/user.png", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    print str
    return
fh = open("imageToSave.png", "wb")
fh.write(str.decode('base64'))
fh.close()
"""
app = wx.PySimpleApp() 
TestFrame().Show() 
app.MainLoop()