# Technical Interview Questions

## Find Smallest Missing Integer (Leetcode 41 -- Hard)

Given an unsorted integer array nums, return the smallest missing positive integer

Example 1:

```
Input: nums = [1,2,0]
Output: 3
Explanation: The numbers in the range [1,2] are all in the array.
```

Example 2:

```
Input: nums = [3,4,-1,1]
Output: 2
Explanation: 1 is in the array but 2 is missing.
```

Example 3:

```
Input: nums = [7,8,9,11,12]
Output: 1
Explanation: The smallest positive integer 1 is missing.
```

<details>
<summary>Solution 1</summary>

- Time Complexity O(nlogn)
- Space Complexity O(1)

```py
def firstMissingPositive(nums):
    nums.sort()
    potential = 1
    for num in nums:
        if num == potential:
            potential += 1

        elif num > potential:
            return potential

    return min(potential, len(nums) + 1)
```

</details>

<details>
<summary>Solution 2</summary>

- Time Complexity O(n)
- Space Complexity O(n)

```py
def firstMissingPositive(nums):
    s = set()
    for num in nums:
        s.add(num)

    for i in range(1, len(nums) + 1):
        if i not in s:
            return i

    return len(nums) + 1
```

</details>

<details>
<summary>Solution 3</summary>

- Time Complexity O(n)
- Space Complexity O(1)

```py
def firstMissingPositive(nums):
    for idx, num in enumerate(nums):
        if num <= 0:
            nums[idx] = len(nums) + 1

    for num in nums:
        if abs(num) <= len(nums) and nums[abs(num) - 1] > 0:
            nums[abs(num) - 1] = -nums[abs(num) - 1]

    for i in range(1, len(nums) + 1):
        if nums[i - 1] > 0:
            return i

    return len(nums) + 1
```

</details>
