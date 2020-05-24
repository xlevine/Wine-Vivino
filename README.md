# Wine_Analysis
An analysis of wines sold in France (2020)

## Production and Consumption of Wines in France

- In 2017 in France, there were 46,600 vineyards producing AOP (Appellation d’Origine Contrôlée) wines, which covered 446,588 ha of land.

- AOP represents ⅔ of all wine produced in France.

- A french person drinks about 60 wine bottles per year on average (60% red, 23% rosé, 17% white).

- About 60% of the wine produced in France is consumed there.

- Wine production in 2017 generated over 11,2bn euros, i.e. about 16 % of the total value of french agriculture.

![Image description](https://github.com/xlevine/Wine_Analysis/blob/master/plots/carte_vin_france_petit.jpg)

- Main regions of AOP production: (1) Alsace, (2) Bordeaux, (4) Bourgogne, (6) Champagne, (9) Languedoc-Roussillon, (12) Provence, (11) Val de Loire, (14) Vallée du Rhône

## Database and methodology

- Vivino.com is an online marketplace and rating app for wine founded in 2010 and headquartered in San Francisco.

- Its database contains more than 10 million wines.

![Image description](https://github.com/xlevine/Wine_Analysis/blob/master/plots/Vivino_screen.png)

Using a web scraping tool (Selenium) compatible with Python3, we extract the following data:

- Country, Region, and Estate name

- Robe (red, wine, sparkling, rose) & Vintage (year)

- Ratings (0 to 5 scale) & number of reviews

- Price of sale

For more details on how the data was scrapped, please refer to script [web_scrapping.py](https://github.com/xlevine/Wine_Analysis/blob/master/web_scraping.py)


