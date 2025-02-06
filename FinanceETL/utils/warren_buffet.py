import pandas as pd
from enum import Enum

# BUFFETT INDICATORS
# Operating Expenses - The companies hard costs


class Valuation(Enum):
    VERY_GOOD = "very_good"
    GOOD = "good"
    BAD = "bad"
    VERY_BAD = "very_bad"


class WarrenBuffets:
    def sgaRatio(self, symbol: pd.DataFrame):
        """
        Coca Cola spends 59% on SGA
        Moodys 25%
        P&C 61%
        Consistently is the key
        wild variations in the SGA is not good
        consistently < 30% is fantastic
        30% - 80% is good
        near or over 100% is sign for highly competetive industry
        """
        symbol["sgaRatio"] = (
            symbol["sellingGeneralAndAdministrativeExpenses"] / symbol["grossProfit"]
        )
        return symbol

    def sgaRatio_valuation(self, symbol: pd.DataFrame):
        s = symbol["sgaRatio"]

        def evaluate_valuation(s):
            if s <= 0.3:
                return Valuation.VERY_GOOD.value
            elif s <= 0.8:
                return Valuation.GOOD.value
            elif s <= 1:
                return Valuation.BAD.value
            else:
                return Valuation.VERY_BAD.value

        symbol["sgaRatio_valuation"] = symbol["sgaRatio"].apply(evaluate_valuation)

        return symbol

    def randdRatio(self, symbol: pd.DataFrame):
        """
        high Research and Development is long term risk
        """
        symbol["randdRatio"] = (
            symbol["researchAndDevelopmentExpenses"] / symbol["grossProfit"]
        )
        return symbol

    def randdRatio_valuation(self, symbol: pd.DataFrame):
        s = symbol["randdRatio"]

        def evaluate_valuation(s):
            if s <= 0.3:
                return Valuation.VERY_GOOD.value
            elif s <= 0.8:
                return Valuation.GOOD.value
            elif s <= 1:
                return Valuation.BAD.value
            else:
                return Valuation.VERY_BAD.value

        symbol["randdRatio_valuation"] = symbol["randdRatio"].apply(evaluate_valuation)

        return symbol

    def deprecationRatio(self, symbol: pd.DataFrame):
        """
        Deprecation - Abschreibung
        All machinery and buildings eventually wear out over time; this wearing out is recognized on the income statement as deprecation.
        Coca Cola: 6%
        Wrigleys: 7%
        Procter and Gamble: 8%
        GM: 22% - 57%
        lower is always better
        green: <10%

        """
        symbol["deprecationRatio"] = (
            symbol["depreciationAndAmortization"] / symbol["grossProfit"]
        )
        return symbol

    def deprecationRatio_valuation(self, symbol: pd.DataFrame):
        s = symbol["deprecationRatio"]

        def evaluate_valuation(s):
            if s <= 0.1:
                return Valuation.VERY_GOOD.value
            elif s <= 0.2:
                return Valuation.GOOD.value
            elif s <= 0.6:
                return Valuation.BAD.value
            else:
                return Valuation.VERY_BAD.value

        symbol["deprecationRatio_valuation"] = symbol["deprecationRatio"].apply(
            evaluate_valuation
        )

        return symbol

    def interestExpenseRatio(self, symbol: pd.DataFrame):
        """
        Interest Expenses is the entry for the interest paid out, during the quarter or year, on the debt the company carries on its balance sheets as a
        liability. This is called financial cost, not an operating cost, an it is isolated out on its own, because it is not tied to any production or sales
        process. Instead, interest is a reflection of the total debt that the company is carrying on its books. The more debt the company has,
        the more interest it has to pay.
        """
        symbol["interestExpenseRatio"] = (
            symbol["interestExpense"] / symbol["operatingIncome"]
        )
        return symbol

    def netEarningsRatio(self, symbol: pd.DataFrame):
        """
        As percentage of total revenue, Higher percentag better competitive advantage
        - Coca Cola 21%
        - Moodys 31%
        - GM only 3%
        - long term >20% -> some kind of competitive advantage
        - <10% highly competitive
        - 10% - 20% gray area
        """
        symbol["netEarningsRatio"] = symbol["netIncome"] / symbol["revenue"]
        return symbol

    def netEarnningsRatio_valuation(self, symbol: pd.DataFrame):
        s = symbol["netEarningsRatio"]

        def evaluate_valuation(s):
            if s >= 0.3:
                return Valuation.VERY_GOOD.value
            elif s >= 0.2:
                return Valuation.GOOD.value
            elif s >= 0.10:
                return Valuation.BAD.value
            else:
                return Valuation.VERY_BAD.value

        symbol["netEarningsRatio_valuation"] = symbol["netEarningsRatio"].apply(
            evaluate_valuation
        )

        return symbol

    def applyAll(self, symbol: pd.DataFrame):
        symbol = self.sgaRatio(symbol)
        symbol = self.sgaRatio_valuation(symbol)
        symbol = self.randdRatio(symbol)
        symbol = self.randdRatio_valuation(symbol)
        symbol = self.deprecationRatio(symbol)
        symbol = self.deprecationRatio_valuation(symbol)
        symbol = self.interestExpenseRatio(symbol)
        symbol = self.netEarningsRatio(symbol)
        symbol = self.netEarnningsRatio_valuation(symbol)
        return symbol
