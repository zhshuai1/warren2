from util.date_util import format_time


class Strategy:
    def __init__(self, day_strategy_class=None, minute_strategy_class=None):
        """
        used to initialize the parameters
        """
        self.name = "Strategy"
        self.day_strategy = day_strategy_class()
        self.minute_strategy = minute_strategy_class()
        self.date_to_index = {}

    def initialize(self, stock, time_range):
        for i in range(len(stock)):
            self.date_to_index[format_time(stock[i]['date'])] = i
        self.minute_strategy.initialize(stock, time_range)

    def get_name(self):
        return self.name

    def check_buy(self, stock, index, context):
        pass

    def check_sell(self, stock, index, context):
        pass

    def validate(self, stock, index_range, context):
        """
        validate the performance of the strategy. It means it will work on all the stocks. It differs from the
        simulate method. `simulate` has the constraint that at most one stock could be bought in one day.
        :param stock:
        :param index_range:
        :param context:
        :return:
        """
        self.initialize(stock, index_range)

        for index in index_range:
            # check sell first. if check buy first, the case sell and buy in the same day will be ignored. it's not
            # reasonable.
            if self.day_strategy.check_sell(stock, index, context):
                self.minute_strategy.check_sell(stock, index, context)
            if self.day_strategy.check_buy(stock, index, context):
                self.minute_strategy.check_buy(stock, index, context)

    def simulate(self, stocks, index_range, context):
        """

        :param stocks:
        :param index_range:
        :param context:
        :return:
        """
        pass
        # for stock in stocks:
        #     self.initialize(stock, index_range)
        # for index in index_range:
        #
        #     if self.day_strategy.check_sell(stock, index, context):
        #         self.minute_strategy.check_sell(stock, index, context)
        #     if self.day_strategy.check_buy(stock, index, context):
        #         self.minute_strategy.check_buy(stock, index, context)

