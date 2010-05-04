// JavaScript Document
function get_popup(url){
    $.get(url, function(data) {
        $("#pop-pu").append(data);
    }); 
      
	var docHeight=$(document).height();
	//$(".pop-up-win").fadeIn("fast");
	//$(".pop-wrap").show().height(docHeight);
	$(".pop-wrap").height(docHeight);
	
    var divWidth=$(".pop-up-win").width()/2;
    var divHeight=$(".pop-up-win").height()/2;
    var divLeft =  document.documentElement.clientWidth/2 - divWidth;
    var divTop =  document.documentElement.clientHeight/2 - divHeight/2;
    $(".pop-up-win").css({"left":divLeft,"top":divTop});
    
    $('.WinClose').click(function(){
        $(".pop-up-win").hide();
    	$(".pop-wrap").hide();
    });
    
    $(window).scroll(function(){
        var divScrollTop = document.documentElement.scrollTop + divTop -40;
        var divScrollLeft = divLeft - document.documentElement.scrollLeft/2;
        $(".pop-up-win").animate({ top: divScrollTop + "px",left: divScrollLeft + "px",},-100); 
    });
    
    
}
