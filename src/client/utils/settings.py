'''
Created on 03.06.2011

@author: moritz
'''
import os
import getpass
import uuid 

class Settings():
    def __init__(self):
        self.configfile = self.__get_config_path()
        self.server = ""
        self.channel = ""
        self.name = ""
        self.id = None
    
    def __get_config_path(self):
        return os.path.expanduser(os.path.join("~",".rateit"))

    def load_settings(self):
        try:
            file = open(self.configfile)
            self.name = file.readline().rstrip()
            if self.name == "" or self.name == None:
                self.name = getpass.getuser()
            if self.name == "" or self.name == None:
                self.name = "A dude"
            self.id = file.readline().rstrip()
            if self.id == "" or self.id == None:
                self.id = uuid.uuid1()
            self.server = file.readline().rstrip()
            self.channel = file.readline().rstrip()
            file.close()
        except IOError, err:
            print "No configuration file " + self.configfile + " found."
            
    def save_settings(self):
        try:
            file = open(self.configfile, 'w')
            file.write(self.name + '\n')
            file.write(str(self.id) + '\n')
            file.write(self.server + '\n')
            file.write(self.channel + '\n')
            file.close()
        except Exception, err:
            print "Could not save settings to configuration file " + self.configfile + "."
        
        
a = Settings()
a.load_settings()