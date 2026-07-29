import random

red_balls = sorted(random.sample(range(1, 33), 6))

blue_balls = random.randint(1,16)

print(f"{red_balls} {blue_balls}")