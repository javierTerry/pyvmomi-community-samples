from pyVim import connect
from pyVmomi import vim

import tools.cli as cli
import ssl
import warnings

# Monkey patch :)

warnings.filterwarnings("ignore")

ssl._create_default_https_context = ssl._create_unverified_context

# Get arguments

args = cli.get_args()

# Connect to ESXi/vCenter

service_instance = connect.SmartConnect(host=args.host,
                                        user=args.user,
                                        pwd=args.password,
                                        port=int(args.port))

# Retrieve content

content = service_instance.RetrieveContent()
objview = content.viewManager.CreateContainerView(
    content.rootFolder, [vim.HostSystem], True)
esxi_hosts = objview.view

# Bunch of list comprehensions

hostState = [esxi_host.runtime.powerState for esxi_host in esxi_hosts]
hostName = [esxi_host.name for esxi_host in esxi_hosts]
hostStatus = [esxi_host.overallStatus for esxi_host in esxi_hosts]
hostIp = [esxi_host.summary.managementServerIp for esxi_host in esxi_hosts]

# Nested list comprehension

hostVms = [[(host.name) for host in eh.vm] for eh in esxi_hosts]
hostVmsIps = [[(host.guest.ipAddress) for host in eh.vm] for eh in esxi_hosts]
hostVmsState = [[(host.runtime.powerState) for host in eh.vm]
                for eh in esxi_hosts]

# Equivalence in for
"""
for eh in esxi_hosts:
    for host in eh.vm:
        print(host.name)
"""
# Finally

z = list(zip(hostName, hostState, hostStatus, hostIp, hostVms, hostVmsIps,
             hostVmsState))
print(z)
