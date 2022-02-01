const api = "https://api.exchangerate-api.com/v4/latest/USD";

var convertButton = document.querySelector(".convert");
var amountBox = document.querySelector("#amountConvert");
var boxFrom = document.querySelector(".from");
var boxTo = document.querySelector(".to");
var amountToConvert;
var currencyFrom;
var currencyTo;

// Function to reload the window on click
function clearValue() {
    window.location.reload();
    document.querySelector(".finalValue").innerHTML = "";
}


// Function to convert one currency to another currency using a exchange rate data
function convertCurrency(data, fromCurrency, toCurrency, amount) {
    var fromRates = data[fromCurrency];
    var toRates = data[toCurrency];

    var finalAmount = (amount * (toRates / fromRates)).toFixed(2);
    return finalAmount;
}


boxFrom.addEventListener("change", function(event) {
    currencyFrom = event.target.value;
});

boxTo.addEventListener("change", function(event) {
    currencyTo = event.target.value;
});

convertButton.addEventListener("click", function() {
    if (currencyFrom === undefined) {
        alert("Select Currency to Convert From");
        return;
    }
    if (currencyTo === undefined) {
        alert("Select Currency to Convert To");
        return;
    }


    amountToConvert = amountBox.value;

    fetch(api).then(response => response.json()).then(data => {
        console.log("Successfully fetched exchange rate data");
        let finalValue = convertCurrency(data.rates, currencyFrom, currencyTo, amountToConvert);
        document.querySelector(".finalValue").innerHTML = "<b>" + finalValue + " " + currencyTo +"</b>";
    });
})