#!/bin/bash

dos2unix_path="/usr/bin/dos2unix"

if [ ! -f "$dos2unix_path" ]
then
        echo "Command: $dos2unix_path doesn't exists on the system. Please run apt-get install dos2unix first."
        exit 1
fi

if [ ! $# -eq 1 ]
then
        echo "Usage: $0 <mimikatz_result.file>"
        exit 2
fi

mimikatz_result_file="$1"
if [ ! -f  "$mimikatz_result_file" ]
then
        echo "File $mimikatz_result_file doesn't exists on the system !!!"
        exit 3
fi

dos2unix $mimikatz_result_file >/dev/null 2&>1
tmp_file="`mktemp /tmp/$USER.XXXXXX`"
grep -B3 "kerberos" "$mimikatz_result_file" | while read -r line
do
        username="`echo "$line" | grep -E "Username : [^$]+" | cut -d ":" -f2`"
        password="`echo "$line" | grep "Password :" | cut -d ":" -f2`"

        if [ ! -z "$username" ] && [ ! "$username" == " (null)" ]
        then
                echo -e "Kadi:$username -> " | tr -d "\n" >> $tmp_file
        fi

        if [ ! -z "$password" ] && [ ! "$password" == " (null)" ] 
        then
                echo "Parola:$password"  >> $tmp_file
        fi
done

cat $tmp_file | sort -n | uniq
rm -rf $tmp_file

exit 0
