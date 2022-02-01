document.addEventListener("DOMContentLoaded", function() {
    var lastUpdated = new Date(document.lastModified);
    var update = document.querySelectorAll("#update");
    for (var i = 0; i < update.length; i++) {
        update[i].innerHTML = "Retrieved On " + lastUpdated;
    }
});
