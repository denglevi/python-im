#_*_coding:utf-8_*_ 
'''
Created on 2014-4-27

@author: denglevi
'''
import wx
import sys
import xmpp
import  wx.lib.scrolledpanel as scrolled
from chat import ChatLayoutf
from wx._core import BITMAP_TYPE_ANY
import os


class mainFrame(wx.Frame):
    
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
    def updateTree(self,fromName,color,item):
        if not item:
            item = self.get_desired_parent(fromName)
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
    def preCB(self,conn,pre):
        attrs = pre.getAttrs()
        fromName = pre.getFrom().getStripped()
        toName = pre.getTo().getStripped()
        if toName != fromName:
            mark = 0
            #unavailable
            if pre.has_attr('type') and attrs['type'] == 'unavailable':
                item = self.get_desired_parent(fromName)
                if(item != None):
                    self.tree.SetItemTextColour(item,'gray')    
                    return            
            for i in pre.getChildren():
                if 'show' == i.getName():
                    mark = 1
                    if i.getData() == 'dnd':
                        wx.CallAfter(self.updateTree,fromName,'red')
                    if i.getData() == 'away':
                        wx.CallAfter(self.updateTree,fromName,'blue')
                    pass
            if mark == 0:
                item = self.get_desired_parent(fromName)
                if(item != None):
                    wx.CallAfter(self.updateTree,fromName,'green',item)
        
        return
    def msgCB(self,conn,msg):
        fromName = msg.getFrom().getStripped()
        body = msg.getBody()
        wind = self.FindWindowByName(fromName)
        if wind:
            #thread.start_new_thread(wind.receiveMsg,('self','sssssssssss'))
            if body:
                wx.CallAfter(wind.receiveMsg,body)
                #threading.Thread(target = wind.receiveMsg, args = (body,)).start()
                return
        item = self.get_desired_parent(fromName)
        if(item != None):
            data = self.tree.GetItemPyData(item)
            data['msg'].append(body)
            size = len(data['msg'])

            self.tree.SetItemText(item,'%s(%s msgs to read)' % (data['nickname'],size))
            
        return
    def iqCB(self,conn,iq):
        
        name = iq.getFrom()
        child = iq.getChildren()
        for x in child:
            for y in x.getChildren():
                for i in y.getChildren():                    
                    if 'BINVAL' == i.getName():
                        str = i.getData()
                        fh = open("images/%s.png" % (name), "wb")
                        fh.write(str.decode('base64'))
                        fh.close()
                        wind = self.FindWindowByName('%s' % (name))
                        wx.CallAfter(wind.updateImg,name)
        
    def __init__(self,parent,id,title,conn,jid):

        self.conn = conn = conn
        conn.RegisterHandler('presence',self.preCB)
        conn.RegisterHandler('message',self.msgCB)
        conn.RegisterHandler('iq',self.iqCB)
        (width,height) = wx.GetDisplaySize()
        wx.Frame.__init__(self,parent,id,title,pos=(width-350,50),size=(300,600),style=wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX)
        roster = conn.getRoster()
        userlist = roster.getItems()
        groups = {}
        for user in userlist:
            grouplist = roster.getGroups(user) or []
            for gname in grouplist:
                if not groups.has_key(gname):
                    groups[gname] = []                                          
                groups[gname].append(user)   
                             
        panel = wx.Panel(self,-1,size=(300,600))
        self.gridbs = gridbs = wx.GridBagSizer(0,0)
        if os.path.isfile('images/%s.png'%jid):
            userPicBit = wx.Bitmap('images/%s.png'%jid,BITMAP_TYPE_ANY)
            userPicBit = self.scale_bitmap(userPicBit, 64, 64)
        else:
            userPicBit = wx.Bitmap('images/im.png',BITMAP_TYPE_ANY)
            userPicBit = self.scale_bitmap(userPicBit, 64, 64)

        username = wx.StaticText(panel, -1, u"denglevi")
        signature  = wx.StaticText(panel,-1,u"存在的就是合理的...........")
        userPic = wx.StaticBitmap(parent=panel,bitmap=userPicBit,size=(64,64)) 
        choiceslist = [u"忙碌",u"离开",u"离线"]
        status = wx.ComboBox(parent=panel,choices=choiceslist,size=(70,30),value=u'在线');
        
        btn1 = wx.Button(panel,-1,u"联系人",size=(75,30))
        self.Bind(wx.EVT_BUTTON,self.getList,btn1)
        btn2 = wx.Button(panel,-1,u"群组",size=(75,30))
        self.Bind(wx.EVT_BUTTON,self.getGroup,btn2)
        btn3 = wx.Button(panel,-1,u"最近沟通",size=(80,30))
        self.Bind(wx.EVT_BUTTON,self.getRecently,btn3)
        st4 = wx.StaticText(panel,-1,'',size=(70,30))
        

        #panelBox = wx.BoxSizer(wx.VERTICAL)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.listPanel = scrolled.ScrolledPanel(panel,-1,size=(300,600))
        self.tree = wx.TreeCtrl(self.listPanel,-1,style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)
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

        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick) 


        #panelBox.Add(self.tree,1,flag=wx.ALL|wx.EXPAND|wx.ALIGN_TOP|wx.SHAPED)
        #panelBox.Add(self.groupTree,1,flag=wx.ALL|wx.EXPAND|wx.ALIGN_TOP|wx.SHAPED)
        #self.listPanel.SetSizer(panelBox)
            
        gridbs.Add(userPic,pos=(0,0),flag=wx.ALL,span=(3,1),border=5)
        gridbs.Add(username,pos=(0,1),flag=wx.ALL|wx.ALIGN_LEFT,border=6)
        gridbs.Add(status,pos=(0,2),flag=wx.ALL|wx.ALIGN_RIGHT,span=(1,2))
        gridbs.Add(signature,pos=(1,1),flag=wx.ALL|wx.ALIGN_LEFT,span=(1,4),border=6)
        gridbs.Add(btn1,pos=(3,0),flag=wx.ALL|wx.ALIGN_LEFT)
        gridbs.Add(btn2,pos=(3,1),flag=wx.ALL|wx.ALIGN_LEFT)
        gridbs.Add(btn3,pos=(3,2),flag=wx.ALL|wx.ALIGN_LEFT)
        gridbs.Add(st4,pos=(3,3),flag=wx.ALL|wx.ALIGN_LEFT)
        
        gridbs.Add(self.listPanel,pos=(4,0),flag=wx.ALL|wx.EXPAND,span=(1,4))

        boxSizer = wx.BoxSizer(wx.VERTICAL)
        boxSizer.Add(gridbs,proportion=1,flag=wx.ALL|wx.EXPAND)
        panel.SetSizer(boxSizer)
        self.Show(True)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        conn.sendInitPresence()
        return
    def scale_bitmap(self,bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result       
    def OnCloseWindow(self,event):
        self.conn.disconnect()
        sys.exit()  
        return
    def getList(self,event):

        return
    def getGroup(self,event):

        return
    def getRecently(self,event):
        
        return        
    def OnSize(self, event):
        
        (w,h) = self.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)   
    
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
            frame = wx.Frame(self,-1,u'%s聊天界面' % (nickname),size=(600,500),style=wx.CAPTION|wx.MINIMIZE_BOX|wx.CLOSE_BOX)           
            chatWin = ChatLayoutf(frame,self.conn,jid,nickname)
            frame.CenterOnScreen()
            frame.Show(True)
            self.conn.send(xmpp.Iq('get','vcard-temp','',xmpp.JID(jid)))
        event.Skip()
    def on_change(self,event):
        self.listPanel.SetAutoLayout(1)
        self.listPanel.SetupScrolling()
        obj = event.GetEventObject()
        obj.GetParent().GetParent().Layout()
        return;