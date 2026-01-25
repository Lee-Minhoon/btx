import unittest

from modules.data import Ticker

from .position import Position


class TestPosition(unittest.TestCase):
    def test_trade(self):
        position = Position(Ticker.MICROSOFT)
        position.buy(1, 100)
        position.sell(1)
        self.assertEqual(position.amount, 0)
        self.assertEqual(position.avg_buy_price, 0)
        self.assertEqual(position.total_cost(), 0)
        self.assertEqual(position.value(), 0)
        self.assertEqual(position.roi(), 0)
        self.assertEqual(position.buy_count, 1)
        self.assertEqual(position.sell_count, 1)
        self.assertEqual(position.unrealized_profit, 0)

        position.buy(2, 100)
        position.update(110)
        position.sell(1)
        self.assertEqual(position.amount, 1)
        self.assertEqual(position.avg_buy_price, 100)
        self.assertEqual(position.total_cost(), 100)
        self.assertEqual(position.value(), 110)
        self.assertEqual(position.roi(), 10)
        self.assertEqual(position.buy_count, 2)
        self.assertEqual(position.sell_count, 2)
        self.assertEqual(position.unrealized_profit, 20)


if __name__ == "__main__":
    unittest.main()
