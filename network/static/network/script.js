async function likeDislike(element) {
    await fetch(`/like/${element.dataset.id}`)
        .then(response => response.json())
        .then(data => {
            element.className = data.css_class;
            element.querySelector('small').innerHTML = data.total_likes;a
        });
}
//Receive an element and hide the post editing form.
function hideForm(element) {
    let p = document.querySelector('#post_text_' + element.dataset.id);
    let form = document.querySelector('#frm_edit_' + element.dataset.id);
    p.style.display = '';
    form.querySelector('#id_post_edit_text').value = p.innerHTML;
    form.style.display = 'none';
}
//Displays the alert message according to the return (success or error).
function alertMessage(data, alert, id) {
    let div = document.createElement('div');
    let sucess = false;
    div.setAttribute('role', 'alert');
    div.setAttribute('id', 'alert_message');
    if (document.getElementById('alert_message') == null) {
        if (data.error) {
            if (data.error.id_post_edit_text) {
                div.innerHTML = data.error.id_post_edit_text.join();
            } else {
                div.innerHTML = data.error;
            }
            div.className = 'alert alert-dismissible fade alert-danger in show';
        } else {
            sucess = true;
            document.querySelector('#post_text_' + id).innerHTML = data.text;
            div.innerHTML = "Post changed successfully!";
            div.className = 'alert alert-dismissible fade alert-success in show';
        }
    }
    alert.appendChild(div);
    var alert_message = document.getElementById('alert_message');
    setTimeout(function () {
        if (alert_message != null) {
            $(alert_message).fadeOut("fast");
            alert_message.remove();
            if (sucess) {
                document.querySelector('#frm_edit_' + id).style.display = 'none';
                document.querySelector('#post_text_' + id).style.display = '';
            }
        }
    }, 1000);
}
