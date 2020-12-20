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
//  Uncomment out the next line if you need users to login/authenticate
//	include_once('includes/authentication.inc.php');

	include_once('includes/header.html');
	require_once('includes/mysql_connect.php');// connection to the mysql database

	if(isset($_GET['submitted'])){
		$keyword=$_GET['browse_db'];
		$dbquery= "Select TrajId from TrajData";
		$dbresults= @mysqli_query($link,$dbquery); //run the query
		$numrows= @mysqli_num_rows($dbresults);
	}
	if(!($keyword)){$keyword=$_GET['keyword'];
		$page=$_GET['page'];
		$limit=$_GET['limit'];
		$numrows=$_GET['numrows'];
	}
	if (!($limit)){
		$limit = 20;} // Default results per-page.
	if ( !$page or $page < 0 ) {
		$page = 0;} // Default page value.	
	$pages = intval($numrows/$limit); // Number of results pages.
	// $pages now contains int of pages, unless there is a remainder from division.
	if ($numrows%$limit) {
		$pages++;} // has remainder so add one page
	if (($pages < 1) ) {
		$total = 1;} // If $pages is less than one or equal to 0, total pages is 1.
	else {
		$total = $pages;} // Else total pages is $pages value.
	$firstpage=0;		
	$current = intval($page/$limit) + 1; // Current page number.
	$first = $page + 1; // The first result.
	$limitnum = 5 * $limit;
	if (!((($page + $limit) / $limit) >= $pages) && $pages != 1) {
		$last = $page + $limit;} //If not last results page, last result equals $page plus $limit.
	else{
		$last = $numrows;} // If last results page, last result equals total number of results.
			
	if ($keyword=='user'){
		$browse_option='USER';
		$query= "Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid from TrajData ORDER BY UserName ASC LIMIT $page, $limit";
		$result= @mysqli_query($link,$query); //run the query
	}
	if ($keyword=='date'){
		$browse_option='DATE';
		$query= "Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid,Date as sortdate from TrajData ORDER BY sortdate DESC LIMIT $page, $limit";
		$result= @mysqli_query($link,$query); //run the query
	}
	if ($keyword=='program_name'){
		$browse_option='PROGRAM NAME';
		$query= "Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid from TrajData ORDER BY ProgramCode ASC LIMIT $page, $limit";
		$result= @mysqli_query($link,$query); //run the query
	}
	if ($keyword=='protein_name'){
		$browse_option='PROTEIN NAME';
		$query= "Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid from TrajData ORDER BY ProteinName ASC LIMIT $page, $limit";
		$result= @mysqli_query($link,$query); //run the query
	}
	echo '<h3 class= "title"> Browse Database by: '.$browse_option.'</h3>';
//start of top page bar
	echo '<table width="100%" >
				<tr><td align="left">
				Results <b>'.$first.'</b> - <b>'.$last.'</b> of <b>'.$numrows.'</b>';
  	echo'<td align="left" >';
	if ($numrows>20){
		if ($page == 0){
			echo'First|';
			echo'Prev|';}
		if ($page != 0){ // Don't show back link if current page is first page.
			echo'<a href="browse_trajdata.php?keyword='.$keyword.'&page='.$firstpage.'&limit='.$limit.'&numrows='.$numrows.'"><b> First| </b></a>';
			$back_page = $page - $limit;
			echo'<a href="browse_trajdata.php?keyword='.$keyword.'&page='.$back_page.'&limit='.$limit.'&numrows='.$numrows.'"><b> Prev| </b></a>';}
			echo ' Page <b>'.$current.'</b> of <b>'.$total.'</b>';
			if (!((($page+$limit) / $limit) >= $pages) && $pages != 1) { // If last page don't give next link.
				$next_page = $page + $limit;
				$lastpage=$numrows-($numrows%$limit);
				echo'<a href="browse_trajdata.php?keyword='.$keyword.'&page='.$next_page.'&limit='.$limit.'&numrows='.$numrows.'"><b> |Next</b></a>';
				echo'<a href="browse_trajdata.php?keyword='.$keyword.'&page='.$lastpage.'&limit='.$limit.'&numrows='.$numrows.'"><b> |Last</b></a>';}	
			else{
				echo'|Next|Last';}
			if ($limit==$numrows){
				$limit=20;
				echo'<td align="right"> <a href="browse_trajdata.php?keyword='.$keyword.'&page='.$firstpage.'&limit='.$limit.'&numrows='.$numrows.' "> <u>Show page</u></a>';}
			else{
				echo'<td align="right"> <a href="browse_trajdata.php?keyword='.$keyword.'&page='.$firstpage.'&limit='.$numrows.'&numrows='.$numrows.' "> <u>Show all</u></a>';}
	}	
	echo'</td></tr></table>';
//end of top page bar
//start of the Data table
			echo'<table align="center" cell spacing="3" cellpadding ="3" width="100%">
				<tr bgcolor="#EDC393"><td align="left"><b> Trajactory Id</b></td> <td align="left"><b>Username</b></td> <td align ="left"> <b> Date</b></td><td align ="left"> <b> Protein Name</b></td><td align ="left"> <b> 					Program Code</b></td><td align ="left"> <b> User comments</b></td></tr>';
			$bg=='#EDE7DB';
			while($row=mysqli_fetch_array($result, MYSQLI_ASSOC)){
				//fetch and print al the records
				$bg=($bg=='#EDE7DB'?'#fffffff':'#EDE7DB');
				echo'<tr bgcolor="'.$bg.'"><td align="left">'.$row['TrajId'].'</td> <td align="left"> '.$row['UserName'].' </td> <td align ="left"> '.$row['Date'].'</td> <td align ="left"> '.$row['ProteinName'].'</td> <td 	align ="left"> '.$row['ProgramCode'].'</td> <td align ="left"> '.$row['UserComments'].'&nbsp;';
				if ($row['PmfOption']=='Yes'){				 
					echo'&nbsp;<b><span style = "background-color:#EDC393">PMF </span></b>&nbsp;';}
				if ($row['Doi']!= 'none'){
					echo'&nbsp;<span style = "background-color:#EDC393">[doi: <a href="http://dx.doi.org/'.$row['Doi'].'"><u>'.$row['Doi'].'</u></a> ]</span>&nbsp;';}
				if ($row['Pid']!= 'none'){
					echo'&nbsp;<span style = "background-color:#EDC393">[pubmed:<a href="http://www.ncbi.nlm.nih.gov/pubmed/'.$row['Pid'].'"><u>'.$row['Pid'].'</u></a> ]</span>&nbsp;';}
				echo'</td></tr>';}//end of while loop
			echo'</table>'; //close the Data table
// start of bottom page bar
			echo '<table width="100%" ><br>
			 	<tr ><td align="center">';
			if ($numrows>20){
				if ($page == 0){
					echo'Prev ||';}		
				if ($page != 0){ // Don't show back link if current page is first page.
					$back_page = $page - $limit;
					echo'<a href="browse_trajdata.php?keyword='.$keyword.'&page='.$back_page.'&limit='.$limit.'&numrows='.$numrows.'"><b>Prev ||</b></a>';}
				for ($i=1; $i <= $pages; $i++)// loop through each page and give link to it.
				{
 					$ppage = $limit*($i - 1);
					if ($ppage == $page){
 					echo'<a><b>'.$i.'</b></a> ';} // If current page don't give link, just text.
					elseif ($ppage < $page - $limitnum || $ppage > $page + $limitnum){}
 					else{
					echo'<a href="browse_trajdata.php?keyword='.$keyword.'&page='.$ppage.'&limit='.$limit.'&numrows='.$numrows.'">'.$i.'</a> ';}
				}//end of for loop
				if (!((($page+$limit) / $limit) >= $pages) && $pages != 1) { // If last page don't give next link.
					$next_page = $page + $limit;
					echo'<a href="browse_trajdata.php?keyword='.$keyword.'&page='.$next_page.'&limit='.$limit.'&numrows='.$numrows.'"><b>|| Next</b></a>';}	
				else{
					echo' ||Next';}
			}
			echo'</td></tr></table>';
// end of bottom page bar
	include_once('includes/footer.html');
?>

