def cost(xA, yA, xB, yB, x, y, lim=100):
    numB = (y-x*yA/xA)/(yB-xB*yA/xA)
    numA = (x-numB*xB)/xA
    if numA > lim or numB > lim:
        return 0
    elif round(numA)*xA+round(numB)*xB != x or round(numA)*yA+round(numB)*yB != y:
        return 0
    else:
        return numA*3+numB

all_cost = []
with open('data/input_day13.txt') as f:
    for line in f:
        button_A = line.strip().split(': ')[1].split(', ')
        xA = int(button_A[0].split('+')[1])
        yA = int(button_A[1].split('+')[1])
        button_B = f.readline().strip().split(': ')[1].split(', ')
        xB = int(button_B[0].split('+')[1])
        yB = int(button_B[1].split('+')[1])
        prize_line = f.readline().strip().split(': ')[1].split(', ')
        x = int(prize_line[0].split('=')[1])
        y = int(prize_line[1].split('=')[1])
        f.readline()

        all_cost.append(cost(xA, yA, xB, yB, x, y))

print('challenge 1', int(sum(all_cost)))

all_cost = []
with open('data/input_day13.txt') as f:
    for line in f:
        button_A = line.strip().split(': ')[1].split(', ')
        xA = int(button_A[0].split('+')[1])
        yA = int(button_A[1].split('+')[1])
        button_B = f.readline().strip().split(': ')[1].split(', ')
        xB = int(button_B[0].split('+')[1])
        yB = int(button_B[1].split('+')[1])
        prize_line = f.readline().strip().split(': ')[1].split(', ')
        x = int(prize_line[0].split('=')[1])+10000000000000
        y = int(prize_line[1].split('=')[1])+10000000000000
        f.readline()

        all_cost.append(cost(xA, yA, xB, yB, x, y, lim=10000000000000000000))

print('challenge 2', int(sum(all_cost)))