$(document).ready(function() {
    $('#like_btn').click(function() {
        var category_id_var;
        category_id_var = $(this).attr('data-categoryid');
        
        $.get('/rango/like_category/',
              {'category_id': category_id_var},
              function(data) {
                  $('#like_count').html(data);
                  $('#like_btn').hide();
              })
    });
});