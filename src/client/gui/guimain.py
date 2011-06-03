'''
Created on 02.06.2011

@author: moritz
'''
import gtk
import os

import utils.resources
import threading
from copy import deepcopy

class GUI(threading.Thread):
    def __init__(self):
        super(GUI, self).__init__()
        self.paint_icon()
        self.connectTo = ''
        # Set the Chatclient
        self.client = None

    def run(self):
        gtk.main()

    def quit_cb(self, widget, data = None):
        if data:
            data.set_visible(False)
        self.client.flag = True
        gtk.main_quit()

    def cb(self, widget, data=None):
        print 'cb'

    def show_about(self, widget, data = None):
        aboutDialog = gtk.AboutDialog()
        aboutDialog.set_title("RateIt!")
        aboutDialog.set_name("RateIt!")

        file = open(os.path.join(utils.resources.get_resource_path(),'rating-rules.txt'))
        aboutDialog.set_comments(file.read())

        file = open(os.path.join(utils.resources.get_resource_path(),'gpl-3.0.txt'))
        aboutDialog.set_license(file.read())

        def close(w, res):
                if res == gtk.RESPONSE_CANCEL:
                    w.hide()
        aboutDialog.connect("response", close)

        aboutDialog.set_authors(["Thomas Kinnen","Moritz Beller"])

        aboutDialog.show()
        return aboutDialog


    def show_connect(self, widget, data = None):
        connectDialog = gtk.Dialog("Connect To", None, gtk.DIALOG_DESTROY_WITH_PARENT, None)
        connectDialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        connectDialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        entry = gtk.Entry()
        entry.set_text(self.connectTo)
        entry.show()
        connectDialog.vbox.add(entry)

        def ok(w, res):
            if res == gtk.RESPONSE_OK:
                connectDialog.hide()
                self.connectTo = entry.get_text()
                self.connect_to(self.connectTo)
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

        menuItem = gtk.MenuItem("xD")
        menuItem.connect('activate', Callback(self.send, "xD"))
        menu.append(menuItem)

        for curRating in xrange(5, 11):
            menuItem = gtk.MenuItem(str(curRating))
            menuItem.connect('activate', Callback(self.send, curRating))
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

    def connect_to(self, connect):
        print "connect to"
        self.client.connect(connect)
        print "connected"

    def send(self, rating):
        print "SEND!"
        self.client.send("Rate: %s\n" % rating)

    def paint_icon(self):
        statusIcon = gtk.StatusIcon()
        menu = self.build_menu(statusIcon)

        data = utils.resources.get_resource_path()
        statusIcon.set_from_file(os.path.join(data,"popo_emotions_The_Blacy_ico","The_Blacy!","red_heart.ico"))
        statusIcon.set_tooltip("RateIt!")
        statusIcon.connect('popup-menu', self.popup_menu_cb, menu)
        statusIcon.set_visible(True)


"""Simple callback class, which can handle can store a given set of parameters.

Useful for menuItems"""
class Callback(object):

    def __init__(self, cb, *args):
        self.cb = cb
        self.args = args

    def __call__(self, x):
        self.cb(self.args)