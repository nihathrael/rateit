'''
Created on 02.06.2011

@author: moritz
'''
import gtk 
import os

import utils.resources

def quit_cb(widget, data = None): 
    if data: 
        data.set_visible(False) 
    gtk.main_quit() 

def cb(widget, data=None): 
    print 'cb' 
    
def show_about(widget, data = None):
    aboutDialog = gtk.AboutDialog()
    aboutDialog.set_title("RateIt!")
    aboutDialog.set_name("RateIt!")
    
    file = open(os.path.join(utils.resources.get_resource_path(),'gpl-3.0.txt'))
    aboutDialog.set_license(file.read())
    
    def close(w, res):
            if res == gtk.RESPONSE_CANCEL:
                w.hide()
    aboutDialog.connect("response", close)
    
    aboutDialog.set_authors(["Thomas Kinnen","Moritz Beller"])
    
    aboutDialog.show()
    return aboutDialog

def popup_menu_cb(widget, button, time, data = None): 
    if button == 3: 
        if data: 
            data.show_all() 
            data.popup(None, None, None, 3, time) 

def build_menu(statusIcon):
    menu = gtk.Menu() 
    
    for curRating in xrange(5, 11):
        menuItem = gtk.MenuItem(str(curRating))
        menu.append(menuItem)  
    
    menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
    menuItem.connect('activate', show_about, statusIcon)
    menu.append(menuItem)
        
    menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT) 
    menuItem.connect('activate', quit_cb, statusIcon)
    menu.append(menuItem) 
    
    return menu

def connect_to(connect):
    # call to API
    pass

def send(rating):
    #send rating to API
    pass

def paint_icon():
    statusIcon = gtk.StatusIcon() 
    menu = build_menu(statusIcon)
    
    data = utils.resources.get_resource_path()
    statusIcon.set_from_file(os.path.join(data,"popo_emotions_The_Blacy_ico","The_Blacy!","red_heart.ico"))
    statusIcon.set_tooltip("RateIt!") 
    statusIcon.connect('popup-menu', popup_menu_cb, menu) 
    statusIcon.set_visible(True) 
    
    gtk.main() 


