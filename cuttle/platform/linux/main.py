import click
import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter
import os

def config_parse(config, username, pem, host):	
	if username != None:
		config['username'] = username
	if pem != None:
		config['pem'] = pem
	if host != None:
		config['host'] = host
	
	return config

@click.command()
@click.option('--username', type=str)
@click.option('--pem', type=str)
@click.option('--host', type=str)
def cli(username, pem, host):
	config = config_parse(cuttle_config, username, pem, host)
	output_file_path = os.path.join(output_path, 'main.py')
	
	k = paramiko.RSAKey.from_private_key_file(config['pem'])
	c = paramiko.SSHClient()
	
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	print("Connecting to EC2 instance.")
	c.connect(hostname=config['host'], username=config['username'], pkey=k)
	print("Connected to EC2 instance.")
	
	scp = SCPClient(c.get_transport())
	scp.put(output_file_path, 'main.py')
	
	commands = ['python3 main.py']
	
	for command in commands:
		print("Executing {}".format(command))
		stdin, stdout, stderr = c.exec_command(command)
		print(stdout.read())
		print("Errors")
		print(stderr.read())
	
	c.close()
	