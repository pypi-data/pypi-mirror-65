import os
import docker
from .docker_util import docker_login, docker_pull_image, get_timestamp, save_stdout, save_stderr
from .java_repo_util import find_m2_location, find_gradle_location

def run_sast_scanner(params):
    client = docker_login(params['scan_info'])
    scanner = params['scanner']
    build_dir = params['build_dir']
    config = params['config']
    scan_info = params['scan_info']
    print('Launching scanner %s ' % scanner)

    output_file = build_dir + 'sken-'+scanner+'-output.json'

    docker_image = ''
    if scanner == 'brakeman':
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/brakeman:latest'
    elif scanner == 'nodejsscan': 
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/nodejsscan:latest'
    elif scanner == 'eslintsec': 
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/eslintsec:latest'
    elif scanner == 'tslintsec': 
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/tslintsec:latest'
    elif scanner == 'banditpy2':
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/bandit-python2:latest'
    elif scanner == 'banditpy3':
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/bandit-python3:latest'
        output_file = build_dir + 'sken-bandit3-output.json'
    elif scanner == 'findsecbugs':
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/findsecbugs:latest'
        output_file = build_dir + 'sken-secbugs-output.xml'
    elif scanner == 'gosec':
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/gosec:latest'
    elif scanner == 'phpcs':
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/phpcs:latest'
    elif scanner == 'gitleaks':
        docker_image = '621002179714.dkr.ecr.us-east-1.amazonaws.com/gitleaks:latest'

    print('Pulling latest image for %s ' % scanner)
    docker_pull_image(client, docker_image)
    print('Scanning started')
    scan_start = get_timestamp()

    if scanner == 'findsecbugs':
        # check and pass in the m2 location
        external_location = ''
        if 'MAVEN_REPO_PATH' in config['variables'] and config['variables']['MAVEN_REPO_PATH'] is not None:
            external_location = config['variables']['MAVEN_REPO_PATH']
        else:
            external_location = find_m2_location()

        if not external_location:
            # check and pass in the Gradle dependency cache location
            if 'GRADLE_CACHE_PATH' in config['variables'] and config['variables']['GRADLE_CACHE_PATH'] is not None:
                external_location = config['variables']['GRADLE_CACHE_PATH']
            else:
                external_location = find_gradle_location()

        if external_location:
            print('using external classes location: ' + external_location)
            container = client.containers.run(docker_image, '--externalCalss=1', volumes={
                build_dir: {
                    'bind': '/scan', 'mode': 'rw'},
                external_location: {
                    'bind': '/class', 'mode': 'rw'}
                }, detach=True, tty=False, stdout=True, stderr=True)
        else:
            container = client.containers.run(docker_image, '--externalCalss=0', volumes={build_dir: {
                                          'bind': '/scan', 'mode': 'rw'}}, detach=True, tty=False, stdout=True, stderr=True)
    elif scanner == 'nodejsscan':
        # check and pass in the excludePath
        exclude_path = ''
        if 'excludePath' in scan_info and scan_info['excludePath'] is not None:
            exclude_path = scan_info['excludePath']

        if exclude_path:
            print('exclude path: ' + exclude_path)
            container = client.containers.run(docker_image, '--excludePath=' + exclude_path, volumes={build_dir: {
                                          'bind': '/scan', 'mode': 'rw'}}, detach=True, tty=False, stdout=True, stderr=True)
        else:
            container = client.containers.run(docker_image, volumes={build_dir: {
                                          'bind': '/scan', 'mode': 'rw'}}, detach=True, tty=False, stdout=True, stderr=True)
    else:
        container = client.containers.run(docker_image, volumes={build_dir: {
                                          'bind': '/scan', 'mode': 'rw'}}, detach=True, tty=False, stdout=True, stderr=True)
    container.wait()

    # write stdout and stderr output
    save_stdout(scanner, container.logs(stdout=True, stderr=False).decode('UTF-8'))
    save_stderr(scanner, container.logs(stdout=False, stderr=True).decode('UTF-8'))

    scan_end = get_timestamp()
    if os.path.exists(output_file):
        print('Scanning completed. Output file: ' + output_file)
    else:
        print('Scanning completed')
    
    return output_file, scan_start, scan_end
