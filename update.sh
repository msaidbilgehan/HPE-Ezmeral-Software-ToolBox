sudo docker compose down

sudo docker rmi $(sudo docker images -a -q) -f

git reset --hard origin/master
git pull origin master

sudo docker compose up -d