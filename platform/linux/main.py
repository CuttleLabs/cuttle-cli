import click
import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter
import os


def config_parse(config, username, pem, host):
	if 'ec2' not in config['services'].keys():
		config['services'] = {
			'ec2': {}
		}
	
	if username != None:
		config['services']['ec2']['username'] = username
	
	if pem != None:
		config['services']['ec2']['pem'] = pem
	
	if host != None:
		config['services']['ec2']['host'] = host
	
	return config


@click.command()
@click.pass_obj
@click.option('--username', type=str)
@click.option('--pem', type=str)
@click.option('--host', type=str)
def cli(config, username, pem, host):
	config = config_parse(config, username, pem, host)
	
	print(config)
	
	with open(os.path.join(config['home_path'], config['notebook'])) as f:
		nb = nbformat.read(f, as_version=4)
	
	exporter = PythonExporter()
	
	(body, resources) = exporter.from_notebook_node(nb)
	
	f = open("test.py", "w")
	f.write(body)
	f.close()
	
	k = paramiko.RSAKey.from_private_key_file(config['services']['ec2']['pem'])
	c = paramiko.SSHClient()
	
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	print("Connecting to EC2 instance.")
	c.connect(hostname=config['services']['ec2']['host'], username=config['services']['ec2']['username'], pkey=k)
	print("Connected to EC2 instance.")
	
	scp = SCPClient(c.get_transport())
	scp.put('test.py', 'test.py')
	
	commands = ['python test.py']
	
	for command in commands:
		print("Executing {}".format(command))
		stdin, stdout, stderr = c.exec_command(command)
		print(stdout.read())
		print("Errors")
		print(stderr.read())
	
	c.close()
	