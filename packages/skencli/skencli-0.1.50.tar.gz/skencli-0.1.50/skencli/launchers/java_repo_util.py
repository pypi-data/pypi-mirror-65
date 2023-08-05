import os
import sys
import subprocess
import platform
from xml.dom.minidom import parse

def get_m2_from_settings(settings_file):
	try:
		dom = parse(settings_file)
		root = dom.documentElement
		node_list = root.getElementsByTagName('localRepository')

		if node_list.length > 0:
			if node_list[0].childNodes.length > 0:
				return node_list[0].childNodes[0].data
	except Exception as e:
		return ''

def get_maven_home():
	command = ['mvn', '--version']
	if sys.version_info < (3, 0) or platform.system() == 'Linux':
		command = ['mvn --version']

	p = subprocess.Popen(command, stdout=subprocess.PIPE,
	                     stderr=subprocess.STDOUT, shell=True)

	maven_home = ''
	for line in iter(p.stdout.readline, b''):
		line = line.rstrip().decode('utf8')
		try:
			if line.index('Maven home') == 0:
				maven_home = line.split(': ')[1]
		except ValueError:
			continue
	p.stdout.close()
	p.wait()

	return maven_home

def find_m2_location():
	# check if ${user.home}/.m2/settings.xml exists
	m2_location = ''
	user_home = os.path.expanduser('~')
	if not user_home.endswith(os.path.sep):
		user_home = user_home + os.path.sep

	if os.path.exists(user_home + '.m2/settings.xml'):
		m2_location = get_m2_from_settings(user_home + '.m2/settings.xml')

	if m2_location:
		#print('found m2 location from user settings: ' + m2_location)
		return m2_location

	# find maven home
	maven_home = get_maven_home()
	# check ${maven.home}/conf/settings.xml exists
	if maven_home:
		if not maven_home.endswith(os.path.sep):
			maven_home = maven_home + os.path.sep
		if os.path.exists(maven_home + 'conf/settings.xml'):
			m2_location = get_m2_from_settings(maven_home + 'conf/settings.xml')

			if m2_location:
				#print('found m2 location from global settings: ' + m2_location)
				return m2_location
			else:
				# use default location
				return user_home + '.m2'

	return ''

def find_gradle_location():
	# detect gradle user home
	user_home = os.path.expanduser('~')
	if not user_home.endswith(os.path.sep):
		user_home = user_home + os.path.sep

	gradle_user_home = user_home + '.gradle' + os.path.sep

	if 'GRADLE_USER_HOME' in os.environ and os.environ['GRADLE_USER_HOME'] is not None:
		gradle_user_home = os.environ['GRADLE_USER_HOME']
		if not gradle_user_home.endswith(os.path.sep):
			gradle_user_home = gradle_user_home + os.path.sep

	cache_location = gradle_user_home + 'caches' + os.path.sep + 'modules-2' + os.path.sep + 'files-2.1' + os.path.sep

	if os.path.exists(cache_location):
		return cache_location

	return ''
