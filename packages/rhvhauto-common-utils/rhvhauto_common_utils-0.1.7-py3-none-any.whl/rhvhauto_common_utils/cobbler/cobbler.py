import copy
import xmlrpc.client


class Cobbler:
    system_tpl = dict(
        name="",
        profile="",
        modify_interface={"macaddress-?": ""},
        comment="managed-by-zoidberg",
        status="testing",
        kernel_options="",
        kernel_options_post=""
    )

    def __init__(self, url: str, credential: tuple):
        self.url = url
        self.credential = credential
        self.token = None

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'disconnected from {self.url}')

    @property
    def proxy(self):
        return xmlrpc.client.ServerProxy(self.url)

    @property
    def profiles(self):
        ret = self.proxy.get_profiles()
        return [pn['name'] for pn in ret if pn['name'].startswith('RHVH-4')]

    def login(self):
        self.token = self.proxy.login(*self.credential)

    def find_system(self, name_pattern):
        print("start to querying system {}".format(name_pattern))

        ret = self.proxy.find_system(dict(name=name_pattern))
        if ret:
            print("found system : {}".format(ret))
            return True
        else:
            print("system not exists")
            return False

    def add_new_system(self, **kwargs):
        system_id = self.proxy.new_system(self.token)
        params = copy.deepcopy(self.system_tpl)
        params.update(kwargs)

        print("add new host with {}".format(params))
        for k, v in params.items():
            self.proxy.modify_system(system_id, k, v, self.token)

        self.proxy.save_system(system_id, self.token)

    def remove_system(self, system_name):
        self.proxy.remove_system(system_name, self.token)
