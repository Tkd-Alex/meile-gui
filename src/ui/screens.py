from geography.continents import OurWorld
from ui.interfaces import Tab, LatencyContent, TooltipMDIconButton, ConnectionDialog, IPAddressTextField, ConnectedNode, QuotaPct,BandwidthBar,BandwidthLabel
from typedef.win import WindowNames
from cli.sentinel import  NodeTreeData
from typedef.konstants import NodeKeys, TextStrings, MeileColors, HTTParams, IBCTokens
from cli.sentinel import disconnect as Disconnect
import main.main as Meile
from ui.widgets import WalletInfoContent, MDMapCountryButton, RatingContent, NodeRV, NodeRV2, NodeAccordion, NodeRow, NodeDetails, PlanAccordion, PlanRow, PlanDetails
from utils.qr import QRCode
from cli.wallet import HandleWalletFunctions
from conf.meile_config import MeileGuiConfig
from typedef.win import CoinsList
from cli.warp import WarpHandler
from adapters import HTTPRequests, DNSRequests
from fiat import fiat_interface
from cli.v2ray import V2RayHandler
from fiat.stripe_pay import scrtsxx

from kivy.properties import BooleanProperty, StringProperty, ColorProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.uix.button import MDFlatButton, MDRaisedButton,MDTextButton, MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock, mainthread
from kivyoav.delayed import delayable
from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.core.window import Window
from kivymd.uix.behaviors.elevation import RectangularElevationBehavior
from kivy_garden.mapview import MapMarkerPopup, MapView, MapSource
from kivymd.toast import toast
from kivy.uix.carousel import Carousel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.anchorlayout import MDAnchorLayout


import requests
from requests.auth import HTTPBasicAuth
import sys
import copy
import re
from shutil import rmtree
from time import sleep
from functools import partial
from os import path,geteuid, chdir
from save_thread_result import ThreadWithResult
from threading import Thread
from unidecode import unidecode
from datetime import datetime

class WalletRestore(Screen):
    screemanager = ObjectProperty()

    dialog = None

    def __init__(self, **kwargs):
        super(WalletRestore, self).__init__()
        self.build()

    def build(self):
        if Meile.app.manager.get_screen(WindowNames.MAIN_WINDOW).NewWallet:
            self.ids.seed.opacity = 0
            self.ids.seed_hint.opacity = 0
            self.ids.restore_wallet_button.text = "Create"
        else:
            self.ids.seed.opacity = 1
            self.ids.seed_hint.opacity = 1
            self.ids.restore_wallet_button.text = "Restore"

    def restore_wallet_from_seed_phrase(self):
        wallet_password = unidecode(self.ids.password.ids.wallet_password.text)
        wallet_name     = unidecode(self.ids.name.ids.wallet_name.text)
        seed_phrase     = unidecode(self.ids.seed.ids.seed_phrase.text)
        
        if not wallet_name and not wallet_password:
            self.ids.wallet_name_warning.opacity = 1
            self.ids.wallet_password_warning.opacity = 1
            return
        elif not wallet_password:
            self.ids.wallet_password_warning.opacity = 1
            return
        elif not wallet_name:
            self.ids.wallet_name_warning.opacity = 1
            return
        elif re.match(r"^[A-Za-z0-9 ]*$", wallet_name) is None:
            self.ids.wallet_name_charset_warning.opacity = 1
            return
        elif len(wallet_password) < 8:
            self.ids.wallet_password_warning.opacity = 1
            return
        else:
            if not self.dialog:
                if not seed_phrase:
                    seed_text = "Creating a new wallet..."
                    button_text = "CREATE"
                else:
                    seed_text = seed_phrase
                    button_text = "RESTORE"
                self.dialog = MDDialog(
                    md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
                    text="Seed: %s\n\nName: %s\nPassword: %s" %
                     (
                     seed_text,
                     wallet_name,
                     wallet_password
                     ),

                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            text_color=Meile.app.theme_cls.primary_color,
                            on_release=self.cancel,
                        ),
                        MDRaisedButton(
                            text=button_text,
                            theme_text_color="Custom",
                            text_color=(1,1,1,1),
                            on_release=self.wallet_restore
                        ),
                    ],
                )
                self.dialog.open()

    def set_previous_screen(self):
        self.switch_window(None)

    def switch_window(self, inst):
        try:
            self.dialog.dismiss()
            self.dialog = None
        except AttributeError:
            pass
        Meile.app.root.remove_widget(self)
        Meile.app.root.transition = SlideTransition(direction = "down")
        Meile.app.root.current = WindowNames.MAIN_WINDOW

    def cancel(self, inst):
        self.dialog.dismiss()

    def wallet_restore(self, inst):
        MeileConfig = MeileGuiConfig()
        CONFIG = MeileConfig.read_configuration(MeileGuiConfig.CONFFILE)
        hwf = HandleWalletFunctions()


        try:
            self.dialog.dismiss()
        except Exception as e:
            print(str(e))

        seed_phrase        = unidecode(self.ids.seed.ids.seed_phrase.text)
        wallet_name        = unidecode(self.ids.name.ids.wallet_name.text)
        keyring_passphrase = unidecode(self.ids.password.ids.wallet_password.text)
        if seed_phrase:
            Wallet = hwf.create(wallet_name.lstrip().rstrip(),
                                keyring_passphrase.lstrip().rstrip(),
                                seed_phrase.lstrip().rstrip())
        else:
            Wallet = hwf.create(wallet_name.lstrip().rstrip(),
                                keyring_passphrase.lstrip().rstrip(),
                                None)

        FILE = open(MeileGuiConfig.CONFFILE,'w')

        CONFIG.set('wallet', 'keyname', wallet_name)
        CONFIG.set('wallet', 'address', Wallet['address'])
        CONFIG.set('wallet', 'password', keyring_passphrase.replace('%','%%'))

        CONFIG.write(FILE)
        FILE.close()
        WalletInfo = WalletInfoContent(Wallet['seed'], wallet_name, Wallet['address'], keyring_passphrase)
        self.dialog = MDDialog(
                type="custom",
                content_cls=WalletInfo,
                md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),

                buttons=[
                    MDRaisedButton(
                        text="I saved this",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_release=self.switch_window
                    ),
                ],
            )
        self.dialog.open()


class PreLoadWindow(Screen):
    StatusMessages = ["Calculating π...",
                      "Squaring the Circle...",
                      "Solving the Riemann Hypothesis...",
                      "Computing the Monster group M...",
                      "Finding the Galois group of f(x)...",
                      "Solving the Discrete Logarithm Problem...",
                      "Done"]
    title = "Meile dVPN"
    k = 0
    j = 0
    go_button = ObjectProperty()
    NodeTree = None
    dialog = None
    UUID = None
    def __init__(self, **kwargs):
        super(PreLoadWindow, self).__init__()

        self.NodeTree = NodeTreeData(None)

        self.GenerateUUID()
        self.CreateWarpConfig()
        self.CopyBin()

        chdir(MeileGuiConfig.BASEDIR)

        self.runNodeThread()



    @delayable
    def runNodeThread(self):
        yield 0.6
        thread2 = Thread(target=lambda: self.progress_load())
        thread2.start()
        thread = Thread(target=lambda: self.NodeTree.get_nodes("13s"))
        thread.start()

        Clock.schedule_interval(partial(self.update_status_text, thread), 1.6)

    @delayable
    def progress_load(self):
        for k in range(1,666):
            yield 0.0375
            self.manager.get_screen(WindowNames.PRELOAD).ids.pb.value += 0.0015


    def CopyBin(self):
        MeileConfig = MeileGuiConfig()
        MeileConfig.copy_bin_dir()

    def CreateWarpConfig(self):
        MeileConfig = MeileGuiConfig()
        CONFIG = MeileConfig.read_configuration(MeileGuiConfig.CONFFILE)

        if 'warp' in CONFIG:
            return
        else:
            CONFIG['warp'] = {}
            CONFIG['warp']['registered'] = str(0)
        with open(MeileGuiConfig.CONFFILE,'w') as FILE:
            CONFIG.write(FILE)
        FILE.close()

    def GenerateUUID(self):
        MeileConfig = MeileGuiConfig()
        CONFIG = MeileConfig.read_configuration(MeileGuiConfig.CONFFILE)
        self.UUID = CONFIG['wallet'].get('uuid')

        if not self.UUID:
            import uuid
            FILE = open(MeileGuiConfig.CONFFILE,'w')
            self.UUID = uuid.uuid4()
            CONFIG.set('wallet', 'uuid', "%s" % self.UUID)
            CONFIG.write(FILE)
            FILE.close()

    def get_logo(self):
        Config = MeileGuiConfig()
        return Config.resource_path(MeileColors.LOGO_HD)

    @mainthread
    def add_loading_popup(self, title_text):
        self.dialog = None
        self.dialog = MDDialog(
            title=title_text,
            md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
            buttons=[
                MDFlatButton(
                    text="OKAY",
                    theme_text_color="Custom",
                    text_color=Meile.app.theme_cls.primary_color,
                    on_release=self.quit_meile,
                ),
                ]
        )
        self.dialog.open()


    @delayable
    def update_status_text(self, t, dt):
        go_button = self.manager.get_screen(WindowNames.PRELOAD).ids.go_button
        #if geteuid() != 0:
        #    self.add_loading_popup("Please start Meile-GUI as root. i.e., sudo -E env PATH=$PATH ./meile-gui or similarly")

        yield 1.0

        if not t.is_alive():
            self.manager.get_screen(WindowNames.PRELOAD).status_text = self.StatusMessages[6]
            self.manager.get_screen(WindowNames.PRELOAD).ids.pb.value = 1
            go_button.opacity = 1
            go_button.disabled = False

            return

        if self.k == 6:
            self.k = 0
        else:
            self.manager.get_screen(WindowNames.PRELOAD).status_text = self.StatusMessages[self.k]
            self.k += 1



    def switch_window(self):
        Meile.app.root.add_widget(MainWindow(name=WindowNames.MAIN_WINDOW, node_tree=self.NodeTree))
        Meile.app.root.transition = SlideTransition(direction = "up")
        Meile.app.root.current = WindowNames.MAIN_WINDOW


class MainWindow(Screen):
    title = "Meile dVPN"
    dialog = None
    Subscriptions = []
    address = None
    old_ip = ""
    ip = ""
    CONNECTED = None
    warpd = False
    warpd_disconnected = True
    NodeTree = None
    SubResult = None
    MeileConfig = None
    ConnectedNode = None
    menu = None
    MeileLand = None
    SortOptions = ['None', "Moniker", "Price"]
    MenuOptions = ['Refresh', 'Sort', 'WARP', 'Exit']
    Sort = SortOptions[1]
    MeileMap = None
    MeileMapBuilt = False
    NodeSwitch = {"moniker" : None, "node" : None, "switch" : False, 'id' : None, 'consumed' : None, 'og_consumed' : None, 'allocated' : None, 'expirary' : None}
    NewWallet = False
    box_color = ColorProperty('#fcb711')
    clock = None
    PersistentBandwidth = {}
    ConnectedDict = {'v2ray_pid' : None,  'result' : False}
    NodeWidget = None
    Markers = []
    LatLong = []



    def __init__(self, node_tree, **kwargs):
        #Builder.load_file("./src/kivy/meile.kv")
        super(MainWindow, self).__init__()

        self.NodeTree = node_tree
        self.MeileLand = OurWorld()

        Clock.schedule_once(self.get_config,1)
        Clock.schedule_once(self.build, 1)
        
        menu_icons = ["cloud-refresh", "sort", "shield-lock", "exit-to-app"]
        menu_items = [
            {
                "viewclass" : "IconListItem",
                "icon": f"{k}",
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i,k in zip(self.MenuOptions, menu_icons)
        ]
        self.menu = MDDropdownMenu(items=menu_items, 
                                   caller=self.ids.settings_menu,
                                   width_mult=3,
                                   background_color=get_color_from_hex(MeileColors.BLACK))
        
    def menu_open(self):
        self.menu.open()
    
    def menu_callback(self, selection):
        self.menu.dismiss()
        if selection == self.MenuOptions[0]:
            self.Refresh()
        elif selection == self.MenuOptions[2]:
            self.start_warp()
        elif selection == self.MenuOptions[3]:
            sys.exit(0)
            
    
    def build(self, dt):
        # Check to build Map
        self.build_meile_map()

        # Build alphabetical country recyclerview tree data
        self.build_country_tree()

        # TODO: Would be good to process this in a background thread so as to not hang the UI
        self.get_ip_address(None)

    def build_country_tree(self):

        CountryTree = []
        CountryTreeTags = []
        # Add counry cards
        for ncountry in self.NodeTree.NodeTree.children(TextStrings.RootTag.lower()):
            CountryTree.append(ncountry)
            CountryTreeTags.append(ncountry.tag)

        CTTagsSorted = sorted(CountryTreeTags)
        #print(CTTagsSorted)
        for tag in CTTagsSorted:
            for ctree in CountryTree:
                if tag == ctree.tag:
                    self.add_country_rv_data(self.build_node_data(ctree))


    def build_node_data(self, ncountry):
        floc = "../imgs/"
        NodeCountries = {}

        iso2 = OurWorld.our_world.get_country_ISO2(ncountry.tag.lstrip().rstrip()).lower()
        flagloc = floc + iso2 + ".png"

        NodeCountries['number']  = len(self.NodeTree.NodeTree.children(ncountry.tag))
        NodeCountries['country'] = ncountry.tag
        NodeCountries['flagloc'] = flagloc

        return NodeCountries

    def build_meile_map(self):

        if not self.MeileMapBuilt:
            self.MeileMap = MapView(zoom=2)
            source = MapSource(url=MeileColors.ARCGIS_MAP,
                               cache_key="meile-map-canvas-dark-grey-base-2",
                               tile_size=256,
                               image_ext="png",
                               attribution="@ Meile",
                               size_hint=(.7,1))
            #self.MeileMap.map_source = "osm"
            self.MeileMap.map_source = source

            layout = FloatLayout(size_hint=(1,1))
            bw_label          = BandwidthLabel()
            self.quota        = BandwidthBar()
            self.quota_pct    = QuotaPct()
            self.map_widget_1 = IPAddressTextField()
            self.map_widget_2 = ConnectedNode()

            layout.add_widget(self.MeileMap)
            layout.add_widget(self.map_widget_1)
            layout.add_widget(self.map_widget_2)
            layout.add_widget(bw_label)
            layout.add_widget(self.quota)
            layout.add_widget(self.quota_pct)

            self.quota.value = 50
            self.quota_pct.text = "50%"

            self.carousel = Carousel(direction='right')
            self.ids.country_map.add_widget(self.carousel)
            #self.carousel.add_widget(self.MeileMap)
            self.carousel.add_widget(layout)
            self.AddCountryNodePins(False)
            self.MeileMapBuilt = True



    def add_country_rv_data(self, NodeCountries):
        self.ids.rv.data.append(
            {
                "viewclass"      : "RecycleViewCountryRow",
                "num_text"       : str(NodeCountries['number']) + " Nodes",
                "country_text"   : NodeCountries['country'],
                "source_image"   : self.MeileConfig.resource_path(NodeCountries['flagloc'])
            },
        )

    def refresh_country_recycler(self):
        self.ids.rv.data.clear()
        self.build_country_tree()
        self.ids.rv.refresh_from_data()

    def AddCountryNodePins(self, clear):
        Config = MeileGuiConfig()
        try:

            if clear:
                for m in self.Markers:
                    self.MeileMap.remove_marker(m)
                self.Markers.clear()


            for ncountry in self.NodeTree.NodeTree.children(TextStrings.RootTag.lower()):
                try:
                    loc = self.MeileLand.CountryLatLong[ncountry.tag]
                    marker = MapMarkerPopup(lat=loc[0], lon=loc[1], source=Config.resource_path(MeileColors.MAP_MARKER))
                    marker.add_widget(MDMapCountryButton(text='%s - %s' %(ncountry.tag, len(self.NodeTree.NodeTree.children(ncountry.tag))),
                                                   theme_text_color="Custom",
                                                   md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
                                                   text_color=(1,1,1,1),
                                                   on_release=partial(self.load_country_nodes, ncountry.tag)
                                                   ))

                    self.Markers.append(marker)
                    self.MeileMap.add_marker(marker)
                except:
                    continue
        except Exception as e:
            print(str(e))
            pass

        #self.get_continent_coordinates(self.MeileLand.CONTINENTS[0])
    
    '''
    def set_item(self, text_item):
        self.ids.drop_item.set_item(text_item)
        self.Sort = text_item
        self.menu.dismiss()
    
    def set_warp_icon(self):
        MeileConfig = MeileGuiConfig()
        return MeileConfig.resource_path("../imgs/warp.png")
    
    def set_protected_icon(self, setbool, moniker):
        MeileConfig = MeileGuiConfig()
        self.map_widget_2 = ConnectedNode()
        if setbool:
            self.ids.protected.opacity = 1
            self.map_widget_2.text = moniker
        else:
            self.ids.protected.opacity = 0
            self.map_widget_2.text = moniker
        return MeileConfig.resource_path("../imgs/protected.png")
    '''
    def get_config(self, dt):
        MeileConfig = MeileGuiConfig()
        CONFIG = MeileConfig.read_configuration(MeileGuiConfig.CONFFILE)
        self.address = CONFIG['wallet'].get("address")

    @mainthread
    def display_warp_success(self):

        self.dialog = MDDialog(
            text="You are now using DoH (DNS-over-HTTPS) and your DNS traffic is encrypted from prying eyes.",
            md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
            buttons=[
                MDRaisedButton(
                    text="Okay",
                    theme_text_color="Custom",
                    text_color=(1,1,1,1),
                    on_release=self.remove_loading_widget
                ),
            ],
        )
        self.dialog.open()

    @delayable
    def start_warp(self):
        MeileConfig = MeileGuiConfig()
        WARP = WarpHandler()
        CONFIG = MeileConfig.read_configuration(MeileGuiConfig.CONFFILE)

        if not self.warpd and self.warpd_disconnected:
            self.add_loading_popup("Starting WARP service...")
            yield 1.3
            if WARP.start_warp_daemon():
                sleep(7)
                self.warpd = True


            if int(CONFIG['warp'].get('registered')) == 0:
                print("Registering WARP...")
                CONFIG.set('warp','registered', '1')
                with open(MeileGuiConfig.CONFFILE, 'w') as FILE:
                    CONFIG.write(FILE)
                FILE.close()
                if WARP.register_warp():
                    sleep(6)
                    print("Running WARP...")
                    if WARP.run_warp():
                        print("SUCCESS")
                        sleep(3)
                        self.remove_loading_widget(None)
                        self.display_warp_success()
                        self.warpd_disconnected = False

            else:
                print("Running WARP...")
                if WARP.run_warp():
                    sleep(3)
                    print("WARP: Success!")
                    self.remove_loading_widget(None)
                    self.display_warp_success()
                    self.warpd_disconnected = False

        elif self.warpd and self.warpd_disconnected:
            self.add_loading_popup("Starting WARP service...")
            yield 1.3
            print("Running WARP...")
            if WARP.run_warp():
                sleep(3)
                print("WARP: Success!")
                self.remove_loading_widget(None)
                self.display_warp_success()
                self.warpd_disconnected = False

        else:
            #self.remove_loading_widget(None)
            self.dialog = MDDialog(
                text="Disconnecting from WARP and using system DNS...",
                md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
                buttons=[
                    MDRaisedButton(
                        text="OKAY",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_release=self.warp_disconnect
                    ),
                ],
            )
            self.dialog.open()

    @mainthread
    def warp_disconnect(self, inst):
        WARP = WarpHandler()
        self.remove_loading_widget(None)

        if WARP.warp_disconnect():
            print("SUCCESS")
            self.warpd_disconnected = True
            self.get_ip_address(None)
        else:
            print("FAIL")

    def get_logo(self):
        self.MeileConfig = MeileGuiConfig()
        return self.MeileConfig.resource_path(MeileColors.LOGO)

    def get_logo_text(self):
        self.MeileConfig = MeileGuiConfig()
        return self.MeileConfig.resource_path(MeileColors.LOGO_TEXT)

    def get_ip_address(self, dt):

        if self.dialog:
            self.dialog.dismiss()

        self.old_ip = self.ip
        try:
            resolver = DNSRequests.MakeDNSRequest(domain=HTTParams.IFCONFIGDNS, timeout=3.5, lifetime=3.5)
            ifconfig = resolver.DNSRequest()
            if ifconfig:
                print("%s:%s" % (HTTParams.IFCONFIGDNS, ifconfig))
                Request = HTTPRequests.MakeRequest()
                http = Request.hadapter()
                req = http.get(HTTParams.IFCONFIGURL)
                ifJSON = req.json()
                print(ifJSON)
                self.ip = str(ifJSON['ip'])
                self.map_widget_1.text = self.ip
                self.LatLong.clear()
                try:
                    self.LatLong.append(ifJSON['latitude'])
                    self.LatLong.append(ifJSON['longitude'])
                except:
                    print("No Lat/Long")
                    try:
                        country = ifJSON['country']
                        loc = self.MeileLand.CountryLatLong[country]
                        self.LatLong.append(loc[0])
                        self.LatLong.append(loc[1])
                    except:
                        print("No Country...Defaulting to my dream.")
                        loc = self.MeileLand.CountryLatLong["Seychelles"]
                        self.LatLong.append(loc[0])
                        self.LatLong.append(loc[1])
                return True
                #self.manager.get_screen(WindowNames.MAIN_WINDOW).ids.old_ip.text = "Old IP: " + self.old_ip
            else:
                print("Error resolving ICANHAZIP... defaulting...")
                return False
        except Exception as e:
            print(str(e))
            return False

    @mainthread
    def disconnect_from_node(self):
        try:
            if self.ConnectedDict['v2ray_pid'] is not None:
                try:
                    returncode, self.CONNECTED = Disconnect(True)
                    print("Disconnect RTNCODE: %s" % returncode)
                    self.get_ip_address(None)
                    # can be changed to a "Uprotected" label over the map
                    #self.set_protected_icon(False, "")
                except Exception as e:
                    print(str(e))
                    print("Something went wrong")

            elif self.CONNECTED == None:
                returncode, self.CONNECTED = Disconnect(False)
                print("Disconnect RTNCODE: %s" % returncode)
                self.get_ip_address(None)
                # can be changed to a "Uprotected" label over the map
                self.set_protected_icon(False, "")
            elif self.CONNECTED == False:
                print("Disconnected!")
                return True
            else:
                returncode, self.CONNECTED = Disconnect(False)
                print("Disconnect RTNCODE: %s" % returncode)
                self.get_ip_address(None)
                # can be changed to a "Uprotected" label over the map
                self.set_protected_icon(False, "")

            #self.warp_disconnect(None)
            self.dialog = None
            rating_dialog = RatingContent(self.NodeSwitch['moniker'], self.NodeSwitch['node'])
            self.dialog = MDDialog(
                title="Node Rating",
                md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
                type="custom",
                content_cls=rating_dialog,
                buttons=[
                    MDFlatButton(
                        text="LATER",
                        theme_text_color="Custom",
                        text_color=Meile.app.theme_cls.primary_color,
                        on_release=self.remove_loading_widget,
                    ),
                    MDRaisedButton(
                        text="RATE",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_release=partial(self.WrapperSubmitRating, rating_dialog),
                    ),
                    ]
                )
            self.dialog.open()
            self.NodeSwitch = {"moniker" : None,
                               "node" : None,
                               "switch" : False,
                               'id' : None,
                               'consumed' : None,
                               'og_consumed' : None,
                               'allocated' : None,
                               'expirary' : None
                               }
            return True
        except Exception as e:
            print(str(e))
            self.dialog = None
            self.dialog = MDDialog(
            text="Error disconnecting from node",
            md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
            buttons=[
                MDFlatButton(
                    text="Okay",
                    theme_text_color="Custom",
                    text_color=Meile.app.theme_cls.primary_color,
                    on_release=self.get_ip_address,
                ),
                ]
            )
            self.dialog.open()
            return False

    def WrapperSubmitRating(self, rc, dt):
        if rc.SubmitRating(rc.return_rating_value(), rc.naddress) == 0:
            toast(text="Rating Sent!", duration=3.5)
        else:
            toast(text="Error submitting rating...", duration=3.5)
        self.remove_loading_widget(None)

    def wallet_dialog(self):

        # Add a check here to see if they already have a wallet available in
        # the app and proceed to the wallet screen
        # o/w proceed to wallet_create or wallet_restore
        #
        # Eventually, I'd like to add multiple wallet support.
        # That will be after v1.0
        self.get_config(None)
        if not self.address:
            self.dialog = MDDialog(
                text="Wallet Restore/Create",
                md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
                buttons=[
                    MDFlatButton(
                        text="CREATE",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_release=partial(self.wallet_restore, True)
                    ),

                    MDRaisedButton(
                        text="RESTORE",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_release=partial(self.wallet_restore, False)
                    ),
                ],
            )
            self.dialog.open()
        else:
            self.build_wallet_interface()



    @mainthread
    def add_loading_popup(self, title_text):
        self.dialog = None
        self.dialog = MDDialog(title=title_text,md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR))
        self.dialog.open()

    @mainthread
    def remove_loading_widget(self, dt):
        try:
            self.dialog.dismiss()
            self.dialog = None
        except Exception as e:
            print(str(e))
            pass
    '''
    def refresh_nodes_and_subs(self):
        lc = LatencyContent()
        self.dialog = MDDialog(
                    title="Latency:",
                    type="custom",
                    content_cls=lc,
                    md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            text_color=Meile.app.theme_cls.primary_color,
                            on_release=self.remove_loading_widget
                        ),
                        MDRaisedButton(
                            text="REFRESH",
                            theme_text_color="Custom",
                            text_color=get_color_from_hex("#000000"),
                            on_release=partial(self.Refresh, lc)
                        ),
                    ],
                )
        self.dialog.open()
    '''
    @delayable
    def Refresh(self):
        self.remove_loading_widget(None)
        self.AddCountryNodePins(True)
        yield 0.314
        cd = ConnectionDialog()
        self.set_conn_dialog(cd, "Reloading Nodes...")
        yield 0.314
        try:
            self.NodeTree.NodeTree = None
            t = Thread(target=lambda: self.NodeTree.get_nodes("13s"))
            t.start()
            l = 13
            pool = l*100
            inc = float(1/pool)
            while t.is_alive():
                yield 0.0365
                cd.ids.pb.value += inc

            cd.ids.pb.value = 1
        except Exception as e:
            print(str(e))
            pass

        # Clear out Subscriptions
        self.SubResult = None
        # Redraw Map Pins
        self.AddCountryNodePins(False)
        self.refresh_country_recycler()
        self.remove_loading_widget(None)
        

    ''' No tabs anymore :*(
    @mainthread
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tabs_label, tab_text):
        self.ids.rv.data = []
        if not tab_text:
            tab_text = OurWorld.CONTINENTS[0]

        # Check to build Map
        self.build_meile_map()

        self.get_ip_address(None)

        # use lambda in future
        if tab_text == OurWorld.CONTINENTS[0]:
            for ncountry in self.NodeTree.NodeTree.children(OurWorld.CONTINENTS[0]):
                self.add_country_rv_data(self.build_node_data(ncountry))
                self.get_continent_coordinates(OurWorld.CONTINENTS[0])
        elif tab_text == OurWorld.CONTINENTS[1]:
            for ncountry in self.NodeTree.NodeTree.children(OurWorld.CONTINENTS[1]):
                self.add_country_rv_data(self.build_node_data(ncountry))
                self.get_continent_coordinates(OurWorld.CONTINENTS[1])
        elif tab_text == OurWorld.CONTINENTS[2]:
            for ncountry in self.NodeTree.NodeTree.children(OurWorld.CONTINENTS[2]):
                self.add_country_rv_data(self.build_node_data(ncountry))
                self.get_continent_coordinates(OurWorld.CONTINENTS[2])
        elif tab_text == OurWorld.CONTINENTS[3]:
            for ncountry in self.NodeTree.NodeTree.children(OurWorld.CONTINENTS[3]):
                self.add_country_rv_data(self.build_node_data(ncountry))
                self.get_continent_coordinates(OurWorld.CONTINENTS[3])
        elif tab_text == OurWorld.CONTINENTS[4]:
            for ncountry in self.NodeTree.NodeTree.children(OurWorld.CONTINENTS[4]):
                self.add_country_rv_data(self.build_node_data(ncountry))
                self.get_continent_coordinates(OurWorld.CONTINENTS[4])
        elif tab_text == OurWorld.CONTINENTS[5]:
            for ncountry in self.NodeTree.NodeTree.children(OurWorld.CONTINENTS[5]):
                self.add_country_rv_data(self.build_node_data(ncountry))
                self.get_continent_coordinates(OurWorld.CONTINENTS[5])
        # Search Criteria
        else:
            pass

    '''
    def get_continent_coordinates(self, c):
        loc = self.MeileLand.ContinentLatLong[c]
        self.MeileMap.zoom = 4
        self.MeileMap.center_on(loc[0], loc[1])

    def get_font(self):
        Config = MeileGuiConfig()
        return Config.resource_path(MeileColors.FONT_FACE)

    def wallet_restore(self, NewWallet, inst):
        if NewWallet:
            self.NewWallet = True
        else:
            self.NewWallet = False

        self.dialog.dismiss()
        self.dialog = None
        Meile.app.manager.add_widget(WalletRestore(name=WindowNames.WALLET_RESTORE))
        Meile.app.root.transition = SlideTransition(direction = "right")
        Meile.app.root.current = WindowNames.WALLET_RESTORE

    def build_wallet_interface(self):
        Meile.app.root.add_widget(WalletScreen(name=WindowNames.WALLET, ADDRESS=self.address))
        Meile.app.root.transition = SlideTransition(direction = "up")
        Meile.app.root.current = WindowNames.WALLET

    def build_help_screen_interface(self):
        Meile.app.root.add_widget(HelpScreen(name=WindowNames.HELP))
        Meile.app.root.transition = SlideTransition(direction = "left")
        Meile.app.root.current = WindowNames.HELP

    def build_settings_screen_interface(self):
        Meile.app.root.add_widget(SettingsScreen(name=WindowNames.SETTINGS))
        Meile.app.root.transition = SlideTransition(direction = "down")
        Meile.app.root.current = WindowNames.SETTINGS

    def switch_window(self, window):
        Meile.app.root.transition = SlideTransition(direction = "up")
        Meile.app.root.current = window

    def switch_to_sub_window(self):
        try:
            self.carousel.remove_widget(self.NodeWidget)
        except Exception as e:
            print(str(e))
        self.NodeWidget = SubscriptionScreen(name=WindowNames.SUBSCRIPTIONS, node_tree=self.NodeTree)
        self.carousel.add_widget(self.NodeWidget)
        self.carousel.load_slide(self.NodeWidget)

    def switch_to_plan_window(self):
        try:
            self.carousel.remove_widget(self.NodeWidget)
        except Exception as e:
            print(str(e))
        self.NodeWidget = PlanScreen(name=WindowNames.PLAN)
        self.carousel.add_widget(self.NodeWidget)
        self.carousel.load_slide(self.NodeWidget)

    def close_sub_window(self):
        self.carousel.remove_widget(self.NodeWidget)
        self.carousel.load_previous()

    def zoom_country_map(self):
        try:
            self.MeileMap.zoom = 7
            self.MeileMap.center_on(self.LatLong[0],self.LatLong[1])
        except Exception as e:
            print(str(e))
            pass

    def set_conn_dialog(self, cd, title):
        self.dialog = None
        self.dialog = MDDialog(
                        title=title,
                        type="custom",
                        content_cls=cd,
                        md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
                    )
        self.dialog.open()

    def load_country_nodes(self, country, *kwargs):
        mw = Meile.app.root.get_screen(WindowNames.MAIN_WINDOW)
        NodeTree = NodeTreeData(self.NodeTree.NodeTree)
        try:
            mw.carousel.remove_widget(self.NodeWidget)
        except Exception as e:
            print(str(e))
            pass

        self.NodeWidget = NodeScreen(name="nodes",
                                     node_tree=NodeTree,
                                     country=country,
                                     sort=self.Sort)
        self.carousel.add_widget(self.NodeWidget)
        self.carousel.load_slide(self.NodeWidget)

    def return_connect_button(self):
        MeileConfig = MeileGuiConfig()

        button_path = "../imgs/ConnectButton.png"

        return MeileConfig.resource_path(button_path)
class WalletScreen(Screen):
    text = StringProperty()
    ADDRESS = None
    MeileConfig = None
    dialog = None

    def __init__(self, ADDRESS,  **kwargs):
        super(WalletScreen, self).__init__()
        self.ADDRESS = ADDRESS
        print("WalletScreen, ADDRESS: %s" % self.ADDRESS)
        self.wallet_address = self.ADDRESS

        Clock.schedule_once(self.build)

    def build(self, dt):
        Wallet = HandleWalletFunctions()
        self.SetBalances(Wallet.get_balance(self.ADDRESS))

    def refresh_wallet(self):
        self.build(None)

    def open_dialog_new_wallet(self):
        self.dialog = MDDialog(
            text="Warning, if you continue your current wallet will be deleted",
            md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
            buttons=[
                MDFlatButton(
                    text="CONTINUE",
                    theme_text_color="Custom",
                    text_color=(1,1,1,1),
                    on_release=self.destroy_wallet_open_wallet_dialog
                ),
                MDRaisedButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=(1,1,1,1),
                    on_release=self.closeDialog
                ),
            ],
        )
        self.dialog.open()

    def destroy_wallet_open_wallet_dialog(self, _):
        keyring_fpath = path.join(MeileGuiConfig.BASEDIR, "keyring-file")
        img_fpath = path.join(MeileGuiConfig.BASEDIR, "img")

        for folder_path in [keyring_fpath, img_fpath]:
            if path.exists(folder_path):
                rmtree(folder_path)

        # Remove also the [wallet] section in config.ini
        # So, if the keyring-file is deleted and the use close accidentaly the application
        # We can bypass the case with a wallet reference (in config) without a keyring
        if path.exists(keyring_fpath) is False:
            MeileConfig = MeileGuiConfig()
            CONFIG = MeileConfig.read_configuration(MeileGuiConfig.CONFFILE)
            # CONFIG.remove_section('wallet')
            # We had to clear all the data as defaultconf file (can't remove)
            for k in CONFIG["wallet"]:
                if k != "uuid":
                    CONFIG.set("wallet", k, "")
            FILE = open(MeileConfig.CONFFILE, 'w')
            CONFIG.write(FILE)

        self.closeDialog(None) # arg is required (?)

        self.dialog = MDDialog(
            text="Wallet Restore/Create",
            md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
            buttons=[
                MDFlatButton(
                    text="CREATE",
                    theme_text_color="Custom",
                    text_color=(1,1,1,1),
                    on_release=partial(self.wallet_restore, True)
                    ),

                MDRaisedButton(
                    text="RESTORE",
                    theme_text_color="Custom",
                    text_color=(1,1,1,1),
                    on_release=partial(self.wallet_restore, False)
                ),
            ],
        )
        self.dialog.open()

    # duplicate of MainWindow.wallet_restore
    def wallet_restore(self, new_wallet = False, _ = None):
        # Use Main_WIndow NewWallet boolean
        Meile.app.manager.get_screen(WindowNames.MAIN_WINDOW).NewWallet = copy.deepcopy(new_wallet)
        self.closeDialog(None)  # arg is required (?)

        Meile.app.root.remove_widget(self)
        Meile.app.manager.add_widget(WalletRestore(name=WindowNames.WALLET_RESTORE))
        Meile.app.root.transition = SlideTransition(direction = "right")
        Meile.app.root.current = WindowNames.WALLET_RESTORE

    def open_fiat_interface(self):
        Meile.app.root.add_widget(fiat_interface.FiatInterface(name=WindowNames.FIAT))
        Meile.app.root.transistion = SlideTransition(direction="right")
        Meile.app.root.current = WindowNames.FIAT

    def return_coin_logo(self, coin):
        self.MeileConfig = MeileGuiConfig()

        predir = "../imgs/"
        logoDict = {}
        for c in CoinsList.coins:
            logoDict[c] = predir + c + ".png"

        for c in CoinsList.coins:
            if c == coin:
                return self.MeileConfig.resource_path(logoDict[c])

    def get_qr_code_address(self):
        CONFIG = MeileGuiConfig()
        conf = CONFIG.read_configuration(MeileGuiConfig.CONFFILE)
        self.ADDRESS = conf['wallet'].get("address")
        QRcode = QRCode()
        if not path.isfile(path.join(CONFIG.IMGDIR, "dvpn.png")):
            QRcode.generate_qr_code(self.ADDRESS)

        return path.join(CONFIG.IMGDIR, "dvpn.png")

    def SetBalances(self, CoinDict):
        if CoinDict:
            self.dec_text  = str(CoinDict['dec']) + " dec"
            self.scrt_text = str(CoinDict['scrt']) + " scrt"
            self.atom_text = str(CoinDict['atom']) + " atom"
            self.osmo_text = str(CoinDict['osmo']) + " osmo"
            self.dvpn_text = str(CoinDict['dvpn']) + " dvpn"
            #self.dvpn_text = str(CoinDict['tsent']) + " tsent"
        else:
            self.dec_text  = str("0.0") + " dec"
            self.scrt_text = str("0.0") + " scrt"
            self.atom_text = str("0.0") + " atom"
            self.osmo_text = str("0.0") + " osmo"
            self.dvpn_text = str("0.0") + " dvpn"
            #self.dvpn_text = str("0.0") + " tsent"

            self.dialog = MDDialog(
                text="Error Loading Wallet Balance. Please try again later.",
                md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
                buttons=[
                    MDRaisedButton(
                        text="OKay",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        on_release=self.closeDialog
                    ),
                ],
            )
            self.dialog.open()

    def closeDialog(self, inst):
        try:
            self.dialog.dismiss()
            self.dialog = None
        except:
            print("Dialog is NONE")
            return

    def set_previous_screen(self):

        Meile.app.root.remove_widget(self)
        Meile.app.root.transistion = SlideTransition(direction="down")
        Meile.app.root.current = WindowNames.MAIN_WINDOW


class SubscriptionScreen(MDBoxLayout):
    SubResult = None

    def __init__(self, node_tree,  **kwargs):
        super(SubscriptionScreen, self).__init__()
        self.NodeTree = node_tree

        self.get_config(None)
        self.add_loading_popup("Loading...")

        if self.address:
            Clock.schedule_once(self.subs_callback, 0.25)
            return
        else:
            self.remove_loading_widget(None)
            self.sub_address_error()
            return

    def GetSubscriptions(self):
        mw = Meile.app.root.get_screen(WindowNames.MAIN_WINDOW)
        try:
            thread = ThreadWithResult(target=self.NodeTree.get_subscriptions, args=(self.address,))
            thread.start()
            thread.join()
            mw.SubResult = thread.result
        except Exception as e:
            print(str(e))
            return None

    @delayable
    def subs_callback(self, dt):
        floc = "../imgs/"
        yield 0.314
        mw = Meile.app.root.get_screen(WindowNames.MAIN_WINDOW)

        if not mw.SubResult:
            self.GetSubscriptions()

        for sub in mw.SubResult:
            if sub[NodeKeys.FinalSubsKeys[5]] == "Czechia":
                sub[NodeKeys.FinalSubsKeys[5]] = "Czech Republic"
            try:
                iso2 = OurWorld.our_world.get_country_ISO2(sub[NodeKeys.FinalSubsKeys[5]].lstrip().rstrip()).lower()
            except:
                iso2 = "sc"
            flagloc = floc + iso2 + ".png"
            self.add_sub_rv_data(sub, flagloc)
        self.remove_loading_widget(None)

    def add_sub_rv_data(self, node, flagloc):

        if node[NodeKeys.FinalSubsKeys[2]] in self.NodeTree.NodeScores:
            nscore = str(self.NodeTree.NodeScores[node[NodeKeys.FinalSubsKeys[2]]][0])
            votes  = str(self.NodeTree.NodeScores[node[NodeKeys.FinalSubsKeys[2]]][1])
        else:
            nscore = "null"
            votes  = "0"

        if node[NodeKeys.FinalSubsKeys[2]] in self.NodeTree.NodeFormula:
            formula = str(self.NodeTree.NodeFormula[node[NodeKeys.FinalSubsKeys[2]]])
        else:
            formula = "NULL"


        ''' Not pulling cities from API any more. It comes with node data.
        if node[NodeKeys.FinalSubsKeys[2]].lstrip().rstrip() in self.NodeTree.NodeLocations:
            city = self.NodeTree.NodeLocations[node[NodeKeys.FinalSubsKeys[2]].lstrip().rstrip()]
        else:
            city = " "
        '''

        price = node[NodeKeys.FinalSubsKeys[4]].lstrip().rstrip()
        match = re.match(r"([0-9]+)([a-z]+)", price, re.I)
        if match:
            amount, coin = match.groups()
            amount = round(float(float(amount) / IBCTokens.SATOSHI),4)
            coin = coin.lstrip("u") # Remove u
            price_text = f"{amount}{coin}"
        else:
            price_text = node[NodeKeys.FinalSubsKeys[4]].lstrip().rstrip()

        if node[NodeKeys.FinalSubsKeys[9]].lstrip().rstrip():
            expirary_date = node[NodeKeys.FinalSubsKeys[9]].lstrip().rstrip().split('.')[0]
            expirary_date = datetime.strptime(expirary_date, '%Y-%m-%d %H:%M:%S').strftime('%b %d %Y, %I:%M %p')
        else:
            expirary_date = "Null"

        if node[NodeKeys.FinalSubsKeys[2]] in self.NodeTree.NodeTypes:
            if self.NodeTree.NodeTypes[node[NodeKeys.FinalSubsKeys[2]]] == NodeKeys.Nodetypes[0]:
                IconButton  = "alpha-r-circle"
                NodeTypeText = "Residential"
            elif self.NodeTree.NodeTypes[node[NodeKeys.FinalSubsKeys[2]]] == NodeKeys.Nodetypes[1]:
                IconButton  = "alpha-b-circle"
                NodeTypeText = "Business"
            elif self.NodeTree.NodeTypes[node[NodeKeys.FinalSubsKeys[2]]] == NodeKeys.Nodetypes[3]:
                IconButton  = "alpha-u-circle"
                NodeTypeText = "University"
            else:
                IconButton  = "alpha-d-circle"
                NodeTypeText = "Datacenter"
        else:
            IconButton  = "alpha-r-circle"
            NodeTypeText = "Unknown"

        item = NodeAccordion(
            node=NodeRow(
                moniker="[b]" + node[NodeKeys.FinalSubsKeys[1]] + "[/b]",
                location=node[NodeKeys.FinalSubsKeys[5]],
                protocol=node[NodeKeys.FinalSubsKeys[8]],
                node_type=NodeTypeText,
                expires=expirary_date,
            ),
            content=NodeDetails(
                sub_id=node[NodeKeys.FinalSubsKeys[0]],
                allocated=node[NodeKeys.FinalSubsKeys[6]],
                consumed=node[NodeKeys.FinalSubsKeys[7]],
                deposit=price_text,
                score=str(nscore),
                votes=str(votes),
                formula=str(formula),
                node_address=node[NodeKeys.FinalSubsKeys[2]],
            )
        )
        self.ids.rv.add_widget(item)
        '''
        if node[NodeKeys.FinalSubsKeys[1]] == "Offline":
            self.ids.rv.data.append(
                 {
                     "viewclass"      : "RecycleViewSubRow",
                     "moniker_text"   : node[NodeKeys.FinalSubsKeys[1]].lstrip().rstrip(),
                     "type_text"      : node[NodeKeys.FinalSubsKeys[8]].lstrip().rstrip(),
                     "sub_id_text"    : node[NodeKeys.FinalSubsKeys[0]].lstrip().rstrip(),
                     "price_text"     : price_text,
                     "country_text"   : "Offline",
                     "address_text"   : node[NodeKeys.FinalSubsKeys[2]].lstrip().rstrip(),
                     "allocated_text" : node[NodeKeys.FinalSubsKeys[6]].lstrip().rstrip(),
                     "consumed_text"  : node[NodeKeys.FinalSubsKeys[7]].lstrip().rstrip(),
                     "source_image"   : self.MeileConfig.resource_path(flagloc),
                     "score"          : nscore,
                     "votes"          : votes,
                     "city"           : "",
                     "expirary_date"  : expirary_date,
                     "md_bg_color"    : MeileColors.INACTIVE_DIALOG_BG_COLOR
                 },
             )
            print("%s" % node[NodeKeys.FinalSubsKeys[0]].lstrip().rstrip(),end=',')
            sys.stdout.flush()

        else:
            self.ids.rv.data.append(
                {
                    "viewclass"      : "RecycleViewSubRow",
                    "moniker_text"   : node[NodeKeys.FinalSubsKeys[1]].lstrip().rstrip(),
                    "type_text"      : node[NodeKeys.FinalSubsKeys[8]].lstrip().rstrip(),
                    "sub_id_text"    : node[NodeKeys.FinalSubsKeys[0]].lstrip().rstrip(),
                    "price_text"     : price_text,
                    "country_text"   : node[NodeKeys.FinalSubsKeys[5]].lstrip().rstrip(),
                    "address_text"   : node[NodeKeys.FinalSubsKeys[2]].lstrip().rstrip(),
                    "allocated_text" : node[NodeKeys.FinalSubsKeys[6]].lstrip().rstrip(),
                    "consumed_text"  : node[NodeKeys.FinalSubsKeys[7]].lstrip().rstrip(),
                    "source_image"   : self.MeileConfig.resource_path(flagloc),
                    "score"          : nscore,
                    "votes"          : votes,
                    "city"           : "",
                    "expirary_date"  : expirary_date,
                    "md_bg_color"    : MeileColors.DIALOG_BG_COLOR

                },
            )
            print("%s" % node[NodeKeys.FinalSubsKeys[0]].lstrip().rstrip(),end=',')
            sys.stdout.flush()
        '''
    def get_config(self, dt):
        self.MeileConfig = MeileGuiConfig()
        CONFIG = self.MeileConfig.read_configuration(MeileGuiConfig.CONFFILE)
        self.address = CONFIG['wallet'].get("address")

    @mainthread
    def add_loading_popup(self, title_text):
        self.dialog = None
        self.dialog = MDDialog(title=title_text,md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR))
        self.dialog.open()

    @mainthread
    def remove_loading_widget(self, dt):
        try:
            self.dialog.dismiss()
            self.dialog = None
        except Exception as e:
            print(str(e))
            pass

    @mainthread
    def sub_address_error(self):
        self.dialog = MDDialog(
            text="Error Loading Subscriptions... No wallet found",
            md_bg_color=get_color_from_hex(MeileColors.DIALOG_BG_COLOR),
            buttons=[
                MDRaisedButton(
                    text="Okay",
                    theme_text_color="Custom",
                    text_color=(1,1,1,1),
                    on_release=self.remove_loading_widget
                ),
            ],
        )
        self.dialog.open()

    def set_previous_screen(self):
        mw = Meile.app.root.get_screen(WindowNames.MAIN_WINDOW)
        mw.carousel.remove_widget(mw.NodeWidget)
        mw.carousel.load_previous()

'''
Main widget of country cards in carousel.
Contains: widgets.RecyclerViewRow, RecyclerViewCountryRow
'''
class NodeScreen(MDBoxLayout):
    NodeTree = None
    Country = None
    MeileConfig = None
    def __init__(self, node_tree, country, sort, **kwargs):
        super(NodeScreen, self).__init__()

        self.NodeTree = node_tree


        floc = "../imgs/"

        try:
            CountryNodes = self.NodeTree.NodeTree.children(country)
        except NodeIDAbsentError as e:
            print(str(e))
            return

        if sort == Meile.app.root.get_screen(WindowNames.MAIN_WINDOW).SortOptions[1]:
            self.SortNodesByMoniker(CountryNodes)
        elif sort == Meile.app.root.get_screen(WindowNames.MAIN_WINDOW).SortOptions[2]:
            self.SortNodesByPrice(CountryNodes)
        else:
            for node_child in CountryNodes:
                node = node_child.data
                iso2 = OurWorld.our_world.get_country_ISO2(node[NodeKeys.NodesInfoKeys[4]].lstrip().rstrip()).lower()
                flagloc = floc + iso2 + ".png"
                self.add_rv_data(node, flagloc)

    def SortNodesByPrice(self, CountryNodes):
        NodeData = []
        for node in CountryNodes:
            NodeData.append(node.data)

        i=0

        OldNodeData = copy.deepcopy(NodeData)

        for data in NodeData:
            try:
                udvpn = re.findall(r'[0-9]+\.[0-9]+' +"dvpn", data['Price'])[0]
                NodeData[i]['Price'] = udvpn
            except IndexError:
                NodeData[i]['Price'] = "10000dvpn"
            i += 1
        NodeDataSorted = sorted(NodeData, key=lambda d: float(d['Price'].split('dvpn')[0]))


        NewNodeData = []

        for ndata in NodeDataSorted:
            for odata in OldNodeData:
                if odata['Address'] == ndata['Address']:
                    ndata['Price'] = odata['Price']
                    NewNodeData.append(ndata)


        NodeDataSorted = NewNodeData

        self.meta_add_rv_data(NodeDataSorted)

    def SortNodesByMoniker(self, CountryNodes):
        NodeData = []
        for node in CountryNodes:
            NodeData.append(node.data)

        NodeDataSorted = sorted(NodeData, key=lambda d: d[NodeKeys.NodesInfoKeys[0]].lower())

        self.meta_add_rv_data(NodeDataSorted)

    def meta_add_rv_data(self, NodeDataSorted):
        floc = "../imgs/"

        for node in NodeDataSorted:
            iso2 = OurWorld.our_world.get_country_ISO2(node[NodeKeys.NodesInfoKeys[4]].lstrip().rstrip()).lower()
            flagloc = floc + iso2 + ".png"
            self.add_rv_data(node, flagloc)

    def compute_speed_rate(self, bandwidth):

        speedRate = []

        for b in bandwidth:
            speed = b
            if speed > 1000:
                speed = round(float(speed / 1024),3)
                if speed > 1000:
                    speed = round(float(speed / 1024),3)
                    if speed > 1000:
                        speed = round(float(speed / 1024),3)
                        speedRate.append(str(speed) + "GB")
                    else:
                        speedRate.append(str(speed) + "MB")
                else:
                    speedRate.append(str(speed) + "KB")
            elif speed < 0:
                speed = 0
                speedRate.append(str(speed) + "B")
            else:
                speedRate.append(str(speed) + "B")

        return speedRate


    def add_rv_data(self, node, flagloc):
        self.MeileConfig = MeileGuiConfig()
        speedRate = []
        bandwidth = []
        floc = "../imgs/"

        bandwidth.append(int(node[NodeKeys.NodesInfoKeys[8]]))
        bandwidth.append(int(node[NodeKeys.NodesInfoKeys[9]]))

        speedRate = self.compute_speed_rate(bandwidth)

        total = float(bandwidth[0] + bandwidth[1])
        if total >= 200:
            speedimage = floc + "fast.png"
        elif 125 <= total < 200:
            speedimage = floc + "fastavg.png"
        elif 75 <= total < 125:
            speedimage = floc + "avg.png"
        elif 30 <= total < 75:
            speedimage = floc + "slowavg.png"
        else:
            speedimage = floc + "slow.png"

        #speedText = str(speedRate[0]) + "↓," + str(speedRate[1]) + "↑"
        speedText = f"{speedRate[0]}[color=#00FF00]↓[/color], {speedRate[1]}[color=#f44336]↑[/color]"
        if "0B" in speedRate[0] or "0B" in speedRate[1]:
            speedText = "    " + speedText

        if node[NodeKeys.NodesInfoKeys[1]] in self.NodeTree.NodeScores:
            nscore = str(self.NodeTree.NodeScores[node[NodeKeys.NodesInfoKeys[1]]][0])
            votes  = str(self.NodeTree.NodeScores[node[NodeKeys.NodesInfoKeys[1]]][1])
        else:
            nscore = "null"
            votes  = "0"

        if node[NodeKeys.NodesInfoKeys[1]] in self.NodeTree.NodeTypes:
            if self.NodeTree.NodeTypes[node[NodeKeys.NodesInfoKeys[1]]] == NodeKeys.Nodetypes[0]:
                IconButton  = "alpha-r-circle"
                ToolTipText = "Residential"
            elif self.NodeTree.NodeTypes[node[NodeKeys.NodesInfoKeys[1]]] == NodeKeys.Nodetypes[1]:
                IconButton  = "alpha-b-circle"
                ToolTipText = "Business"
            elif self.NodeTree.NodeTypes[node[NodeKeys.NodesInfoKeys[1]]] == NodeKeys.Nodetypes[3]:
                IconButton  = "alpha-u-circle"
                ToolTipText = "University"
            else:
                IconButton  = "alpha-d-circle"
                ToolTipText = "Datacenter"
        else:
            IconButton  = "alpha-r-circle"
            ToolTipText = "Residential"

        if node[NodeKeys.NodesInfoKeys[1]] in self.NodeTree.NodeHealth:
            if self.NodeTree.NodeHealth[node[NodeKeys.NodesInfoKeys[1]]]:
                HealthButton = MeileColors.HEALTH_ICON
                HealthToolTip = TextStrings.PassedHealthCheck
            else:
                HealthButton = MeileColors.SICK_ICON
                HealthToolTip = TextStrings.FailedHealthCheck

        else:
            HealthButton = MeileColors.SICK_ICON
            HealthToolTip = TextStrings.FailedHealthCheck

        self.ids.rv.data.append(
            {
                "viewclass"          : "RecycleViewRow",
                "moniker_text"       : node[NodeKeys.NodesInfoKeys[0]],
                #"price_text"         : node[NodeKeys.NodesInfoKeys[2]].lstrip().rstrip(),
                #"hourly_price_text"  : node[NodeKeys.NodesInfoKeys[3]].lstrip().rstrip(),
                "country_text"       : node[NodeKeys.NodesInfoKeys[4]],
                #"address_text"       : node[NodeKeys.NodesInfoKeys[1]].lstrip().rstrip(),
                "protocol_text"      : node[NodeKeys.NodesInfoKeys[13]],
                "speed_text"         : speedText,
                "isp_type_text"      : ToolTipText,
                "node_data"          : node,
                "node_types"         : self.NodeTree.NodeTypes,
                "node_scores"        : self.NodeTree.NodeScores,
                "node_formula"       : self.NodeTree.NodeFormula
                #"node_score"         : nscore,
                #"votes"              : votes,
                #"city"               : city,
                #"icon"               : IconButton,
                #"tooltip"            : ToolTipText,
                #"healthcheck"        : HealthButton,
                #"healthchecktooltip" : HealthToolTip,
                #"speed_image"        : self.MeileConfig.resource_path(speedimage),
                #"source_image"       : self.MeileConfig.resource_path(flagloc)

            },
        )




    def set_previous_screen(self):
        mw = Meile.app.root.get_screen(WindowNames.MAIN_WINDOW)
        mw.carousel.remove_widget(mw.NodeWidget)
        mw.carousel.load_previous()

class PlanScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super(PlanScreen, self).__init__()
        self.mw = Meile.app.root.get_screen(WindowNames.MAIN_WINDOW)
        wallet = self.mw.address
        Request = HTTPRequests.MakeRequest()
        http = Request.hadapter()

        req = http.get(HTTParams.PLAN_API + HTTParams.API_PLANS, auth=HTTPBasicAuth(scrtsxx.PLANUSERNAME, scrtsxx.PLANPASSWORD))
        plan_data = req.json()

        # Prevent plan parsing when wallet is not initialized
        user_enrolled_plans = []
        if wallet not in [None, ""]:
            req2 = http.get(HTTParams.PLAN_API + HTTParams.API_PLANS_SUBS % wallet, auth=HTTPBasicAuth(scrtsxx.PLANUSERNAME, scrtsxx.PLANPASSWORD))

            # If the request failed please don't .json() or will raised a exception
            user_enrolled_plans = req2.json() if req2.ok and req2.status_code != 404 else []

        for pd in plan_data:
            self.build_plans( pd, user_enrolled_plans)

    def build_plans(self, data, plans):
        plan = None
        for p in plans:
            if data['uuid'] == p['uuid']:
                plan = p
                break


        # In the future cost should be both in dvpn and euro (fuck usd)
        # Can use coin_api to get dvpn price and translate cost
        item = PlanAccordion(
            node=PlanRow(
                plan_name=data['plan_name'],
                num_of_nodes=str(45),
                num_of_countries=str(30),
                cost=str(round(float(data['plan_price'] / IBCTokens.SATOSHI),2)) + data['plan_denom'],
                logo_image=data['logo'],
                uuid=data['uuid'],
                id=str(data['subscription_id']),
                plan_id=str(data['plan_id'])
            ),
            content=PlanDetails(
                uuid=plan['uuid'] if plan else data['uuid'],
                id=str(plan['subscription_id']) if plan else str(data['subscription_id']),
                expires=plan['expires'] if plan else "NULL",
                deposit=str(round(float(plan['amt_paid']),2)) if plan else "NULL",
                coin=plan['amt_denom'] if plan else "NULL",
            )
        )

        self.ids.rv.add_widget(item)

    def set_previous_screen(self):
        mw = Meile.app.root.get_screen(WindowNames.MAIN_WINDOW)
        mw.carousel.remove_widget(mw.NodeWidget)
        mw.carousel.load_previous()
'''
This is the card class of the country cards on the left panel
'''
class RecycleViewCountryRow(MDCard,RectangularElevationBehavior,ThemableBehavior, HoverBehavior):
    text = StringProperty()

    def on_enter(self, *args):
        self.md_bg_color = get_color_from_hex(MeileColors.ROW_HOVER)
        Window.set_system_cursor('hand')

    def on_leave(self, *args):
        self.md_bg_color = get_color_from_hex(MeileColors.DIALOG_BG_COLOR)
        Window.set_system_cursor('arrow')

    def switch_window(self, country):
        print(country)
        mw       = Meile.app.root.get_screen(WindowNames.MAIN_WINDOW)
        NodeTree = NodeTreeData(mw.NodeTree.NodeTree)


        try:
            mw.carousel.remove_widget(mw.NodeWidget)
        except Exception as e:
            print(str(e))
            pass

        mw.NodeWidget = NodeScreen(name="nodes",
                                   node_tree=NodeTree,
                                   country=country,
                                   sort=mw.Sort)
        print(mw.NodeWidget)
        mw.carousel.add_widget(mw.NodeWidget)
        mw.carousel.load_slide(mw.NodeWidget)

class HelpScreen(Screen):

    def GetMeileVersion(self):
        return TextStrings.VERSION

    def set_previous_screen(self):

        Meile.app.root.remove_widget(self)
        Meile.app.root.transistion = SlideTransition(direction="right")
        Meile.app.root.current = WindowNames.MAIN_WINDOW


class SettingsScreen(Screen):
    MeileConfig = MeileGuiConfig()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        params = HTTParams()
        self.RPC = params.RPC

        self.MeileConfig = MeileGuiConfig()

        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "server-security",
                "text": f"{i}",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in params.RPCS
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=50,
        )
        self.menu.bind()

    def get_rpc_config(self):
        CONFIG = self.MeileConfig.read_configuration(self.MeileConfig.CONFFILE)

        self.ids.drop_item.set_item(CONFIG['network']['rpc'])
        return CONFIG['network']['rpc']

    def set_item(self, text_item):
        self.ids.drop_item.set_item(text_item)
        self.RPC = text_item
        self.menu.dismiss()

    def build(self):
        return self.screen

    def SaveOptions(self):

        CONFIG = self.MeileConfig.read_configuration(self.MeileConfig.CONFFILE)
        CONFIG.set('network', 'rpc', self.RPC)

        FILE = open(self.MeileConfig.CONFFILE, 'w')
        CONFIG.write(FILE)

        self.set_previous_screen()

    def set_previous_screen(self):

        Meile.app.root.remove_widget(self)
        Meile.app.root.transistion = SlideTransition(direction="up")
        Meile.app.root.current = WindowNames.MAIN_WINDOW