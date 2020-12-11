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
	include_once('includes/authentication.inc.php');
	include_once('includes/header.html');
	require_once('includes/mysql_connect.php');
	$db="BookShelf";
	mysqli_select_db($link,$db);
	$query="Select distinct UserName from TrajData";
	$result= @mysqli_query($link,$query); //run the query
	$num= @mysqli_num_rows($result);
	echo'<h3 class= "title"> Bookshelf Summary</h3>';
	echo'<table align="center"  cell spacing="3" cellpadding ="3" width="100%">
		<tr bgcolor="#EDC393"><td align="left" ><b> Username</b></td> <td align="left"><a href="browse_progname.php?browse_db=GROMACS"><b> GROMACS</b><td align="left"><a href="browse_progname.php?browse_db=CHARMM"><b> CHARMM</b><td align="left"><a href="browse_progname.php?browse_db=NAMD"><b> NAMD</b><td align="left"><a href="browse_progname.php?browse_db=GAUSSIAN"><b> GAUSSIAN</b></td><td align="left"><b> Total</b></td></tr>';
			//fetch and print al the records
	$sum_grotraj=0;$sum_chatraj=0;$sum_namtraj=0;$sum_gautraj=0; $tot_traj=0;
	$bg=='#EDE7DB';
	while($row=mysqli_fetch_array($result, MYSQLI_ASSOC)){
		$bg=($bg=='#EDE7DB'?'#fffffff':'#EDE7DB');
		$sum=0;
		$queryone="Select * from TrajData where userName='$row[UserName]'and ProgramCode='GROMACS'";
		$resultone= @mysqli_query($link,$queryone); //run the query
		$num_of_grotraj= @mysqli_num_rows($resultone);
		$sum=$sum+$num_of_grotraj;
		$sum_grotraj=$sum_grotraj+$num_of_grotraj;

		$querytwo="Select * from TrajData where userName='$row[UserName]'and ProgramCode='CHARMM'";
		$resulttwo= @mysqli_query($link,$querytwo); //run the query
		$num_of_chatraj= @mysqli_num_rows($resulttwo);
		$sum=$sum+$num_of_chatraj;
		$sum_chatraj=$sum_chatraj+$num_of_chatraj;

		$querythree="Select * from TrajData where userName='$row[UserName]'and ProgramCode='NAMD'";
		$resultthree= @mysqli_query($link,$querythree); //run the query
		$num_of_namtraj= @mysqli_num_rows($resultthree);
		$sum=$sum+$num_of_namtraj;
		$sum_namtraj=$sum_namtraj+$num_of_namtraj;

		$queryfour="Select * from TrajData where userName='$row[UserName]'and ProgramCode='GAUSSIAN'";
		$resultfour= @mysqli_query($link,$queryfour); //run the query
		$num_of_gautraj= @mysqli_num_rows($resultfour);
		$sum=$sum+$num_of_gautraj;
		$sum_gautraj=$sum_gautraj+$num_of_gautraj;

		echo'<tr bgcolor="'.$bg.'"><td align="left"><b><a href="browse_byuser.php?browse_db='.$row['UserName'].'">'.$row['UserName'].'</a></b></td><td align="left">'.$num_of_grotraj.'</td><td align="left">'.$num_of_chatraj.'</td><td align="left">'.$num_of_namtraj.'</td><td align="left">'.$num_of_gautraj.'</td><td align="left">'.$sum.'</td></tr>';	
	}
		$tot_traj=$sum_grotraj+$sum_chatraj+$sum_namtraj+$sum_gautraj;
		echo'<tr bgcolor="#EDC393"><td align="left"><b> Total</b></td><td align="left">'.$sum_grotraj.'</td><td align="left">'.$sum_chatraj.'</td><td align="left">'.$sum_namtraj.'</td><td align="left">'.$sum_gautraj.'</td></td><td align="left">'.$tot_traj.'</td></tr>';
			echo'</table>'; //close the table
			mysqli_free_result($result); // free up the resources.
?>
<?php
	include_once('includes/footer.html');
?>
