$(function(){
	$('form').addClass('ui form');
    $('input[type="checkbox"]').wrap("<div class='ui toggle checkbox'></div>");
    $('input[type="submit"]').addClass("ui large primary button");

    $('#register-btn').addClass("ui labeled icon large basic green button")
                      .prepend("<i class='pencil icon'></i>");


    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox();

    $('.ui.message').click(function(){
    	$(this).slideUp();
    })

    // $('.sidebar-toggle').sidebar('toggle');
});