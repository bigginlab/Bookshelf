<!--
Copyright (C) 2010 University of Oxford. All rights reserved.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->

<?php
	include_once('includes/header.html');
?>
<h3 class="title">Help</h3>
<div class="entry">
	<p><b> How to use Bookshelf?</b></br>
	It is a python script which can be run in a shell on a Linux/Unix machine with python installed on it. The user need to enter details like the protein name, program name(software tool used to generate 		the trajectory) and a few lines about the trajectory and the file names they want to deposit. It is essential to deposit all the files required to run the simulation e.g input, topology, coordinates, 		trajectory and stream files.</br>
	<p>The command to run the script is</p>
	<p><b><i>$ python bookshelf.py -m &#060;protein name&#062; -p &#060;program name&#062; -c &#060;"comments"&#062; &#060;test.inp&#062; &#060;test.mdp&#062; &#060;test.xtc&#062; &#060;test.pdb&#062;</i></	b></p>
	<p><b> Pmf Deposition -</b> For pmf deposition, copy all the files or directories into a folder and deposit the folder. Add -f flag with value yes while passing the arguments  <p>
	<p>The command for the pmf deposition is </p>
	<p><b><i>$ python bookshelf.py -m &#060;protein name&#060; -p &#060;program name&#062; -c &#060;"comments"&#062; -f &#060;yes&#062; &#060;foldername&#062;</i></b></p>
	<p><b> Pubmed and DOI link -</b> If the trajectories are linked to a published paper than you can add the Pubmed id and the Doi identifier with the respective flags. Enter only the Ids and not the entire url as the script will raise an error.
	<p><i>Example:</i> </p>
	<p><b><i>$ python bookshelf.py -m &#060;protein name&#060; -p &#060;program name&#062; -c &#060;"comments"&#062; -f &#060;no&#062; -d &#060;doi-identifier&#062; -i&#060;pubmed-id &#062;&#060;test.inp&#062; &#060;test.mdp&#062; &#060;test.xtc&#062; &#060;test.pdb&#062;</i></b></p>
	<p><b>What files does it accept?</b></br>
It accepts all the files use to generate trajectories by different simulation packages such as Charmm, Gromacs, NAMD and Guassian.It checks for the essential files required to run the trajectory but there is no limtation to the number of files deposited.</p>
	<p><b>How is the data stored?</b></br>
The files are stored as flat files on the nfs storage system. It creates a sub-directory and copies all the files to the directory and enters the metadata in the mysql database. The files and the metadata are stored with unique id named as Trajid.</p>
	<p><b>How to search the database?</b></br>
The metadata can be accessed by  command line or web interface. Using the command line, the database can be searched using keyword which can be a protein name or program name or user name or keywords in comments. </p>
	<p>The command to run the script is</p>
	<p><b><i>$ python bookshelf.retrieve -s &#060;keyword&#062;</i></b></p>
	<p>The meta data can be also acceesed through web interface. A keyword search can be performed or it can be browsed on the following options.
		<li>Date in descending order</li>
		<li>Protein name arranged alpahbatically</li>
		<li>User name arranged alphabatically</li>
		<li>Program Name arranged alphabatically</li>
	</p>
</div>
<?php
	include_once('includes/footer.html');
?>


