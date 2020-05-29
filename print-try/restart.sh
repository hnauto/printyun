#!/bin/sh

while true

do

	ps -ef | grep "connect.py" | grep -v "grep"

	if [ "$?" -eq 1 ]

	then

		python3 connect.py

		echo "process has been restarted!"

	else

		echo "process already started!"

	fi

	sleep 10

done
