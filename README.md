# Planed models
## predict tomorrow's label(-9~+9 classification together with probabilities)
1. feature list
* meta: code,industry
* day level: this[open,close,high,low,volume],index[...],industry[...] # pecent will be mapped to -9~+9
* minute level: this[open,now,high,low,volume],index[...],industry[...]
* N day: highest,lowest,start,now,max_rise,max_fall
## cluster similar stocks
## predict label series of the next N days
## predict tomorrow's price(regression)
## rank the stocks most worth buying
## best time of the day to buy a stock
## specific strategies: continuously fast growing
## random search with clipping(monte carlo search)
# Meta models
## discriminate the predictable and unpredictable stocks
