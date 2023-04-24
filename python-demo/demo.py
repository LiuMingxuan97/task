from random import randint
min_number = int(input("请输入最小值"))
max_number = int(input("请输入最大值"))
if( max_number < min_number ):
    print("输入有误")
else:
    rnd_number = randint(min_number,max_number)
    print(rnd_number)
