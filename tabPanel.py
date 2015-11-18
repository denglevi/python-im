#_*_coding:utf-8_*_
'''
Created on 2014-5-5

@author: denglevi
'''
import wx
import  wx.lib.scrolledpanel as scrolled
from wx._core import BITMAP_TYPE_ANY
import os

class tabPanel(wx.Notebook):
    def scale_bitmap(self,bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result   
    def __init__(self, parent, id,roster):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )

        win = self.friendPanel(roster)
        self.AddPage(win, u"好友")

        # Show how to put an image on one of the notebook tabs,
        # first make the image list:
        il = wx.ImageList(16, 16)
        bitmap = wx.Bitmap('images/im.png')
        bitmap = self.scale_bitmap(bitmap, 16, 16)
        idx1 = il.Add(bitmap)
        self.AssignImageList(il)

        # now put an image on the first tab we just created:
        self.SetPageImage(0, idx1)


        win = self.makeColorPanel(wx.WHITE)
        self.AddPage(win, u"群组")

        win = self.makeColorPanel(wx.WHITE)
        self.AddPage(win, u"最近沟通")
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    def friendPanel(self,roster):
        userlist = roster.getItems()
        groups = {}
        for user in userlist:
            grouplist = roster.getGroups(user) or []
            for gname in grouplist:
                if not groups.has_key(gname):
                    groups[gname] = []                                          
                groups[gname].append(user) 
        self.Bind(wx.EVT_SIZE, self.OnSize)
        friendPanel = scrolled.ScrolledPanel(self,-1,size=(300,600))

        self.tree = wx.TreeCtrl(friendPanel,-1,style=wx.TR_HAS_BUTTONS)
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))

        defaultPic = wx.Bitmap('images/fun_Level.png',BITMAP_TYPE_ANY)
        defaultPic = self.scale_bitmap(defaultPic, 16, 16)

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
                    btm = self.scale_bitmap(btm, 16, 16)
                    smileidx    = il.Add(btm)
                else:
                    smileidx    = il.Add(defaultPic)
                self.tree.SetItemImage(last, smileidx, wx.TreeItemIcon_Normal)


        self.tree.Expand(self.root) 
        return friendPanel
    
    def OnSize(self,event):
        (w,h) = self.GetClientSizeTuple()
        print h
        self.tree.SetDimensions(0, 0, w, h-30)  
        
    def makeColorPanel(self, color):
        p = wx.Panel(self, -1)
        p.SetBackgroundColour(color)
        return p


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
    def updateTree(self,fromName,color):
        item = self.get_desired_parent(fromName)
        if(item == None):
            return
        parent = self.tree.GetItemParent(item)
        text = self.tree.GetItemText(item)
        image = self.tree.GetItemImage(item)
        data = self.tree.GetItemPyData(item)
        last = self.tree.PrependItem(parent,"%s" % (text))
        self.tree.SetPyData(last,data)
        isz = (16,16)
        il = self.tree.GetImageList()
        if os.path.isfile('images/%s.png'%data['jid']):
            bitmap = wx.Bitmap('images/%s.png'%data['jid'],BITMAP_TYPE_ANY)
        else:
            bitmap = wx.Bitmap('images/im.png',BITMAP_TYPE_ANY)
        btm = self.scale_bitmap(bitmap, 16, 16)
        fileidx = il.Add(btm)
        self.tree.SetItemImage(last, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemTextColour(last,'%s'%color)
        self.tree.Delete(item)       
        return        
if __name__ == '__main__':        
    app = wx.PySimpleApp()
    (width,height) = wx.GetDisplaySize()
    frame = wx.Frame(None,-1,u'xxxx',size=(300,600),pos=(width-350,50))
    boxsizer = wx.BoxSizer(wx.VERTICAL)
    toppanel = wx.Panel(frame,-1)
    wx.StaticText(toppanel,-1,'xxxxxxxxxxxx')
    tabpanel = tabPanel(frame,-1)
    boxsizer.Add(toppanel,1,flag=wx.ALL|wx.EXPAND)
    boxsizer.Add(tabpanel,5,flag=wx.ALL|wx.EXPAND)
    frame.SetSizer(boxsizer)
    frame.Show(True)
    app.MainLoop()


