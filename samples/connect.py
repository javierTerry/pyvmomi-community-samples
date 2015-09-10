from pyVim import connect
from pyVmomi import vim

import ssl
import tools.cli as cli


ssl._create_default_https_context = ssl._create_unverified_context
args = cli.get_args()

service_instance = connect.SmartConnect(host=args.host,
                                        user=args.user,pwd=args.password,
                                        port=args.port)


content = service_instance.RetrieveContent()
obj_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.ClusterComputeResource], True)
clusters = obj_view.view

list_clusters = [ cluster.name for cluster in clusters]

print("")
print("Connected to {0} as {1}".format(args.host, args.user))
print("Clusters available here are {0}".format(list_clusters))
