import argparse
import subprocess
import os


def main():
    description = 'Run a command in docker'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--test', required=False, default='app')

    args, extra_params = parser.parse_known_args()

    test_cmd = 'cd /philo && pip3 install -r tests/tools/requirements/requirements.txt > /dev/null && python3 setup.py install > /dev/null && pytest -s -q tests/{}'.format( # noqa
        args.test)

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
    except subprocess.CalledProcessError:
        subprocess.run(cmd)
    else:
        print("Done")


if __name__ == '__main__':
    main()
