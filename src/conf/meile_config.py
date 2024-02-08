from os import path,environ,mkdir
from typedef.konstants import HTTParams

import configparser
import shutil

import sys


class MeileGuiConfig():
    USER = environ['SUDO_USER'] if 'SUDO_USER' in environ else environ['USER']
    BASEDIR   = path.join(path.expanduser('~' + USER), '.meile-gui')
    BASEBINDIR = path.join(BASEDIR, 'bin')
    CONFFILE  = path.join(BASEDIR, 'config.ini')
    IMGDIR    = path.join(BASEDIR, 'img')
    CONFIG    = configparser.ConfigParser()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
        return path.join(base_path, relative_path)

    def copy_bin_dir(self):
        self.copy_and_overwrite(self.resource_path("../bin"), self.BASEBINDIR)

    def copy_and_overwrite(self, from_path, to_path):
        if path.exists(to_path):
            shutil.rmtree(to_path)
        shutil.copytree(from_path, to_path)

    def read_configuration(self, confpath):
        """Read the configuration file at given path."""
        # copy our default config file

        if path.isdir(self.BASEDIR):
            if not path.isfile(confpath):
                defaultconf = self.resource_path(path.join('config', 'config.ini'))
                shutil.copyfile(defaultconf, self.CONFFILE)

        else:
            mkdir(self.BASEDIR)
            defaultconf = self.resource_path(path.join('config', 'config.ini'))
            shutil.copyfile(defaultconf, self.CONFFILE)

        if not path.isdir(self.IMGDIR):
            mkdir(self.IMGDIR)

        self.CONFIG.read(confpath)

        write_file = False
        if not self.CONFIG.has_section('network'):
            self.CONFIG.add_section('network')
            self.CONFIG.set('network', 'rpc', HTTParams.RPC)
            self.CONFIG.set('network', 'grpc', HTTParams.GRPC)
            self.CONFIG.set('network', 'api', HTTParams.APIURL)
            self.CONFIG.set('network', 'mmapi', HTTParams.MMAPI)
            write_file = True

        # backporting
        for what in ['rpc', 'grpc', 'api', 'mmapi']:
            if self.CONFIG['network'].get(what, None) is None:
                self.CONFIG.set('network', what, getattr(HTTParams, what.upper()) if what != "api" else HTTParams.APIURL)
                write_file = True

        if write_file is True:
            FILE = open(self.CONFFILE, 'w')
            self.CONFIG.write(FILE)

        return self.CONFIG
