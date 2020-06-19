$(document).ready(function () {

    $.ajax({
        type: 'get',
        url: '/app/connected/fetch/',
        async: false,
        success: function (res) {
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
                    <input class="ml-4" type="checkbox" name="postingId" id="posting-${i}" value="${res.data[i].posting_id}" style="float:right">
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

// image compression for post now

var postNowImg
$('#form-postnow #postimg').change(function (e) {

    if (!(e.target.files[0] == undefined)) {
        $('.imageloader').css('display', 'block')
        const file = e.target.files[0]
        new ImageCompressor(file, {
            quality: 0.5,
            async: true,
            success: function (result) {
                postNowImg = result
                $('.imageloader').css('display', 'none')
            }
        })
    }
})

// image compression for singleschedule

var singleImg
$('#form-singleSchedule #postimg').change(function (e) {

    if (!(e.target.files[0] == undefined)) {
        $('.imageloader').css('display', 'block')
        const file = e.target.files[0]
        new ImageCompressor(file, {
            quality: 0.5,
            async: true,
            success: function (result) {
                singleImg = result
                $('.imageloader').css('display', 'none')
            }
        })
    }
})

// submit form
$('#form-postnow').submit(function () {
    event.preventDefault()

    let formdata = new FormData()

    if ($('#form-postnow #postimg').val() !== '') {
        formdata.append('post_img', postNowImg, postNowImg.name)

    }

    if ($('#form-postnow #postcaption').val() !== '') {
        formdata.append('post_caption', $('#postcaption').val())
    }

    for (let j = 0; j < $('#fbpages').children().length; j++) {
        if ($('#posting-' + j).is(":checked")) {
            formdata.append('app_Facebook', $('#posting-' + j).val())
        }
    }

    for (let j = $('#fbpages').children().length; j < $('#lnpages').children().length + $('#fbpages').children().length; j++) {
        if ($('#posting-' + j).is(":checked")) {
            formdata.append('app_LinkedIn', $('#posting-' + j).val())
        }
    }
    if ($('#form-postnow #postimg').val() !== '' || $('#form-postnow #postcaption').val() !== '') {
        return $.ajax({
            type: 'post',
            data: formdata,
            url: '/app/create-zets/',
            processData: false,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            },
            async: false,
            success: function (res) {
                location.reload()
            }
        })
    }
    alert('please either upload img or enter caption')



})

//  single post
$('#form-singleSchedule').submit(function () {
    event.preventDefault()
    let formdata = new FormData()
    formdata.append('schedule_date', $('#scheduledate').val())
    formdata.append('schedule_time', $('#scheduletime').val())

    if ($('#form-singleSchedule #postimg').val() !== '') {
        formdata.append('post_img', singleImg)
    }

    if ($('#form-singleSchedule #postcaption').val() !== '') {
        formdata.append('post_caption', $('#form-singleSchedule #postcaption').val())
    }

    for (let j = 0; j < $('#fbpages').children().length; j++) {
        if ($('#singleposting-' + j).is(":checked")) {
            formdata.append('app_Facebook', $('#singleposting-' + j).val())
        }
    }

    for (let j = $('#fbpages').children().length; j < $('#lnpages').children().length + $('#fbpages').children().length; j++) {
        if ($('#singleposting-' + j).is(':checked')) {
            formdata.append('app_LinkedIn', $('#singleposting-' + j).val())
        }
    }
    // console.log(formdata.getAll('app_LinkedIn'))
    // console.log(formdata.getAll('app_Facebook'))
    // console.log(formdata.get('post_img'))
    // console.log(formdata.get('post_caption'))
    // console.log(formdata.get('schedule_date'))
    // console.log(formdata.get('schedule_time'))
    if ($('#form-singleSchedule #postcaption').val() !== '') {
        return $.ajax({
            type: 'post',
            data: formdata,
            url: '/app/create-zets/',
            processData: false,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            },
            success: function (res) {
                location.reload()
            }
        })
    }
    alert('please either upload img or enter caption')

})


// let formdata = {
//     app_Facebook: [],
//     app_LinkedIn: [],
// }

// if ($('#form-postnow #postimg').val() !== '') {
//     formdata.post_img = postNowImg
//     console.log(postNowImg)
// }

// if ($('#form-postnow #postcaption').val() !== '') {
//     formdata.post_caption = $('#postcaption').val()
// }

// for (let j = 0; j < $('#fbpages').children().length; j++) {
//     if ($('#posting-' + j).is(":checked")) {
//         formdata.app_Facebook.push($('#posting-' + j).val())
//     }
// }

// for (let j = $('#fbpages').children().length; j < $('#lnpages').children().length + $('#fbpages').children().length; j++) {
//     if ($('#posting-' + j).is(":checked")) {
//         formdata.app_LinkedIn.push($('#posting-' + j).val())
//     }
// }
// console.log(formdata)