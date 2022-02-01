document.addEventListener("DOMContentLoaded", function() {
    let invalid = document.querySelector("#invalid");

    if (invalid.innerHTML !== "") {
    invalid.style.visibility = "visible";
}
});