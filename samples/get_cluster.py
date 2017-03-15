from pyVim import connect
from pyVmomi import vim

import tools.cli as cli
import ssl
import warnings
import humanize

MBFACTOR = float(1 << 20)
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
    content.rootFolder, [vim.ClusterComputeResource], True)
cluster = objview.view


for nodo  in cluster:
    for host in nodo.host:
        i = 0
        for vm in host.vm:
            i = i + vm.summary.config.memorySizeMB

        print i
        exit()
        summary = host.summary
        stats = summary.quickStats
        hardware = host.hardware
        cpuUsage = stats.overallCpuUsage
        memoryCapacity = hardware.memorySize
        memoryCapacityInMB = hardware.memorySize / MBFACTOR
        memoryUsage = stats.overallMemoryUsage
        freeMemoryPercentage = 100 - (
            (float(memoryUsage) / memoryCapacityInMB) * 100
        )
        print("--------------------------------------------------")
        print("Host name: ", host.name)
        # dump(host)
        print("Host CPU usage: ", cpuUsage)
        print("Host memory capacity: ", humanize.naturalsize(memoryCapacity,
                                                             binary=True))
        print("Host memory usage: ", memoryUsage / 1024, "GiB")
        print("Free memory percentage: " + str(freeMemoryPercentage) + "%")
        print("--------------------------------------------------")
        #print nodo.host.name
        print (host.summary.quickStats)
        exit()
    print (nodo.name)
    print (nodo.summary)
    exit() 


exit()
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
