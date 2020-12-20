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
	if(isset($_POST['submitted'])){
		$errors=array(); //Intialize an error array
		
		if (empty($_POST['keyword'])){
			$errors[]='You have not enter any keyword to carry out the search.';
		}
		else{
			$keyword=trim($_POST['keyword']);}

		if(empty($errors)){// if there are no errors
			$query= "Select TrajId from TrajData where TrajId like '%$keyword%'OR ProteinName like '%$keyword%'OR ProgramCode like 
						'%$keyword%'OR 	UserName like '%$keyword%'OR UserComments like '%$keyword%'";
			$result= @mysqli_query($link,$query); //run the query
			$numrows= @mysqli_num_rows($result);
			if(!$result){//if the query did not run ok
				echo'<div class="error"><p > Could not display the list</p>';
					echo '<p>' .mysql_error($link).' //debugging message
					<br /> <br />Query:' .$query.'</p> 
					</div>';
			}
			if($numrows<1){
				echo'<div class="error"><h1 > No match found for your query!!!</h1></div>';
			}
		}
		else{	//report the errors
			echo'<div class="error"><h1 > Error!!</h1>
			<p> The following erros occured:<br/>';
			foreach($errors as $msg){		//print each error.
				echo " -$msg <br/>";
			}// end of for loop
			echo ' Please try again </p></div>';
		} //end of if empty($errors)
	}	//end of if(isset($_POST['submitted']))	
				
	if(!($keyword)){$keyword=$_GET['keyword'];
			$page=$_GET['page'];
			$limit=$_GET['limit'];
			$numrows=$_GET['numrows'];
			$num=$_GET['num'];
	}
				
	if($numrows>=1){
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
		$current = intval($page/$limit) + 1; // Current page number.
		$first = $page + 1; // The first result.
		$limitnum = 5 * $limit;
		$firstpage=0;
		$show='Show All';
		if (!((($page + $limit) / $limit) >= $pages) && $pages != 1) {
			$last = $page + $limit;} //If not last results page, last result equals $page plus $limit.
		else{
			$last = $numrows;} // If last results page, last result equals total number of results.
		
		$query= "Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid from TrajData where TrajId like '%$keyword%'OR ProteinName like '%$keyword%'OR ProgramCode like '%$keyword%'OR 	UserName like '%$keyword%'OR UserComments like '%$keyword%'	LIMIT $page, $limit"; 
		$results= @mysqli_query($link,$query); //run the newquery
					//table header
		echo '<h3 class= "title"> Results for the query: '.$keyword. '</h3>';
// top page bar
		echo '<table width="100%" style="border: none; font-size:14">
			<tr><td align="left">
			Results <b>'.$first.'</b> - <b>'.$last.'</b> of <b>'.$numrows.'</b>';
		echo'<td align="left" >';
		if ($numrows>20){
			if ($page == 0){
				echo'First|';
				echo'Prev|';}
			if ($page != 0){ // Don't show back link if current page is first page.
				echo'<a href="search_trajdata.php?keyword='.$keyword.'&page='.$firstpage.'&limit='.$limit.'&numrows='.$numrows.'"><b> First| </b></a>';
				$back_page = $page - $limit;
				echo'<a href="search_trajdata.php?keyword='.$keyword.'&page='.$back_page.'&limit='.$limit.'&numrows='.$numrows.'"><b> Prev| </b></a>';
			}
			echo ' Page <b>'.$current.'</b> of <b>'.$total.'</b>';
			if (!((($page+$limit) / $limit) >= $pages) && $pages != 1) { // If last page don't give next link.
				$next_page = $page + $limit;
				$lastpage=$numrows-($numrows%$limit);
				echo'<a href="search_trajdata.php?keyword='.$keyword.'&page='.$next_page.'&limit='.$limit.'&numrows='.$numrows.'"><b> |Next</b></a>';
				echo'<a href="search_trajdata.php?keyword='.$keyword.'&page='.$lastpage.'&limit='.$limit.'&numrows='.$numrows.'"><b> |Last</b></a>';}
			else{
				echo'|Next|Last';}
			if ($limit==$numrows){
				$limit=20;
				echo'<td align="right"> <a href="search_trajdata.php?keyword='.$keyword.'&page='.$firstpage.'&limit='.$limit.'&numrows='.$numrows.' "> <u>Show page</u></a>';}
			else{
				echo'<td align="right"> <a href="search_trajdata.php?keyword='.$keyword.'&page='.$firstpage.'&limit='.$numrows.'&numrows='.$numrows.' "> <u>Show all</u></a>';}
		}
		echo'</td></tr></table>';
//End of the top page bar
// Data table		
		echo'<table align="center" cellspacing="3" cellpadding ="5" width="100%">
			<tr bgcolor="#EDC393"><td align="left"><b> Trajactory Id</b></td> <td align="left"><b>Username</b></td> <td align ="left"> <b> Date</b></td><td align ="left"> <b> Protein Name</b></ td><td align ="left"> <b> Program Code</b></td><td align ="left"> <b> User comments</b></td></tr>';
		$bg=='#EDE7DB';
		while($row=mysqli_fetch_array($results, MYSQLI_ASSOC)){
			$bg=($bg=='#EDE7DB'?'#fffffff':'#EDE7DB');
			echo'<tr bgcolor="'.$bg.'"><td align="left">'.$row['TrajId'].'</td> <td align="left"> '.$row['UserName'].' </td> <td align ="left"> '.$row['Date'].'</td> <td align ="left"> '.$row['ProteinName'].'</td> <td 	align ="left"> '.$row['ProgramCode'].'</td> <td align ="left"> '.$row['UserComments'].'&nbsp;';
				if ($row['PmfOption']=='Yes'){				 
					echo'&nbsp;<b><span style = "background-color:#CDC0B0">PMF </span></b>&nbsp;';}
				if ($row['Doi']!= 'none'){
					echo'&nbsp;<span style = "background-color:#CDC0B0">[doi: <a href="http://dx.doi.org/'.$row['Doi'].'"><u>'.$row['Doi'].'</u></a> ]</span>&nbsp;';}
				if ($row['Pid']!= 'none'){
					echo'&nbsp;<span style = "background-color:#CDC0B0">[pubmed:<a href="http://www.ncbi.nlm.nih.gov/pubmed/'.$row['Pid'].'"><u>'.$row['Pid'].'</u></a> ]</span>&nbsp;';}
				
				echo'</td></tr>';}
		echo'</table>'; //close the Data table
//bottom page bar
		echo '<table width="100%" style="border: none;font-size:14" ><br> <tr ><td align="center" border="0" >';
		if ($numrows>20){
			if ($page == 0){
				echo'Prev ||';}		
			if ($page != 0){ // Don't show back link if current page is first page.
				$back_page = $page - $limit;
				echo'<a href="search_trajdata.php?keyword='.$keyword.'&page='.$back_page.'&limit='.$limit.'&numrows='.$numrows.'"><b>Prev ||</b></a>';}
			for ($i=1; $i <= $pages; $i++)// loop through each page and give link to it.
			{
				$ppage = $limit*($i - 1);
				if ($ppage == $page){
					echo'<a><b>'.$i.'</b></a> ';} // If current page don't give link, just text.
				elseif ($ppage < $page - $limitnum || $ppage > $page + $limitnum){}
				else{
										echo'<a href="search_trajdata.php?keyword='.$keyword.'&page='.$ppage.'&limit='.$limit.'&numrows='.$numrows.'">'.$i.'</a> ';	}
			}//end of for loop
			if (!((($page+$limit) / $limit) >= $pages) && $pages != 1) { // If last page don't give next link.
				$next_page = $page + $limit;
				echo'<a href="search_trajdata.php?keyword='.$keyword.'&page='.$next_page.'&limit='.$limit.'&numrows='.$numrows.'"><b>|| Next</b></a>';
			}else{
				echo' ||Next';
			}
		}
		echo'</td></tr></table>';
		echo'</div>';
	}//end of if($numrows>=1)		
// end of bottom page bar
 	include_once('includes/footer.html');
?>

