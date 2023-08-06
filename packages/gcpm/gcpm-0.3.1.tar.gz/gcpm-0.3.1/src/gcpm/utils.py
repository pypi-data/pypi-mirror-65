# -*- coding: utf-8 -*-

"""
    Module to provide utilities
"""


def expand(path):
    import os
    return os.path.expandvars(os.path.expanduser(path))


def proc(cmd):
    import sys
    import shlex
    import subprocess
    if type(cmd) != list:
        cmd = shlex.split(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if sys.version_info.major > 2:
        stdout = stdout.decode()
        stderr = stderr.decode()
    return (p.returncode, stdout, stderr)


def make_startup_script_swap(swap):
    content = """#!/usr/bin/env bash
dd if=/dev/zero of=/swapfile bs=1M count={swap}
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo /swapfile swap swap defaults 0 0 >>/etc/fstab
""".format(swap=swap)
    return content


def make_startup_script(core, mem, swap, disk, image, preemptible, admin,
                        head, port, domain, owner, bucket, off_timer=0,
                        wn_type="", startup_cmd=""):
    if wn_type == "test_wn":
        start = "IsPrimaryJob =!= True"
    else:
        start = "SlotID == 1"
    content = """#!/usr/bin/env bash
echo "{{\\"date\\": $(date +%s), \\"core\\": {core}, \\"mem\\": {mem}, \
\\"swap\\": {swap}, \\"disk\\": {disk}, \\"image\\": \\"{image}\\", \
\\"preemptible\\": {preemptible} \
}}" >/var/log/nodeinfo.log
date +%s > /root/start_date

{startup_cmd}

dd if=/dev/zero of=/swapfile bs=1M count={swap}
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo /swapfile swap swap defaults 0 0 >>/etc/fstab

sed -i"" 's/FIXME_ADMIN/{admin}/' /etc/condor/config.d/00_config_local.config

sed -i"" 's/FIXME_HOST/{head}/' /etc/condor/config.d/10_security.config
sed -i"" 's/FIXME_PORT/{port}/' /etc/condor/config.d/10_security.config
sed -i"" 's/FIXME_DOMAIN/{domain}/' /etc/condor/config.d/10_security.config
sed -i"" "s/FIXME_PRIVATE_DOMAIN/$(hostname -d)/" \
/etc/condor/config.d/10_security.config

sed -i"" 's/FIXME_OWNER/{owner}/' /etc/condor/config.d/20_workernode.config
sed -i"" 's/FIXME_CORE/{core}/' /etc/condor/config.d/20_workernode.config
sed -i"" 's/FIXME_MEM/{mem}/' /etc/condor/config.d/20_workernode.config

sed -i"" 's/FIXME_START/{start}/' /etc/condor/config.d/20_workernode.config

gsutil cp "gs://{bucket}/pool_password" /etc/condor/
chmod 600 /etc/condor/pool_password
systemctl enable condor
systemctl start condor
while :;do
  condor_reconfig
  status="$(condor_status | grep "${{HOSTNAME}}")"
  if [ -n "$status" ];then
    break
  fi
  sleep 10
done
date >> /root/condor_started""".format(core=core, mem=mem, swap=swap,
                                       disk=disk, image=image,
                                       preemptible=preemptible, admin=admin,
                                       head=head, port=port, domain=domain,
                                       owner=owner, bucket=bucket, start=start,
                                       startup_cmd=startup_cmd)

    if off_timer != 0:
        content += """
sleep {off_timer}
condor_off -peaceful -startd
date >> /root/condor_off""".format(off_timer=off_timer)
    return content


def make_shutdown_script(core, mem, swap, disk, image, preemptible,
                         shutdown_cmd):
    content = """#!/usr/bin/env bash
unset http_proxy

${shutdown_cmd}

preempted=$(\
curl "http://metadata.google.internal/computeMetadata/v1/instance/preempted" \
-H "Metadata-Flavor: Google")
if echo "$preemptible"|grep -q error;then
  preemptible="-"
fi
echo "{{\\"date\\": $(date +%s), \\"core\\": {core}, \\"mem\\": {mem}, \
\\"swap\\": {swap}, \\"disk\\": {disk}, \\"image\\": \\"{image}\\", \
\\"preemptible\\": {preemptible}, \\"preempted\\": \\"${{preempted}}\\", \
\\"uptime\\": $(cut -d "." -f1 /proc/uptime) \
}}" >>/var/log/shutdown.log""".format(core=core, mem=mem, swap=swap,
                                      disk=disk, image=image,
                                      preemptible=preemptible,
                                      shutdown_cmd=shutdown_cmd)
    return content
