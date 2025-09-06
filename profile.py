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

# Function for creating VM guests with common parameters
def mkVM(pnode, name):
    node = request.XenVM(name)
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD";
    node.cores = 4
    node.ram = 16384
    node.exclusive = True
    #
    # This is the crux of the biscuit; tell the mapper exactly where to place the VM.
    #
    node.InstantiateOn(pnode)
    return node

# Create a Request object to start building the RSpec.
pc = portal.Context()
request = pc.makeRequestRSpec()

vitisVersion = ['2023.1'] 
xrtVersion = ['2023.1'] 


pc.defineParameter("vitisVersion", "Vitis Version",
                   portal.ParameterType.STRING,
                   vitisVersion[0], vitisVersion,
                   longDescription="Select the Vitis version.")   

pc.defineParameter("xrtVersion", "XRT Version",
                   portal.ParameterType.STRING,
                   xrtVersion[0], xrtVersion,
                   longDescription="Select the tool version.")   

pc.defineParameter("enableRemoteDesktop", "Remote Desktop Access",
                   portal.ParameterType.BOOLEAN, False,
                   advanced=False,
                   longDescription="Enable remote desktop access by installing GNOME desktop and VNC server.")

pc.defineParameter("docker",  "Install docker",
                    portal.ParameterType.BOOLEAN, False,
                    advanced=False,
                    longDescription="Check this box to install docker")

params = pc.bindParameters() 
 
#
# Set up your physical nodes as usual.
#
pnode1 = request.RawPC('pnode1')
pnode1.hardware_type = "build-flax0"

#
# Create the VMs, the first argument is which pnode to place the new VM on.
#
vm1 = mkVM("pnode1", "vm1");



#params_str = ','.join(['{}={}'.format(key, value) for key, value in params.items()])

#node.addService(pg.Execute(shell="bash", command="sudo /local/repository/post-boot.sh " + params_str + " >> /local/repository/output_log.txt"))  

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()


