
$(document).ready(function(){

    $.ajax({
        type: 'get',
        url: '/app/connected/fetch/',
        async: false,
        success: function(res) {
            for(let i=0;i<res.data.length;i++){
                if(res.data[i].provider==='Facebook'){
                    
                    $('.fbpages').append(`<div class="page">
                    <label for="${res.data[i].posting_id}" style="font-weight: 700;width:100px;overflow:hidden; font-family: sans-serif;font-size: 12px;letter-spacing: 0.4px;">${res.data[i].page_name}</label>
                    <input class="ml-4" type="checkbox" name="postingId" id="${res.data[i].posting_id}" value="${res.data[i].posting_id}" style="float:right">
                </div> `)
                }
                if(res.data[i].provider ==='LinkedIn'){
                    $('.lnpages').append(`<div class="page">
                    <label for="${res.data[i].posting_id}" style="font-weight: 700;width:100px;overflow:hidden; font-family: sans-serif;font-size: 12px;letter-spacing: 0.4px;">${res.data[i].page_name}</label>
                    <input class="ml-4" type="checkbox" name="postingId" id="${res.data[i].posting_id}" value="${res.data[i].posting_id}" style="float:right">
                </div> `)
                }
            }
        }
    })
})

function pagedropdown(data){
    event.stopPropagation()
    if(!$(data).next().hasClass('show')){
        $('.pages-dropdown').removeClass('show')
    }
    $(data).next().toggleClass('show')
}