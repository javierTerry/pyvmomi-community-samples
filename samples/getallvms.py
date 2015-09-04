#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2013 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Python program for listing the vms on an ESX / vCenter host
"""

from __future__ import print_function
import atexit

from pyVim import connect
from pyVmomi import vmodl

import tools.cli as cli
import warnings
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings("ignore")


def print_vm_info(virtual_machine, depth=1):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(virtual_machine, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = virtual_machine.childEntity
        for c in vmList:
            print_vm_info(c, depth + 1)
        return


    try:
        summary = virtual_machine.summary
        vmdata = {}
        vmdata["name"] = summary.config.name
        vmdata["ipaddr"] = summary.guest.ipAddress
        vmdata["uuid"] = summary.config.instanceUuid
        vmdata["state"] = summary.runtime.powerState
        vmdata["host"] = summary.runtime.host.name
        vmdata["os"] = summary.guest.guestFullName
        print(vmdata)


    except AttributeError:
        pass



def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

    args = cli.get_args()

    try:
        service_instance = connect.SmartConnect(host=args.host,
                                                user=args.user,
                                                pwd=args.password,
                                                port=int(args.port))

        atexit.register(connect.Disconnect, service_instance)

        content = service_instance.RetrieveContent()
        children = content.rootFolder.childEntity
        for child in children:
            if hasattr(child, 'vmFolder'):
                datacenter = child
            else:
                # some other non-datacenter type object
                continue

            vm_folder = datacenter.vmFolder
            vm_list = vm_folder.childEntity
            for virtual_machine in vm_list:
                print_vm_info(virtual_machine, 10)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : ")
        return -1

    return 0

# Start program
if __name__ == "__main__":
    main()
