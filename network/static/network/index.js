document.addEventListener("DOMContentLoaded", () => {
    const followButton = document.querySelector("#followButton");
    if (followButton) {
        followButton.addEventListener("click", function(event) {toggleFollow(event)}); 
    }
    const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    // edit buttons
    let editButtons = document.querySelectorAll(".editButton");
    for (i=0; i<editButtons.length; i++) {
        const editButton = editButtons[i];
        editButton.onclick = event => {
            event.preventDefault();
            editPost(event, csrf);
        };
    }

    // like buttons
    let hearts = document.querySelectorAll(".like-heart");
    for (i=0; i<hearts.length; i++) {
        const heart = hearts[i];
        const id = heart.getAttribute("name")
        heart.onclick = event => {
            event.preventDefault();
            fetch("", {
                method: "PUT",
                body: JSON.stringify({
                    id: parseInt(id)
                
                }),
                headers: {'X-CSRFToken': csrf}
            }).then(response => {
                if (response.ok) {
                    toggleLikeButton(heart)
                }
                return response.json()
            }).then(obj => {
                const counter = document.querySelector("#like-count-"+obj.id.toString());
                counter.innerHTML = obj.count;
            });
        }
    }
});

function editPost(event, csrf) {
    const id = event.target.id;
    const editButton = event.target
    const textDiv = document.querySelector("#textDiv"+id);
    const textarea = document.querySelector("#textarea"+id);
    const editTextDiv = document.querySelector("#editTextDiv"+id);
    const updateButton = document.querySelector("#updateButton"+id);
    const updateCancelButton = document.querySelector("#updateCancelButton"+id);
    textDiv.style.display = "none";
    editTextDiv.style.display = "block";
    editButton.style.display = "none"; 
    updateCancelButton.onclick = (event) => {
        textDiv.style.display = "block";
        editTextDiv.style.display = "none";
        editButton.style.display = "inline-block";
    }
    updateButton.onclick = function(event) {
        const updatedText = textarea.value
        fetch("edit", {
            method: "PUT",
            body: JSON.stringify({
                id: id,
                text: updatedText
            }),
            headers: {'X-CSRFToken': csrf}
        }).then(response => {
            if (response.ok) {
                textDiv.children[0].innerHTML = updatedText;
                textarea.innerHTML = updatedText;
                textDiv.style.display = "block";
                editTextDiv.style.display = "none";
                editButton.style.display = "inline-block";
            }
        });
    }
}

function toggleFollow(event) {
    event.preventDefault();
    const username = event.target.getAttribute("name")
    const csrf = document.getElementsByName("csrfmiddlewaretoken")
    fetch(location.origin+"/follow/"+username, {
        method: "PUT",
        headers: {'X-CSRFToken': csrf[0].value}
    }).then(response => {
        if (response.ok){
            toggleFollowButton(event.target);
        }
        return response.json()
    }).then(obj => {
        document.querySelector("#followerCount").innerHTML = "Followers: "+obj["followers"];
    });
}

function toggleFollowButton(button){
    button.classList.toggle("btn-primary");
    button.classList.toggle("btn-danger");
    if(button.innerHTML == "Follow"){
        button.innerHTML = "Unfollow";
    } else {
        button.innerHTML = "Follow";
    }
}

function toggleLikeButton(button) {
    button.classList.toggle("bi-suit-heart-fill");
    button.classList.toggle("bi-suit-heart");
}