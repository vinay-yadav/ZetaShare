$('#post').change(function () {
    imagePreview(this)
})
function imagePreview(file) {
    if (file.files && file.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('image_preview').setAttribute('src', e.target.result)
        }

        reader.readAsDataURL(file.files[0]); // convert to base64 string


    }
}

function social_selected(ref) {
    console.log(ref.firstElementChild.style.color)
    if (ref.firstElementChild.style.color !== "rgb(222, 221, 219)") {
        ref.firstElementChild.style.color = "#dedddb"
        const ele = document.createElement('i')
        ele.setAttribute('class', 'bx bx-check')
        ele.setAttribute('id', 'checked')
        ref.appendChild(ele)
        console.log('if block')
    }
    else {
        console.log('else block')
        ref.firstElementChild.style.color = "#ae9033"
        ref.lastElementChild.remove()
    }
}