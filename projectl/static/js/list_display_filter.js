$(document).ready(function(){

    $(".filter-button").click(function(e){
      e.preventDefault();

      var value = $(this).attr('data-filter');

      $(".filter").not('.'+value).hide();
      $('.filter').filter('.'+value).show(500);
    });

    // Set active link for filter sidebar
    var selector = ".nav a";
    $(selector).on('click', function(){

      $(selector).removeClass('active');
      $(this).addClass('active');

    });

});

$('body').click('a[href="#"]', function(e) {e.preventDefault() });
