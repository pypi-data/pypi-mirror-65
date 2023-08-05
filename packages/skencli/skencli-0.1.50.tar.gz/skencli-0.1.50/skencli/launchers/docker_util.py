import docker
import boto3
import base64
import subprocess
from datetime import datetime
import time
import sys
import os
import json
import shutil

sken_output_foler = ''
linguist_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/linguist:latest'

def docker_login(scan_info):
    print('Login to docker')
    session = boto3.Session(
        aws_access_key_id=scan_info['awsAccessKeyId'], 
        aws_secret_access_key=scan_info['awsSecretAccessKey'], 
        region_name=scan_info['awsRegion'])

    ecr_client = session.client('ecr')
    token = ecr_client.get_authorization_token()
    ecr_username, ecr_password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    registry = token['authorizationData'][0]['proxyEndpoint']
    
    command = ['docker', 'login', '-u', ecr_username, '--password-stdin', registry]
    if sys.version_info < (3, 0):
        command = ['docker login -u ' + ecr_username + ' --password-stdin ' + registry]

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    p.communicate(input=ecr_password.encode('utf-8'))
    p.wait()
    client = docker.from_env()
    print('Login to docker succeeded.')

    return client

def docker_pull_image(docker_client, image):
    command = ['docker', 'image', 'pull', image]
    if sys.version_info < (3, 0):
        command = ['docker image pull ' + image]
        
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in iter(p.stdout.readline, b''):
        line = line.rstrip().decode('utf8')
        print(line)
    p.stdout.close()
    p.wait()
    
    #docker_client.images.pull(image)

def get_timestamp():
    now = datetime.now()
    try:
        return round(now.timestamp())
    except Exception as e:
        return int(round(time.mktime(now.timetuple())))

def get_formated_timestamp():
    now = get_timestamp()
    return datetime.strftime(datetime.utcfromtimestamp(now),'%Y%m%d%H%M%S')

def create_skenoutput_folder(dir):
    global sken_output_foler
    sken_output_foler = dir

    if not os.path.exists(dir):
        os.makedirs(dir)
        os.chmod(dir, 0o777)

def delete_skenoutput_folder():
    shutil.rmtree(sken_output_foler)

def save_stdout(scanner, content):
    if not content:
        return
    if sys.version_info < (3, 0):
        content = content.encode('utf-8')

    with open(sken_output_foler + os.path.sep + scanner + '-stdout.txt', 'w') as f:
        f.write(content)

def save_stderr(scanner, content):
    if not content:
        return
    if sys.version_info < (3, 0):
        content = content.encode('utf-8')

    with open(sken_output_foler + os.path.sep + scanner + '-stderr.txt', 'w') as f:
        f.write(content)

def detect_lang(scan_info, build_dir, support_languages):
    client = docker_login(scan_info)
    docker_pull_image(client, linguist_image)
    container = client.containers.run(linguist_image, volumes={build_dir: {
        'bind': '/scan', 'mode': 'rw'}}, detach=True, tty=False, stdout=True, stderr=True)
    container.wait()
    print(container.logs().decode('UTF-8'))

    lang_file = build_dir + 'sken-lang.json'
    if not os.path.exists(lang_file):
        return ''

    languages = []
    with open(lang_file, 'r') as f:
        data = json.load(f)
        detected_languages = data['languages']
        for language in detected_languages:
            if language.lower() in support_languages:
                languages.append(language.lower())
        
        print('Detected languages: ' + ', '.join(languages))

    if os.path.exists(lang_file):
        os.remove(lang_file)

    return ','.join(languages)


