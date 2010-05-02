// JavaScript Document
$(function(){
	var winClose=$(".WinClose");
	//var showWin=$("#ShowWin");
	var docHeight=$(document).height();
	//showWin.click(function(){$(".pop-up-win").fadeIn("fast");$(".pop-wrap").show().height(docHeight);});
	$(".pop-up-win").fadeIn("fast");$(".pop-wrap").show().height(docHeight);
	winClose.click(function(){$(".pop-up-win").fadeOut("fast").detach();$(".pop-wrap").hide().detach();});

})