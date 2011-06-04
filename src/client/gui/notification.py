'''
Created on 04.06.2011

@author: moritz
'''
import pynotify

def showNotification(text):
    global statusIcon
    print "Text received:", text
    n = pynotify.Notification(text)
    n.set_urgency(pynotify.URGENCY_CRITICAL)
    n.set_timeout(15000) # 10 seconds
    n.set_category("device")
    try:
        # due to a bug, some libnotifys dont have this method
        n.attach_to_status_icon(statusIcon)
    except AttributeError:
        # dont attach then
        pass

    if not n.show():
        print "Failed to send notification"