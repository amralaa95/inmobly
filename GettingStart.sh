
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo apt install docker.io

sudo service docker start

sudo docker-compose build

sudo docker-compose run web python manage.py makemigrations

sudo docker-compose run web python manage.py migrate

sudo docker-compose up