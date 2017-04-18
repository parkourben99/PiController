# PiController

cp PiControl/.env.example PiControl/.env

sudo cp .meta/config/etc/nginx/sites-available/pipool /etc/nginx/sites-enabled/pipool
sudo ln -s /etc/nginx/sites-available/pipool /etc/nginx/sites-enabled/pipool
sudo cp .meta/config/etc/systemd/system/gunicorn.service /etc/systemd/system/gunicorn.service

sudo nginx -t
sudo systemctl restart nginx

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

crontab -e
*/1 * * * * bash /home/pi/projects/PiController/.meta/scripts/cron.sh

sudo systemctl restart gunicorn