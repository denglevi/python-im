#_*_coding:utf-8_*_
'''
Created on 2014-4-29

@author: denglevi
'''
import wx
import wx.lib.layoutf as layoutf
import wx.lib.agw.aquabutton as aquabutton
import time
import  wx.lib.scrolledpanel as scrolled
from wx._core import BITMAP_TYPE_ANY

class GroupChatLayoutf(wx.Panel):
    def __init__(self, parent,conn,jid,name):
        wx.Panel.__init__(self, parent, -1,name=jid)
        self.SetAutoLayout(True)
        
        self.detailPanel = wx.Panel(self, -1, style=wx.RAISED_BORDER)
        self.detailPanel.SetBackgroundColour(wx.WHITE)

        self.detailPanel.SetConstraints(
            layoutf.Layoutf('t=t#1;r=r#1;h%h100#1;w%w30#1',(self,))
        )
        
        boxSizerC = wx.BoxSizer(wx.VERTICAL)
        
        bitmap = wx.Bitmap('images/img.png',BITMAP_TYPE_ANY)
        userPic = wx.StaticBitmap(parent=self.detailPanel,bitmap=bitmap)
        username = wx.StaticText(self.detailPanel,-1,u'姓名:')
        position = wx.StaticText(self.detailPanel,-1,u'职位:')
        deparment = wx.StaticText(self.detailPanel,-1,u'部门:')
        tel = wx.StaticText(self.detailPanel,-1,u'电话:')
        phone = wx.StaticText(self.detailPanel,-1,u'手机:')
        email = wx.StaticText(self.detailPanel,-1,u'邮箱:')
        
        
        boxSizerC.Add(userPic,flag=wx.ALL|wx.ALIGN_CENTRE_HORIZONTAL,border=30)
        boxSizerC.Add(username,flag=wx.ALL|wx.ALIGN_LEFT,border=10)
        boxSizerC.Add(position,flag=wx.ALL|wx.ALIGN_LEFT,border=10)
        boxSizerC.Add(deparment,flag=wx.ALL|wx.ALIGN_LEFT,border=10)
        boxSizerC.Add(tel,flag=wx.ALL|wx.ALIGN_LEFT,border=10)
        boxSizerC.Add(phone,flag=wx.ALL|wx.ALIGN_LEFT,border=10)
        boxSizerC.Add(email,flag=wx.ALL|wx.ALIGN_LEFT,border=10)
        
        self.detailPanel.SetSizer(boxSizerC)

        self.contentPanel = scrolled.ScrolledPanel(self, -1)
        self.contentPanel.SetBackgroundColour(wx.WHITE)
        self.contentPanel.SetConstraints(
            layoutf.Layoutf('t=t#1;l=l#1;b=b#1;r%r70#1;h%h65#1;r<r#2',(self,self.detailPanel))
            )
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)
        self.contentPanel.SetSizer(self.boxSizer)
        self.contentPanel.SetAutoLayout(1)
        self.contentPanel.SetupScrolling()

        self.inputPanel = wx.Window(self, -1)
        self.inputPanel.SetBackgroundColour(wx.WHITE)
        self.inputPanel.SetConstraints(
            layoutf.Layoutf('b_b#2;l=l#1;b=b#1;r%r70#1;h%h35#1;r<r#3',(self,self.contentPanel,self.detailPanel))
            )
        toolBar = wx.ToolBar(self.inputPanel,-1,style=wx.TB_HORIZONTAL)
        toolBar.SetConstraints(layoutf.Layoutf('t=t#1;l=l#1;h%h25#1;w%w100#1',(self.inputPanel,)))
        sendBtn = aquabutton.AquaButton(self.inputPanel,-1,None,u"send",size=(60,36))
#         self.textArea = wx.TextCtrl(self.inputPanel, -1, "",style=wx.TE_MULTILINE|wx.TE_RICH2|wx.NO_BORDER)
#         self.textArea.SetConstraints(layoutf.Layoutf('t_t5#2;r=r#1;h%h52#1;w%w100#1',(self.inputPanel,toolBar)))
        sendBtn.SetConstraints(layoutf.Layoutf('b=b#1;r=r#1;h*;w*',(self.inputPanel,)))
        
        self.Bind(wx.EVT_BUTTON,self.onSendMsg,sendBtn)
    
    def onSendMsg(self,event):
        
        timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        msg = 'denglevi--'+timestr+'\n\t'+self.textArea.GetValue()
        self.textArea.SetValue('')
        content = wx.StaticText(self.contentPanel,-1,msg,style=wx.TE_WORDWRAP|wx.TE_MULTILINE)
        self.boxSizer.Add(content,flag=wx.ALL|wx.GROW,border=5)
        self.contentPanel.Layout()
        self.contentPanel.SetAutoLayout(1)
        self.contentPanel.SetupScrolling()
        return
    
    def onRecevieMsg(self,event):
        
        return
    
if __name__ == '__main__':
    
    app = wx.PySimpleApp()
    frame = wx.Frame(None,-1,u'聊天界面',size=(600,500),style=wx.CAPTION|wx.MINIMIZE_BOX|wx.CLOSE_BOX)
    GroupChatLayoutf(frame)
    frame.Show(True)
    frame.Center()
    app.MainLoop()