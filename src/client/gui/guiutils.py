'''
Created on 04.06.2011

@author: moritz
'''
import pynotify
import os 
import utils.resources
import string
import gtk, gobject

class IconUpdater():
    def __init__(self, statusIcon):
        self.statusIcon = statusIcon
        self.iconAfterStart = None
        
    def callback(self):
        if self.iconAfterStart == self.statusIcon.get_pixbuf():
            self.__setIcon("red_heart.ico")
            
    def __setIcon(self, newIcon):
        data = utils.resources.get_resource_path()
        self.statusIcon.set_from_file(os.path.join(data,"popo_emotions_The_Blacy_ico","The_Blacy!",newIcon))
        self.iconAfterStart = self.statusIcon.get_pixbuf()
        
    def changeIcon(self, newIcon):
        gobject.timeout_add(GuiUtils.NotificationAliveTime, self.callback)
        self.__setIcon(newIcon)

class GuiUtils(object):
    statusIcon=None
    NotificationAliveTime=10000
    
    def DetermineAndSetNewIcon(text):
        iconUpdater = IconUpdater(GuiUtils.statusIcon)
        if string.find(text, 'xD') > -1:
            iconUpdater.changeIcon("electric_shock.ico")
        elif string.find(text, '5') > -1:
            iconUpdater.changeIcon("bad_smile.ico")
        elif string.find(text, '6') > -1:
            iconUpdater.changeIcon("shocked.ico")
        elif string.find(text, '7') > -1:
            iconUpdater.changeIcon("girl.ico")
        elif string.find(text, '8') > -1:
            iconUpdater.changeIcon("big_smile.ico")
        elif string.find(text, '9') > -1:
            iconUpdater.changeIcon("exciting.ico")
        elif string.find(text, '10') > -1:
            iconUpdater.changeIcon("money.ico")
    
    DetermineAndSetNewIcon = staticmethod(DetermineAndSetNewIcon)
        
    def showNotification(text):
        print "Text received:", text
        n = pynotify.Notification(text)
        n.set_urgency(pynotify.URGENCY_CRITICAL)
        n.set_timeout(GuiUtils.NotificationAliveTime) 
        n.set_category("device")
        GuiUtils.DetermineAndSetNewIcon(text)
        try:
            # due to a bug, some libnotifys dont have this method
            n.attach_to_status_icon(GuiUtils.statusIcon)
        except AttributeError:
            # dont attach then
            pass
    
        if not n.show():
            print "Failed to send notification"
            
    showNotification = staticmethod(showNotification)