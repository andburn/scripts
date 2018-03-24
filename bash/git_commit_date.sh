#!/bin/bash

if [ -z "$1" ]; then
	echo -e "\e[0;31mmessage required\e[0m"
	exit
elif [ "$1" = '-amend' ]; then
	amend=true
fi
message=$1

if [ -z "$2" ]; then
	echo -e "\e[0;31mdate required\e[0m"
	exit
fi
date=$2

if [ -z "$3" ]; then
	echo -e "\e[0;32musing random time\e[0m"
	
	# hours between 9-23
	hour=$(($RANDOM%14+9))

	mins=$(($RANDOM%60))
	secs=$(($RANDOM%60))

	time=$(printf "%02d:%02d:%02d" $hour $mins $secs)
else
	time="$3"
fi

# check locale for DST for given date
locale="Europe/Dublin"
datetime=$(date --date="TZ=\"$locale\" $date $time" +'%Y-%m-%d %H:%M:%S %z')

if [ "$amend" = true ]; then 
	GIT_COMMITTER_DATE="$datetime" git commit --date="$datetime" --amend --no-edit
else
	GIT_COMMITTER_DATE="$datetime" git commit --date="$datetime" -m "$message"
fi
