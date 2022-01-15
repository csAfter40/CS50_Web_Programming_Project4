document.addEventListener("DOMContentLoaded", () => {
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

function toggleLikeButton(button) {
    button.classList.toggle("bi-suit-heart-fill");
    button.classList.toggle("bi-suit-heart");
}