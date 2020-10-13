import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter

with open('test.ipynb') as f:
    nb = nbformat.read(f, as_version=4)
    exporter = PythonExporter()

    (body, resources) = exporter.from_notebook_node(nb)

    f = open("test.py", "w")
    f.write(body)
    f.close()

k = paramiko.RSAKey.from_private_key_file("./karishnu.pem")
c = paramiko.SSHClient()

c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("connecting")
c.connect(hostname = "35.154.44.251", username = "ubuntu", pkey = k)
print("connected")

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(c.get_transport())
scp.put('test.py', 'test.py')

commands = [ 'python test.py' ]

for command in commands:
	print ("Executing {}".format( command ))
	stdin , stdout, stderr = c.exec_command(command)
	print (stdout.read())
	print( "Errors")
	print (stderr.read())
c.close()