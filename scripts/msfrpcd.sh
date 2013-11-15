#!/bin/bash
# Msfrpc startup script, By Galkan

msfrpcd="/usr/bin/msfrpcd"

if [ ! -f $msfrpcd ] 
then 
	echo "$msfrpcd doesn't exists !!!"
	exit 1 
fi 

function start()
{
	echo "$(tput bold)$(tput setaf 4)MsfRpcd: $(tput bold)$(tput setaf 2) Starting"
	$msfrpcd -a 127.0.0.1 -U msf -P msf -p 55552 -S >/dev/null 2&>1
        while [ 1 ]
        do
                is_start="`netstat -nlput | grep 55552 | grep -v grep`"

                if [ -z "$is_start" ]
                then   
                        echo -n "."
                        sleep 0.5
                else   
                        break
                fi
        done

        echo ""
        echo "$(tput bold)$(tput setaf 4)MsfRpcd: $(tput bold)$(tput setaf 2) Started"
}
 
function status()
{
	proc="`netstat -nlput | grep 55552 | grep -v grep`"
        if [ -z "$proc" ]
        then   
                echo "$(tput bold)$(tput setaf 4)MsfRpcd: $(tput bold)$(tput setaf 2)Stopped"
        else
                echo "$(tput bold)$(tput setaf 4)MsfRpcd: $(tput bold)$(tput setaf 2)Running"
        fi
}

function stop()
{
	msfrpc_pid="`pidof $msfrpcd`"
	if [ ! -z $msfrpc_pid ]
	then
        	kill -9 $msfrpc_pid
	fi

        echo "$(tput bold)$(tput setaf 4)MsfRpcd: $(tput bold)$(tput setaf 2) Stopped"
}

case "$1" in 
'start') 
	start
;; 
'status')
	status
;;
'stop') 
	stop
;;
'restart')
	stop
	sleep 1
	start
;; 
*) 
echo "Usage: $0 { start | stop | restart}" 
exit 1 
;; 
esac 
exit 0 
# 
