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
	if(isset($_POST['submitted'])){
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
				if(mail("$em","Your Request for login details","This is in response to your request for login details at Bookshelf database \n \nEmail: $em \n Password: $pass \n\n Thank You \n \n 			Bookshelfadmin","$headers")){echo "<h4><center><b>THANK YOU</b> <br>Your password is posted to your email address . Please check your mail after some time. </center></h4>";}

				else{// there is a system problem in sending mail
			echo " <h4><center><font color=red >There is some system problem in sending login details to your address. Please contact bookshelf-admin. <br><br><input type='button' value='Retry' onClick='history.go		(-1)'></font></center></h4>";} //end of if(mail)
			}else{
			echo"<h4>There is some system problem in reseting your password.Please contact bookshelf-admin.</h4>";
			}//end of update

		}else{
			echo "<h4> Sorry! Your address is not there in our database . You can <a href='register.php'><u>Signup</u> to login Bookshelf.</h4>";
		}  
		include_once('includes/footer.html');
		exit();
	}
?>
<form name="forgotpassword" action ="forgotpasswd.php" method ="POST" onsubmit="return Validate();">
	<table cellspacing="20" cellpadding="10" style="border: none">
		<tr> 
			<td align="center" > Forgot Password ?&nbsp;Enter your email address </td>
		<tr> 
			<td align="center" > <b> Email address </b><input type ="text" size= "20" maxlenght= "60"name = "email" value=""/></td>
		<tr><td></td></tr>
		<tr>
			<td align="center"><input type="submit" name="submit" value= "Submit" class="button">
			<input type="hidden" name="submitted" value= "True"></td></tr>
		<tr>
			<td align="center" style="font-size:14px">Not registered yet?<a href="register.php"><u>SignUp</u></a></td></tr>
	</table>			
<?php
	include_once('includes/footer.html');
?>
<script language = "Javascript">
function Validate()
{
    if (document.forgotpassword.email.value == '') 
    {
        alert('Please enter the Email address!');
		document.forgotpassword.email.focus();
        return false;
    }
	var emailExp = /^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/;
	if(!document.forgotpassword.email.value.match(emailExp)){
		alert('Not a vaild Email address ');
		document.forgotpassword.email.focus();
		return false;
	}
return true;
}
</script>

