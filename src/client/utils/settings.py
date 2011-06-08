'''
Created on 03.06.2011

@author: moritz
'''
import os
import getpass

class Settings():
    def __init__(self):
        self.configfile = self.__get_config_path()
        self.server = ""
        self.channel = ""
    
    def __get_config_path(self):
        return os.path.expanduser(os.path.join("~",".rateit"))

    def load_settings(self):
        try:
            file = open(self.configfile)
            self.server = file.readline().rstrip()
            self.name = file.readline().rstrip()
            if self.name == "":
                self.name = getpass.getuser()
            self.channel = file.readline().rstrip()
            file.close()
        except IOError, err:
            print "No configuration file " + self.configfile + " found."
            
    def save_settings(self):
        try:
            file = open(self.configfile, 'w')
            file.write(self.server + '\n')
            file.write(self.name + '\n')
            file.write(self.channel + '\n')
            file.close()
        except Exception, err:
            print "Could not save settings to configuration file " + self.configfile + "."
        
        
a = Settings()
a.load_settings()