import pexpect
import json
import requests
import psutil
import binascii
from time import sleep
from os import path, remove

from json.decoder import JSONDecodeError

from conf.meile_config import MeileGuiConfig
from typedef.konstants import IBCTokens
from typedef.konstants import ConfParams
from typedef.konstants import HTTParams
from adapters import HTTPRequests
from cli.v2ray import V2RayHandler

import bech32
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
from sentinel_protobuf.sentinel.subscription.v2.msg_pb2 import MsgCancelRequest, MsgCancelResponse

from sentinel_sdk.sdk import SDKInstance
from sentinel_sdk.types import NodeType, TxParams, Status
from sentinel_sdk.utils import search_attribute

from mnemonic import Mnemonic
from keyrings.cryptfile.cryptfile import CryptFileKeyring
import ecdsa
import hashlib

# from cosmpy.aerial.client import LedgerClient, NetworkConfig
# from cosmpy.aerial.wallet import LocalWallet
# from cosmpy.crypto.keypairs import PrivateKey
# from cosmpy.aerial.tx import Transaction
# from cosmpy.aerial.tx_helpers import TxResponse
# from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction

MeileConfig = MeileGuiConfig()
sentinelcli = MeileConfig.resource_path("../bin/sentinelcli")
v2ray_tun2routes_connect_bash = MeileConfig.resource_path("../bin/routes.sh")

class HandleWalletFunctions():
    connected =  {'v2ray_pid' : None, 'result' : False, 'status' : None}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        CONFIG = MeileConfig.read_configuration(MeileConfig.CONFFILE)
        self.RPC = CONFIG['network'].get('rpc', HTTParams.RPC)



    def create(self, wallet_name, keyring_passphrase, seed_phrase = None):
        # Credtis: https://github.com/ctrl-Felix/mospy/blob/master/src/mospy/utils.py

        if seed_phrase is None:
            seed_phrase = Mnemonic("english").generate(strength=256)

        print(seed_phrase)  # TODO: only-4-debug
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
        bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()

        privkey_obj = ecdsa.SigningKey.from_string(bip44_def_ctx.PrivateKey().Raw().ToBytes(), curve=ecdsa.SECP256k1)
        pubkey  = privkey_obj.get_verifying_key()
        s = hashlib.new("sha256", pubkey.to_string("compressed")).digest()
        r = hashlib.new("ripemd160", s).digest()
        five_bit_r = bech32.convertbits(r, 8, 5)
        account_address = bech32.bech32_encode("sent", five_bit_r)
        print(account_address)

        # Create a class of separated method for keyring please
        kr = CryptFileKeyring()
        kr.filename = "keyring.cfg"
        print(ConfParams.KEYRINGDIR)
        kr.file_path = path.join(ConfParams.KEYRINGDIR, kr.filename)
        print(kr.file_path)
        kr.keyring_key = keyring_passphrase
        kr.set_password("meile-gui", wallet_name, bip44_def_ctx.PrivateKey().Raw().ToBytes().hex())

        return {
            'address': account_address,
            'seed': seed_phrase
        }


    def subscribe(self, KEYNAME, NODE, DEPOSIT, GB, hourly):
        if not KEYNAME:  # TODO: (?)
            return (False, 1337)

        print("Deposit/denom")
        print(DEPOSIT)
        DENOM = self.DetermineDenom(DEPOSIT)
        print(DENOM)

        CONFIG = MeileConfig.read_configuration(MeileConfig.CONFFILE)
        PASSWORD = CONFIG['wallet'].get('password', '')

        self.RPC = CONFIG['network'].get('rpc', HTTParams.RPC)
        self.GRPC = CONFIG['network'].get('grpc', HTTParams.GRPC)

        grpc = self.GRPC.replace("grpc+http://", "").replace("/", "")  # TODO: why const is grpc is saved as ... (?)
        grpcaddr, grpcport = grpc.split(":")

        # Create a class of separated method for keyring please
        kr = CryptFileKeyring()
        kr.filename = "keyring.cfg"
        print(ConfParams.KEYRINGDIR)
        kr.file_path = path.join(ConfParams.KEYRINGDIR, kr.filename)
        print(kr.file_path)
        kr.keyring_key = PASSWORD  # TODO: very ungly
        private_key = kr.get_password("meile-gui", KEYNAME)  # TODO: very ungly

        print(private_key)  # TODO: only-4-debug
        sdk = SDKInstance(grpcaddr, int(grpcport), secret=private_key)

        # From ConfParams
        # GASPRICE         = "0.2udvpn"
        # GASADJUSTMENT    = 1.15
        # GAS              = 500000
        # ConfParams.GASPRICE, ConfParams.GAS, ConfParams.GASADJUSTMENT,

        tx_params = TxParams(
            # denom="udvpn",  # TODO: from ConfParams
            # fee_amount=20000,  # TODO: from ConfParams
            # gas=ConfParams.GAS,
            gas_multiplier=ConfParams.GASADJUSTMENT
        )

        print("node_address", NODE)
        print("gigabytes", 0 if hourly else GB)  # TODO: review this please
        print("hours", GB if hourly else 0)  # TODO: review this please
        print("denom", DENOM)
        print("tx_params", tx_params)

        tx = sdk.nodes.SubscribeToNode(
            node_address=NODE,
            gigabytes=0 if hourly else GB,  # TODO: review this please
            hours=GB if hourly else 0,  # TODO: review this please
            denom=DENOM,
            tx_params=tx_params,
        )
        if tx.get("log", None) is not None:
            return(False, tx["log"])

        if tx.get("hash", None) is not None:
            tx_response = sdk.nodes.wait_transaction(tx["hash"])
            print(tx_response)
            subscription_id = search_attribute(
                tx_response, "sentinel.node.v2.EventCreateSubscription", "id"
            )
            if subscription_id:
                return (True,0)

        return(False, "Tx error")

        # return self.ParseSubscribe()

    def DetermineDenom(self, deposit):
        for key,value in IBCTokens.IBCUNITTOKEN.items():
            if value in deposit:
                return value

    """
    def ParseSubscribe(self):
        SUBJSON = False
        with open(ConfParams.SUBSCRIBEINFO, 'r') as sub_file:
                lines = sub_file.readlines()
                for l in lines:
                    if "Error" in l:
                        return(False, l)

                for l in lines:
                    try:
                        tx_json = json.loads(l)
                        SUBJSON = True
                    except Exception as e:
                        continue
                if SUBJSON:
                    if tx_json['data']:
                        try:
                            sub_id = tx_json['logs'][0]['events'][4]['attributes'][0]['value']
                            if sub_id:
                                #remove(ConfParams.SUBSCRIBEINFO)
                                return (True,0)
                            else:
                                #remove(ConfParams.SUBSCRIBEINFO)
                                return (False,2.71828)
                        except:
                            #remove(ConfParams.SUBSCRIBEINFO)
                            return (False, 3.14159)
                    elif 'insufficient' in tx_json['raw_log']:
                        #remove(ConfParams.SUBSCRIBEINFO)
                        return (False, tx_json['raw_log'])
                else:
                    return(False, "Error loading JSON")
    """

    def unsubscribe(self, subId):
        CONFIG = MeileConfig.read_configuration(MeileConfig.CONFFILE)
        PASSWORD = CONFIG['wallet'].get('password', '')
        KEYNAME = CONFIG['wallet'].get('keyname', '')

        if not KEYNAME:
            return {'hash' : "0x0", 'success' : False, 'message' : "ERROR Retrieving Keyname"}

        ofile = open(ConfParams.USUBSCRIBEINFO, "wb")

        unsubCMD = "%s keys export --unarmored-hex --unsafe --keyring-backend file --keyring-dir %s '%s'" % (sentinelcli,  ConfParams.KEYRINGDIR, KEYNAME)

        try:
            child = pexpect.spawn(unsubCMD)
            child.logfile = ofile

            child.expect(".*")
            child.sendline("y")
            child.expect("Enter*")
            child.sendline(PASSWORD)
            child.expect(pexpect.EOF)

            ofile.flush()
            ofile.close()
        except Exception as e:
            return {'hash' : "0x0", 'success' : False, 'message' : f"ERROR: {str(e)}"}

        privkey_hex = self.ParseUnSubscribe()
        return self.grpc_unsubscribe(privkey_hex, subId)

    def grpc_unsubscribe(self, privkey, subId):
        pass

    """
    def grpc_unsubscribe(self, privkey, subId):
        tx_success = False
        tx_hash    = "0x0"

        cfg = NetworkConfig(
            chain_id=ConfParams.CHAINID,
            url=HTTParams.GRPC,
            fee_minimum_gas_price=0.4,
            fee_denomination=IBCTokens.mu_coins[0],
            staking_denomination=IBCTokens.mu_coins[0],
        )

        client = LedgerClient(cfg)

        priv_key_bytes = binascii.unhexlify(bytes(privkey.rstrip().lstrip(), encoding="utf8"))

        wallet = LocalWallet(PrivateKey(priv_key_bytes), prefix="sent")
        address = wallet.address()

        print(f"Address: {address},\nSubscription ID: {subId}")

        try:
            tx = Transaction()
            try:
                tx.add_message(MsgCancelRequest(frm=str(address), id=int(subId)))
            except Exception as e1:
                print(str(e1))
                print("Error Failed on add_message")


            try:
                tx = prepare_and_broadcast_basic_transaction(client, tx, wallet)
                tx.wait_to_complete()
            except Exception as e2:
                print("error on broadcasting transaction")
                print(str(e2))

            tx_hash     = tx._tx_hash
            tx_response = tx._response.is_successful()
            tx_height   = int(tx._response.height)

            print("Hash: %s" % str(tx_hash))
            print("Response: %s" % tx_response)
            print("Height: %d" % int(tx._response.height))

            if tx_response:
                tx_success = tx_response
                message    = "Unsubscribe from Subscription ID: %s, was successful at Height: %d" % (subId, tx_height )

            else:
                message = "Unsubscribe failed"
        except Exception as e:
            message = f"Error creating or broadcasting unsubscribe tx message: {str(e)}"

        return {'hash' : tx_hash, 'success' : tx_success, 'message' : message}
    """

    def ParseUnSubscribe(self):
        with open(ConfParams.USUBSCRIBEINFO, 'r') as usubfile:
            lines = usubfile.readlines()
            lines = [l for l in lines if l != '\n']
            for l in lines:
                l.replace('\n','')

        usubfile.close()
        remove(ConfParams.USUBSCRIBEINFO)
        return l


    def connect(self, ID, address, type):

        CONFIG = MeileConfig.read_configuration(MeileConfig.CONFFILE)
        self.RPC = CONFIG['network'].get('rpc', HTTParams.RPC)
        PASSWORD = CONFIG['wallet'].get('password', '')
        KEYNAME = CONFIG['wallet'].get('keyname', '')
        connCMD = "pkexec env PATH=%s %s connect --home %s --keyring-backend file --keyring-dir %s --chain-id %s --node %s --gas-prices %s --gas %d --gas-adjustment %f --yes --from '%s' %s %s" % (ConfParams.PATH,
                                                                                                                                                                                                    sentinelcli,
                                                                                                                                                                                                    ConfParams.BASEDIR,
                                                                                                                                                                                                    ConfParams.KEYRINGDIR,
                                                                                                                                                                                                    ConfParams.CHAINID,
                                                                                                                                                                                                    self.RPC,
                                                                                                                                                                                                    ConfParams.GASPRICE,
                                                                                                                                                                                                    ConfParams.GAS,
                                                                                                                                                                                                    ConfParams.GASADJUSTMENT,
                                                                                                                                                                                                    KEYNAME,
                                                                                                                                                                                                    ID,
                                                                                                                                                                                                    address)

        print(connCMD)
        ofile =  open(ConfParams.CONNECTIONINFO, "wb")

        try:
            child = pexpect.spawn(connCMD)
            child.logfile = ofile

            child.expect(".*")
            child.sendline(PASSWORD)
            child.expect(pexpect.EOF)

            ofile.flush()
            ofile.close()
        except pexpect.exceptions.TIMEOUT:
            self.connected = {"v2ray_pid" : None,  "result": False, "status" : "Error running expect"}
            return


        with open(ConfParams.CONNECTIONINFO, "r") as connection_file:
            lines = connection_file.readlines()

            for l in lines:
                if "Error" in l and "v2ray" not in l and "inactive_pending" not in l:
                    self.connected = {"v2ray_pid" : None,  "result": False, "status" : l}
                    return

        if type == "WireGuard":
            if psutil.net_if_addrs().get("wg99"):
                self.connected = {"v2ray_pid" : None,  "result": True, "status" : "wg99"}
                return
            else:
                self.connected = {"v2ray_pid" : None,  "result": False, "status" : "Error bringing up wireguard interface"}
                return
        else:
            TUNIFACE = False
            V2Ray = V2RayHandler(v2ray_tun2routes_connect_bash + " up")
            V2Ray.start_daemon()
            sleep(15)

            for iface in psutil.net_if_addrs().keys():
                if "tun" in iface:
                    TUNIFACE = True
                    break

            if TUNIFACE:
                self.connected = {"v2ray_pid" : V2Ray.v2ray_pid, "result": True, "status" : TUNIFACE}
                print(self.connected)
                return
            else:
                try:
                    V2Ray.v2ray_script = v2ray_tun2routes_connect_bash + " down"
                    V2Ray.kill_daemon()
                    #V2Ray.kill_daemon()
                    #Tun2Socks.kill_daemon()
                except Exception as e:
                    print(str(e))

                self.connected = {"v2ray_pid" : V2Ray.v2ray_pid,  "result": False, "status": "Error connecting to v2ray node: %s" % TUNIFACE}
                print(self.connected)
                return

    def get_balance(self, address):
        Request = HTTPRequests.MakeRequest()
        http = Request.hadapter()
        endpoint = HTTParams.BALANCES_ENDPOINT + address
        CoinDict = {'dvpn' : 0, 'scrt' : 0, 'dec'  : 0, 'atom' : 0, 'osmo' : 0}
        #CoinDict = {'tsent' : 0, 'scrt' : 0, 'dec'  : 0, 'atom' : 0, 'osmo' : 0}

        try:
            r = http.get(HTTParams.APIURL + endpoint)
            coinJSON = r.json()
        except:
            return None

        print(coinJSON)
        try:
            for coin in coinJSON['result']:
                if "udvpn" in coin['denom']:
                #if "tsent" in coin['denom']:
                    CoinDict['dvpn'] = round(float(float(coin['amount']) /IBCTokens.SATOSHI),4)
                    #CoinDict['tsent'] = round(float(float(coin['amount']) /IBCTokens.SATOSHI),4)
                elif IBCTokens.IBCSCRT in coin['denom']:
                    CoinDict['scrt'] = round(float(float(coin['amount']) /IBCTokens.SATOSHI),4)
                elif IBCTokens.IBCDEC in coin['denom']:
                    CoinDict['dec'] = round(float(float(coin['amount']) /IBCTokens.SATOSHI),4)
                elif IBCTokens.IBCATOM in coin['denom']:
                    CoinDict['atom'] = round(float(float(coin['amount']) /IBCTokens.SATOSHI),4)
                elif IBCTokens.IBCOSMO in coin['denom']:
                    CoinDict['osmo'] = round(float(float(coin['amount']) /IBCTokens.SATOSHI),4)
        except Exception as e:
            print(str(e))
            return None
        return CoinDict




