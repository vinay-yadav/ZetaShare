// Mailer Function
function passwordMailer(data) {
    $.ajax({
        url: data.getAttribute('data-url'),
        success: function (res) {
            alert(res.msg);
        }
    })
}