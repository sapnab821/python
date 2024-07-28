recipes_list = []
ingredients_list = []

def take_recipe():
    name = str(input("Name of recipe: "))
    cooking_time = int(input("Cooking time (min): "))
    ingredients = input("List of ingredients: ").split(", ")
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    return recipe


n= int(input("How many recipes would you like to enter: "))

recipe = {}
for x in range(n):
    recipe = take_recipe()
    print()

    for y in recipe.get('ingredients'):
        if y not in ingredients_list:
            ingredients_list.append(y)

    recipes_list.append(recipe)
print()
for recipe in recipes_list:
    if recipe.get('cooking_time') < 10 and len(recipe.get('ingredients'))<4:
        difficulty = 'easy'
    elif recipe.get('cooking_time') < 10 and len(recipe.get('ingredients'))>=4:
        difficulty = 'medium'
    elif recipe.get('cooking_time') >= 10 and len(recipe.get('ingredients'))<4:
        difficulty = 'intermediate'
    elif recipe.get('cooking_time') >= 10 and len(recipe.get('ingredients'))>=4:
        difficulty = 'hard'
    print('Recipe: ', end=" ")
    print(recipe.get('name'))
    print('Cooking Time (min): ', end=" ")
    print(recipe.get('cooking_time'))
    for z in recipe.get('ingredients'):
        print(z)
    print('difficulty level: ', end=" ")
    print(difficulty)
    print()

print()
print('Ingredients Available Across All Recipes')
print('----------------------------------------')
ingredients_list.sort()
for a in ingredients_list:
    print(a)
