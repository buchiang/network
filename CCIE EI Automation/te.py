import random

red_balls = random.sample(range(1,34), 6)
blue_ball = random.randint(1, 17)
red_balls.sort()

cus_red = random.sample(range(1,34), 6)
cus_blue = random.randint(1, 17)
cus_red.sort()

print(f"你选的号码:\n\t红色球: {cus_red}, 蓝色球: {cus_blue}")
print("=" * 50)
print(f"中奖号码:\n\t红色球: {red_balls}, 蓝色球: {blue_ball}")
print("=" * 50)

prize = []
for value in cus_red:
    if value in red_balls:
        prize.append(value)

if len(prize) == 6 and cus_blue == blue_ball:
    print("一等奖")
elif len(prize) == 6:
    print("二等奖")
elif len(prize) == 5 and cus_blue == blue_ball:
    print("三等奖")
elif len(prize) == 5:
    print("四等奖")
elif len(prize) == 4 and cus_blue == blue_ball:
    print("四等奖")
elif len(prize) == 4:
    print("五等奖")
elif len(prize) == 3 and cus_blue == blue_ball:
    print("五等奖")
elif len(prize) == 2 and cus_blue == blue_ball:
    print("六等奖")
elif cus_blue == blue_ball:
    print("六等奖")
else:
    print("你没中奖")



