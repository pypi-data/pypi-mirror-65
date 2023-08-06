NAME = "atv_local-vlani_01.ks"

HOST = ("dell-per515-01",)

VARS = dict(
    network="--device=em2 --bootproto=dhcp",
    partition="""
ignoredisk --only-use=/dev/disk/by-id/scsi-360a9800050334c33424b41762d726954
zerombr
clearpart --all
bootloader --location=mbr
autopart --type=thinp
    """,
    other="",
)

CONTENT = """
#
# KS for vdsm vlan ifcfg test on dell-per515-01
#

lang ${lang}

timezone ${timezone}

keyboard ${keyboard}

### Kdump ###

### Security ###

rootpw ${rootpw}
auth ${auth}

services ${services}
selinux --enforcing


install

liveimg --url=${liveimg}
text
reboot


network ${network}


${partition}

${other}

### Pre deal ###


%%post --erroronfail

imgbase layout --init
%%end
"""
