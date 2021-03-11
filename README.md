## It's just CLI ticker parser 

This script parse tickers from https://finviz.com/screener.ashx?v=411 according to your requirements and sending to stdout.

Examples:

`python3 parser.py > tee tickers.txt > some another place`

## CLI help end args

`python3 parser.py -h` or `python3 parser.py --help` 

`python3 parser.py -c` or `python3 parser.py --cheap` for parsing chares under 10$ with my preset params.

`python3 parser.py -e` or `python3 parser.py -expensive` for parsing chares over 10$ with my preset params.

### Also you can set you own params.

1. Go to https://finviz.com/screener.ashx?v=411 and set anything you want params.
2. Copy link. 

For example:
`https://finviz.com/screener.ashx?v=411&f=an_recom_holdbetter,geo_usa,sh_price_u40,sh_short_u5,ta_averagetruerange_o1.5,ta_sma200_pb&ft=3`

3. Set this link with `-l` params.

`python3 parser.py -l https://finviz.com/screener.ashx?v=411&f=an_recom_holdbetter,geo_usa,sh_price_u40,sh_short_u5,ta_averagetruerange_o1.5,ta_sma200_pb&ft=3`

4. Enjoy!