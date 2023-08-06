import attr
from mako.template import Template

from .templates import vdsm


@attr.s
class KickStartVars:
    """"""
    liveimg = attr.ib()
    network = attr.ib()
    partition = attr.ib()
    lang = attr.ib(default="en_US.UTF-8")
    timezone = attr.ib(default="Asia/Shanghai")
    keyboard = attr.ib(default="--vckeymap=us --xlayouts='us'")
    rootpw = attr.ib(default="--plaintext redhat")
    auth = attr.ib(default="--enableshadow --passalgo=md5")
    services = attr.ib(default="--enabled=sshd")
    other = attr.ib(default="")


class KickStartFiles:
    """"""

    def __init__(self):
        pass

    @staticmethod
    def get_ks_tpl(ks_name: str):
        return getattr(vdsm, ks_name)

    def make_ks_file(self, ks_name, liveimg):
        ks_meta = self.get_ks_tpl(ks_name)
        ks_vars = KickStartVars(
            liveimg=liveimg,
            network=ks_meta.VARS.get("network"),
            partition=ks_meta.VARS.get("partition")
        )
        tpl = Template(ks_meta.CONTENT)

        with open(ks_meta.NAME, "w") as fp:
            fp.write(tpl.render(**ks_vars.__dict__))
