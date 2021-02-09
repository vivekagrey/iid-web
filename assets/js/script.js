/*global $ document */

$(document).ready(function() {
    
  $('.js--nav-icon').click(function(){
      var nav = $('.js--main-nav');
      var icon = $('.js--nav-icon span');
      nav.slideToggle(200);
      
      
      if(icon.hasClass('glyphicon glyphicon-menu-hamburger')){
          icon.removeClass('glyphicon glyphicon-menu-hamburger');
          icon.addClass('glyphicon glyphicon-remove');
          $("#logo-div").hide();
      }
      else {
          icon.removeClass('glyphicon glyphicon-remove');
          icon.addClass('glyphicon glyphicon-menu-hamburger');
          
          setTimeout(function(){
              $("#logo-div").show();
          },210);
      }
      
  });
    
  $('.js--acknow').waypoint(function(direction){
      if(direction=="down"){
          $('div.top-navi').addClass('sticky');
          
      } else {
          $('div.top-navi').removeClass('sticky');
          
      }
  });    
    
});