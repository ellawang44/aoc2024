from itertools import product

def operate(target, nums):
    for ops in product('*+', repeat=len(nums)-1):
        total = nums[0]
        for op, val in zip(ops, nums[1:]):
            if op == '*':
                total *= val
                if total > target:
                    break
            elif op == '+':
                total += val
                if total > target:
                    break
            else:
                continue
        if total == target:
            return target
    return 0

count = 0
with open('input_day7.txt') as f:
    for line in f:
        target, nums = line.strip().split(': ')
        target = int(target)
        nums = [int(i) for i in nums.split(' ')]
        count += operate(target, nums)

print('challenge 1', count)

####################################

def operate2(target, nums):
    for ops in product('*+|', repeat=len(nums)-1):
        total = nums[0]
        for op, val in zip(ops, nums[1:]):
            if op == '*':
                total *= val
                if total > target:
                    break
            elif op == '+':
                total += val
                if total > target:
                    break
            elif op == '|':
                total = int(str(total) + str(val))
                if total > target:
                    break
            else:
                continue
        if total == target:
            return target
    return 0

count = 0
with open('input_day7.txt') as f:
    for line in f:
        target, nums = line.strip().split(': ')
        target = int(target)
        nums = [int(i) for i in nums.split(' ')]
        count += operate2(target, nums)

print('challenge 2', count)
