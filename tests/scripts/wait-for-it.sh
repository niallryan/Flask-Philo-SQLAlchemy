#!/bin/bash
# wait-for-postgres.sh

set -e

export PGPASSWORD="dsps"

apk add --no-cache postgresql > /dev/null

until PGPASSWORD=$PGPASSWORD psql -h "postgresql" -U "ds" --dbname "ds" -c '\l' > /dev/null; do
  >&2 echo "waiting..."
  sleep 1
done

>&2 echo "Go!"

cd /philo
pip3 install -r tests/tools/requirements/requirements.txt > /dev/null
python3 setup.py install > /dev/null
