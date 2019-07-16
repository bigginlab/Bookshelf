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
<h3 class="title">Search Bookshelf</h3>
<form action ="search_trajdata.php" method ="POST">
	<p> A simple search can be performed on Bookshelf based on annotations related to protein name and user comments. A serach can be done based on Username,Programcode (like Gromacs, Charmm) and Trajid.The trajectories with PMF calculations are marked as Pmf highlighted in yellow. If the data is published it may have a link to the scientific paper.</p>
	<h4> Enter the keyword  <input type ="text" size= "40"name = "keyword"
value="<?php if(isset($_POST['keyword'])) echo $_POST['keyword'];?>" /> </h4>
	<ul>
		<div align="left">								
			<input type ="submit" class="button" name ='submitted' value="Search" />
			<input type ="hidden" name ='submitted' value='True' />
		</div>
	</ul>
</form>
<?php
	include_once('includes/footer.html');
?>

