function get_popup(url){
$.get(url, function(data) {
    $("#pop-up").append(data);
      
    var docHeight=$(document).height();
    var docWidth=$(document).width();
    $(".pop-up-win").fadeIn("fast");
    $(".pop-wrap").show().height(docHeight).width(docWidth);
	
    var divWidth=$(".pop-up-win").width()/2;
    var divHeight=$(".pop-up-win").height()/2;
    var divLeft =  document.documentElement.clientWidth/2 - divWidth;
    var divTop =  document.documentElement.clientHeight/2 - divHeight/2 -100;
    var divScrollLeft = divLeft - document.documentElement.scrollLeft/2;
    var divScrollTop = document.documentElement.scrollTop + divTop;
    $(".pop-up-win").css({"left":divScrollLeft,"top":divScrollTop});
    
    $('.WinClose').click(function(){
       $(".pop-up-win").remove();
       $(".pop-wrap").hide();
    });
    
    $(window).scroll(function(){
        var divScrollLeft = divLeft - document.documentElement.scrollLeft/2;
        var divScrollTop = document.documentElement.scrollTop + divTop;
        $(".pop-up-win").animate({ top: divScrollTop + "px",left: divScrollLeft + "px"},-100); 
    });
    
}); 
}
