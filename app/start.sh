#!/bin/sh
#
# Deep Learning Studio - GUI platform for designing Deep Learning AI without programming
#
# Copyright (C) 2016-2017 Deep Cognition Labs, Skiva Technologies Inc.
#
# All rights reserved.
#

export PYTHONHOME=/conda3
OLDPATH=$PATH
export PATH=/usr/bin:/conda3:/conda3/Scripts:/php:$PATH
PARENT=$PPID

sigterm()
{
	echo "Deep Learning studio is terminating"
	for process in `ps|tr -s " "|cut -d' ' -f 2`; do kill $process; done
}

sigint()
{
	for process in `ps|tr -s " "|cut -d' ' -f 2`; 
		do 
			if [ "$process" != "$PPID" ]; then
				kill $process; 
			fi
		done
}
trap 'sigquit' QUIT TERM 
trap 'sigint' INT

if [ "$1" == "stop" ]; then
	echo Stopping deep learning studio
	kill -KILL -`cat /dls.pid`
	rm /dls.pid
	sigint
	exit 0
fi

echo $$ >/dls.pid
/conda3/Scripts/redis-server 1>/dev/null &
cp -r /etc/nginx/* /nginx/conf/
cp /etc/php.ini /php/
sed -i -e "s|listen 8880|listen $WEBAPP_PORT|" /nginx/conf/sites-available/default
sed -i -e "s|listen 8881|listen $COMPUTE_PORT|" /nginx/conf/sites-available/default
sed -i -e "s|listen 8888|listen $FILEBROWSER_PORT|" /nginx/conf/sites-enabled/filebrowser
sed -i -e "s|../files/'.*|../../../data/1',|g" /nginx/html/php/connector.minimal.php
#sed  -i -e "s|location /data/.*|location /data/ { internal; alias '$DLS_DATA_DIR'; }|" /nginx/conf/sites-available/default
/php/php-cgi.exe -b 127.0.0.1:5001 &
cd /nginx && /nginx/nginx &

if [ ! -d "/data/public/datasets/" ]; then
	mkdir -p /data/public/datasets/
fi

if [ ! -d "/data/1/" ]; then
	mkdir -p /data/1/datasets
	mkdir -p /data/1/project
	mkdir -p /data/1/notebook
fi

if [ ! -d "/home/app/database/" ]; then
	mkdir -p /home/app/database
fi


export PYTHONPATH=/
export HOME=/home/app
mkdir -p /home/app/.keras
cp /etc/keras.json /home/app/.keras
export GPU_ENABLED=0
echo; echo "Checking GPU support..."
python -u /home/app/gpucheck.py	> gpucheck.log 2>&1
if [ $? -eq 0 ]; then
	if [ ! -d "/mxnet-cpu" ]; then
		mv /conda3/Lib/site-packages/mxnet /mxnet-cpu
	fi
	cp -r /mxnet /conda3/Lib/site-packages/
	export GPU_ENABLED=1
	echo "GPU supported"
else
	if [  -d "/mxnet-cpu" ]; then
		cp -r /mxnet-cpu/* /conda3/Lib/site-packages/mxnet/
	fi
	echo "GPU not supported"
fi

if [ ! -f /data/1/.conda/cudnn64_7.dll ]; then
	cp /mxnet/cudnn64_7.dll /data/1/.conda/
fi

export PYTHONPATH=/home/app

#download datasets in background
for script in `ls /datasets_scripts/*.py`
	do
		cd /data/public/datasets/ && python -u $script 
	done
cd /home/app

if [ ! -f /home/app/database/db.sqlite3 ]; then
	./manage.py makemigrations --noinput &&  ./manage.py migrate --noinput 
	# use following command to update initialdb if needed. 
	#./manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude explorer --exclude admin.logentry --exclude sessions --indent 2 > initialdb.json
	echo "loading initial db"
	./manage.py loaddata initialdb.json
else
	./manage.py makemigrations --noinput &&  ./manage.py migrate --noinput
fi

python -u server.py &

if [ ! -d "/data/1/deploy" ]; then
	mkdir -p /data/1/deploy
fi
export DEPLOY_DIR=/data/1/deploy
if [ ! -f "/conda3/Scripts/olympus.exe" ]; then
	cd /home/olympus && python setup.py install  > olympus.log 2>&1
	cd /home/app
fi

olympus up --no-debug --port 6666 --host 127.0.0.1 &

if [ -f app.so ]; then
	./app.so &
else
  python -u app.py  &
fi

#cp -r /home/app/jupyter ~/
cat << EOF >>~/jupyter/jupyter_notebook_config.py
c.NotebookApp.token = 'deepcognition'
EOF
sed -i -e "s|#c.NotebookApp.port = 8888|c.NotebookApp.port =  $JUPYTER_PORT|" ~/jupyter/jupyter_notebook_config.py
sed -i -e "s|c.NotebookApp.ip = '0.0.0.0'|c.NotebookApp.ip = '127.0.0.1'|" ~/jupyter/jupyter_notebook_config.py

if [ ! -d "/data/temp" ]; then
	mkdir -p /data/temp
fi
echo -n deepcognition > /home/theia/.token
cd /data/1 && jupyter-notebook --config=~/jupyter/jupyter_notebook_config.py --no-browser --allow-root &
rm -rf /data/public/dlenvs
cp -r /dlenvs /data/public/
export THEIA_SHELL=
node /home/theia/fix_symlink.js
export PYTHONEHOME=/data/1/.conda
export PATH=/usr/bin:$PYTHONEHOME:$PYTHONEHOME/Scripts:/conda3/:$OLDPATH
cd /home/theia/examples/browser && ./node_modules/.bin/theia start --hostname 0.0.0.0 --port $THEIA_PORT --root-dir=/data/1/

sigterm()
