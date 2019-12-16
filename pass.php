<?php 
session_start();
$db = mysqli_connect('localhost', 'root', '', 'web tech2');
if(isset($_POST['login_user'])){
	$username=$_POST['id'];
	$password=$_POST['password'];
	$query="select * from users where username='$username' and password='$password'";
	$result=mysqli_query($db,$query);

	if (mysqli_num_rows($result)==1) {
		//$_SESSION['user']=$username;
		//header("location:home.php");
		echo "<script>alert('done')</script>";
	}
	else{
		echo "<script>alert('error')</script>";
		echo "<script>window.open('login.php','_self')</script>";
	}
}

if(isset($_POST['register_user'])){
	$username=$_POST['id'];
	if($_POST['password'] == $_POST['CNFpassword']){
	$password=$_POST['password'];
	}
	else{
		echo "<script>alert('error')</script>";
		echo "<script>window.open('login.php','_self')</script>";
	}
	$email=$_POST['email'];
	$query="insert into users (username,password,email) values('$usename','$password','$email') ";
	$result=mysqli_query($db,$query);

	if($result){
		echo "<script>alert('done')</script>";
		echo "<script>window.open('login.php','_self')</script>";

	}
	else{
		echo "<script>alert('error')</script>";
		//echo "<script>window.open('login.php','_self')</script>";
	}
}
