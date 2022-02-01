document.addEventListener("DOMContentLoaded", function() {
    information = document.querySelector("#information");

    if (information.innerHTML != "") {
        information.style.visibility = "visible";
    }
});