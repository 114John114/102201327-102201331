<?php
if(isset($_POST['email']) && !empty($_POST['email'])){

		$name = $_POST["name"];
		$email = $_POST["email"];
		$phone = $_POST["phone"];
		$datevalue = $_POST["date"];
		$subject = 'Dental Appointment Query From '.$name;
		//$message = $_POST["message"];


		//date_default_timezone_set('Asia/Kolkata');
		$timestamp_capture = time();
		//$reg_time = date('d-m-Y h:i:s a', time());
		//$reg_ip = $_SERVER['REMOTE_ADDR'];
		//$reg_ip_proxy = $_SERVER['HTTP_X_FORWARDED_FOR'];

		if(isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on'){
	    	$siteurl = "https://".$_SERVER['SERVER_NAME'];
	    }else{
	    	$siteurl = "http://".$_SERVER['SERVER_NAME'];
	    }

	
		$to = "rajkvx@gmail.com";
		$mail_subject = "Dental Appointment Query From $name | Message ID ".$timestamp_capture;
		$mail_message = "
		<br>
		<p>You received a dental appointment query from your website. The details are as below:</p>
		<br>
		<p><strong>Name:</strong> $name</p> 
		<p><strong>Email:</strong> $email</p> 
		<p><strong>Phone:</strong> $phone</p> 
		<p><strong>Date of Appointment:</strong> $datevalue</p>
		<br><br><br>...<br>
		This message is sent from $siteurl using a contact form.
		";
		$headers = "MIME-Version: 1.0" . "\r\n";
		$headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
		// More headers
		$headers .= 'From: '.$name.' <noreply@'.$_SERVER['SERVER_NAME'].'>' . "\r\n" . 'Reply-To: '.$email."\r\n";
		$sendmail = mail($to,$mail_subject,$mail_message,$headers);
		//$sendmail = 'ok';
		if($sendmail){
			$response['status'] = 'Ok';
			$response['msg'] = 'Request Submitted Successfully. &nbsp; <span class="fa-solid fa-check"></span>';
			echo json_encode($response);
		}else{
			$response['status'] = 'Error';
			$response['msg'] = 'Something Went Wrong. Send Us an Email Directly.';
			echo json_encode($response);
		}
			

}else{
	$response['status'] = 'Error';
	$response['msg'] = 'Something Went Wrong. Send Us an Email Directly.';
	echo json_encode($response);
}
?>