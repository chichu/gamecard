// JavaScript Document
$(function(){
	var winClose=$(".WinClose");
	var docHeight=$(document).height();
	$(".pop-up-win").fadeIn("fast");
	//$(".pop-up-win").show();
	$(".pop-wrap").show().height(docHeight);
	winClose.click(function(){
		$(".pop-up-win").remove();
		$(".pop-wrap").remove();
	});

})
