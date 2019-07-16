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
 if(isset($_POST['submitted'])){
                require_once('includes/loginCheck.inc.php');
                require_once('includes/login_connect.php');// connection to the mysql database
                list($check,$data)=checkLogin($dbc,$_POST['email'],$_POST['pass']);
                if($check=='true'){
                        setcookie('userId',$data['uid'],time()+4800,'/','',0,0);
                        setcookie('emailId',$data['email'],time()+4800,'/','',0,0);
                        $url=absoluteUrl('home.php');
                        header("Location:$url");
                        exit();
                }else{
                include_once('includes/header.html');
                        $error=$data;
                        echo '<h4>' .$error.'</h4>';
		echo '<p> Please <a href="login.php"><u>try</a></u> again. </p>';
	}mysqli_close($dbc);
	include_once('includes/footer.html');
                exit();
        }
include_once('includes/header.html');
?>
<form name="login" action ="login.php" method ="POST" onsubmit="return Validate();">
	<table cellspacing="20" cellpadding="10" style="border: none">
		<tr> 
			<td align="center" > <b> Email </b><input type ="text" size= "20" maxlenght= "16"name = "email" value=""/></td>
		<tr>
			<td align="center"><b>Password</b> <input type ="password" size= "20" maxlenght= "16" name = "pass" value="" /> </td></tr>
		<tr><td></td></tr>
		<tr>
			<td align="center"><input type="submit" name="submit" value= "Login" class="button">
			<input type="hidden" name="submitted" value= "True"></td></tr>
		<tr>
			<td align="center" style="font-size:14px">Not registered yet?<a href="register.php"><u>SignUp</u></a></td></tr>
		<tr>
		<td align="center" style="font-size:14px"><a href="forgotpasswd.php"><u>Forget your password?</u></a></br><a href="resetpasswd.php"><u>Reset password</u></a></td></tr>

	</table>			
<?php
	include_once('includes/footer.html');
?>
<script language = "Javascript">
function Validate()
{
    	
	if (document.login.email.value == '') 
    {
       alert('Please fill in your email address!');
		document.login.email.focus();
       return false;
    }
	var emailExp = /^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/;
	if(!document.login.email.value.match(emailExp)){
		alert('Not a vaild Email address ');
		document.login.email.focus();
		return false;
	}
	if (document.login.pass.value == '') 
    {
      alert('Please enter the password!');
	  document.login.pass.focus();
      return false;
    }
return true;
}
</script>
