
function like_post(postId) {
    const icon = document.getElementById(postId);
    icon.classList.toggle('active');
    // is there error handling for fetch?
    fetch(`/like/${postId}`)
        .then(response => response.json())
        .then(result => {
            const count = result.count;
            document.getElementById(`count` + postId).innerHTML = count + " likes";
        })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}

function edit_post(postId) {
    var editButton = document.getElementById(`edit` + postId); //get edit button
    //replace the content with textarea
    var content = document.getElementById(`text` + postId);
    var textarea = document.createElement('textarea');
    var postDate = document.getElementById(`date` + postId).innerHTML;
    textarea.value = content.innerHTML;
    textarea.rows = "3";
    textarea.cols = "80";
    textarea.id = 'textarea-' + postId;
    content.parentNode.replaceChild(textarea, content);
    // Add a save button and a cancel button to the card footer
    var saveButton = document.createElement('button');
    saveButton.innerHTML = 'Save';
    saveButton.className = 'btn btn-primary'
    saveButton.id = 'save' + postId;
    saveButton.addEventListener('click', () => {
        console.log(postId);
        const new_content = document.getElementById(`textarea-` + postId);
        if (new_content.value.trim() === '') {
            alert('Textarea cannot be empty!');
            return;
        }
        fetch(`/edit/${postId}`, {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            body: JSON.stringify({
                new_content: new_content.value
            })
        })
            .then(response => response.json())
            .then(result => {
                update_edit(postId, result.date, result.content)
                saveButton.parentNode.removeChild(cancelButton)
                saveButton.parentNode.replaceChild(editButton, saveButton)
            })
    })
    editButton.parentNode.replaceChild(saveButton, editButton);
    var cancelButton = document.createElement('button');
    cancelButton.innerHTML = 'Cancel';
    cancelButton.className = 'btn btn-primary'
    cancelButton.addEventListener('click', () => {
        update_edit(postId, postDate, content.innerHTML);
        cancelButton.parentNode.removeChild(saveButton)
        cancelButton.parentNode.replaceChild(editButton, cancelButton)
    })
    saveButton.parentNode.appendChild(cancelButton);
}

//easy way to revert everything back ?

function update_edit(postId, date, content) {

    var textarea = document.getElementById(`textarea-` + postId);
    var newContent = document.createElement('p');
    newContent.className = 'card-text';
    newContent.id = 'text' + postId;
    newContent.innerHTML = content;
    textarea.parentNode.replaceChild(newContent, textarea);
    var newDate = document.getElementById(`date` + postId);
    newDate.innerHTML = date
}

function user_follow(userId) {
    const btn = document.getElementById(`follow-btn` + userId);
    var status = btn.innerHTML;
    if (status === "Follow") {
        btn.innerHTML = "Unfollow"
    } else {
        btn.innerHTML = "Follow"
    }
    // is there error handling for fetch?
    fetch(`/follow/${userId}`)
        .then(response => response.json())
        .then(result => {
            console.log(result)
            follower_count = result.followers_count
            document.getElementById(`follower` + userId).innerHTML = `<strong>Followers:</strong> ${follower_count}`;
        })
}

// //update the followers following count for Friend db


