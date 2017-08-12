# PiController

sudo apt-get update && apt-get install nginx

sudo pip3 install -r requirements.txt

cp PiControl/.env.example PiControl/.env

sudo cp .meta/config/etc/nginx/sites-available/pi_controller /etc/nginx/sites-available/pi_controller

sudo ln -s /etc/nginx/sites-available/pi_controller /etc/nginx/sites-enabled/pi_controller

sudo cp .meta/config/etc/systemd/system/gunicorn.service /etc/systemd/system/gunicorn.service


sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default

sudo systemctl restart nginx

sudo systemctl start gunicorn

sudo systemctl enable gunicorn

crontab -e
*/2 * * * * bash /home/pi/scripts/PiController/.meta/scripts/cron.sh

after updating need to resart gunicorn

sudo systemctl restart gunicorn