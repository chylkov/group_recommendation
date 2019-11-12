function get_public_block(json, index) {
    var container = $("<div class='media mt-3 border rounded p-2'></div>").attr("id", 'rec_' + index);
    var public_url = 'https://vk.com/public' + json.id;
    container.append($("<span class='mr-2 align-self-center'></span>").text(json.similarity.toFixed(2)));
    container.append($("<img class='public_img mr-3 align-self-center'></img>").attr('src', json.photo_50))
    container.append($("<a class='public_link mt-0 align-self-center' target='_blank' rel='noopener noreferrer'></a>").attr('href', public_url).text(json.name));
    return container
}

$("#get-recommendations-btn").click(function(btn) {
    $.get( "get_recommendations", { user_id: $('#input-link').val()}).done(function( data ) {
          $("#recommendations").html($.map(data, get_public_block));
    });
});