#!/bin/bash
#

sudo apt-get update -y
sudo apt-get install -y openjdk-17-jdk
sudo apt-get install -y tomcat9

sudo cat  << EOF | sudo tee >> /etc/profile
export CATALINA_HOME=/usr/share/tomcat9
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
export PATH=$PATH:/usr/lib/jvm/java-17-openjdk-amd64/bin:/usr/share/tomcat9/bin
EOF

sudo source /etc/profile

sudo cp -rf /vagrant/post/* /var/lib/tomcat9/webapps/ROOT/
sudo cp -rf /vagrant/*.war /var/lib/tomcat9/webapps
sudo mkdir /var/lib/tomcat9/webapps/images
sudo cp -rf /vagrant/post/*.jpg /var/lib/tomcat9/webapps/images/
sudo cp -rf /vagrant/server.xml /var/lib/tomcat9/conf/

sudo wget https://downloads.mysql.com/archives/get/p/3/file/mysql-connector-java_8.0.29-1ubuntu20.04_all.deb
sudo dpkg -x mysql-connector-java_8.0.29-1ubuntu20.04_all.deb ./temp
sudo mv ./temp/usr/share/java/mysql-connector-java-8.0.29.jar /var/lib/tomcat9/lib

sed 's/#JAVA_HOME=\/usr\/lib\/jvm\/java-8-openjdk/JAVA_HOME=\/usr\/lib\/jvm\/java-17-openjdk-amd64/' /etc/default/tomcat9 > tomcat9
sudo mv tomcat9 /etc/default/tomcat9

sudo systemctl restart tomcat9
sudo systemctl enable tomcat9
