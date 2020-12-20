Using Bookshelf
===============

Bookshelf is written in  python and is tested on linux and mac.  It is a command line tool, but the database can also be easily queried via a web-interface using something like php.  Example php code is also provide to facilitate that.

Deposition
----------
To deposit and catalogue a trajectory, the user needs to enter details like the protein name, program name(software tool used to generate the trajectory) and a few lines about the trajectory and the file names they want to deposit. It is essential to deposit all the files required to run the simulation e.g input, topology, coordinates, trajectory and stream files.

Simple MD deposition
++++++++++++++++++++

The command to run the deposition is ::

$ python bookshelf.deposit.py -m <protein name> -p <program name> -c <"comments"> <test.inp> <test.mdp> <test.xtc> <test.pdb>


PMF Deposition
++++++++++++++

Potential of Mean Force calculations are also fairly routine these days and bookshelf can handle these as well.  Prior to  deposition, copy all the files or directories into a folder and deposit the entire folder.  Add the  -f flag with value yes while passing the arguments.

The command for the pmf deposition is ::

$ python bookshelf.py -m <protein name< -p <program name> -c <"comments"> -f <yes> <foldername>

Linking to Publications
+++++++++++++++++++++++

Bookshelf can also link to relevanet publications or a DOI.  You can add these with the -i and -d flags.  Enter only the Ids and not the entire url as the script will raise an error.

Example:  ::

$ python bookshelf.depsoit.py -m <protein name< -p <program name> -c <"comments"> -f <no> -d <doi-identifier> -i<pubmed-id ><test.inp> <test.mdp> <test.xtc> <test.pdb>

Known Packages
--------------

Bookshelf already knows about several well-used MD engines.  It accepts all the files use to generate trajectories by different simulation packages such as CHARMM, GROMACS, NAMD and Gaussian. It checks for the essential files required to run the trajectory but there is no limitation to the number of files deposited.


Adding other simulation packages
It is easy to add a new simulation package.  To add a simulation package run the following command:  ::

           $python add.program.py –p <program name> <.ext1> <.ext2> <.ext3> <.ext4>

where program name is the name of software package one wants to add;  ext1, ext2, etc are the extensions for the mandatory files that need to be submitted for the deposition.


How is the data stored?
-----------------------

The files are stored as flat files in the storage area. At installation the script creates a sub-directory and copies all the files to the directory and enters the metadata in the mysql database.  The files and the metadata are stored with unique id named as *Trajid*.


How to search the database?
---------------------------

The metadata can be accessed by command line or web interface. Using the command line, the database can be searched using keyword which can be a protein name or program name or user name or keywords in comments.

The command to run the script is ::

$ python bookshelf.browse.py -s <keyword>

The meta data can be also accessed through a web interface. A keyword search can be performed or it can be browsed by date, protein name, username and program name. (see Web browsing interface for more information)

Deletion
--------

An entry in the bookshelf database can be deleted by the  bookshelf administrator: ::

        $python ./bookshelf/bin/exe/bookshelf.erase.py -e <trajid>
