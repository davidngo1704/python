
cd /var/lib/ApiGateway/source_code/python

git pull

docker compose down --rmi all

docker compose up -d --build

bash clean.sh