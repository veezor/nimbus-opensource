#!/usr/bin/python
# -*- coding: utf-8 -*-
#Copyright © 2010, 2011 Veezor Network Intelligence (Linconet Soluções em Informática Ltda.), <www.veezor.com>
#
# This file is part of Nimbus Opensource Backup.
#
#    Nimbus Opensource Backup is free software: you can redistribute it and/or 
#    modify it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License.
#
#    Nimbus Opensource Backup is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Nimbus Opensource Backup.  If not, see <http://www.gnu.org/licenses/>.
#
#In this file, along with the Nimbus Opensource Backup code, it may contain 
#third part code and software. Please check the third part software list released 
#with every Nimbus Opensource Backup copy.
#
#You can find the correct copyright notices and license informations at 
#their own website. If your software is being used and it's not listed 
#here, or even if you have any doubt about licensing, please send 
#us an e-mail to law@veezor.com, claiming to include your software.
#


import subprocess

import windowsnotifier
import wx
import wx.lib.masked as masked





class App(wx.Frame):

    def __init__(self, parent, title):
        super(App, self).__init__(parent, title=title,
            size=(450, 200))
        self.SetSizeHints(minW=450,minH=200,maxW=450,maxH=200)

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)

        self.username_label = wx.StaticText(panel, label="Username:")
        sizer.Add(self.username_label, pos=(1, 0), flag=wx.LEFT, border=10)

        self.username = wx.TextCtrl(panel)
        sizer.Add(self.username, pos=(1, 1), span=(1, 5), flag=wx.TOP|wx.EXPAND)


        self.password_label = wx.StaticText(panel, label="Password:")
        sizer.Add(self.password_label, pos=(2, 0), flag=wx.LEFT, border=10)

        self.password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        sizer.Add(self.password, pos=(2, 1), span=(1, 5), flag=wx.TOP|wx.EXPAND)


        self.address_label = wx.StaticText(panel, label="IP Address:")
        sizer.Add(self.address_label, pos=(3, 0), flag=wx.LEFT, border=10)

        self.address = masked.Ctrl(panel, -1, "", autoformat="IPADDR")
        sizer.Add(self.address, pos=(3, 1), span=(1, 5), flag=wx.TOP|wx.EXPAND)



        self.button_ok = wx.Button(panel, label="Adicionar")
        self.button_ok.Bind(wx.EVT_BUTTON, self.button_ok_pressed)
        sizer.Add(self.button_ok, pos=(5, 3))

        self.button_close = wx.Button(panel, label="Fechar")
        self.button_close.Bind(wx.EVT_BUTTON, self.button_close_pressed)
        sizer.Add(self.button_close, pos=(5, 4), span=(1, 1),
            flag=wx.BOTTOM|wx.RIGHT, border=5)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)



    def button_close_pressed(self, event):
        self.Close()


    def button_ok_pressed(self, event):
        try:
            username = self.username.GetValue()
            password = self.password.GetValue()
            address = self.address.GetValue().replace(' ','')
            windowsnotifier.Notifier(username, password, address).notify_new_computer()
            self.dialog_on_success()
        except Exception, error:
            self.dialog_on_error()



    def dialog_on_success(self):
        dlg = wx.MessageDialog(self, "Computador adicionado com sucesso.",
                              "", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def dialog_on_error(self):
        dlg = wx.MessageDialog(self, u"Erro na adição do computador. Verifique a conexão com o servidor Nimbus.",
                              u"Atenção", wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()



if __name__ == '__main__':
    app = wx.App()
    App(None, title="Nimbus Client for Windows")
    app.MainLoop()
