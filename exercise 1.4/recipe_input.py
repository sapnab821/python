import pickle

# user inputs the recipe information and recipe info is stored in recipe as dictionary
def take_recipe():
    name = str(input("Name of recipe: "))
    cooking_time = int(input("Cooking time (min): "))
    ingredients = input("List of ingredients: ").split(", ")
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {'name': name,
               'cooking_time': cooking_time,
               'ingredients': ingredients,
               'difficulty': difficulty}
    return recipe

# calculated the difficulty of the recipe
def calc_difficulty(cooking_time, ingredients):
    if cooking_time< 10 and len(ingredients)<4:
        return 'easy'
    elif cooking_time < 10 and len(ingredients)>=4:
        return 'medium'
    elif cooking_time >= 10 and len(ingredients)<4:
        return 'intermediate'
    elif cooking_time >= 10 and len(ingredients)>=4:
        return 'hard'
    

filename = input("Enter the name of the file you want to save to: ")

# Try to open the file, if it doesn't exist, creat a new file
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File loaded successfully!")
# This is the error that will be raised if the file doesn't exist
except FileNotFoundError:
    print("No such files match that name - creating a new file")
    data = {"recipes_list": [], "all_ingredients": []}
# This is a general error that will be raised if something else goes wrong
except:
    print("Oops! Something went wrong. Try again.")
    data = {"recipes_list": [], "all_ingredients": []}
# This will close the file
else:
    file.close()
# Extracts the data into two variables
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

# Asks the user how many recipes they want to enter
n = int(input("How many recipes would you like to enter?: "))

# For each recipe, it will add the ingredients to the all_ingredients list
for i in range(0, n):
    recipe = take_recipe()
    for element in recipe["ingredients"]:
        if element not in all_ingredients:
            all_ingredients.append(element)
    recipes_list.append(recipe)
    print("Recipe added successfully!")


# Creates a new dictionary with the updated data
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

# Opens the file and saves the data to it
updated_file = open(filename, "wb")
pickle.dump(data, updated_file)
# Closes the file
updated_file.close()
print("Recipe file has been updated!")

