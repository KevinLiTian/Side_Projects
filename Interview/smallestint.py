# [0, -1, 4, -5]
# [0, 1, 2, 2, 3] 1 -> len(list) + 1 = 5
# 4
def smallestPosInt(nums):
    s = set()

    for num in nums:
        s.add(s)

    for i in range(1, len(nums)+1):
        if i not in s:
            return i

    return len(nums) + 1

    """
    nums.sort()
    potential = 1
    for num in nums:
        if num == potential:
            potential += 1

        elif num > potential:
            return potential

    return min(potential, len(nums)+1)
    """
