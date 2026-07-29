import random

numbers = []

RANDINT = random.randint(1,33)
#随机整数
print(RANDINT)
numbers.append(RANDINT)
print(numbers)

RANDRANGE = random.randrange(10, 18, 2)
#取值范围在10, 12, 14, 16, 18
print(RANDRANGE)

CHOICE = random.choice(["python", "java"])
CHOICE_signle = random.choice("python")
#获取列表的随机元素,  
print(CHOICE)
print(CHOICE_signle)

numbers= [1,2,3,4,5,6,7,8,9]
SHUFFLE = random.shuffle(numbers)
#打乱列表排序
print(numbers)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  
SAMPLE = random.sample(numbers, 5)  
#从list中随机获取5个元素，作为一个片断返回  
print (SAMPLE) 
print (numbers) #原有序列不会改变。