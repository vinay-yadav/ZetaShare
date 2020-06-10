$(document).ready(function () {

    $.ajax({
        type: 'get',
        url: '/app/connected/fetch/',
        async: false,
        success: function (res) {
            console.log(res)
            for (let i = 0; i < res.data.length; i++) {
                if (res.data[i].provider === 'Facebook') {

                    $('#form-postnow .fbpages').append(`<div class="page">
                    <label for="posting-${i}" style="font-weight: 700;width:100px;overflow:hidden; font-family: sans-serif;font-size: 12px;letter-spacing: 0.4px;">${res.data[i].page_name}</label>
                    <input class="ml-4" type="checkbox" name="postingId" id="posting-${i}" value="${res.data[i].posting_id}" style="float:right">
                </div> `)

                    $('#form-singleSchedule .fbpages').append(`<div class="page">
                    <label for="singleposting-${i}" style="font-weight: 700;width:100px;overflow:hidden; font-family: sans-serif;font-size: 12px;letter-spacing: 0.4px;">${res.data[i].page_name}</label>
                    <input class="ml-4" type="checkbox" name="postingId" id="singleposting-${i}" value="${res.data[i].posting_id}" style="float:right">
                </div> `)
                }
                if (res.data[i].provider === 'LinkedIn') {
                    $('#form-postnow .lnpages').append(`<div class="page">
                    <label for="posting-${i}" style="font-weight: 700;width:100px;overflow:hidden; font-family: sans-serif;font-size: 12px;letter-spacing: 0.4px;">${res.data[i].page_name}</label>
                    <input class="ml-4" type="checkbox" name="postingId" id="posting-${i}" value="posting-${i}" style="float:right">
                </div> `)

                    $('#form-singleSchedule .lnpages').append(`<div class="page">
                    <label for="singleposting-${i}" style="font-weight: 700;width:100px;overflow:hidden; font-family: sans-serif;font-size: 12px;letter-spacing: 0.4px;">${res.data[i].page_name}</label>
                    <input class="ml-4" type="checkbox" name="postingId" id="singleposting-${i}" value="${res.data[i].posting_id}" style="float:right">
                </div> `)
                }
            }
        }
    })
})

function pagedropdown(data) {
    event.stopPropagation()
    if (!$(data).next().hasClass('show')) {
        $('.pages-dropdown').removeClass('show')
    }
    $(data).next().toggleClass('show')
}


// image compression
function compressedImg(formdata) {
    const file = document.getElementById('postimg').files[0]
    new ImageCompressor(file, {
        quality: 0.8,
        success: function (result) {

            formdata.post_img = result

        }
    })

}


// submit form
$('#form-postnow').submit(function () {
    event.preventDefault()
    let formdata = {
        app_Facebook: [],
        app_LinkedIn: [],
    }

    if ($('#postimg').val() !== '') {
        compressedImg(formdata)
    }

    if ($('#postcaption').val() !== '') {
        formdata.post_caption = $('#postcaption').val()
    }

    for (let j = 0; j < $('#fbpages').children().length; j++) {
        if ($('#posting-' + j).is(":checked")) {
            formdata.app_Facebook.push($('#posting-' + j).val())
        }
    }

    for (let j = $('#fbpages').children().length; j < $('#lnpages').children().length + $('#fbpages').children().length; j++) {
        if ($('#posting-' + j).is(":checked")) {
            formdata.app_LinkedIn.push($('#posting-' + j).val())
        }
    }

    console.log(formdata)
    $.ajax({
        type: 'post',
        data: formdata,
        url: '/app/create-zets/',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        async: false,
        success: function (res) {
            // after submit code
        }
    })
})

//  single post
$('#form-singleSchedule').submit(function () {
    event.preventDefault()
    let formdata = {
        schedule_date: $('#scheduledate').val(),
        schedule_time: $('#scheduletime').val(),
        app_Facebook: [],
        app_LinkedIn: []
    }
    if ($('#postimg').val() !== '') {
        compressedImg(formdata)
    }

    if ($('#postcaption').val() !== '') {
        formdata.post_caption = $('#postcaption').val()
    }

    for (let j = 0; j < $('#fbpages').children().length; j++) {
        if ($('#singleposting-' + j).is(":checked")) {
            formdata.app_Facebook.push($('#singleposting-' + j).val())
        }
    }

    for (let j = $('#fbpages').children().length; j < $('#lnpages').children().length + $('#fbpages').children().length; j++) {
        if ($('#singleposting-' + j).is('checked')) {
            formdata.app_LinkedIn.push($('#singleposting-' + j).val())
        }
    }
    console.log(formdata)
    $.ajax({
        type: 'post',
        data: formdata,
        url: '/app/create-zets/',
        async: false,
        success: function (res) {
            // after submit code
        }
    })
})