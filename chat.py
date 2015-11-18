#_*_coding:utf-8_*_
'''
Created on 2014-4-29

@author: denglevi
'''
import wx
import time
import  wx.lib.scrolledpanel as scrolled
from wx._core import BITMAP_TYPE_ANY
import xmpp
import os
import tools

class ChatLayoutf(wx.Panel):
    def __init__(self, parent,conn,jid,nickname):
        wx.Panel.__init__(self, parent, -1,name=jid)
        self.SetAutoLayout(True)
        self.detailPanel = wx.Panel(self, -1, style=wx.RAISED_BORDER)
        self.detailPanel.SetBackgroundColour(wx.WHITE)
        self.jid = jid
        self.nickname = nickname
        self.conn = conn = conn  
        self.initUI()
        
    def initUI(self):
        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        leftP = wx.Panel(self,-1)
        boxsizerL = wx.BoxSizer(wx.VERTICAL)
        self.contentPanel = scrolled.ScrolledPanel(leftP, -1)
        self.contentPanel.SetBackgroundColour('white')
        self.contentBS = wx.BoxSizer(wx.VERTICAL)
        self.contentPanel.SetSizer(self.contentBS)
        self.contentPanel.Layout()
        self.contentPanel.SetAutoLayout(1)
        self.contentPanel.SetupScrolling()
        self.toolP = wx.Panel(leftP,-1)
        boxsizertb = wx.BoxSizer(wx.HORIZONTAL)
        bm1 = tools.scale_bitmap_from_file('images/send.png', 25, 25)
        bm2 = tools.scale_bitmap_from_file('images/emt.png', 25, 25)
        bm3 = tools.scale_bitmap_from_file('images/chat.png', 25, 25)
        bmb1 = wx.BitmapButton(self.toolP,-1,bitmap=bm1,size=(40,30),style=0)
        bmb2 = wx.BitmapButton(self.toolP,-1,bitmap=bm2,size=(40,30),style=0)
        bmb3 = wx.BitmapButton(self.toolP,-1,bitmap=bm3,size=(40,30),style=0)
        boxsizertb.Add(bmb2,0,flag=wx.ALL|wx.ALIGN_LEFT)
        boxsizertb.Add(bmb1,0,flag=wx.ALL|wx.ALIGN_LEFT)
        boxsizertb.Add(bmb3,0,flag=wx.ALL|wx.ALIGN_LEFT)
        self.toolP.SetSizer(boxsizertb)
        self.textArea = wx.TextCtrl(leftP, -1, "",style=wx.TE_MULTILINE|wx.TE_RICH2|wx.NO_BORDER)
        bottomP = wx.Panel(leftP,-1)
        bottomPBS = wx.BoxSizer(wx.HORIZONTAL)
        self.sendBtn = wx.Button(bottomP,-1,u'发送',size=(50,30))
        self.closeBtn = wx.Button(bottomP,-1,u'关闭',size=(50,30))
        bottomPBS.Add(self.closeBtn,1,flag=wx.ALL)
        bottomPBS.Add(self.sendBtn,1,flag=wx.ALL)
        bottomP.SetSizer(bottomPBS)
        boxsizerL.Add(self.contentPanel,10,flag=wx.ALL|wx.EXPAND)
        boxsizerL.Add(self.toolP,1,flag=wx.ALL|wx.EXPAND)
        boxsizerL.Add(self.textArea,4,flag=wx.ALL|wx.EXPAND)
        boxsizerL.Add(bottomP,1,flag=wx.ALL|wx.ALIGN_RIGHT)
        leftP.SetSizer(boxsizerL)
        boxsizer.Add(leftP,5,flag=wx.ALL|wx.EXPAND)
        
        rightP = wx.Panel(self,-1)    
        rightP.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        rightP.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground) 
        rightP.SetBackgroundColour('white')     
        boxsizerR = wx.BoxSizer(wx.VERTICAL)
        if os.path.isfile('images/%s.png'%self.jid):
            bitmap = wx.Bitmap('images/%s.png'%self.jid,BITMAP_TYPE_ANY)
        else:
            bitmap = wx.Bitmap('images/im.png',BITMAP_TYPE_ANY)

        image = self.scale_bitmap(bitmap, 80, 80)
        blankP = wx.Panel(rightP,-1)
        blankP2 = wx.Panel(rightP,-1)
        username = wx.StaticText(rightP,-1,u'    姓名: %s'%self.nickname)
        position = wx.StaticText(rightP,-1,u'    职位: ')
        deparment = wx.StaticText(rightP,-1,u'    部门: ')
        tel = wx.StaticText(rightP,-1,u'    电话: ')
        phone = wx.StaticText(rightP,-1,u'    手机: ')
        email = wx.StaticText(rightP,-1,u'    邮箱: ')
        self.userPic = userPic = wx.StaticBitmap(rightP,bitmap=image)
        boxsizerR.Add(blankP,1,flag=wx.ALL|wx.EXPAND)
        boxsizerR.Add(userPic,5,flag=wx.ALL|wx.ALIGN_CENTER)
        boxsizerR.Add(username,1,flag=wx.ALL|wx.EXPAND)
        boxsizerR.Add(position,1,flag=wx.ALL|wx.EXPAND)
        boxsizerR.Add(deparment,1,flag=wx.ALL|wx.EXPAND)
        boxsizerR.Add(tel,1,flag=wx.ALL|wx.EXPAND)
        boxsizerR.Add(phone,1,flag=wx.ALL|wx.EXPAND)
        boxsizerR.Add(email,1,flag=wx.ALL|wx.EXPAND)
        boxsizerR.Add(blankP2,3,flag=wx.ALL|wx.EXPAND)
        rightP.SetSizer(boxsizerR)
        
        boxsizer.Add(rightP,2,flag=wx.ALL|wx.EXPAND)
        
        self.Bind(wx.EVT_BUTTON,self.onSendMsg,self.sendBtn)
        self.Bind(wx.EVT_BUTTON,self.onClose,self.closeBtn)
           
        self.SetSizer(boxsizer)
    def onKeyUp(self,event):
        if 13 == event.KeyCode:
            self.onSendMsg(event)
        return
    def onSendMsg(self,event):
        if self.textArea.GetValue() == '':
            return
        self.conn.send(xmpp.Message(xmpp.JID(self.jid),self.textArea.GetValue(),'chat'))
        timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        msg = '%s--%s\n\t%s' % (self.nickname,timestr,self.textArea.GetValue())
        self.textArea.SetValue('')
        content = wx.StaticText(self.contentPanel,-1,msg,style=wx.TE_WORDWRAP|wx.TE_MULTILINE)
        self.contentBS.Add(content,flag=wx.ALL|wx.GROW,border=5)
        self.contentPanel.Layout()
        self.contentPanel.SetAutoLayout(1)
        self.contentPanel.SetupScrolling(scrollToTop=False)
        self.contentPanel.Scroll(0,50)
        return

    def scale_bitmap(self,bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result   
    
    def receiveMsg(self,msg):
        timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        msg = '%s--%s\n\t%s' % (self.nickname,timestr,msg)
        content = wx.StaticText(self.contentPanel,-1,msg,style=wx.TE_WORDWRAP|wx.TE_MULTILINE)
        self.contentBS.Add(content,flag=wx.ALL|wx.GROW,border=5)
        self.contentPanel.Layout()
        self.contentPanel.SetAutoLayout(1)
        self.contentPanel.SetupScrolling(scrollToTop=False)
        self.contentPanel.Scroll(0,50)
        return
    
    def updateImg(self,name):
        bitmap = wx.Bitmap('images/%s.png' % (name),BITMAP_TYPE_ANY)
        image = self.scale_bitmap(bitmap, 80, 80)
        self.userPic.SetBitmap(image)
        
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("images/CRM.png")
        dc.DrawBitmap(bmp, 0, 0)

    def onClose(self,event):
        
        self.GetParent().Close()
        self.GetParent().Destroy()
        return
         
if __name__ == '__main__':
    
    app = wx.PySimpleApp()
    frame = wx.Frame(None,-1,u'聊天界面',size=(600,500),style=wx.CAPTION|wx.MINIMIZE_BOX|wx.CLOSE_BOX)
    ChatLayoutf(frame)
    frame.Show(True)
    frame.Center()
    app.MainLoop()