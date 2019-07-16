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
		require_once('includes/loginCheck.inc.php');
		require_once('includes/login_connect.php');// connection to the mysql database
		$db="login";
		@mysqli_select_db($dbc,$db);
		list($check,$data)=checkLogin($dbc,$_POST['email'],$_POST['pass']);
		if($check=='true'){
			$email = $_POST['email'];
			$password = hash('sha1',(trim($_POST['newpass'])));
			$updatequery="UPDATE member SET password ='$password'where email = '$email'";
			$updateresult=@mysqli_query($dbc,$updatequery)OR die ('Could not run the query:'.mysqli_connect_error());
			if($updateresult){
				echo "<h4>Your password has been reset sucessfully . Please <a href='login.php'><u>login</u></a> using new password</h4>";} 
			else{
				echo"<h4>There is some system problem in reseting your password.Please contact bookshelf-admin.</h4>";}}
		else{
		 	echo '<h4>'.$data. '<h4>';
		}
		include_once('includes/footer.html');
		exit();
	}
?>
<form name="reset" action ="resetpasswd.php" method ="POST" onsubmit="return Validate();">
	<table  align="center" cellspacing="20" cellpadding="10" style="width:40%;  border:none">
		<tr> 
			<td align="right" > Email* </td><td align="left"><input type ="text" size= "20" maxlenght= "60"name = "email" value=""/></td>
		<tr>
			<td align="right">Old Password* </td><td align="left"><input type ="password" size= "20" maxlenght= "16" name = "pass" value="" /> </td></tr>
		<tr>
			<td align="right">New Password* </td><td align="left"><input type ="password" size= "20" maxlenght= "16" name = "newpass" value="" /> </td></tr>
		<tr>
			<td align="right">Confirm New Password* </td><td align="left"><input type ="password" size= "20" maxlenght= "16" name = "confirmnewpass" value="" /> </td></tr>
		<tr><td></td></tr>
		<tr>
			<td></td><td align="left"><input type="submit" name="submit" value= "Reset" class="button">
			<input type="hidden" name="submitted" value= "True"></td></tr>
		<tr>
			<td></td><td align="left" style="font-size:14px">Not registered yet?<a href="register.php"><u>SignUp</u></a></td></tr>
		<tr>
		<td></td><td align="left" style="font-size:14px"><a href="forgotpasswd.php"><u>Forget your password?</u></a></td></tr>

	</table>			
<?php
	include_once('includes/footer.html');
?>
<script language = "Javascript">
function Validate()
{
    if (document.reset.email.value == '') 
    {
        alert('Please enter the Email!');
		document.reset.email.focus();
        return false;
    }
	if (document.reset.pass.value == '') 
    {
      alert('Please enter the old password!');
	  document.reset.pass.focus();
      return false;
    }
	if (document.reset.pass.value == '') 
    {
      alert('Please enter the new password!');
	  document.reset.newpass.focus();
      return false;
    }
	var passd=document.reset.newpass.value;
	if(passd.length <6 ){
		alert('Please enter between 6-16 characters ');
		document.reset.newpass.focus();
		return false;
	}
	if(passd.length >16 ){
		alert('Please enter the password between 6-16 characters ');
		document.reset.newpass.focus();
		return false;
	}
	if (document.reset.newpass.value != document.reset.confirmnewpass.value) 
    {
        alert("The two passwords are not identical! "+
        "Please enter the same password again for confirmation");
		document.reset.pass.focus();
        return false;
    }
	if (document.reset.newpass.value == document.reset.pass.value) 
    {
        alert("The old and new passwords are identical! "+
        "Please enter a different password");
		document.reset.newpass.focus();
        return false;
    }
return true;
}
</script>
