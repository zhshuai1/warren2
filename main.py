from datasource.db.db import StockSource

if __name__ == '__main__':
    stock_source = StockSource()
    print(stock_source.get_all_stocks())
    print(stock_source.get_stock_by_code('sh000001', int(10)))
