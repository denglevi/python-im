#_*_coding:utf-8_*_
'''
Created on 2014-4-29

@author: denglevi
'''
import wx
import wx.lib.layoutf as layoutf
import wx.lib.agw.aquabutton as aquabutton
import time
import xmpp
import  wx.lib.scrolledpanel as scrolled
from wx._core import BITMAP_TYPE_ANY
from groupUserList import groupUserList
import tools

class GroupChatLayoutf(wx.Panel):
    def __init__(self, parent,conn,jid,name):
        wx.Panel.__init__(self, parent, -1,name=jid)
        
        self.conn = conn
        self.initUI()
        return
        self.conn.send(xmpp.Iq('get','http://jabber.org/protocol/disco#items','',xmpp.JID(jid)))    
    
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
        rightP.SetBackgroundColour('gray')     
        boxsizerR = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(rightP,-1,u'群公告')
        stPanel = wx.Panel(rightP,-1)
        stPanel.SetBackgroundColour('white')
        wx.StaticText(stPanel,-1,u'xxxxxxxxxxxxxx')
        self.grouplist = self.updateUserList(rightP)
        

        boxsizerR.Add(st,1,flag=wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,border=8)
        boxsizerR.Add(stPanel,5,flag=wx.ALL|wx.EXPAND,border=5)
        boxsizerR.Add(self.grouplist,10,flag=wx.ALL|wx.EXPAND)
        rightP.SetSizer(boxsizerR)
        
        boxsizer.Add(rightP,2,flag=wx.ALL|wx.EXPAND)
        
        self.Bind(wx.EVT_BUTTON,self.onSendMsg,self.sendBtn)
        self.Bind(wx.EVT_BUTTON,self.onClose,self.closeBtn)
           
        self.SetSizer(boxsizer)
    def updateGroupUserList(self,users):
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        group = wx.Bitmap('images/games_rpg.png',BITMAP_TYPE_ANY)
        groupbm = tools.scale_bitmap(group, 16, 16)
        fldridx = il.Add(groupbm)

        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot("The Root Item")
        for jid,name in users:
            child = self.tree.AppendItem(self.root,'%s'%name)
#             self.tree.SetPyData(child,  {'jid':'%s'%jid,'msg':[],'name':"%s" % (name)})
            self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
            
        return
    def updateUserList(self,panel):
        groupUserList = wx.Panel(panel,-1)
        groupUserList.Bind(wx.EVT_SIZE, self.OnSize)
        self.tree = wx.TreeCtrl(groupUserList,-1,style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.NO_BORDER)
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        group = wx.Bitmap('images/games_rpg.png',BITMAP_TYPE_ANY)
        groupbm = tools.scale_bitmap(group, 16, 16)
        fldridx = il.Add(groupbm)

        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot("The Root Item")
            
        #self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        return groupUserList
    def OnSize(self, event):
        w,h = self.grouplist.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)
        
    def onClose(self,event):
        
        self.GetParent().Close()
        self.GetParent().Destroy()
        return
    
    def onSendMsg(self,event):
        timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        msg = 'denglevi--'+timestr+'\n\t'+self.textArea.GetValue()
        self.textArea.SetValue('')
        content = wx.StaticText(self.contentPanel,-1,msg,style=wx.TE_WORDWRAP|wx.TE_MULTILINE)
        self.contentBS.Add(content,flag=wx.ALL|wx.GROW,border=5)
        self.contentPanel.Layout()
        self.contentPanel.SetAutoLayout(1)
        self.contentPanel.SetupScrolling()
        return
    
    def onRecevieMsg(self,event):
        
        return
    
if __name__ == '__main__':
    
    app = wx.PySimpleApp()
    frame = wx.Frame(None,-1,u'聊天界面',size=(600,500),style=wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX)
    GroupChatLayoutf(frame,None,'None',u'XXX')
    frame.Show(True)
    frame.Center()
    app.MainLoop()