class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        cars_right_to_left = sorted(zip(position, speed), reverse=True)

        bottleneck = float('-inf')
        fleets = 0

        for d, s in cars_right_to_left:
            remaining_dist = target - d
            time_to_reach_target = remaining_dist / s

            print((d, s), (remaining_dist, time_to_reach_target), bottleneck)

            if time_to_reach_target > bottleneck:
                bottleneck = time_to_reach_target
                fleets += 1

        return fleets


def main():
    target = 12
    position = [10, 8, 0, 5, 3]
    speed = [2, 4, 1, 1, 3]
    print(Solution().carFleet(target, position, speed))


if __name__ == '__main__':
    main()
