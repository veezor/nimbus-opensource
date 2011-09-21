#!/bin/bash

function makedir(){
  mkdir -p $1 2>> /dev/null;
}


source initenv.sh;

find . -iname "*.pyc" -exec rm {} \;

makedir "deb/usr/bin"
makedir "deb/var"
makedir "deb/etc/init.d"
makedir "deb/etc/nimbus"
makedir "deb/etc/cron.hourly"
makedir "deb/etc/nginx/sites-enabled"
makedir "deb/var/log/nimbus"
makedir "deb/var/nimbus/deps"
makedir "deb/var/nimbus/custom"


find deb -iname "*~" -exec rm {} \;


cd nimbus
cp settings_executable.py settings.py;
python manage.py makeenviron ../deb;
python setup.py build_exe ;
chmod +x binary/nimbus;
cp -a binary ../deb/var/www;
cd ..;


cd webservices/manager;
python setup.py build_exe;
cp -a binary ../../deb/var/nimbusmanager;
cd ../..;

cp -a apps/unix/client/usr/sbin/nimbusclientservice deb/usr/bin
cp -a apps/unix/client/etc/init.d/nimbusclient deb/etc/init.d
cp nimbus/confs/nginx-nimbus.site deb/etc/nginx/sites-enabled/default
cp nimbus/confs/nimbus.cron deb/etc/cron.hourly/nimbus
cp nimbus/confs/logging.conf deb/etc/nimbus/
cp nimbus/confs/reload_manager_logging.conf deb/etc/nimbus/
cp nimbus/confs/nimbus.initd deb/etc/init.d/nimbus
cp webservices/manager/nimbus_manager.conf deb/etc/nimbus
cp webservices/manager/nimbus_manager_log.conf deb/etc/nimbus
cp libs/keymanager/conf/ssl.conf deb/etc/nimbus
cp webservices/manager/init.d/nimbusmanager deb/etc/init.d
cp LICENSE deb/var/www/
cp third_part_software.txt deb/var/www
cp -a doc deb/var/www
cp README deb/var/www
cp version deb/var/www/media/
 
VERSION=`cat version`
dpkg-deb -b deb nimbus-$VERSION.deb

rm -rf deb/var/www
rm -rf deb/etc
rm -rf deb/var/nimbus/custom
rm -rf deb/var/nimbusmanager/
