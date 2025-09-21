from icecream import ic


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = prices[0]
        max_profit = 0
        for current_price in prices[1:]:
            min_price = min(current_price, min_price)
            max_profit = max(current_price - min_price, max_profit)

        return max_profit


def main():
    sol = Solution()
    result = sol.maxProfit([7, 1, 5, 3, 6, 4])
    print(result)


if __name__ == '__main__':
    main()
