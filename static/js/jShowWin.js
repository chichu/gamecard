// JavaScript Document
$(function(){
	var winClose=$(".WinClose");
	var showWin=$("#ShowWin");
	showWin.click(function(){$(".pop-up-win").fadeIn("fast");$(".pop-up-wrap").fadeIn("fast");});
	winClose.click(function(){$(".pop-up-win").fadeOut("fast");$(".pop-up-wrap").fadeOut("fast");});
})