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

# Create a Request object to start building the RSpec.
pc = portal.Context()
request = pc.makeRequestRSpec()

RAM = [16, 32, 64]
CPU = [2, 4, 8, 12, 16, 32]
toolVersion = ['2023.1', '2023.2'] 
nodeName= ['fpga-build1', 'fpga-build2', 'build']

pc.defineParameter("RAM",  "RAM (GB)",
                   portal.ParameterType.INTEGER, RAM[0], RAM,
                   longDescription="RAM size")

pc.defineParameter("CPU",  "No: of VCPUs",
                   portal.ParameterType.INTEGER, CPU[0], CPU,
                   longDescription="No: of VCPUs")

pc.defineParameter("toolVersion", "Tool Version",
                   portal.ParameterType.STRING,
                   toolVersion[0], toolVersion,
                   longDescription="Select the tool version.")   

#pc.defineParameter("nodeName", "Physical host",
#                   portal.ParameterType.STRING,
#                   nodeName[0], nodeName,
#                   longDescription="Select the physical host.")  

pc.defineParameter("remoteDesktop", "Remote Desktop Access",
                   portal.ParameterType.BOOLEAN, False,
                   advanced=False,
                   longDescription="Enable remote desktop access by installing GNOME desktop and VNC server.")

params = pc.bindParameters() 
 
# Create a XenVM

exclusive=False
#phost = "urn:publicid:IDN+cloudlab.umass.edu+node+" + params.nodeName
node = request.XenVM('umass-vm',exclusive=False)
node.component_manager_id = "urn:publicid:IDN+cloudlab.umass.edu+authority+cm"
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
node.setFailureAction('nonfatal')
node.Desire("FPGA-Build-Pool", 1.0)

# Request a specific number of VCPUs.
node.cores = params.CPU

# Request a specific amount of memory (in MB).

node.ram = 1024 * params.RAM
#node.ram = 1024

# Set Storage
# node.disk = 100

#iface = node.addInterface()
#fsnode = request.RemoteBlockstore("fsnode", "/mydata")
#fsnode.dataset = "urn:publicid:IDN+emulab.net:octfpga+ltdataset+Xilinx"
# Now we add the link between the node and the special node
#fslink = request.Link("fslink")
#fslink.addInterface(iface)
#fslink.addInterface(fsnode.interface)
# Special attributes for this link that we must use.
#fslink.best_effort = True
#fslink.vlan_tagging = True

node.addService(pg.Execute(shell="bash", command="sudo /local/repository/post-boot.sh " + str(params.remoteDesktop) + " " + params.toolVersion + " >> /local/logs/output_log.txt"))  

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
