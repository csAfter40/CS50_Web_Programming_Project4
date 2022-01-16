document.addEventListener("DOMContentLoaded", () => {
    const followButton = document.querySelector("#followButton");
    if (followButton) {
        followButton.addEventListener("click", function(event) {toggleFollow(event)}); 
    }
    
    let hearts = document.querySelectorAll(".like-heart");
    const csrf = document.getElementsByName("csrfmiddlewaretoken");
    console.log(csrf[0].value)
    for (i=0; i<hearts.length; i++) {
        const heart = hearts[i];
        const id = heart.getAttribute("name")
        heart.onclick = event => {
            event.preventDefault();
            const csrf = document.getElementsByName("csrfmiddlewaretoken")
    
            fetch("", {
                method: "PUT",
                body: JSON.stringify({
                    id: parseInt(id)
                
                }),
                headers: {'X-CSRFToken': csrf[0].value}
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
    }).then(obj => console.log(obj));
    console.log(location.origin);
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