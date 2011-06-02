'''
Created on 02.06.2011

@author: moritz
'''
import gtk 

def quit_cb(widget, data = None): 
    if data: 
        data.set_visible(False) 
    gtk.main_quit() 

def cb(widget, data=None): 
    print 'cb' 

def popup_menu_cb(widget, button, time, data = None): 
    if button == 3: 
        if data: 
            data.show_all() 
            data.popup(None, None, None, 3, time) 

statusIcon = gtk.StatusIcon() 

menu = gtk.Menu() 
menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT) 
menuItem.connect('activate', quit_cb, statusIcon)
menu.append(menuItem) 
for x in xrange(5,11):
    menuItem = gtk.MenuItem(str(x))
    menu.append(menuItem)  

statusIcon.set_from_file("/home/moritz/files/arbeit/rateit/data/popo_emotions_The_Blacy_ico/The_Blacy!/red_heart.ico")
statusIcon.set_tooltip("RateIt!") 
statusIcon.connect('popup-menu', popup_menu_cb, menu) 
statusIcon.set_visible(True) 

gtk.main() 
