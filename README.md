# PiController

sudo ln -s /etc/nginx/sites-available/pipool /etc/nginx/sites-enabled/pipool

sudo nginx -t
sudo systemctl restart nginx

sudo systemctl start gunicorn
sudo systemctl enable gunicorn
