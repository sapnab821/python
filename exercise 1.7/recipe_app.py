# Import the required modules from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import select

#connect to database
engine = ${{ SECRET.DATABASE }}

# Create the base class for your models
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

# Define Recipe Class
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"Recipe ID: {self.id}, Name: {self.name}, Ingredients: {self.ingredients}, Cooking_Time: {self.cooking_time} Difficulty: {self.difficulty}"

    
# Create tables
Base.metadata.create_all(engine)

# function to calculate difficulty
def calculate_difficulty(cooking_time, num):
    if cooking_time < 10 and num < 4:
        difficulty = 'easy'
    elif cooking_time < 10 and num >= 4:
        difficulty =  'medium'
    elif cooking_time >= 10 and num < 4:
        difficulty = 'intermediate'
    elif cooking_time >= 10 and num >= 4:
        difficulty = 'hard'
    return difficulty
    
# function to return ingredients as list
def return_ingredients_as_list(self):
     if len(self.ingredients) == 0:
        return self.ingredients 
     elif len(self.ingredients) >0:
         return (self.ingredients).split(", ")

# function to create recipe
def create_recipe():
    # input name, cooking time, make sure they are correct
    name = input("Name of recipe: ")
    if len(name)>50:
        name = input("name less than 50 char: ") 
    cooking_time = input("Cooking time (min): ")
    while not cooking_time.isnumeric():
        cooking_time = input("Invalid input. Cooking time must be a number. Please enter again: ")
    cooking_time= int(cooking_time)
    # input ingredients
    ingredients = []   
    num = int(input("Enter number of ingredients: "))
    for  i in range (num):
        ingredients.append(input("Enter ingredient name: "))
    
    _ingredients = ", ".join(ingredients)
   

    recipe_entry= Recipe(name=name, cooking_time=cooking_time, ingredients= _ingredients, 
                         difficulty = calculate_difficulty(cooking_time, num)
        )
    
    session.add(recipe_entry)
    session.commit()
    
    
# view all recipes function
def view_all_recipes():
    recipes = session.query(Recipe).all()
    #make sure to only show recipes if any exist
    if recipes:
        for recipe in recipes:
            print(recipe)
    else:
        print("No recipes found.")

#function to search by ingredient
def search_by_ingredient():
    all_ingredients = []
    #make sure to only do it if any recipes exist
    if session.query(Recipe).count()==0:
        print("there are no recipes: ")
    else:
        recipes_list = session.query(Recipe).all()
        # create list of distinct ingredients
        for recipe in recipes_list:
            ingredients = recipe.ingredients.split(", ")
            for ing in ingredients:
                    if ing in all_ingredients:
                        all_ingredients
                    else:
                        all_ingredients.append(ing)

    # create key-value pairs for ingredient and number
    x=1
    pairs={}
    print("Pick a number from the list")
    for ingred in all_ingredients:

        print(f"{x} {ingred}")
        pair={x: ingred}
        pairs.update(pair)
        x=x+1

    search_ingredients =[]
    numbers = input("Pick numbers from the list separated by a space: ")
    num= numbers.split(" ")
    for n in num:
        search_values=pairs.get(int(n))
        search_ingredients.append(search_values)
    print(search_ingredients)
    # Initialize the query
    query = session.query(Recipe)
    conditions = []
    for ing in search_ingredients:
        like_term = f"%{ing}%"
        query = query.filter(Recipe.ingredients.like(like_term))

    recipes = query.all()

    # Print the results
    if recipes:
        for recipe in recipes:
            print(recipe)
    else:
        print("No recipes found with the selected ingredients.")
    
# function to edit recipe    
def edit_recipe():
    recipe_to_edit = None
    if session.query(Recipe).count()==0:
        print("there are no recipes: ")
        main_menu()
    else: 
        
        results = session.query(Recipe).all()
        
        for recipe in results:
            print(f"ID: {recipe.id}, Name: {recipe.name}")

        pick = int(input("Choose the id of the recipe you want to change: "))

        recipe_to_edit = session.query(Recipe).filter(Recipe.id == pick).first()
        
    if recipe_to_edit:
        print(f"Editing Recipe: ID: {recipe_to_edit.id}, Name: {recipe_to_edit.name}")
        # Add code to actually edit the recipe here
    else:
        print("That recipe does not exist.")       
    
    print("1. Name")
    print("2. Ingredient")
    print("3. Cooking_time")

    choose = int(input("Choose number of what you want to change: "))

    if choose == 1:
        new_value = input("Enter the new name: ")
        session.query(Recipe).filter(Recipe.id == pick).update({Recipe.name: new_value})
    elif choose == 2:
        
        current_ingredients = ((session.query(Recipe.ingredients).filter(Recipe.id == pick).first().ingredients)).split(", ")
        print(current_ingredients)
    # Get the new ingredients from the user
        new_ingredients = input("Enter the new ingredients to add (comma-separated): ").split(", ")
    
    # Combine the current ingredients with the new ones 
        
        updated_ingredients = current_ingredients + new_ingredients
    
    # Join the ingredients into a string for storage
        _ingredients = ", ".join(updated_ingredients)
        session.query(Recipe).filter(Recipe.id== pick).update({Recipe.ingredients: _ingredients})
        
    elif choose == 3:
        new_value = int(input("Enter the new cooking time (in minutes): "))
        session.query(Recipe).filter(Recipe.id== pick).update({Recipe.cooking_time: new_value})
        
    else:
        print("Invalid choice")
        return
    session.commit()

    if choose == 2 or choose == 3:
    # Get the current ingredients and split them into a list
        ingredients = session.query(Recipe.ingredients).filter(Recipe.id == pick).first().ingredients.split(", ")
    
    # Get the current cooking time
        time = session.query(Recipe.cooking_time).filter(Recipe.id == pick).first().cooking_time
    
    # Calculate the difficulty based on cooking time and the number of ingredients
        new_difficulty = calculate_difficulty(time, len(ingredients))
    
    # Update the difficulty in the database
        session.query(Recipe).filter(Recipe.id == pick).update({Recipe.difficulty: new_difficulty})
        session.commit()
        
def delete_recipe():
    # Fetch all recipes from the database and list them to the user
    recipes = session.query(Recipe).all()
    print("Available Recipes:")
    for index, recipe in enumerate(recipes, start=1):
        print(f"{index}. {recipe.name}")

    # Prompt user to select a recipe for deletion
    recipe_index = int(input("Enter the index of the recipe you want to delete: ")) - 1

    # Check if the provided recipe index is valid
    if 0 <= recipe_index < len(recipes):
        recipe = recipes[recipe_index]

        # Delete the specified recipe
        session.delete(recipe)

        # Commit the changes
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Error: Invalid recipe index.")

def main_menu():
    while True:
        print("Main Menu")
        print("----------------")
        print("Pick a number: ")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search by ingredients")
        print("4. Edit recipe")
        print("5. Delete recipe")

        choice = input("Your choice: ").strip().lower()

        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredient()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == 'quit':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
    
    session.close()
    print("Session closed.")
main_menu()
