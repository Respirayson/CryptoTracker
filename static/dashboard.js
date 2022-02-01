document.addEventListener("DOMContentLoaded", function () {
    // Get the last updated data
    document.querySelector("#lastUpdated").innerHTML = "Last Updated On " + Date();

    // Change the colour of the percentage and the profits
    profits = document.querySelectorAll(".profit");
    for (var i = 0; i < profits.length; i++) {
        if (parseFloat(profits[i].innerHTML) < 0) {
            profits[i].style.color = "red";
            profits[i].innerHTML = "-$" + Math.abs(profits[i].innerHTML);

        } else if (parseFloat(profits[i].innerHTML) > 0){
            profits[i].style.color = "green";
            profits[i].innerHTML = "$" + Math.abs(profits[i].innerHTML);
        } else {
            profits[i].innerHTML = "$" + profits[i].innerHTML;
        }
    }

    percentage = document.querySelectorAll(".percentage");
    for (var i = 0; i < percentage.length; i++) {
        if (parseFloat(percentage[i].innerHTML) < 0) {
            percentage[i].style.color = "red";
            percentage[i].innerHTML = "-" + Math.abs(percentage[i].innerHTML) + "%";

        } else if (parseFloat(percentage[i].innerHTML) > 0) {
            percentage[i].style.color = "green";
            percentage[i].innerHTML = "+" + Math.abs(percentage[i].innerHTML) + "%";
        } else {
            percentage[i].innerHTML = percentage[i].innerHTML + "%";
        }
    }

    totalProfits = document.querySelectorAll(".totalProfits");
    for (var i = 0; i < totalProfits.length; i++) {
        if (parseFloat(totalProfits[i].innerHTML) < 0) {
            totalProfits[i].style.color = "red";
            totalProfits[i].innerHTML = "<b>-$" + Math.abs(totalProfits[i].innerHTML) + "</b>";
        } else if (parseFloat(totalProfits[i].innerHTML) > 0) {
            totalProfits[i].style.color = "green";
            totalProfits[i].innerHTML = "<b>$" + Math.abs(totalProfits[i].innerHTML) + "</b>";
        } else {
            totalProfits[i].innerHTML = "<b>$" + totalProfits[i].innerHTML + "</b>";
        }
    }

    totalPercentage = document.querySelectorAll(".totalPercentage");
    for (var i = 0; i < totalPercentage.length; i++) {
        if (parseFloat(totalPercentage[i].innerHTML) < 0) {
            totalPercentage[i].style.color = "red";
            totalPercentage[i].innerHTML = "<b>-" + Math.abs(totalPercentage[i].innerHTML) + "%</b>";
        } else if (parseFloat(totalPercentage[i].innerHTML) > 0) {
            totalPercentage[i].style.color = "green";
            totalPercentage[i].innerHTML = "<b>+" + Math.abs(totalPercentage[i].innerHTML) + "%</b>";
        } else {
            totalPercentage[i].innerHTML = "<b>" + totalPercentage[i].innerHTML + "%</b>";
        }
    }
})