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

$email=$_POST['email'];
$email=mysql_real_escape_string($email);
$msg="";
require_once('includes/login_connect.php');// connection to the mysql database
$query="SELECT email,password FROM member WHERE email = '$email'";
$result=@mysqli_query($dbc,$query)OR die ('Could not run the query:'.mysqli_connect_error());
$rows=@mysqli_num_rows($result);
if ($rows==1){
	$row=@mysqli_fetch_array($result, MYSQLI_ASSOC);
	$em=$row['email'];
	$newquery="SELECT SUBSTRING(sha1(RAND()) FROM 1 FOR 6) AS password";
	$newresult=@mysqli_query($dbc,$newquery)OR die ('Could not run the query:'.mysqli_connect_error());
	$newrows=@mysqli_num_rows($newresult);
	if ($newrows==1){
		$data=@mysqli_fetch_array($newresult, MYSQLI_ASSOC);}
	$pass=$data['password'];
	$updatequery="UPDATE member SET password =SHA1('$pass')where email = '$em'";
	$updateresult=@mysqli_query($dbc,$updatequery)OR die ('Could not run the query:'.mysqli_connect_error());
	if($updateresult){
		// formating the mail posting
	
		$headers4="vohra@gltph.bioch.ox.ac.uk"; 
		$headers.="Reply-to: $headers4\n";
		$headers .= "From: $headers4\n";
		$headers .= "Errors-to: $headers4\n";

	// mail funciton will return true if it is successful
		if(mail("$em","Your Request for login details","This is in response to your request for login details at Bookshelf database \n \nEmail: $em \n Password: $pass \n\n Thank You \n \n 			Bookshelfadmin","$headers"))		{echo "<center><b>THANK YOU</b> <br>Your password is posted to your email address . Please check your mail after some time. </center>";}

		else{// there is a system problem in sending mail
	echo " <center><font color=red >There is some system problem in sending login details to your address. Please contact bookshelf-admin. <br><br><input type='button' value='Retry' onClick='history.go		(-1)'></center></font>";} //end of if(mail)
	}else{
	echo"There is some system problem in reseting your password.Please contact bookshelf-admin.";
	}//end of update

}else{
	echo " Sorry! Your address is not there in our database . You can <a href='register.php'><u>Signup</u> to login Bookshelf.";
}  
	include_once('includes/footer.html');
?>
