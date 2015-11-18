#_*_coding:utf-8_*_
'''
Created on 2014-5-5

@author: denglevi
'''
import wx
import tools
from notebook import tabPanel
import os
import sys
from threading import Thread
import xmpp

from wx._core import PySimpleApp, BITMAP_TYPE_ANY
class mainFrame(wx.Frame):
    
    def __init__(self,parent,id,title,conn,jid):
        (width,height) = wx.GetDisplaySize()
        wx.Frame.__init__(self,parent,id,size=(300,600),pos=(width-350,50),title=title,style=wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX)
        self.jid = jid
        self.conn = conn
        roster = self.conn.getRoster()
        conn.RegisterHandler('presence',self.preCB)
        conn.RegisterHandler('message',self.msgCB)
        conn.RegisterHandler('iq',self.iqCB)
        self.initUI(roster)

    
    def initUI(self,roster):
        boxsizer = wx.BoxSizer(wx.VERTICAL)
        toppanel = wx.Panel(self,-1)
        gridbs = wx.GridBagSizer()
        icon = wx.Icon('images/char.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)  
        bitmap = wx.Bitmap('images/im.png',BITMAP_TYPE_ANY)
        bitmap = tools.scale_bitmap(bitmap, 64, 64)
        if os.path.isfile('images/%s.png'%self.jid):
            userPicBit = wx.Bitmap('images/%s.png'%self.jid,BITMAP_TYPE_ANY)
            bitmap = tools.scale_bitmap(userPicBit, 64, 64)
        else:
            userPicBit = wx.Bitmap('images/im.png',BITMAP_TYPE_ANY)
            bitmap = tools.scale_bitmap(userPicBit, 64, 64)
        self.sm = sm = wx.StaticBitmap(toppanel,-1,bitmap=bitmap)
        font = wx.Font(16,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        self.username = username = wx.StaticText(toppanel, -1, "")
        username.SetFont(font)
        choiceslist = [u"忙碌",u"离开",u"离线"]
        status = wx.ComboBox(parent=toppanel,choices=choiceslist,size=(50,30),value=u'在线')
        signature  = wx.StaticText(toppanel,-1,u"存在的就是合理的...........")
        
        gridbs.Add(sm,pos=(0,0),span=(4,3),flag=wx.ALL|wx.EXPAND,border=5)
        gridbs.Add(username,pos=(0,3),span=(1,15),flag=wx.ALIGN_BOTTOM)
        gridbs.Add(status,pos=(0,21),flag=wx.ALL|wx.ALIGN_RIGHT,border=1)
        gridbs.Add(signature,pos=(1,3),span=(1,15))
        
        toppanel.SetSizer(gridbs) 
             
        #self.tabpanel = tabpanel = tabPanel(self,-1,roster)
        self.tabpanel = tabpanel = tabPanel(self,-1,roster,self.conn)

        boxsizer.Add(toppanel,1,flag=wx.ALL|wx.EXPAND)
        boxsizer.Add(tabpanel,7,flag=wx.ALL|wx.EXPAND)
        self.SetSizer(boxsizer)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Show(True)      
        self.conn.sendInitPresence()
        self.conn.send(xmpp.Iq('get','vcard-temp','',xmpp.JID(self.jid)))  
        self.conn.send(xmpp.Iq('get','http://jabber.org/protocol/disco#items','','conference.m.zy.cm'))
        
    def OnCloseWindow(self,event):
        self.conn.disconnect()
        sys.exit()  
        return  
    def preCB(self,conn,pre):
        attrs = pre.getAttrs()
        fromName = pre.getFrom().getStripped()
        toName = pre.getTo().getStripped()
        if toName != fromName:
            mark = 0
            #unavailable
            if pre.has_attr('type') and attrs['type'] == 'unavailable':
                    wx.CallAfter(self.tabpanel.rosterPanel.updateTree,fromName,'gray')   
                    return            
            for i in pre.getChildren():
                if 'show' == i.getName():
                    mark = 1
                    if i.getData() == 'dnd':
                        wx.CallAfter(self.tabpanel.rosterPanel.updateTree,fromName,'red')
                        #Thread(target=self.tabpanel.rosterPanel.updateTree,args=(fromName,'red')).start()
                    if i.getData() == 'away':
                        #Thread(target=self.tabpanel.rosterPanel.updateTree,args=(fromName,'blue')).start()
                        wx.CallAfter(self.tabpanel.rosterPanel.updateTree,fromName,'blue')
                    pass
            if mark == 0:
                    wx.CallAfter(self.tabpanel.rosterPanel.updateTree,fromName,'black')
                    #Thread(target=self.tabpanel.rosterPanel.updateTree,args=(fromName,'green')).start()
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
        item = self.tabpanel.rosterPanel.get_desired_parent(fromName)
        if(item != None):
            data = self.tabpanel.rosterPanel.tree.GetItemPyData(item)
            data['msg'].append(body)
            size = len(data['msg'])

            self.tabpanel.rosterPanel.tree.SetItemText(item,'%s(%s条消息未读)' % (data['nickname'],size))
            
        return
    def iqCB(self,conn,iq):
        if iq.getAttr('id') == 'getGroupUserList':
            child = iq.getChildren()
            fromName = iq.getFrom()
            for x in child:
                if x.getName() == 'query':
                   query = x.getChildren()
                   jids = []
                   for y in query:
                       jid = y.getAttr('jid')
                       name = jid.split('/')
                       jids.append((jid,name[1]))
                   wind = self.FindWindowByName('%s' % (fromName))
                   wx.CallAfter(wind.updateGroupUserList,jids)
                   return
            
        if iq.getFrom() == self.jid:
            name = iq.getFrom()
            child = iq.getChildren()
            nickname = '暂无昵称'
            for x in child:
                for y in x.getChildren():
                    if 'FN' == y.getName():
                        nickname = y.getData()
                    for i in y.getChildren():                    
                        if 'BINVAL' == i.getName():
                            str = i.getData()
                            #if not os.path.exists("images/%s.jpg" % (name)):
                            fh = open("images/%s.jpg" % (name), "wb")
                            fh.write(str.decode('base64'))
                            fh.close()
                            wx.CallAfter(self.updateImg,name,nickname)
                            return         

        if iq.getFrom() == 'conference.m.zy.cm':
            rooms = []
            for query in iq.getChildren():
                for room in query.getChildren():
                    jid,name = room.getAttr('jid'),room.getAttr('name')
                    self.conn.send(xmpp.Presence(jid+'/denglevi'))
                    rooms.append((jid,name))
                wx.CallAfter(self.tabpanel.groupPanel.updateTree,rooms)
                return
        if iq.getTo() != iq.getFrom():
            print iq
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
                            return
        return   
    
    def updateImg(self,name,nickname):
        image = tools.scale_bitmap_from_file('images/%s.png' % (name), 64, 64)
        self.sm.SetBitmap(image)
        self.username.SetLabel('%s'%nickname)   
if __name__ == '__main__':
    
    app = PySimpleApp()
    frame = mainFrame(None,-1,u'主界面',None,None)
    icon = wx.Icon('images/chat.ico', wx.BITMAP_TYPE_ICO)
    frame.SetIcon(icon)     
    app.MainLoop()
