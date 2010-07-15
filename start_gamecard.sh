/usr/local/bin/mysqld_safe &
/usr/local/memcached/bin/memcached -d -m 256 -l 127.0.0.1 -p 11211 -u www &
/usr/local/memcached/bin/memcached -d -m 16 -l 127.0.0.1 -p 11212 -u www &
/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf 
/usr/local/mongodb/bin/mongod --repair --dbpath='/zzdata/mongodb/' && /usr/local/mongodb/bin/mongod --dbpath='/zzdata/mongodb/' --master &
/usr/local/mongodb/bin/mongod --repair --dbpath='/data/mongodb_bak/' && /usr/local/mongodb/bin/mongod --dbpath='/data/mongodb_bak/' --slave --source localhost --slavedelay 15 --port 27018 &
/usr/local/apache22/bin/apachectl restart
cd /zzdata/gamecard/ && /usr/bin/python manage.py runserver ka.178.com:8088 &
cd /data/gamecard/ && /usr/bin/python manage.py runserver ka.178.com:7077 &
