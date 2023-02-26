"""An example of constructing a profile with a single Xen VM.

Instructions:
Wait for the profile instance to start, and then log in to the VM via the
ssh port specified below.  (Note that in this case, you will need to access
the VM through a high port on the physical host, since we have not requested
a public IP address for the VM itself.)
"""

import geni.portal as portal
import geni.rspec.pg as pg

# Create a Request object to start building the RSpec.
pc = portal.Context()
request = pc.makeRequestRSpec()

# Pick your image.
    
toolVersion = [#('2022.1'),
               ('2021.1'), 
               ('2020.2.1'), 
               ('2020.2'), 
               ('2020.1.1'),
               ('2020.1'),
               ('Do not install tools')] 
    
pc.defineParameter("toolVersion", "Tool Version",
                   portal.ParameterType.STRING,
                   toolVersion[0], toolVersion,
                   longDescription="Select a tool version. It is recommended to use the latest version for the deployment workflow. For more information, visit https://www.xilinx.com/products/boards-and-kits/alveo/u280.html#gettingStarted")   


params = pc.bindParameters() 
 
# Create a XenVM
node = request.XenVM("build-vm")
node.xen_ptype = "build-vm"

# Request a specific number of VCPUs.
node.cores = 8

# Request a specific amount of memory (in MB).
node.ram = 65536

# Set Storage
node.disk = 100

if params.toolVersion != "Do not install tools":
  node.addService(pg.Execute(shell="bash", command="sudo /local/repository/post-boot.sh " + params.toolVersion + " >> /local/repository/output_log.txt"))
pass 
   

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
