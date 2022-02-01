// Fetch the crypto data and store it

var ajax = new XMLHttpRequest();

ajax.open("GET", "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd", false);
ajax.send(null);
let data = JSON.parse(ajax.responseText);

var cryptocurrencies;
var timerId;
const updateInterval = 1500;


// Function to convert the long integers into Millions(M), Billions(B), Trillions(T)
function convert(number) {
    number = Math.round(number);
    if (number < 1000000) {
        return number;
    }
    else if (number < 1000000000) {
        return (number / 1000000).toFixed(2) + 'M';
    }
    else if (number < 1000000000000) {
        return (number / 1000000000).toFixed(2) + 'B';
    }
    else {
        return (number / 1000000000000).toFixed(2) + 'T';
    }
}



// Function to return the required attribute from the cryptocurrency data so that can we can replace it
function retrieveAttribute(data, attributeName, name) {
    for (var x in data) {
        if (data[x].name == name) {
            return data[x][attributeName];
        }
    }
    return null;
}


// Function to retrieve new data
function fetchNewData() {
    // Get the new data via another http request
    var newAjax = new XMLHttpRequest();

    newAjax.open("GET", "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd", false);
    newAjax.send(null);
    let newData = JSON.parse(newAjax.responseText);

    // Iterate through the array of cryptocurrencies and then update the attributes that change
    for (let i = 0; i < cryptocurrencies.length; i++) {
        let cryptocurrency = cryptocurrencies[i];
        // Price
        cryptocurrency.price = retrieveAttribute(newData, 'current_price', cryptocurrency.name);
        cryptocurrency.$item.find(".price").text('$' + cryptocurrency.price);
        // Price change in 24h
        cryptocurrency.percentage_change_24h = retrieveAttribute(newData, 'price_change_percentage_24h', cryptocurrency.name);
        cryptocurrency.$item.find(".percentage_change_24h").text(cryptocurrency.percentage_change_24h.toFixed(2) + "%");
        // Total Volume
        cryptocurrency.volume_24h = retrieveAttribute(newData, 'total_volume', cryptocurrency.name);
        cryptocurrency.$item.find(".volume_24h").text('$' + convert(cryptocurrency.volume_24h));
    }

    console.log('Successfully fetched new data');
}


// Function to change the table
function resetBoard() {
    var $list = $("#cryptocurrencies");
    $list.find(".cryptocurrency").remove();

    if (timerId !== undefined) {
        clearInterval(timerId);
    }

    cryptocurrencies = [];
    for (let i = 0; i < 100; i++) {
        cryptocurrencies.push(
            {
                name: data[i].name,
                image: data[i].image,
                symbol: data[i].symbol,
                price: data[i].current_price,
                market_cap: data[i].market_cap,
                circulating_supply: data[i].circulating_supply,
                volume_24h: data[i].total_volume,
                percentage_change_24h: data[i].price_change_percentage_24h,
            }
        );
    }
    for (let i = 0; i < cryptocurrencies.length; i++) {
        let $item = $(
            "<tr class='cryptocurrency'>" +
                "<th class='rank'>" + (i + 1) + "</th>" +
                "<td class='name'>" + "<img src='" + cryptocurrencies[i].image + "' alt='" + cryptocurrencies[i].name + "'height='28px' width='28px'>  <b>" + cryptocurrencies[i].name + "</b></td>" +
                "<td class='symbol'>" + cryptocurrencies[i].symbol + "</td>" +
                "<td class='price'>" + "$" + cryptocurrencies[i].price + "</td>" +
                "<td class='market_cap'>" + "$" + convert(cryptocurrencies[i].market_cap) + "</td>" +
                "<td class='circulating_supply'>" + convert(cryptocurrencies[i].circulating_supply) + "</td>" +
                "<td class='volume_24h'>" + "$" + convert(cryptocurrencies[i].volume_24h) + "</td>" +
                "<td class='percentage_change_24h'>" + cryptocurrencies[i].percentage_change_24h.toFixed(2) + "%" + "</td>" +
            "</tr>"
        );
        cryptocurrencies[i].$item = $item;
        $list.append($item);
    }
    // Fetch the new data
    timerId = setInterval("fetchNewData()", updateInterval);
}

resetBoard();