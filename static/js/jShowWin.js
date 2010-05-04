// JavaScript Document
function get_popup(url){
    $.get(url, function(data) {
        $("#pop-up").append(data);
    }); 
      
	var docHeight=$(document).height();
	$(".pop-up-win").fadeIn("fast");
	$(".pop-wrap").show().height(docHeight);
	
    var divWidth=$(".pop-up-win").width()/2;
    var divHeight=$(".pop-up-win").height()/2;
    var divLeft =  document.documentElement.clientWidth/2 - divWidth;
    var divTop =  document.documentElement.clientHeight/2 - divHeight -120;
    $(".pop-up-win").css({"left":divLeft,"top":divTop});
    
    $(window).scroll(function(){
        var divScrollTop = document.documentElement.scrollTop + divTop;
        var divScrollLeft = divLeft - document.documentElement.scrollLeft/2;
        $(".pop-up-win").animate({ top: divScrollTop + "px",left: divScrollLeft + "px",},1); 
    });
    
    var winClose=$(".WinClose");
    winClose.click(function(){
		$(".pop-up-win").remove();
		$(".pop-wrap").remove();
	});

})
