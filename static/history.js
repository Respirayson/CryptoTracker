function convertUTCDateToLocalDate(date) {
    var newDate = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);

    var offset = date.getTimezoneOffset() / 60;
    var hours = date.getHours();

    newDate.setHours(hours - offset);

    return newDate;
}

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".timestamp").forEach(timestamp => {
        timestamp.innerHTML = convertUTCDateToLocalDate(new Date(timestamp.innerHTML));
    });

    document.querySelectorAll(".type").forEach(type => {
        if (type.innerHTML === "ADD") {
            type.style.color = "green";
        } else if (type.innerHTML === "REMOVE") {
            type.style.color = "red";
        } else {
            type.style.color = "blue";
        }
    });
});