#_*_coding:utf-8_*_

import wx
from wx._core import BITMAP_TYPE_ANY
import tools

class groupUserList(wx.Panel):
    
    def __init__(self,parent,conn):
        
        wx.Panel.__init__(self,parent,-1)
        self.conn = conn
    def updateTree(self,userlist):
        
        
        print userlist
        return
        self.tree = wx.TreeCtrl(self,-1,style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.NO_BORDER)
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        group = wx.Bitmap('images/games_rpg.png',BITMAP_TYPE_ANY)
        groupbm = tools.scale_bitmap(group, 16, 16)
        fldridx = il.Add(groupbm)

        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot("The Root Item")
        for jid,name in userlist:
            child = self.tree.AppendItem(self.root,'%s'%name)
            self.tree.SetPyData(child,  {'jid':'%s'%jid,'msg':[],'name':"%s" % (name)})
            self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
            
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        
    def OnLeftDClick(self,event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:
            itemdata = self.tree.GetPyData(item)
            jid = itemdata['jid']
            name = itemdata['name']
        event.Skip()
    