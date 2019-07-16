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
<?php # login-functions.inc.php
function absoluteUrl($page='home.php'){
        $url='http://'.$_SERVER['HTTP_HOST'].dirname($_SERVER['PHP_SELF']);
        $url=rtrim($url,'/\\');
        $url.= '/'.$page;
        return $url;
}
function checkLogin($dbc,$email='',$pass='')
{
        $email = $_POST['email'];
        $password = hash('sha1',(trim($_POST['pass'])));
        $query = "SELECT * FROM member WHERE email = '$email' AND password = '$password'";
        $result=@mysqli_query($dbc,$query)OR die ('Could not run the query:'.mysqli_connect_error());
        $rows=@mysqli_num_rows($result);
        if ($rows==1){
        $row=@mysqli_fetch_array($result, MYSQLI_ASSOC);
        return array('true',$row);
        }else{
        $error='The email address and password entered does not match!!!';
        return array('false', $error);}
}
?>
