# CryptoTracker
#### Video Demo: https://youtu.be/h2aZNsKGZRw
#### Description:
##### Project Summary:
The main overaching theme surrounding my final project was to create a one-stop place for people to obtain all the information they need about cryptocurrency. Hence, I decided to build a web-based application whose main purpose is to primarily track a portfolio, although I did include other features that I believed would be useful to someone using such a tracker.

##### Project Components:
I will now explain the links that I have made as well as all the design choices that I chose to implemenent down below.

###### Index: index.html
The main page of the web-based application has been designed to intrigue users into using it. I chose to keep it clean and simple to use with few clickable buttons on the screen apart from the navbar, so that the user will not be confused on how to utilise the web-based application.

###### Live Prices: live.html
The purpose of this page was to provide the prices of the different cryptocurrencies in the market. My initial implementation was to fetch the data through python using a HTTP GET Request. However, I realised that using python to fetch the data creates a static webpage. In contrast, I wanted a page that was able to update and provide live prices and so I decided to change the code from python to javascript. Using AJAX programming, I was able to retrieve the data every few seconds without needing the page to refresh. This made it possible for me to display live prices on the page that updated frequently. However, one downside is that the API Key I used only returns new data every 30 seconds. Hence, the data retrieved and displayed is not fully live in a sense. Other than utilising a better API key, I feel that the page has turned out the way that I wanted it to.

###### News: news.html
I wanted to create a page where the user can retrieve latest updates about cryptocurrencies. During the design of the page, I decided to use python instead of javascript to request for the information as I believe that new and relevant articles are not released every second. Hence, I do not need the page to keep refreshing its data automatically, which will reduce the number of server requests that I make, and ultimately, reduce the amount of data consumed client-side.

###### Account Related Pages: login.html, register.html, username.html, password.html, forgot.html, change.html
All these pages are for account-related procedures so that the web-based application is able to track and display the portfolio that is unique to the user logged in. In the creation of the register and login page, I decided to implement a "forgot password" page that will allow the user to change his password without logging in first, in case the user forgets his password. To ensure that the user changing the password of the account is the actual owner of the account, I implemented a method of verification in the form of a date of birth which will be obtained during the registration of an account. Only after verifying with the date of birth will the user be allowed to change his password to access his portfolio. Other than this forgot password feature, I also implemented a feature to change the username and password after logging in to improve user accessibility.

###### Dashboard: dashboard.html
The main function of this page is to display all the relevant entries that the user has keyed in into the SQL database. The most important feature that this dashboard has is that it calculates the volume of gains / losses using the price that the user bought the cryptocurrency against current price of it now. It shows the user the amount of money that has been earned / lost as well as the percentage next to it. Using javascript, I was also able to code it to make it appear green and red to represent postive and negative values respectively. This allows for convenience and improves user readability. Ultimately, this dashboard allows users to view their portfolio's performance as a whole, while simultaneously allowing users to see the individual performance of each coin within the portfolio. I also created the option for users to delete the entry using the remove button located beside each entry. This is to allow users to have better visibility and control over what they choose to delete from the porfolio, rather than having to enter a new page just to remove one entry.

###### Add / Edit: add.html, edit.html
As the name suggests, the main purpose is to add entries into the database which will be displayed on the dashboard, and to edit the existing entries already in the database. I decided for the add option to create a completely new entry in the database rather than updating any existing coins as updating the database will create some discrepencies during the calculation of the profit, especially if the holdings were purchased at different times resulting in different prices. Hence, through the add option, the user will be able to track the cryptocurrency that he purchased at a given price, rather than over a range of prices. This brings in the purpose of the edit page, which is to change the holdings and the price of any existing entry, since the add option will create a completely new entry. This will give users the ability to make any amendments to the cryptocurrency that they hold. For example, if they purchase 1 bitcoin at 60000, but sell only 0.5 btc at 61000. This option allows changes to be made so that the remaining 0.5 btc can still be tracked.

###### History: history.html
This table displays all the actions that have been made by the user in relation to the dashboard. It displays all the information related to each action(add, edit and remove), which includes the change in holdings, price and value, as well as the time of the action so that the user can easily track what they had done on the account.

###### Currency Converter: currency.html
During my time dabbling in cryptocurrency, I encountered an issue or at least a minor inconvenience in exchange rates. All my crypto related portfolio is tracked in USD, but my actual transactions are in SGD. Hence, I realised the need for an exchange rate converter so that I will be able to easily convert the price in SGD to USD and vice versa. During the implementation of this, I decided to go with javascript everytime the user clicks the "convert" button so as to ensure that any exchange rate data pulled is the most updated one. Once again, I used AJAX programming and a bunch of event listeners to achieve this. Ultimately, this makes sure that whenever I want to convert my currency to another, I will get the most reliable conversion at that point in time.

##### Conclusion:
In conclusion, I have implemented the features that I believe are most essential to tracking a portfolio, into a web-based application. However, there are a few drawbacks that I have come up with.

Firstly, it is with the use of the API keys. As I am only using free API keys, the data received may not be real-time and instead 30 seconds to a full minute behind. Hence, if I am able to upgrade to a better API key, probably one that requires payment, it will be able to pull actual live data that will improve the accuracy of the data provided.

Secondly, I believe that another drawback with the web-based application is the overall user interface can be further improved through better CSS. This will greatly enhance the user friendliness of the web-based application.

Lastly, an improvement that I believe could be implemented is to be able to change the currency that the page is displayed in. Currently, all the prices and numbers are in USD, which is why I implemented the currency converter as a temporary solution. A more permanent and effective solution would be to be able to change the currency of the whole web-based application through an option. This will allow users to view the web-based application in their own respective home currencies and overall, enhance user friendliness.

Overall, the final outcome of the project has met my expectations and fulfilled all the goals and benchmarks that I had set out to accomplish. Even so, I will continue to brainstorm to come up with solutions to address all the relevant issues that I have come up with. Thank you!