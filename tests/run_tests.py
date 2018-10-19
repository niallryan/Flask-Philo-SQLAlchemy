import argparse
import subprocess
import os


def main():
    description = 'Run a command in docker'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--test', required=False, default='app')

    args, extra_params = parser.parse_known_args()

    test_cmd = 'pytest -s -q /philo/tests/{}'.format(
        args.test)

    #test_cmd ='python'
    cmd = [
        'docker-compose',
        'run',
        '--rm',
        '--volume={}/../:/philo'.format(os.getcwd()),
        'python',
        'sh',
        '-c',
        test_cmd
    ]


    try:
        subprocess.call(cmd)

    except Exception:
        subprocess.run(cmd)


if __name__ == '__main__':
    main()
