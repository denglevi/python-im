#_*_coding:utf-8_*_
import wx
from wx._core import PySimpleApp
from wx._core import BITMAP_TYPE_ANY
import os
import tools
from groupPanel import groupPanel
from recentlyPanel import recentlyPanel
from chat import ChatLayoutf
import xmpp

class tabPanel(wx.Notebook):
    def __init__(self, parent, id,roster,conn):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        self.conn = conn
        win = self.getFriendList(roster,conn)
        self.AddPage(win, u"好友")

        # Show how to put an image on one of the notebook tabs,
        # first make the image list:
        il = wx.ImageList(16, 16)
        friend = wx.Bitmap('images/user.png',BITMAP_TYPE_ANY)
        group = wx.Bitmap('images/group.png',BITMAP_TYPE_ANY)
        friendbm = tools.scale_bitmap(friend, 16, 16)
        groupbm = tools.scale_bitmap(group, 16, 16)
        friendimg = il.Add(friendbm)
        groupimg = il.Add(groupbm)
        self.AssignImageList(il)

        win = self.getGroupList()
        self.AddPage(win, u"群组")
        
        win = self.getRecentlyList()
        self.AddPage(win, u"最近沟通")

        # now put an image on the first tab we just created:
        self.SetPageImage(0, friendimg)
        self.SetPageImage(1, groupimg)
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
    
    def getFriendList(self,roster,conn):
        self.rosterPanel = RosterPanel(self,roster,conn)
        return self.rosterPanel
    
    def getGroupList(self):

        self.groupPanel = groupPanel(self,self.conn)
        return self.groupPanel
    
    def getRecentlyList(self):

        self.recentlyPanel = recentlyPanel(self)
        return self.recentlyPanel
    
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        event.Skip()
        
class RosterPanel(wx.Panel):
    def __init__(self, parent,roster,conn):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1)
        self.conn = conn
        self.Bind(wx.EVT_SIZE, self.OnSize)
        userlist = roster.getItems()
        groups = {}
        for user in userlist:
            grouplist = roster.getGroups(user) or []
            for gname in grouplist:
                if not groups.has_key(gname):
                    groups[gname] = []                                          
                groups[gname].append(user) 
        self.tree = wx.TreeCtrl(self,-1,style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.NO_BORDER)
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        group = wx.Bitmap('images/games_rpg.png',BITMAP_TYPE_ANY)
        groupbm = tools.scale_bitmap(group, 16, 16)
        fldridx = il.Add(groupbm)
        defaultPic = wx.Bitmap('images/offline-user.png',BITMAP_TYPE_ANY)
        defaultPic = tools.scale_bitmap(defaultPic, 16, 16)

        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot("The Root Item")
        for key,value in groups.iteritems():
            child = self.tree.AppendItem(self.root, key)
            self.tree.SetPyData(child, None)
            self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)

            for user in value:
                name = roster.getName(user) or user
                last = self.tree.AppendItem(child,"%s" % (name))
                self.tree.SetPyData(last, {'jid':user,'msg':[],'nickname':"%s" % (name)})
                if os.path.isfile('images/%s.png'%user):
                    btm = wx.Bitmap('images/%s.png'%user,BITMAP_TYPE_ANY)
                    btm = tools.scale_bitmap(btm, 16, 16)
                    smileidx    = il.Add(btm)
                else:
                    smileidx    = il.Add(defaultPic)
                self.tree.SetItemTextColour(last,'gray')
                self.tree.SetItemImage(last, smileidx, wx.TreeItemIcon_Normal)
                
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)

    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)
        
    def get_desired_parent(self, name, selectednode = None):
        if selectednode == None:
            selectednode = self.tree.RootItem
        rootcount = self.tree.GetChildrenCount(selectednode, False)
        if rootcount == 0:
            return None
        
        for x in range(rootcount):
            (item,cookie) = self.tree.GetFirstChild(selectednode)    
            childcount = self.tree.GetChildrenCount(item, False)
            (child,cookie) = self.tree.GetFirstChild(item)
            itemdata = self.tree.GetItemData(child)
            data = itemdata.GetData()
            jid = data['jid']
            if jid == name:
                return child
            while childcount > 1:
                childcount = childcount - 1                      
                (child,cookie) = self.tree.GetNextChild(item,cookie)
                itemdata = self.tree.GetItemData(child)
                data = itemdata.GetData()
                jid = data['jid']
                if jid == name:
                    return child        
        return None
    def OnLeftDClick(self,event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item and not self.tree.ItemHasChildren(item):
            itemdata = self.tree.GetPyData(item)
            jid = itemdata['jid']
            nickname = itemdata['nickname']
            win = self.FindWindowByName(jid)
            if win:
                win.SetFocus()  
                win.Show(True)  
                event.Skip()      
                return
            frame = wx.Frame(self,-1,u'%s聊天' % (nickname),size=(600,500),style=wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX)           
            chatWin = ChatLayoutf(frame,self.conn,jid,nickname)
            frame.CenterOnScreen()
            icon = wx.Icon('images/char.ico', wx.BITMAP_TYPE_ICO)
            frame.SetIcon(icon)  
            frame.Show(True)
            self.conn.send(xmpp.Iq('get','vcard-temp','',xmpp.JID(jid)))
        event.Skip()
    def updateTree(self,fromName,color):
        item = self.get_desired_parent(fromName)
        if(item == None):
            return
        if(color != 'gray'):
            parent = self.tree.GetItemParent(item)
            text = self.tree.GetItemText(item)
            image = self.tree.GetItemImage(item)
            data = self.tree.GetItemPyData(item)
            last = self.tree.PrependItem(parent,"%s" % (text))
            self.tree.SetPyData(last,data)
            il = self.tree.GetImageList()
            if os.path.isfile('images/%s.png'%data['jid']):
                bitmap = wx.Bitmap('images/%s.png'%data['jid'],BITMAP_TYPE_ANY)
            else:
                bitmap = wx.Bitmap('images/user.png',BITMAP_TYPE_ANY)
            btm = tools.scale_bitmap(bitmap, 16, 16)
            fileidx = il.Add(btm)
            self.tree.SetItemImage(last, fileidx, wx.TreeItemIcon_Normal)
            self.tree.SetItemTextColour(last,'%s'%color)
            self.tree.Delete(item)
            
            return
        
        parent = self.tree.GetItemParent(item)
        text = self.tree.GetItemText(item)
        image = self.tree.GetItemImage(item)
        data = self.tree.GetItemPyData(item)
        last = self.tree.AppendItem(parent,"%s" % (text))
        self.tree.SetPyData(last,data)
        il = self.tree.GetImageList()
        if os.path.isfile('images/%s.png'%data['jid']):
            bitmap = wx.Bitmap('images/%s.png'%data['jid'],BITMAP_TYPE_ANY)
        else:
            bitmap = wx.Bitmap('images/offline-user.png',BITMAP_TYPE_ANY)
        btm = tools.scale_bitmap(bitmap, 16, 16)
        fileidx = il.Add(btm)
        self.tree.SetItemImage(last, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemTextColour(last,'gray')
        self.tree.Delete(item)      
if __name__ == '__main__':
    
    app = PySimpleApp()
    frame = wx.Frame(None,-1)
    tabPanel(frame,-1)
    frame.Show(True)
    frame.Center()
    app.MainLoop()