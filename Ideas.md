## Major fix:
* use T-1 data only, find the profit is negative;
## way forward
- [x] rough categorical model
  - [x] not good
- [x] recall model
  - [x] good train and bad predict
- [ ] only train with continuously growing
- [ ] add more features
- [ ] check some trading entries to find why it gains or loses.
- [ ] use model directly
  - [ ] if a simple rule could not make profit, the model hardly can do. Therefore, optimize the rule first until it makes profit.
  - [ ] implement the framework and with a simple strategy?
- [ ] implement a real time stock decider
- [ ] do a refactor to reuse the code for validate and simulate
- [x] draw the gains and losses graph by day, stock
- [x] simulate the strategy with day going: one day you could only trade on no more than one stock.
  - [x] random
  - [x] first hit
  - [ ] fix the index not aligned issue: due to suspending in some day
