#_*_coding:utf-8_*_ 
'''
Created on 2014-4-27

@author: denglevi
'''

import wx
import os.path
import xmpp
import pickle
from threading import Thread

from main2 import mainFrame
        
class WorkerThread(Thread):
    def __init__(self, notify_window,user,server,jid,password):
        
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.conn = conn =xmpp.Client(server,debug=['always', 'nodebuilder'])
        conres=conn.connect()
        if not conres:
            wx.MessageBox("连接服务器错误", "系统提示",wx.CANCEL | wx.ICON_ERROR)
            return
        if conres<>'tls':
            print "Warning: unable to estabilish secure connection - TLS failed!"
        authres=conn.auth(user,password)
        if not authres:
            wx.MessageBox("连接认证错误，用户名或密码错误","系统提示",wx.CANCEL | wx.ICON_ERROR)
            return
        if authres<>'sasl':
            print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server
        if mainFrame(None,-1,"主界面",conn,jid):
            self.start()
            notify_window.Close(True)
            notify_window.Destroy()
            #self.timer.Stop()
            return


    def run(self):

        while self.conn.Process(1): pass
        return
  
class loginFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size =(400,200),style=wx.DEFAULT_DIALOG_STYLE)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.panel = panel = wx.Panel(self, -1,size=(400,200))
        self.gridBagSizer = gridBagSizer = wx.GridBagSizer(3,2)
        username = ''
        password = ''
        if os.path.exists("data/userinfo"):            
            userinfo = self.getUserInfo()
            username = userinfo[0]
            password = userinfo[1]
        self.icon = wx.Icon('images/char.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)      
        st1 = wx.StaticText(panel, -1, '登录名:')
        st2 = wx.StaticText(panel, -1, '密     码:')
        self.usernameText = wx.TextCtrl(panel,-1,username, size=(175, -1))
        self.passwordText = wx.TextCtrl(panel, -1,password, size=(175, -1), style=wx.TE_PASSWORD)
        self.checkBox = wx.CheckBox(panel,-1,"记住密码")
        self.checkBox.SetValue(True)
        loginBtn = wx.Button(panel,-1,"登录")

        gridBagSizer.Add(st1,pos=(0,0),border=6,flag=wx.ALL)
        gridBagSizer.Add(st2,pos=(1,0),border=6,flag=wx.ALL)
        gridBagSizer.Add(self.usernameText,pos=(0,1))
        gridBagSizer.Add(self.passwordText,pos=(1,1))
        gridBagSizer.Add(self.checkBox,pos=(2,0),border=6,flag=wx.ALL)
        gridBagSizer.Add(loginBtn,pos=(2,1),flag=wx.ALIGN_RIGHT)
        
        hbox.Add(gridBagSizer,proportion=1,flag=wx.ALIGN_CENTRE_VERTICAL)
        vbox.Add(hbox,proportion=1,flag=wx.ALIGN_CENTRE_HORIZONTAL)
        self.Bind(wx.EVT_BUTTON,self.onLogin,loginBtn)
        self.SetSizer(vbox)
        self.Centre()     
        self.Show(True)
      
    def getUserInfo(self):
        
        datafile = open("data\userinfo","rb")
        data = pickle.load(datafile)
        datafile.close()
        return data
    
    def setUserInfo(self,data):
        
        datafile = open("data\userinfo","wb")
        pickle.dump(data, datafile, 2)
        datafile.close()
        return  
    
    def onLogin(self,event):

        username = self.usernameText.GetValue()
        password = self.passwordText.GetValue()
        checkBox = self.checkBox.GetValue()
        if username == '' or password == '':
            wx.MessageBox("用户名或登录密码不能为空", "系统提示",wx.CANCEL | wx.ICON_ERROR)
            return; 
        jid=xmpp.JID(username)
        user,server,password=jid.getNode(),jid.getDomain(),password
        if checkBox:
            userinfo = [username,password]
            self.setUserInfo(userinfo)
        else:
            userinfo = [username,'']
            self.setUserInfo(userinfo)        

        WorkerThread(self,user,server,jid,password) 
        return;
    
def main():
    app = wx.PySimpleApp()
    loginFrame(None, -1, '登录')
    app.MainLoop()

if __name__ == '__main__':
    main()
        