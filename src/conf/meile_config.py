from os import path

import configparser
import pkg_resources
import shutil
import os
import sys

class MeileGuiConfig():
    BASEDIR   = path.join(path.expanduser('~'), '.meile-gui')
    CONFFILE  = path.join(BASEDIR, 'config.ini')
    IMGDIR    = path.join(BASEDIR, 'img')
    CONFIG    = configparser.ConfigParser()
    
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
        return path.join(base_path, relative_path)
        
    
    def read_configuration(self, confpath):
        """Read the configuration file at given path."""
        # copy our default config file
        
        if path.isdir(self.BASEDIR):
            if not path.isfile(confpath):
                defaultconf = self.resource_path(os.path.join('config', 'config.ini'))
                shutil.copyfile(defaultconf, self.CONFFILE)
                
        else:
            os.mkdir(self.BASEDIR)
            defaultconf = self.resource_path(os.path.join('config', 'config.ini'))
            shutil.copyfile(defaultconf, self.CONFFILE)
            
        if not os.path.isdir(self.IMGDIR):
            os.mkdir(self.IMGDIR)
            
        self.CONFIG.read(confpath)
        return self.CONFIG
