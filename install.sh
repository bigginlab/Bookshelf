#!/bin/bash
error_script()
{
	echo -e "\033[1m\nExiting the installation due to error!!! \033[0m"
	exit 1
}
check_Name()
{
	VMC_NAME=`echo $VMC_NAME`
	while ! [ -z "${VMC_NAME//[a-zA-Z0-9]}" ] 
	do 
		read -p "Error! Enter a valid value or only alphanumeric characters:" VMC_NAME
	done
	echo $VMC_NAME
}
check_User()
{
	username=`echo $username`
	if
		userCheck=$(egrep "$username" /etc/passwd)
	then
		read -p "$username user exists! Do you want to continue with the existing username? yes/no - " opt
		while [ "$opt" != "yes" ] && [ "$opt" != "no" ];do
			read -p "Invalid option. yes/no ? - " opt
		done
		if [ "$opt" == "yes" ];then
			flag="none"
		elif [ "$opt" == "no" ];then
			flag="true"
		fi
	else
		flag="false"
	fi
	echo $flag
}
trap 'error_script' ERR
set -e
if [ $(id -u) -eq 0 ]; then
############## check if MySql and python exist ##############
	if 
		y=$(which mysql)
	then
		echo $y
	else
		echo -e "\n You need to install MySQl and set it in your path to create Bookshelf database."
		exit 1
	fi
	if 
		x=$(which python)
	then
		echo $x
	else
		echo -e "\n You need to install Python and set it in your path to run Bookshelf scritps."
		exit 1
	fi
############## Check if bookshelf.daemon.py  alreday running ##############
	SERVICE='bookshelf.daemon.py'
 
	if ps ax | grep -v grep | grep $SERVICE > /dev/null 
	then
    		echo -e "\n $SERVICE is running. You need to kill the process to install the bookshelf."
		exit
	fi
############## Check if bookshelf folder and executables already exist ##############
	bookcheck="./bookshelf"
	execheck="./exe"
	echo -e
	if [ -d "${execheck}" ]; then
		read -p "'./exe' folder already exists. Do you want to overwrite it ? yes/no - " opt
		while [ "$opt" != "yes" ] && [ "$opt" != "no" ];do
			read -p "Invalid option. yes/no? - " opt
		done
		if [ "$opt" == "yes" ];then
			rm -r $bookcheck

		elif [ "$opt" == "no" ];then
			echo -e "\n Exiting !!!"
			exit 1
		fi
	fi
	if [ -d "${bookcheck}" ]; then
		[ "$(ls -A ./bookshelf/data/trajfiles)" ] || [ "$(ls -A ./bookshelf/data/error_trajfiles)" ] ||[ "$(ls -A ./bookshelf/temp)" ]  && x=1 || x=0
		if [ "$x" == 1 ];then
			echo -e "\n'./bookshelf' folder already exists and has trajectory files. You need to move or delete the folder to continue with the installation."
			exit 1
		fi
	fi	
		
	cp -r "./install-files/bookshelf" "./"
	cp -r "./install-files/exe" "./"

############## Running mysql queries to check if the database already exists ##############
	echo -e "\033[1m\nYou need to enter the mysql password for root to run the mysql queries."
	echo -e " \n MySQL PASSWORD \033[0m"
	read -s -p "Enter password- " mysqlpass
	echo -e "\n"
	DBS=`mysql -u root -p$mysqlpass -Bse 'show databases'| egrep -v 'information_schema|mysql'`
	for db in $DBS; do
		if [ "$db" == "bookshelf" ];then
			read -p "'$db' database already exists.Do you want to overwrite it? It will create a backup of the existing database before overwriting. yes/no - " opt
			while [ "$opt" != "yes" ] && [ "$opt" != "no" ];do
				read -p "Invalid option. yes/no? - " opt
			done
			if [ "$opt" == "yes" ];then
				echo -e "Overwriting $db database!.  "
				mysqldump -h localhost -u root -p$mysqlpass bookshelf | gzip >./bookshelfdump`date +%m_%d_%y`.gz

			elif [ "$opt" == "no" ];then
				echo -e "Exiting!!! "
				exit 1
			fi
   		fi
		if [ "$db" == "bslog" ];then
			read -p "'$db' database already exists.Do you want to overwrite it? It will create a backup of the existing database before overwriting. yes/no - " opt
			mysqldump -h localhost -u root -p$mysqlpass bslog | gzip >./bslogdump`date +%m_%d_%y`.gz
			while [ "$opt" != "yes" ] && [ "$opt" != "no" ];do
				read -p "Invalid option. yes/no? - " opt
			done
			if [ "$opt" == "yes" ];then
				echo -e "Overwriting $db database!"

			elif [ "$opt" == "no" ];then
				echo -e "Exiting!!! "
				exit 1
			fi
   		fi
	done
	
############## Create MySql user to read and write to bookshelf database ###############
	echo -e "\033[1m\nCreating  bookshelf database and users in MySQL. \033[0m"
	read -p  "Enter name to set up MySQl user for bookshelf. (Default - BS.writer) - " bswriter
	if [ "$bswriter" == "" ]; then
 		bswriter=BS.writer
	else
		VMC_NAME=$bswriter
		bswriter=$(check_Name $VMC_NAME)
	fi
  	echo "MySQl user to write to bookshelf - '$bswriter'"
	echo "MySQl passowrd for '$bswriter'" 
	
	pass=$(</dev/urandom tr -dc A-Za-z0-9 | head -c12 )
	echo -e "\033[1m$pass \033[0m"
	
############## Create bookshelf user only to read database ###############
	echo -e "\n"
	read -p "Enter name for MySQl user to retrieve data from bookshelf. (Default- BS.reader) - " bsreader
	if [ "$bsreader" == "" ]; then
 		bsreader=BS.reader
	else
		VMC_NAME=$bsreader
		bsreader=$(check_Name $VMC_NAME)
	fi
  	echo "MySQl user to read bookshelf - '$bsreader'"

############## Create login user only to read and write the login database ###############
	
	echo -e "\033[1m\nCreating a database to maintain the login details for the web-interface.\033[0m"
	read -p "Set a MySql user to write the details to the login database. (Default - BS.login) - " bslogin
	if [ "$bslogin" == "" ]; then
 		bslogin=BS.login
	else
		VMC_NAME=$bslogin
		bslogin=$(check_Name $VMC_NAME)
	fi
	echo "MySQl user to login database -  '$bslogin'"

	echo "Passowrd for mysql.login $loginpass"
 	loginpass=$(</dev/urandom tr -dc A-Za-z0-9 | head -c12)
	echo -e "\033[1m$loginpass\033[0m"

############## Create users and database ###############
	CMD="DROP DATABASE IF EXISTS bookshelf;
	CREATE DATABASE bookshelf;
	USE bookshelf;
	CREATE TABLE TrajData(
         	TrajId  VARCHAR(30) NOT NULL,
         	UserName VARCHAR(40),
         	Date VARCHAR(40) NOT NULL,
         	ProteinName VARCHAR(200) NOT NULL,
         	ProgramCode VARCHAR(30) NOT NULL,
			UserComments VARCHAR(300) NOT NULL,
			PmfOption VARCHAR(3) NOT NULL,
			Doi VARCHAR(40) NOT NULL,
			pid VARCHAR(20) NOT NULL,
			PRIMARY KEY (TrajId));
	CREATE TABLE TrajFiles(
         	TrajId  VARCHAR(30) NOT NULL,
         	FileName VARCHAR(100) NOT NULL,
         	CheckSum VARCHAR(40) NOT NULL,
         	FilePathName VARCHAR(100) NOT NULL,
         	UserName VARCHAR(40) NOT NULL,
			Date VARCHAR(40) NOT NULL,
			Foreign Key(TrajId) references TrajData(TrajId));

	SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ANSI';
	USE bookshelf;
	DROP PROCEDURE IF EXISTS bookshelf.drop_user_if_exists ;
	DELIMITER $$
	CREATE PROCEDURE  bookshelf.drop_user_if_exists()
	BEGIN
  	DECLARE bswcheck BIGINT DEFAULT 0 ;
  	SELECT COUNT(*)
  	INTO bswcheck
    	FROM mysql.user
      WHERE User = '$bswriter' and  Host = '127.0.0.1';
   	IF bswcheck > 0 THEN
         DROP USER '$bswriter'@'127.0.0.1' ;
  	END IF;
	END ;$$
	DELIMITER ;
	CALL bookshelf.drop_user_if_exists() ;
	DROP PROCEDURE IF EXISTS bookshelf.drop_users_if_exists ;

	SET SQL_MODE=@OLD_SQL_MODE ;
	SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ANSI';
	USE bookshelf;
	DROP PROCEDURE IF EXISTS bookshelf.drop_user_if_exists ;
	DELIMITER $$
	CREATE PROCEDURE  bookshelf.drop_user_if_exists()
	BEGIN
  	DECLARE bsrcheck BIGINT DEFAULT 0 ;
  	SELECT COUNT(*)
  	INTO bsrcheck
    	FROM mysql.user
        WHERE User = '$bsreader' and  Host = '127.0.0.1';
   	IF bsrcheck > 0 THEN
         DROP USER '$bsreader'@'127.0.0.1' ;
  	END IF;
	END ;$$
	DELIMITER ;
	CALL bookshelf.drop_user_if_exists() ;
	DROP PROCEDURE IF EXISTS bookshelf.drop_users_if_exists ;

	CREATE USER '$bswriter'@'127.0.0.1' IDENTIFIED BY '$pass';
	GRANT ALL PRIVILEGES  ON bookshelf.* TO '$bswriter'@'127.0.0.1'
 	WITH GRANT OPTION;
	ALTER USER 'BS.writer'@'127.0.0.1' IDENTIFIED WITH mysql_native_password BY '$pass';

	CREATE USER '$bsreader'@'127.0.0.1';
	GRANT SELECT  ON bookshelf.* TO '$bsreader'@'127.0.0.1';
	FLUSH PRIVILEGES;
	ALTER USER 'BS.reader'@'127.0.0.1' IDENTIFIED WITH mysql_native_password BY '';	

	DROP DATABASE IF EXISTS bslog;
	CREATE DATABASE bslog;
	USE bslog;
	CREATE TABLE member(
         	uid  int NOT NULL auto_increment,
			email varchar(60) NOT NULL default '',
			password varchar(40) NOT NULL default '',
			firstname varchar(40) NOT NULL default '',
			lastname varchar(40) NOT NULL default '',
			affiliation varchar(80) NOT NULL default '',
			PRIMARY KEY (uid),
			UNIQUE KEY username (email));

	SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ANSI';
	USE bslog;
	DROP PROCEDURE IF EXISTS bslog.drop_user_if_exists ;
	DELIMITER $$
	CREATE PROCEDURE  bslog.drop_user_if_exists()
	BEGIN
  	DECLARE bslcheck BIGINT DEFAULT 0 ;
  	SELECT COUNT(*)
  	INTO bslcheck
    	FROM mysql.user
        WHERE User = '$bslogin' and  Host = '127.0.0.1';
   	IF bslcheck > 0 THEN
        DROP USER '$bslogin'@'127.0.0.1' ;
  	END IF;
	END ;$$
	DELIMITER ;
	CALL bslog.drop_user_if_exists() ;
	DROP PROCEDURE IF EXISTS bslog.drop_users_if_exists ;
	SET SQL_MODE=@OLD_SQL_MODE ;
	CREATE USER '$bslogin'@'127.0.0.1' IDENTIFIED BY '$loginpass';
	GRANT ALL PRIVILEGES  ON login.* TO '$bslogin'@'127.0.0.1'
 	WITH GRANT OPTION;
	FLUSH PRIVILEGES;
        ALTER USER 'BS.login'@'127.0.0.1' IDENTIFIED WITH mysql_native_password BY '$loginpass';"
	
	mysql -u root -p$mysqlpass  -e "$CMD"
	
############## Running mysql queries to check if the database already exists ##############

	sed -i 's/host=""/host="127.0.0.1"/g' ./exe/bin/mysql_connect.py
	sed -i 's/user=""/user="'$bswriter'"/g' ./exe/bin/mysql_connect.py
	sed -i 's/passwd=""/passwd="'$pass'"/g' ./exe/bin/mysql_connect.py
	sed -i 's/db=""/db="bookshelf"/g' ./exe/bin/mysql_connect.py
	sed -i 's/host=""/host="127.0.0.1"/g' ./exe/bs/dbConnect.py
	sed -i 's/user=""/user="'$bsreader'"/g' ./exe/bs/dbConnect.py
	sed -i 's/db=""/db="bookshelf"/g' ./exe/bs/dbConnect.py
	sed -i 's/server=""/server="127.0.0.1"/g' ./exe/web/Bookshelf/includes/mysql_connect.php
	sed -i 's/user=""/user="'$bsreader'"/g' ./exe/web/Bookshelf/includes/mysql_connect.php 
	sed -i 's/db=""/db="bookshelf"/g' ./exe/web/Bookshelf/includes/mysql_connect.php
	sed -i 's/server=""/server="127.0.0.1"/g' ./exe/web/Bookshelf/includes/login_connect.php 
	sed -i 's/user=""/user="'$bslogin'"/g' ./exe/web/Bookshelf/includes/login_connect.php 
	sed -i 's/passwd=""/passwd="'$loginpass'"/g' ./exe/web/Bookshelf/includes/login_connect.php 
	sed -i 's/db=""/db="login"/g' ./exe/web/Bookshelf/includes/login_connect.php 
	echo -e "\nThe files will be stored in a temporary folder before daemon copies it to the permanent location.  You will be soon prompted for the path to these folders.The two folders have to be different.\nYou can press enter for default options.\033[0m"
		
	SCRIPT=$(readlink -f $0)
	SCRIPTPATH=`dirname $SCRIPT`
	[[ $SCRIPTPATH != */ ]] && bpth="$SCRIPTPATH"/
	echo -e "\033[1mHome Diretory - $bpth \033[0m"
	homeDir="defaultpath"
	sed -i "s%${homeDir}%${bpth}%g" ./exe/bin/bookshelf.daemon.py 
	sed -i "s%${homeDir}%${bpth}%g" ./exe/bin/bookshelf.erase.py
	sed -i "s%${homeDir}%${bpth}%g" ./exe/bs/bookshelf.deposition.py
	chmod 777 ./bookshelf	
	tempFolder='homeDir+"bookshelf/temp/"'

	read -p "Enter the path to the temporary folder. (Default - $bpth'bookshelf/temp/') - " newtempFolder
	if [ "$newtempFolder" == "" ]; then
		echo "Folder for the temporary storage of files  - "$bpth'bookshelf/temp/'
		chmod -R 777 ./bookshelf/temp
	else
		[[ $newtempFolder != */ ]] && newtempFolder="$newtempFolder"/
		chmod -R 777 $newtempFolder
		newtempFolder=\"$newtempFolder\"
		sed -i "s%${tempFolder}%${newtempFolder}%g" ./exe/bin/bookshelf.daemon.py
		sed -i "s%${tempFolder}%${newtempFolder}%g" ./exe/bs/bookshelf.deposition.py
		echo "Folder for the temporary storage of files  - "$newtempFolder
	fi
	trajFolder='homeDir+"bookshelf/data/trajfiles/"'
	read -p "Enter the path to the permanent folder. (Default- $bpth'bookshelf/data/trajfiles/') - " newtrajFolder

	if [ "$newtrajFolder" == "" ]; then
		echo "Folder for the final storage of files  - "$bpth'bookshelf/data/trajfiles/'
		chmod -R 755 ./bookshelf/data/trajfiles/
		chmod -R 755 ./bookshelf/data/error_trajfiles/
	else
		[[ $newtrajFolder != */ ]] && newtrajFolder="$newtrajFolder"/
		newerrorFolder=$newtrajFolder"error_trajfiles"
		chmod -R 755 $newtrajFolder
		newtrajFolder=\"$newtrajFolder\"
		if [[ $newtempFolder == $newtrajFolder ]]; then
			echo -e "\033[1m\nThe temporary and the permanent storage area cannot be same!\033[0m"
			error_script
		fi
		sed -i "s%${trajFolder}%${newtrajFolder}%g" ./exe/bin/bookshelf.daemon.py
		sed -i "s%${trajFolder}%${newtrajFolder}%g" ./exe/bin/bookshelf.erase.py
		echo "Folder for the final storage of files by daemon -"$newtrajFolder
		
		mkdir $newerrorFolder	
		chmod -R 755 $newerrorFolder
		junkFolder='homeDir+"bookshelf/data/error_trajfiles/"'
		newerrorFolder=\"$newerrorFolder\"
		sed -i "s%${junkFolder}%${newerrorFolder}%g" ./exe/bin/bookshelf.daemon.py
	fi
############## Creating Bookshelf administrator ##############
	echo -e "\033[1m \nCreating a Bookshelf administrator to run daemon with permissions  to copy the files from temp area to permanent location.\033[0m"
	flag="true"
	while [ "$flag" == "true" ];do
		read -p "Enter username for Bookshelf administrator. (Default -BookShelf) - " username
		if [ "$username" == "" ]; then
 			username=Bookshelf
		else
			VMC_NAME=$username
			username=$(check_Name $VMC_NAME)
			echo $username
		fi
	
		flag=$(check_User $username)
	done
	if [ "$flag" == "false" ];then
		echo "Username for Bookshelf administartor - $username"
		read -s -p "Enter password : " password
		bspass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
		useradd -m -p $bspass $username
		if [ $? -eq 0 ] ;then 
			 echo -e "\033[1m\nUser has been added to system!\033[0m" 
		else 
			echo -e "\033[1m\n System error!!Failed to add a user!\033[0m" 
			error_script
		fi
	fi
############## changing permissions ##############
	chmod -R 700 ./exe/bin/
	chown -R $username bookshelf 
	chown -R $username exe
	sudo -u $username python ./exe/bin/bookshelf.daemon.py
	echo -e "\033[1m\nInstallation is complete!"
	echo -e "\nYou can now deposit to bookshelf database."
	echo -e "\nHelp on how to deposit and browse the data is in 'Run-Bookshelf.txt'."
	echo -e "\nFor web-interface, you need to copy the web [./exe/web/] folder to Web server directory (www or public_html)." 
	echo -e "\nPlease cite Bookshelf with the following reference: \nShabana Vohra, Benjamin A. Hall, Daniel A. Holdbrook, Syma Khalid, and Philip C. Biggin. Bookshelf: a simple curation system for the storage of biomolecular simulation data (2010).Database(Oxford) Vol. 2010, Article ID baq033, doi:10.1093/database/baq033.\033[0m"
else
	echo -e "\nYou have to login as a root to run the script !"
	exit 2
fi


