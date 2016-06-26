# zillowscraper
![MIT License](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/)
##### Multi-threaded Zillow scraper that retrieves and parses all agents in a given state.
Note: zillowscraper is an educational tool that demonstrates how one might retrieve real-estate agents from Zillow. This tool only saves the information of a Zillow agent when an email address can be located on their personal website.  The rest are discarded.<br>
#### Usage Example:
-
Getting agents in California
```console
python zillow.py California
```
Agents are saved in <zip code>.xlxs for each zip code in the state. This tool can be closed and restarted, and scraping will resume on the last zip code.<br>

-
#### Example output in an xlxs file:
```
Maria Casas	Buyer Seller	Coldwell Banker Beachside	"19671 Beach Blvd
Huntington Beach, CA 92648"	(714) 402-6047	Maria.Casas@Coldwellbanker.com		
Michael Henderson	Seller	Keller Williams 	"16820 Ventura Blvd.
Encino, CA 91436"	(818) 307-5017	michael@myagentmichael.com		
Maribel Munoz	Buyer Seller	RE/MAX 	"Los Angeles 
Los Angeles, CA 90032"	(626) 414-5255	Maribelsellshomes@gmail.com		
Michelle T. Crane	Buyer Seller	Crane & Co Realty International	"11812 San Vicente Blvd Ste 100
Los Angeles, CA 90049"	(844) 326-7045	mcrane@kw.com		
Michelle Rivera	Buyer Seller	Z Realty	"10918 Hesperia Rd. Suite A1
Hesperia, CA 92345"	(760) 933-4072	highdeserthomes@yahoo.com		
Nick Astrupgaard	Buyer Seller	Brock Real Estate	"2235 Hyperion Ave
Los Angeles, CA 90027"	(323) 486-2418	nastrupgaard@gmail.com		
Natalya Shcherbatyuk	Buyer Seller	Champion Realty	"1701 Truman St. #1
Los Angeles, CA 91340"	(818) 451-5057	natalya@championrealty4u.com		
Ryan Shaw	Buyer Seller	Teles Properties	"129 Gull St.
Manhattan Beach, CA 90266"	(855) 534-5921	ryan.shaw@telesproperties.com		
Scott McCain	Buyer Seller	Palm Realty Boutique	"401 Manhattan Beach Blvd. Suite B
Manhattan Beach, CA 90266"	(310) 648-9624	scottamccain@gmail.com		
Samira Kermani	Buyer Seller	Karlton Stone	"9663 Santa Monica Blvd Suite 709
Beverly Hills, CA 90210"	(310) 488-7870	Consult@KarltonStone.com		
```
-
#### Dependencies
zillowscraper uses the BeautifulSoup module. To install BeautifulSoup in command line via pip:
```console
pip install beautifulsoup4
```
