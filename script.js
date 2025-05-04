//Light & Dark Mode 
lightMode = document.getElementById("LightSwitch");
darkMode = document.getElementById("DarkSwitch");
textQuery = document.getElementById("textQuery");
paperPlaneIcon = document.getElementById("paperPlaneIcon");
queryContainer = document.querySelector(".queryContainer");
body = document.querySelector("body");

function applyTheme(theme){ // Goes to dark Mode
    if(theme === 'dark'){
        lightMode.classList.add("hideVisibility");
        darkMode.classList.remove("hideVisibility");
        body.classList.add("darkModeBody");
    
        document.querySelectorAll(".inputContainer").forEach(container => {
            container.classList.add("darkModeInputContainer");
        });
    
        document.querySelectorAll(".responseContainer").forEach(container => {
            container.classList.add("darkModeResponseContainer");
        });
    
        document.querySelectorAll(".inputText, .responseText,.touriticityRating,.cntyVibesWords").forEach(text => {
            text.classList.add("darkModeText");
        });
    
        queryContainer.classList.add("darkModeInputContainer");
        paperPlaneIcon.classList.add("darkModePaperPlane");
    
        textQuery.style.backgroundColor = "rgb(34, 68, 122)";
        textQuery.style.color = "rgb(226, 222, 222)";
        paperPlaneIcon.style.color= "rgb(226,222,222)";
    }
    if(theme === 'light'){ // Goes to light mode
        darkMode.classList.add("hideVisibility");
        lightMode.classList.remove("hideVisibility");
        body.classList.remove("darkModeBody");
        
        document.querySelectorAll(".inputContainer").forEach(container => {
            container.classList.remove("darkModeInputContainer");
        });
        
        document.querySelectorAll(".responseContainer").forEach(container => {
            container.classList.remove("darkModeResponseContainer");
        });
        
        document.querySelectorAll(".inputText, .responseText,.touriticityRating,.cntyVibesWords").forEach(text => {
            text.classList.remove("darkModeText");
        });
            
        
        queryContainer.classList.remove("darkModeInputContainer");
        textQuery.classList.remove("darkModeInputContainer");
        paperPlaneIcon.classList.remove("darkModePaperPlane");
        
        textQuery.style.backgroundColor = "#f5f5f5";
        textQuery.style.color = "rgb(161, 161, 161)";
        paperPlaneIcon.style.color= "rgb(148, 145, 145)";
    }
}
lightMode.addEventListener("click",function(){//Turn into darkmode
    localStorage.setItem('theme','dark');
    const theme = localStorage.getItem('theme');
    applyTheme(theme);
});
    
darkMode.addEventListener("click",function(){
    localStorage.setItem('theme', 'light');
    const theme = localStorage.getItem('theme');
    applyTheme(theme); 
});
document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem('theme') || 'light'; // fallback to light
    applyTheme(savedTheme);
});

function bottom() {
    document.getElementById( 'scrollToBottom' ).scrollIntoView();
};




// Set up a MutationObserver to detect when .starRating elements are added
const observer = new MutationObserver(() => {
    observer.disconnect();  // Prevent infinite loop
    renderStars();          
    observer.observe(document.body, { childList: true, subtree: true }); // Reconnect
});

observer.observe(document.body, { childList: true, subtree: true });

//Rendering stars
function renderStars() {
    const starRatings = document.querySelectorAll(".starRating");
    bottom();

    for (let i = 0; i < starRatings.length; i++) {
        const starRating = starRatings[i];
        const rawValue = starRating.getAttribute("data-stars");

        // Parse the array and extract the first value
        let parsedArray;
        parsedArray = JSON.parse(rawValue);
     

        const starValue = parseFloat(parsedArray[0]);
        
       
        const fullStars = Math.floor(starValue);
        const halfStar = starValue % 1 >= 0.25 && starValue % 1 < 0.75;
        const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

        starRating.innerHTML = "";

        for (let j = 0; j < fullStars; j++) {
            const full = document.createElement("i");
            full.className = "fa-solid fa-star";
            starRating.appendChild(full);
        }

        if (halfStar) {
            const half = document.createElement("i");
            half.className = "fa-solid fa-star-half-stroke";
            starRating.appendChild(half);
        }

        for (let j = 0; j < emptyStars; j++) {
            const empty = document.createElement("i");
            empty.className = "fa-regular fa-star";
            starRating.appendChild(empty);
        }
    }
    
    
    
}




//Import the stars data from python
document.addEventListener("DOMContentLoaded", () => {
    let hasRendered = false; // Flag to prevent double execution

    const observer = new MutationObserver((mutationsList) => {
        if (hasRendered) return;

        for (const mutation of mutationsList) {
            if (mutation.type === "childList") {
                const targetNode = document.querySelector("#starRating");
                if (targetNode) {
                    const starsData = JSON.parse(targetNode.getAttribute("data-stars"));
                    renderStars()

                    hasRendered = true;
                    observer.disconnect();  // Stop observing after first render
                    break; // Exit loop once found
                }
            }
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
