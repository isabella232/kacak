#!/bin/bash

function is_user_logged_in()
{
	full_user_name="$1"
	user_file="$2"

	echo -n "$full_user_name" | grep -qE ".*\\$"
	if [ $? -eq 0 ]
	then	
		echo 1	
	else
		logged_user="`echo -n "$full_user_name" | sed 's/\\\/\\\\\\\\\\\/g'`"
		
		cat $user_file | grep -iqE "^$logged_user"
		if [ $? -eq 0 ]
		then
			echo 0
		else
			echo 1
		fi

		rm -rf $control_file
	fi			
}


function main()
{
	rhosts="$1"
	user_file="$2"
	smbdomain="$3"
	smbpass="$4"
	smbuser="$5"
	threads="$6"

	output_file="`mktemp /tmp/$USER.XXXXXX`"

	$msfcli auxiliary/scanner/smb/smb_enumusers_domain RHOSTS=file:$rhosts SMBDomain=$smbdomain SMBPass=$smbpass  SMBUser=$smbuser THREADS=$threads E >$output_file 2>$output_file

	cat -e "$output_file" | sed -e "s/\^@//g" | grep -aE "\[\*\][^ ]+ [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" | cut -d " " -f2,4- | while read -r line
	do
		ip_addr="`echo "$line" | cut -d " " -f1`"
		user_infos="`echo "$line" | cut -d " " -f2-`"
		
		cat $user_file | while read -r user
		do
			for tmp_user in $user_infos
			do
				logged_user="`echo -n $tmp_user | tr -d ","`"	

				ret_val="`is_user_logged_in "$logged_user" "$user_file"`"
				if [ "$ret_val" -eq 0 ]
				then
					echo "$ip_addr -> $logged_user"
				fi
			done	
		done
	done | sort -n | uniq

	rm -rf $output_file
}

##
### Main ... go go go 
##

if [ ! $# -eq 6 ]
then
	echo "Usage: $0 <rhost_file> <user_file> <smbdomain> <smbpass> <smbuser> <threads>"
	exit 2
fi

rhosts="$1"
user_file="$2"
smbdomain="$3"
smbpass="$4"
smbuser="$5"
threads="$6"

msfcli="/usr/bin/msfcli"
for is_file in $user_file $msfcli $rhosts
do
	if [ ! -f $is_file ]
	then
		echo "$is_file: Doesn't Exists On The System !!!"
		exit 1
	fi
done

main "$rhosts" "$user_file"  "$smbdomain" "$smbpass" "$smbuser" "$threads"
