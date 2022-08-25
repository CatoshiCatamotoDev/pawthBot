# PawthereumStatBots
The goal of this repo is to create a framework from which engaging bots can be made (twitter, telegram, ...).
The bots can then use the generated data to tweet interesting statistics about Pawthereum, post regular updates in Telegram channels or respond to requests...
The goal is to gather as many interesting statistics as possible that can then be distributed.

This is a public & open source repo. Feel free to add any functionality, comments, ...

Inspiration for this repo comes from https://twitter.com/SafeMoonNewsBot. Make sure to give this cool bot a follow.

## Statistics
Some statistics that are calculated:
 - Historical $PAWTH prices

### Holder Statistics
 - How many holders are there?
 - How is the token distribution?
 - What actions do the whales make?

 #### Thresholds
 - Threshold values (how much $PAWTH do I need to enter the top x?)
 e.g.:
```
(Top 10 - )
See here:
Pawthereum whale dominance 🐳 
Total circulating supply:
123,000,000 $PAWTH

Top 10: 123.456 M (1%)
Top 100: 123.456 M (9%)
Top 1000: 123.456 M (90%)
```

### Social Media
#### Twitter
 - Keep track of updates of the official Pawthereum twitter account (@Pawthereum) and report any changes.
 - ...

#### Telegram
 - ...

### Buys/Sells
 - Keep track of on-chain buys and report big buys.

## How to use
Make sure you have a recent version of Python on your machine. It could be that you have to install some packages to meet all dependencies.
```
python pawthBot.py
```

A few notes:
 - By default the twitter authentication keys are not provided. Running this code out of the box will just print anything that would be tweeted in the terminal prompt.

  - You can set up your own twitter account and fill in the authentication keys in a file authentication_keys.py. The template is provided in ```authentication_keys_template.py```.



## TODO
This bot is brand new and there are many TODOs. Here's a non-exhaustive list
Besides statistics some other features could be made..
## Functionality
### Daily quote
Post a cheerful daily (cat) quote.
Need to make a database for that.

### Pawthereum History
Mention historical events from a specific day.
e.g. On this day 1y ago Pawthereum got launched.
...


## Epilogue
We init for the animals. Go and give your furry fren a hug and spread love <3.

Catoshi