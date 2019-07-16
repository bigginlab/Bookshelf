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
		require_once('includes/login_connect.php');// connection to the mysql database
		$select_query= "Select * from member where email='$_POST[email]'";
		$check=@mysqli_query($dbc,$select_query);
		$numrows= @mysqli_num_rows($check);
		if($numrows>0){
			echo'<h4> You could not be registered!!!This email address has already been registered! You can retrieve the password for this email id by using the <a href="forgotpasswd.php"><u>forgot password </a></u>page.</h4>';
		}
		else{
			$insert_query ="INSERT into member (email,password,firstname,lastname,affiliation)values('$_POST[email]',SHA1('$_POST[pass]'),'$_POST[firstname]','$_POST[lastname]','$_POST[affiliation]')";
			$r=@mysqli_query($dbc,$insert_query);
			if ($r){
				echo'<h4> You are now registered!!!Try<a href="login.php?"><u> Login</u></a></h4>';}
			else{
				echo'<h4> System Error!!! You could not be registered due to system error. We apologize for any inconvenience.You can <a href="register.php?"><u>Try again</u></a></h4>';
			}
		}
		include_once('includes/footer.html');
		exit();
	}
	
?>
<h4 class="title" align="center">New User Account</h4>
	<p align="center"> A login account is required to browse through the Bookshelf database . Please fill in the following details. All fields are mandatory. Your Email address is your LoginId.</p3>
	<form name="register" action ="register.php" method ="POST" onsubmit="return Validate();">
		<table align="center" style="width:40%;  border:none">
			<tr>
				<td align="right"><i>Email* </i> </td><td align="left"><input type ="text" size= "20" maxlenght= "60" name = "email" value="" /> </td></tr>
			<tr>
				<td align="right"><i>Confirm Email* </i> </td><td align="left"><input type ="text" size= "20" maxlenght= "60" name = "confirmemail" value="" /> </td></tr>
			<tr>
				<td align="right"><i>Password* </i> </td><td align="left"><input type ="password" align="left"size= "20" maxlenght= "20" name = "pass" value="" /> (min. 6 characters)</td></tr>
			<tr>
				<td align="right"><i>Confirm Password* </i> </td><td align="left"><input type ="password" align="left" size= "20" maxlenght= "20" name = "confirmpass" value="" /> </td></tr>
			<tr> 
				<td align="right" > <i> FirstName* </i></td><td align="left"><input type ="text" size= "20" maxlenght= "20"name = "firstname" value=""/></td></tr>
			<tr> 
				<td align="right" > <i> LastName* </i></td><td align="left"><input type ="text" size= "20" maxlenght= "20"name = "lastname" value=""/></td></tr>

			<tr>
				<td align="right"><i>Affiliation* </i></td><td align="left"> <input type ="text" size= "20" maxlenght= "80" name = "affiliation" value="" /> </td></tr>
			<tr><td></td></tr>
			<tr>
				<td></td><td align="left"><input type="submit" name="submit" value= "Register" class="button"/>
				<input type="hidden" name="submitted" value= "True"/></td></tr>
		</table></form>			
<?php
	include_once('includes/footer.html');
?>
<script language = "Javascript">
function Validate()
{
	
	if (document.register.email.value == '') 
    {
       alert('Please fill in your email address!');
		document.register.email.focus();
       return false;
    }
	if (document.register.confirmemail.value == '') 
    {
       alert('Please fill in your email address again for confirmation!');
		document.register.confirmemail.focus();
       return false;
    }
	var emailExp = /^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/;
	if(!document.register.email.value.match(emailExp)){
		alert('Not a vaild Email address ');
		document.register.email.focus();
		return false;
	}
  	if (document.register.email.value != document.register.confirmemail.value) 
    {
        alert("The two email ids are not identical! "+
        "Please enter the same email address again for confirmation");
		document.register.email.focus();
        return false;
    }

	if (document.register.pass.value == '') 
    {
      alert('Please fill in your desired password!');
	  document.register.pass.focus();
      return false;
    }
  	if (document.register.confirmpass.value == '') 
    {
      	alert('Please fill in your password again for confirmation!');
		document.register.confirmpass.focus();
     	 return false;
    }
	var passd=document.register.pass.value;
	if(passd.length <6 ){
		alert('Please enter between 8-20 characters ');
		document.register.pass.focus();
		return false;
	}
	if(passd.length >16 ){
		alert('Please enter the password between 8-20 characters ');
		document.register.pass.focus();
		return false;
	}
	if (document.register.pass.value != document.register.confirmpass.value) 
    {
        alert("The two passwords are not identical! "+
        "Please enter the same password again for confirmation");
		document.register.pass.focus();
        return false;
    }
	var alphaExp = /^[a-zA-Z]+$/;
	if (document.register.firstname.value == '') {
        alert('Please fill in your FirstName!');
		document.register.firstname.focus();
        return false;
    }
	var first=document.register.firstname.value;
	if(first.length > 20){
		alert('Please enter maximum 20 characters ');
		document.register.firstname.focus();
		return false;
	}
	if(!document.register.firstname.value.match(alphaExp)){
		alert('FirstName cannot be alphanumeric, only alphabets');
		document.register.firstname.focus();
		return false;
	}
	if (document.register.lastname.value == '') 
    {
        alert('Please fill in your LastName!');
		document.register.lastname.focus();
        return false;
    }
	var last=document.register.lastname.value;
	if(last.length > 20){
		alert('Please enter maximum 20 characters ');
		document.register.lastname.focus();
		return false;
	}
	if(!document.register.lastname.value.match(alphaExp)){
		alert('LastName cannot be alphanumeric, only alphabets');
		document.register.lastname.focus();
		return false;
	}
    if (document.register.affiliation.value == '') 
    {
        alert('Please fill in your affiliation!');
		document.register.affiliation.focus();
		   return false;
    }
	return true;
}
</script>
