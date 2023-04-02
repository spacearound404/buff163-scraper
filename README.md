# BUFF163 Scraper

[![Python: versions](
https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)]()

Collect data at BUFF163 based on a search query. It compares the reference price with the sale price, if the reference price + percentage of this price is less than the sale price, then the information about the product is written to the file.

## Features

- compare reference and sell price with percentage from reference price; 
- use buff163 rest api;
- parse data from buff163 by search keyword;
- data normalization;

## Requirements
- Python 3.x.x

## Install
1. `pip install -r requirements.txt`
2. `playwright install`

## Setup
1. Turn off Steam Guard an Steam account
2. Disable two-factor authentication an Steam account 
3. Fill out the file with keywords to search for. Each keyword/word combination on a new line. By default: `data/input.txt` 

### Setup `config.py`
| Param           |                                                                  Desc                                                                  |
|-----------------|:--------------------------------------------------------------------------------------------------------------------------------------:|
| `LOGIN_STEAM`  |                                                              login Steam                                                               |
| `PASSWORD_STEAM`    |                                                             password Steam                                                             |
| `STEAMID`            |                                                                Steam ID                                                                |
| `PATH_TO_LOGS`  |                                                          path to logs folder                                                           |
| `PAINTWEAR_QUALITY_RANGE_LIST`  |                                 paintwear quality range list (view avaliable range on buff163 website)                                 |
| `PERCETAGE_FROM_REFERENCE_PRICE`  | percentage from reference price (divide the desired percentage by 100 and set the resulting value, i.e. if 10%, then the value is 0.1) |
| `INPUT_TXT_FILE_PATH`  |                                                path to file with search keywords (.txt)                                                |
| `OUTPUT_TXT_FILE_PATH`  |                                                       path to result file (.txt)                                                       |


## Usage
Run it, enter the command:

`python main.py`

## License

SpaceAround404