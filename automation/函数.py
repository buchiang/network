
def greet_user(username):
    """Display a simple greeting."""
    print(f"Hello, {username.title()}!")

greet_user('jesse')

def describe_pet(animal_type, pet_name):
    """Display information about a pet."""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet('hamster', 'harry')

def make_shirt(size, message):
    print(f"\nThe size is {size}")
    print(f"The message is: {message}")

make_shirt('L', 'Hello World!')

def name(first_name, last_name):
    full_name = f"{first_name} {last_name}"
    return full_name.title()
print("\n")
musician = name('jimi', 'hendrix')
print(musician)

def CCIE(exam, result):
    if result == 'pass':
        print(f"\nCongratulations! You passed the {exam} exam.")
    else:
        print(f"\nSorry, you did not pass the {exam} exam. Keep trying!")

CCIE('CCIE Security', 'pass')
CCIE('CCIE Routing and Switching', 'fail')