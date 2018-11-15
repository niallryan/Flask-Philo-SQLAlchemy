import argparse
import subprocess
import os


def main():
    description = 'Run a command in docker'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--test', required=False, default='app')

    args, extra_params = parser.parse_known_args()

    test_cmd = 'bash -c "/philo/tests/scripts/wait-for-it.sh" && cd /philo/ && pytest -s -q tests/{}'.format( # noqa
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
