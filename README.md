# PiController

sudo cp .meta/config/etc/nginx/sites-available/pipool /etc/nginx/sites-enabled/pipool
sudo ln -s /etc/nginx/sites-available/pipool /etc/nginx/sites-enabled/pipool
sudo cp .meta/config/etc/systemd/system/gunicorn.service /etc/systemd/system/gunicorn.service

sudo nginx -t
sudo systemctl restart nginx

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

Cron
*/1 * * * * bash /home/pi/projects/PiController/.meta/scripts/cron.sh