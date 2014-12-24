
$(document).ready(function(){
  $('.main-wrapper').parents('body').css('background','#fff');
	$('#start_info').on("click",function(){
       	$("#startInfo").toggleClass('hidden');

	});

    $('#concluding_info').on("click",function(){
        $("#concludingInfo").toggleClass('hidden');
    });
  
  $('.delete').on("click",function(){
    return confirm ("Are you sure you want to delete ?") ;
  });
  
  $('.error-wrapper').parents('body').find('.header-wrapper').css('display','none');
  
  $.fn.center = function ()
  {
    this.css("position","fixed");
    this.css("top", ($(window).height() / 2) - (this.outerHeight() / 2));
    this.css("left", ($(window).width() / 2) - (this.outerWidth() / 2));
    return this;
  }

  $('.error-wrapper').center();
});