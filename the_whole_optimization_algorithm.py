import random
import math

num = 100
X1 = [13,20]
X2 = [20,5]
p = round(random.uniform(0,1), 1)

mat =[[0]*20]*20
print(mat)






for i in range (num):
    p = round(random.uniform(0,1), 1)
    if(p <=0.5):
        a = 2
        r = round(random.uniform(0,1), 2)
        A = 2*a*r - a
        C = 2 * r
        D = [int(abs(C*X2[0]-X1[0])), int(abs(C*X2[1]-X1[1]))]
        X1 = [int(abs(X2[0]- A*D[0])), int(abs(X2[1]- A*D[1]))]
        if(X1[0] < 20 and X1[1] < 20):
            mat[X1[0]][X1[1]] = 1
        a -= 2/num
    else:
        D = [int(abs(X2[0]-X1[0])), int(abs(X2[1]-X1[1]))]
        l = random.uniform(-1,1)
        log = math.exp(5*l)
        trig = math.cos(math.pi * l)
        X1 = [int(abs(D[0]*trig*log)+X2[0]), int(abs(D[1]*trig*log)+X2[0])]
        if(X1[0] < 20 and X1[1] < 20):
            mat[X1[0]][X1[1]] = 1

print(mat)


