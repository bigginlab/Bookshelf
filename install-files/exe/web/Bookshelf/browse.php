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
<h3 class="title">Browse Bookshelf</h3>
<form action ="browse_trajdata.php" method ="GET">
<h4> Browse Database by </h4> 
<select name="browse_db"> 
	<option value= user>USER
	<option value= date>DATE
	<option value=program_name>PROGRAM NAME
	<option value=protein_name>PROTEIN NAME
</select>
<input type ="submit" name ='submitted' value="GO" />
<input type ="hidden" name ='submitted' value='True' />						
<?php
	include_once('includes/footer.html');
?>



