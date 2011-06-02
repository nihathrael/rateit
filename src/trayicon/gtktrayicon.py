'''
Created on 02.06.2011
   
@author: moritz
'''
import gtk 
import os
    
import utils.resources
    
class GUI:
    def __init__(self):
        self.window = self.paint_icon()
        self.connectTo = ''
        gtk.main() 
        
    def quit_cb(self, widget, data = None): 
        if data: 
            data.set_visible(False) 
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
            elif res == gtk.RESPONSE_CANCEL:
                connectDialog.hide()
                
        connectDialog.connect("response", ok)
        
        connectDialog.show()
        
    def ret_val(self, text):
        return text
    
    def popup_menu_cb(self, widget, button, time, data = None): 
        if button == 3: 
            if data: 
                data.show_all() 
                data.popup(None, None, None, 3, time) 
    
    def build_menu(self, statusIcon):
        menu = gtk.Menu() 
        
        menuItem = gtk.MenuItem("xD")
        menu.append(menuItem)  
        
        for curRating in xrange(5, 11):
            menuItem = gtk.MenuItem(str(curRating))
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
        # call to API
        pass
    
    def send(self, rating):
        #send rating to API
        pass
    
    def paint_icon(self):
        statusIcon = gtk.StatusIcon() 
        menu = self.build_menu(statusIcon)
        
        data = utils.resources.get_resource_path()
        statusIcon.set_from_file(os.path.join(data,"popo_emotions_The_Blacy_ico","The_Blacy!","red_heart.ico"))
        statusIcon.set_tooltip("RateIt!") 
        statusIcon.connect('popup-menu', self.popup_menu_cb, menu) 
        statusIcon.set_visible(True) 
        
        return statusIcon

