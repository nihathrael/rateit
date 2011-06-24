'''
Created on 02.06.2011

@author: moritz
'''
import gtk
import os

from twisted.internet import reactor

import utils.resources
import utils.settings

import gui.guiutils

class GUI():
    def __init__(self):
        self.paint_icon()
        # Set the Chatclient
        self.client = None

    def run(self):
        gtk.main()

    def quit_cb(self, widget, data = None):
        if data:
            data.set_visible(False)
        if self.client:
            self.client.quit()
        gtk.main_quit()
        reactor.stop()

    def cb(self, widget, data=None):
        print 'cb'

    def show_about(self, widget, data = None):
        aboutDialog = gtk.AboutDialog()
        aboutDialog.set_title("RateIt!")
        aboutDialog.set_name("RateIt!")
        aboutDialog.set_destroy_with_parent(gtk.DIALOG_DESTROY_WITH_PARENT)

        file = open(os.path.join(utils.resources.get_resource_path(),'rating-rules.txt'))
        aboutDialog.set_comments(file.read())
        file.close()

        file = open(os.path.join(utils.resources.get_resource_path(),'gpl-3.0.txt'))
        aboutDialog.set_license(file.read())
        file.close()

        def close(w, res):
                if res == gtk.RESPONSE_CANCEL:
                    w.hide()
        aboutDialog.connect("response", close)

        aboutDialog.set_authors(["Moritz Beller","Thomas Kinnen"])
        aboutDialog.show()

    def show_chat(self, widget, data = None):
        connectDialog = gtk.Dialog("Connect To", None, gtk.DIALOG_DESTROY_WITH_PARENT, None)
        connectDialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        connectDialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        entry = gtk.Entry()
        entry.show()
        connectDialog.vbox.add(entry)

        def ok(w, res):
            if res == gtk.RESPONSE_OK:
                connectDialog.hide()
                self.send(entry.get_text())
            elif res == gtk.RESPONSE_CANCEL:
                connectDialog.hide()

        connectDialog.connect("response", ok)
        connectDialog.show()

    def show_connect(self, widget, data = None):
        connectDialog = gtk.Dialog("Connect To", None, gtk.DIALOG_DESTROY_WITH_PARENT, None)
        connectDialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        connectDialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        entry = gtk.Entry()
        entry.set_text(utils.settings.a.server)
        entry.show()
        connectDialog.vbox.add(entry)
        
        channel = gtk.Entry()
        channel.set_text(utils.settings.a.channel)
        channel.show()
        connectDialog.vbox.add(channel)

        def ok(w, res):
            if res == gtk.RESPONSE_OK:
                connectDialog.hide()
                utils.settings.a.server = entry.get_text()
                utils.settings.a.channel = channel.get_text()
                if utils.settings.a.channel == '':
                    utils.settings.a.channel = 'default'
                self.connect_to()
                utils.settings.a.save_settings()
            elif res == gtk.RESPONSE_CANCEL:
                connectDialog.hide()

        connectDialog.connect("response", ok)
        connectDialog.show()

    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)

    def build_menu(self, statusIcon):
        menu = gtk.Menu()

        menuItem = gtk.MenuItem("Missed It!")
        menuItem.connect('activate', Callback(self.send, "Missed It!"))
        menu.append(menuItem)
        
        menuItem = gtk.SeparatorMenuItem()
        menu.append(menuItem)

        menuItem = gtk.MenuItem("xD")
        menuItem.connect('activate', Callback(self.send, "xD"))
        menu.append(menuItem)

        for curRating in xrange(5, 11):
            menuItem = gtk.MenuItem(str(curRating))
            menuItem.connect('activate', Callback(self.send, curRating))
            menu.append(menuItem)

        menuItem = gtk.SeparatorMenuItem()
        menu.append(menuItem)

        menuItem = gtk.MenuItem("Chat")
        menuItem.connect('activate', self.show_chat, statusIcon)
        menu.append(menuItem)

        menuItem = gtk.SeparatorMenuItem()
        menu.append(menuItem)

        menuItem = gtk.MenuItem("Connect To")
        menuItem.connect('activate', self.show_connect, statusIcon)
        menu.append(menuItem)

        menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menuItem.connect('activate', self.show_about, statusIcon)
        menu.append(menuItem)

        menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menuItem.connect('activate', self.quit_cb, statusIcon)
        menu.append(menuItem)

        return menu

    def connect_to(self):
        if self.client:
            self.client.quit()
        print "calling connect to"
        reactor.callFromThread(self.client.connect)

    def send(self, rating):
        print "SEND!"
        self.client.send(utils.settings.a.name + ": %s\n" % rating)

    def paint_icon(self):
        statusIcon = gtk.StatusIcon()
        menu = self.build_menu(statusIcon)

        data = utils.resources.get_resource_path()
        statusIcon.set_from_file(os.path.join(data,"popo_emotions_The_Blacy_ico","The_Blacy!","red_heart.ico"))
        statusIcon.set_tooltip("RateIt!")
        statusIcon.connect('popup-menu', self.popup_menu_cb, menu)
        statusIcon.set_visible(True)
        gui.guiutils.GuiUtils.statusIcon = statusIcon


"""Simple callback class, which can handle can store a given set of parameters.

Useful for menuItems"""
class Callback(object):

    def __init__(self, cb, *args):
        self.cb = cb
        self.args = args

    def __call__(self, x):
        self.cb(self.args)