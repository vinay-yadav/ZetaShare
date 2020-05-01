// nav active class

$(function () {
    $('#app-nav li a').click(function () {
        $("#app-nav li.active").removeClass('active')
        $('#app-nav li a').filter(function () {
            if ($(this).attr('href') == location.pathname) {
                $(this).parent().addClass('active')
            }
        })

    })
})

function slidertoggle() {

    $('.login-sidebar').toggle('slow')
}

// switch forms

$('#login').click(function () {
    $('.signup-user').hide()
    $('.auth-data').show()

})
$('#signup').click(function () {
    $('.auth-data').hide()
    $('.signup-user').show()

})