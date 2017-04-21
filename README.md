# PiController

cp PiControl/.env.example PiControl/.env

sudo cp .meta/config/etc/nginx/sites-available/pi_controller /etc/nginx/sites-enabled/pi_controller
sudo ln -s /etc/nginx/sites-available/pi_controller /etc/nginx/sites-enabled/pi_controller
sudo cp .meta/config/etc/systemd/system/gunicorn.service /etc/systemd/system/gunicorn.service

sudo systemctl restart nginx

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

crontab -e
*/1 * * * * bash /home/pi/projects/PiController/.meta/scripts/cron.sh

after updating need to resart gunicorn
sudo systemctl restart gunicorn