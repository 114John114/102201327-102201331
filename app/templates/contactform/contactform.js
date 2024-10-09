$(document).ready(function() {
	$("#contactform").submit(function(e) {
		e.preventDefault();
	    var form = $(this);
	    var url = form.attr("action");
	    $("#contactform_btn").html('Please wait... <span class="fas fa-circle-notch fa-spin"></span>');
	    setTimeout(
			  function() 
			  {
				$.ajax({          
			        	type: "post",
			        	url: url,
			        	data: form.serialize(),
			        	dataType: "json",
			        	cache: false,
			        	success: function(data){
			        		if(data.status == 'Ok'){
						        $("#contactform_btn").html('Submit Request <span class="fa-solid fa-angle-right"></span>');
						        $(".responsetype").show();
						    	$(".responsetype").addClass("ok");
						    	$(".responsetype").html(data.msg);
						        form.trigger("reset");
						        grecaptcha.reset();
						        setTimeout(function() {
						        	$(".responsetype").html("");
						        	$(".responsetype").fadeOut();
						        }, 7000);
						    }else{
						    	$(".responsetype").show();
						    	$(".responsetype").addClass("alert");
						    	$(".responsetype").html(data.msg);
						    	$("#contactform_btn").html('Submit Request <span class="fa-solid fa-angle-right"></span>');
						    	grecaptcha.reset();
						    	setTimeout(function() {
						    		$(".responsetype").html("");
						        	$(".responsetype").fadeOut();
						        }, 7000);
						    }
			        	}
				});
			}, 2000);
	});
});