import mysql.connector

def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return 'easy'
    elif cooking_time < 10 and len(ingredients) >= 4:
        return 'medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        return 'intermediate'
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return 'hard'

def create_recipe(conn, cursor):
    name = input("Name of recipe: ")
    cooking_time = int(input("Cooking time (min): "))
    ingredients = input("List of ingredients: ").split(", ")
    difficulty = calculate_difficulty(cooking_time, ingredients)
    _ingredients = ", ".join(ingredients)

    insert_query = """
    INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, _ingredients, cooking_time, difficulty))
    conn.commit()
    print("Recipe added successfully!")

def search_recipe(conn, cursor):
    cursor.execute("SELECT DISTINCT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = set()
    for row in results:
        ingredients = row[0].split(", ")
        all_ingredients.update(ingredients)
    
    sorted_ingredients = sorted(all_ingredients)
    for idx, ingredient in enumerate(sorted_ingredients, 1):
        print(f"{idx}. {ingredient}")
    
    choice = 0
    choice = int(input("Choose an ingredient by number to search: ")) - 1
    search_ingredient = sorted_ingredients[choice]

    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(search_query, ('%' + search_ingredient + '%',))
    
    results = cursor.fetchall()
    if results:
        for row in results:
            print(row[0])
            print (row[1])
            print(row[2])
            print(row[4])
    else:
        print("No recipes found with that ingredient.")

def update_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()

    print("\nExisting recipes:")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")
    
    recipe_id = int(input("Enter the ID of the recipe to update: "))
    column_to_update = input("Enter the column to update (name, ingredients, cooking_time): ")

    if column_to_update == 'name':
        new_value = input("Enter the new name: ")
        update_query = "UPDATE Recipes SET name = %s WHERE id = %s"
        cursor.execute(update_query, (new_value, recipe_id))
    elif column_to_update == 'ingredients':
        new_value = input("Enter the new ingredients (comma-separated): ").split(", ")
        _ingredients = ", ".join(new_value)
        update_query = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
        cursor.execute(update_query, (_ingredients, recipe_id))
    elif column_to_update == 'cooking_time':
        new_value = int(input("Enter the new cooking time (in minutes): "))
        update_query = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
        cursor.execute(update_query, (new_value, recipe_id))
    else:
        print("Invalid column.")
        return

    if column_to_update in ['ingredients', 'cooking_time']:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        row = cursor.fetchone()
        ingredients_list = row[1].split(", ")
        difficulty = calculate_difficulty(row[0], ingredients_list)
        update_query = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
        cursor.execute(update_query, (difficulty, recipe_id))

    conn.commit()
    print("Recipe updated successfully!")

def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    
    print("\nExisting recipes:")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe to delete: "))

    delete_query = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(delete_query, (recipe_id,))
    conn.commit()
    print("Recipe deleted successfully!")

def create_database_and_table(conn, cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
    cursor.execute("USE task_database")


    # Create the table with the correct schema
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Recipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

def main_menu(conn, cursor):
    while True:
        print("Main Menu")
        print("----------------")
        print("Pick a number: ")
        print("1. Create a new recipe")
        print("2. Search for recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("Type quit to exit the program")

        choice = input("Your choice: ").strip().lower()

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == 'quit':
            print("Exiting...")
            conn.commit()
            cursor.close()
            conn.close()
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    conn = mysql.connector.connect(
       ${{ SECRET.SQL }}
    )
    cursor = conn.cursor()

    create_database_and_table(conn, cursor)
    
    main_menu(conn, cursor)
