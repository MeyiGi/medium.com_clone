// AJAX LIKING

function like(post_id) {
    likesCount = document.getElementById(`likes-count-${post_id}`);
    likeButton = document.getElementById(`like-button-${post_id}`);

    fetch(`/like-post/${post_id}`, { method : "POST" })
        .then((res) => res.json())
        .then((data) => {
            likesCount.innerHTML = data["likes-count"];
            if (data["liked"]) {
                likeButton.className="fa-solid fa-thumbs-up" 
            } else {
                likeButton.className="fa-regular fa-thumbs-up"
            }
        }); 
}

// COMMENT DROPDOWN

document.addEventListener("DOMContentLoaded", function() {
    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach( dropdown => {
        const dropdownBtn = dropdown.querySelector(".dropdownBtn");
        const dropdownContent = dropdown.querySelector(".dropdown-content");

        dropdownBtn.addEventListener("click", function() {
            dropdownContent.classList.toggle("show");
        });

        document.addEventListener("click", function() {
            if (!dropdown.contains("show")) {
                dropdownContent.classList.remove("show")
            }
        });
    });

    document.addEventListener("click", function(event) {
        dropdowns.forEach( dropdown => {
            if (!dropdown.contains(event.target)) {        
                const dropdownContent = dropdown.querySelector(".dropdown-content");
                const dropdownBtn = dropdown.querySelector(".dropdownBtn");
                dropdownContent.classList.remove("show");
            }
        })
    })
});

// STICKY SIDEBAR

let sidebar         = document.getElementsByClassName("sidebar")[0]
let sidebar_content = document.getElementsByClassName("content-wrapper")[0]

window.onscroll = () => {
    let scrollTop      = window.scrollY;
    let viewportHeight = window.innerHeight;
    let sidebarTop     = sidebar.getBoundingClientRect().top + window.pageYOffset
    let contentHeight  = sidebar_content.getBoundingClientRect().height;

    if (scrollTop >= contentHeight - viewportHeight + sidebarTop) {
        sidebar_content.style.transform = `translateY(-${contentHeight - viewportHeight + sidebarTop}px)`
        sidebar_content.style.position =  `fixed`
    } else {
        sidebar_content.style.transform = ``
        sidebar_content.style.position =  ``
    }
}