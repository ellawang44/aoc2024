def cost(A, B, prize, lim=100):
    costs = []
    num = min(prize[0]//A[0], prize[1]//A[1])
    for numA in range(num):
        X_remaining = prize[0]-numA*A[0]
        Y_remaining = prize[1]-numA*A[1]
        if X_remaining % B[0] == 0 and Y_remaining % B[1] == 0:
            numB = X_remaining // B[0]
            if numB == Y_remaining // B[1]:
                if numA <= lim and numB <= lim:
                    costs.append(numA*3+numB)
    if len(costs) == 0:
        return 0
    else:
        return min(costs)

all_cost = []
with open('data/input_day13.txt') as f:
    for line in f:
        button_A = line.strip().split(': ')[1].split(', ')
        A = int(button_A[0].split('+')[1]), int(button_A[1].split('+')[1])
        button_B = f.readline().strip().split(': ')[1].split(', ')
        B = int(button_B[0].split('+')[1]), int(button_B[1].split('+')[1])
        prize_line = f.readline().strip().split(': ')[1].split(', ')
        prize = int(prize_line[0].split('=')[1]), int(prize_line[1].split('=')[1])
        f.readline()

        all_cost.append(cost(A, B, prize))

print('challenge 1', sum(all_cost))
