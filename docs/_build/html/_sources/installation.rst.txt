Bookshelf Installation for Unix
===============================
Prerequisites
-------------

To use bookshelf, python and mysql should be installed on the system.  You will also need the  MySQLdb plugin for python to connect to the database.  You will also need to install pymsyql. ::

       conda install -c anaconda pymysql

Installation script
-------------------

Run install.sh as root to set up the program.

The  install script does the following :

   1.  It will create a MySQL database named "bookshelf" with two tables to store the metadata and set up a bookshelf user in mysql with a password  granting all privileges on the database.

   2.  It sets the hostname, username, password and the database name in:

        *./bookshelf/bin/exe/mysql_connect.py .*

   3.  For browsing the database, it will create another mysql user with only read permissions to browse the meta data in the bookshelf database. It will set the variables in:

        *./bookshelf/bs/exe/dbConnect.py .*

   4.  It will prompt to set up the path  to temporary storage location and the final storage disk. The files are stored temporarily in temporary storage area before they are copied by the daemon to the permanent location.

   5.  The script also creates a bookshelf  administrator with username and password. The bookshelf administrator has write permissions to the bookshelf storage disk. The daemon process is run by the administrator to copy the trajectories from the temporary folder ( ./bookshelf/temp)  to the permanent location  (./bookshelf/data/trajfiles).


Mac Install Specific Instructions
---------------------------------

   i.  You will need to ensure that the path to mysql can be found for example ::

           export PATH="//usr/local/mysql-8.0.22-macos10.15-x86_64/bin/:$PATH"

   ii.  To get the MySQLDB modules in python easiest thing to do is :- ::

              sudo easy_install pymysql


        or ::

                conda install -c anaconda pymysql

   The code will look for this module to import query functions from.



This completes the installation of the main service.
