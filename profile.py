#!/usr/bin/python

"""
An example of how to specify exactly how VMs are mapped to physical nodes.
"""

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.emulab as emulab

# Function for creating VM guests with common parameters
def mkVM(pnode, name):
    node = request.XenVM(name)
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
    node.cores = 4
    node.ram = 4096
    node.exclusive = True
    #
    # This is the crux of the biscuit; tell the mapper exactly where to place the VM.
    #
    node.InstantiateOn(pnode)
    return node

request = portal.context.makeRequestRSpec()

#
# Set up your physical nodes as usual.
#
pnode1 = request.RawPC('pnode1')
pnode1.hardware_type = "build"

#
# Create the VMs, the first argument is which pnode to place the new VM on.
#
vm1 = mkVM("pnode1", "vm1");


portal.context.printRequestRSpec()
