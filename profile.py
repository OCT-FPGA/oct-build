"""This profile is used to instantiate a build VM in OCT. DO NOT USE 

Instructions:
Wait for the profile instance to start, and then log in to the VM via the
ssh port specified below.  (Note that in this case, you will need to access
the VM through a high port on the physical host, since we have not requested
a public IP address for the VM itself.)
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab

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

# Create a Request object to start building the RSpec.
pc = portal.Context()
request = pc.makeRequestRSpec()

RAM = [16, 32, 64, 96]
CPU = [2, 4, 8, 12]
toolVersion = ['2023.1', '2023.2'] 
nodeName= ['fpga-build1', 'fpga-build2', 'build']

pc.defineParameter("RAM",  "RAM size (GB)",
                   portal.ParameterType.INTEGER, RAM[0], RAM,
                   longDescription="RAM size")

pc.defineParameter("CPU",  "No: of VCPUs",
                   portal.ParameterType.INTEGER, CPU[0], CPU,
                   longDescription="No: of VCPUs")

pc.defineParameter("toolVersion", "Tool Version",
                   portal.ParameterType.STRING,
                   toolVersion[0], toolVersion,
                   longDescription="Select the tool version.")   

pc.defineParameter("nodeName", "Physical host",
                   portal.ParameterType.STRING,
                   nodeName[0], nodeName,
                   longDescription="Select the physical host.")  

pc.defineParameter("enableRemoteDesktop", "Remote Desktop Access",
                   portal.ParameterType.BOOLEAN, False,
                   advanced=False,
                   longDescription="Enable remote desktop access by installing GNOME desktop and VNC server.")

params = pc.bindParameters() 
 
# Create a XenVM

# Set up your physical nodes as usual.
#
pnode1 = request.RawPC('pnode1')
pnode1.hardware_type = "build-flax0"

#
# Create the VMs, the first argument is which pnode to place the new VM on.
#
vm1 = mkVM("pnode1", "vm1");

#node.addService(pg.Execute(shell="bash", command="sudo /local/repository/post-boot.sh " + str(params.enableRemoteDesktop) + " " + params.toolVersion + " >> /local/repository/output_log.txt"))  

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()


