$(document).ready(function() {
	$('a.shownav').on('click', function(){
		$('nav.headernav').slideDown();
		$(this).next('a.hidenav').fadeIn();
		$(this).hide();
	});
	$('a.hidenav').on('click', function(){
		$('nav.headernav').fadeOut();
		$(this).prev('a.shownav').fadeIn();
		$(this).hide();
	});

	var setscreen_width = $(window).width();
	if(setscreen_width < 1100){
		$('nav ul li').on('click', function(){
			$('nav.headernav').fadeOut('slow');
			$('a.hidenav').hide();
			$('a.shownav').fadeIn();
		});
	}


	$(window).scroll(function() {
		if($(this).scrollTop() >= 100){
			$('header').addClass('fixed');
		}else{
			$('header').removeClass('fixed');
		}
	});

	var owl = $('.owl-carousel').owlCarousel({
		autoplay: true,
		autoplayTimeout: 4000,
		slideTransition: 'ease',
		autoplayHoverPause: true,
	    loop:true,
	    //center: true,
	    margin:55,
	    nav:false,
	    dots: false,
	    responsive:{
	        0:{
	            items:1
	        },
	        440:{
	            items:2
	        },
	        690:{
	            items:3
	        },
	        1240:{
	            items:4
	        }
	    }
	});

	$( function() {
	    $( "#datepicker" ).datepicker({ minDate: 0, maxDate: "+1M +10D" });
	    $( "#datepicker" ).datepicker('option', 'dateFormat', 'DD, d MM, yy');
	});
	//修改密码
	// script.js
	const editButton = document.getElementById('editButton');
	const saveButton = document.getElementById('saveButton');
	const cancelButton = document.getElementById('cancelButton');
	const formElements = document.querySelectorAll('#profileForm input');
	
	// 点击“修改信息”按钮时，启用表单编辑
	editButton.addEventListener('click', function() {
		formElements.forEach(element => {
			element.disabled = false; // 启用所有表单输入框
		});
		editButton.style.display = 'none'; // 隐藏“修改信息”按钮
		saveButton.style.display = 'inline'; // 显示“保存修改”按钮
		cancelButton.style.display = 'inline'; // 显示“取消”按钮
	});
	
	// 点击“保存修改”按钮时，禁用表单编辑并保存数据
	document.getElementById('profileForm').addEventListener('submit', function(event) {
	// 启用所有表单输入框
	formElements.forEach(element => {
		element.disabled = false;
	});
	// 显示和隐藏相应的按钮
	editButton.style.display = 'inline';
	saveButton.style.display = 'none';
	cancelButton.style.display = 'none';
	});
	
	// 点击“取消”按钮时，恢复原始状态并禁用表单
	cancelButton.addEventListener('click', function() {
		formElements.forEach(element => {
			element.disabled = true; // 禁用所有表单输入框
			element.value = element.defaultValue; // 恢复默认值
		});
		editButton.style.display = 'inline'; // 显示“修改信息”按钮
		saveButton.style.display = 'none'; // 隐藏“保存修改”按钮
		cancelButton.style.display = 'none'; // 隐藏“取消”按钮
	});
});

