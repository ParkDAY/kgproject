#!/bin/bash
#
sudo cat  << EOF | sudo tee /etc/nginx/conf.d/tomcat.conf
upstream tomcat {
  ip_hash;
  server 192.168.1.22:8080;
  server 192.168.1.23:8080;
}
server {
        listen 80;
		listen  [::]:80;
        server_name 192.168.1.30;

        root /var/www/html;

        location / {
                proxy_set_header Host \$http_host;
                proxy_set_header X-Real-IP \$remote_addr;
                proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

                proxy_pass http://tomcat;
                proxy_redirect off;
                charset utf-8;
        }
}
EOF

sudo systemctl restart nginx