<?php
session_start();
include('db.php');

if($_SERVER["REQUEST_METHOD"] == "POST") {
    // username and password sent from form 
    $myusername = mysqli_real_escape_string($conn,$_POST['username']);
    $mypassword = mysqli_real_escape_string($conn,$_POST['password']); 
    $myusername = stripslashes($myusername);
    $mypassword = stripslashes($mypassword);
    $myusername = htmlspecialchars($myusername);
    $mypassword = htmlspecialchars($mypassword);
    $sql = "SELECT id FROM admin WHERE username = '$myusername' and password = '$mypassword'";
    $result = mysqli_query($conn,$sql);
    $row = mysqli_fetch_array($result,MYSQLI_ASSOC);
    $active = $row['active'];
    $count = mysqli_num_rows($result);
    // If result matched $myusername and $mypassword, table row must be 1 row
    if($count == 1) {
        $_SESSION['login_user'] = $myusername;
        header("location: index.php");
    }else {
        $error = "Your Login Name or Password is invalid";
    }
}