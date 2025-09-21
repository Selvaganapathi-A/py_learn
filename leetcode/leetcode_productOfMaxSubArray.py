def maxProductSubArray(nums: list[int]) -> float:
    length_of_array: int = len(nums)
    if length_of_array < 1:
        return 0
    left_pointer: int = 0
    right_pointer: int = 0
    #
    current_product: float = nums[left_pointer]
    maximum_of_product: float = current_product
    #
    product_of_previous_array_elements: float = nums[left_pointer]
    #
    right_pointer = 1
    while right_pointer < length_of_array:
        temp = nums[right_pointer] * product_of_previous_array_elements
        if temp < nums[right_pointer]:
            product_of_previous_array_elements = nums[right_pointer]
            left_pointer = right_pointer + 1
        else:
            product_of_previous_array_elements = temp
        if maximum_of_product < product_of_previous_array_elements:
            maximum_of_product = product_of_previous_array_elements
            left_pointer = right_pointer
        right_pointer += 1
    return maximum_of_product


def main():
    nums: list[int]
    result: float
    #
    nums = [2, 3, -2, 4, 1, 0, 5, 2, 3]
    result = maxProductSubArray(nums)
    print(result)
    #
    nums = [-2, 0, -1]
    result = maxProductSubArray(nums)
    print(result)
    #
    nums = [2, 3, -1, 4]
    result = maxProductSubArray(nums)
    print(result)


if __name__ == '__main__':
    import subprocess

    subprocess.run('clear')
    main()
