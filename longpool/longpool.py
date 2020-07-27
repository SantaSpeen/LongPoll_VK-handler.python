import traceback

from . import config
import requests
import vk
import configs

LONGPOOL_VERSION = int(config.LONGPOOL_VERSION.replace(".",""))

class messages(object):

    def __init__(self, lp):
        self.lp = lp
        self.lp_updates = lp['updates'][0]
        self.lp_type = lp['updates'][0]['type']

    def update(self, all_updates):
        if all_updates: return self.lp_updates
        if LONGPOOL_VERSION >= 5103:
            return self.lp_updates['object']['message']
        else:
            return self.lp_updates['object']

def listen(all_updates=False):
    token = configs.token()
    api = vk.API(vk.Session(access_token=token), v=5.151)
    group_id = api.groups.getById()[0]['id']
    GetInfo = api.groups.getLongPollServer(group_id=group_id)
    key = GetInfo.get('key')
    server = GetInfo.get('server')
    ts = GetInfo.get('ts')
    print('[LongPool] Module enabled!')
    print('[LongPool] Version: ' + config.LONGPOOL_VERSION)
    while True:
        try:
            lp = requests.get(f'{server}?act=a_check&key={key}&ts={ts}&wait=25').json()
            if lp.get('failed') is not None:
                key = api.groups.getLongPollServer(group_id=group_id, v=5.151)['key']
            if ts != lp.get('ts') and lp.get('updates'):
                if lp['updates'][0]['type'] =='message_new':
                    yield messages(lp).update(all_updates)

            ts = lp.get('ts')

        except KeyboardInterrupt:
            print('\nExiting...')
            exit(0)

        except KeyError:
            global LONGPOOL_VERSION
            print("[LongPool] Make sure the settings have the correct LongPool version\n[LongPool] Аutomatically set 5.100 v.")
            LONGPOOL_VERSION = 5100

        except Exception as e:
            print("Found exception:")
            print(traceback.format_exc())