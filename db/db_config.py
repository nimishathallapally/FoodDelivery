from pymongo import MongoClient

# 1. Connect to MongoDB (change the URL if you're using Atlas)
client = MongoClient("mongodb://localhost:27017")
db = client["restaurant_app"]

# 2. Define collections
restaurants_col = db["restaurants"]
info_col = db["restaurant_info"]
menu_col = db["menus"]

# 3. Your fake data
restaurants = [
    {"id": 1, "name": "Pizza Paradise", "image": "images/pizza.jpg"},
    {"id": 2, "name": "Burger Haven", "image": "images/burger.webp"},
    {"id": 3, "name": "Sushi World", "image": "images/sushi.webp"},
    {"id": 4, "name": "Taco Fiesta", "image": "images/Taco.jpg"},
    {"id": 5, "name": "Pasta Palace", "image": "images/pasta.webp"},
    {"id": 6, "name": "Indian Delight", "image": "images/indian.jpeg"},
    {"id": 7, "name": "BBQ Kingdom", "image": "images/bbq.avif"},
    {"id": 8, "name": "Vegan Bites", "image": "images/vegan.webp"},
    {"id": 9, "name": "Seafood Bay", "image": "images/seafood.jpg"},
    {"id": 10, "name": "Dessert Heaven", "image": "images/dessert.jpg"},
]

restaurant_info = {
    1: {"name": "Pizza Paradise", "rating": 4.5},
    2: {"name": "Burger Haven", "rating": 4.3},
    3: {"name": "Sushi World", "rating": 4.7},
    4: {"name": "Taco Fiesta", "rating": 4.2},
    5: {"name": "Pasta Palace", "rating": 4.4},
    6: {"name": "Indian Delight", "rating": 4.6},
    7: {"name": "BBQ Kingdom", "rating": 4.5},
    8: {"name": "Vegan Bites", "rating": 4.3},
    9: {"name": "Seafood Bay", "rating": 4.6},
    10: {"name": "Dessert Heaven", "rating": 4.8},
}

menu_data = {
    # include all menu_data here as in your script (truncated for brevity in this snippet)
    1: [
        {
            "name": "Margherita Pizza",
            "price": "10",
            "description": "Classic Italian pizza with fresh tomatoes, mozzarella, basil, and a drizzle of olive oil."
        },
        {
            "name": "Pepperoni Pizza",
            "price": "12",
            "description": "A delicious pizza topped with spicy pepperoni slices, melted mozzarella, and tangy tomato sauce."
        },
        {
            "name": "BBQ Chicken Pizza",
            "price": "14",
            "description": "Grilled chicken, smoky BBQ sauce, red onions, and mozzarella on a crispy crust."
        },
        {
            "name": "Veggie Supreme Pizza",
            "price": "11",
            "description": "A colorful mix of bell peppers, mushrooms, olives, onions, and fresh mozzarella."
        },
        {
            "name": "Hawaiian Pizza",
            "price": "13",
            "description": "A sweet and savory combination of ham, pineapple, and mozzarella cheese."
        },
        {
            "name": "Four Cheese Pizza",
            "price": "15",
            "description": "A rich blend of mozzarella, parmesan, gouda, and blue cheese for cheese lovers."
        },
        {
            "name": "Mushroom Truffle Pizza",
            "price": "16",
            "description": "Creamy truffle sauce, wild mushrooms, mozzarella, and fresh herbs for an earthy flavor."
        },
        {
            "name": "Meat Lovers Pizza",
            "price": "18",
            "description": "A loaded pizza with pepperoni, sausage, bacon, and ground beef."
        },
        {
            "name": "Spicy Jalapeno Pizza",
            "price": "12",
            "description": "Fiery jalapeños, spicy tomato sauce, mozzarella, and a hint of garlic."
        },
        {
            "name": "White Sauce Pizza",
            "price": "14",
            "description": "Creamy Alfredo sauce, chicken, mushrooms, and mozzarella on a thin crust."
        }
    ],
     2: [{"name": "Cheese Burger", "price": "8"}, {"name": "Veggie Burger", "price": "7"}],
        3: [{"name": "Salmon Sushi", "price": "15"}, {"name": "Tuna Sushi", "price": "14"}],
        4: [{"name": "Chicken Taco", "price": "9"}, {"name": "Veg Taco", "price": "8"}],
        5: [{"name": "Alfredo Pasta", "price": "11"}, {"name": "Pesto Pasta", "price": "12"}],
        6: [{"name": "Butter Chicken", "price": "13"}, {"name": "Paneer Tikka", "price": "10"}],
        7: [{"name": "BBQ Ribs", "price": "18"}, {"name": "BBQ Chicken", "price": "16"}],
        8: [{"name": "Vegan Salad", "price": "9"}, {"name": "Quinoa Bowl", "price": "10"}],
        9: [{"name": "Grilled Salmon", "price": "20"}, {"name": "Garlic Shrimp", "price": "18"}],
        10: [{"name": "Chocolate Cake", "price": "6"}, {"name": "Ice Cream Sundae", "price": "5"}],
}

# 4. Insert into MongoDB
restaurants_col.delete_many({})
info_col.delete_many({})
menu_col.delete_many({})

restaurants_col.insert_many(restaurants)

# Insert restaurant info (as list of documents with id)
info_docs = [{"id": rid, **info} for rid, info in restaurant_info.items()]
info_col.insert_many(info_docs)

# Insert menu data (restaurant_id and menu list)
menu_docs = [{"restaurant_id": rid, "menu": items} for rid, items in menu_data.items()]
menu_col.insert_many(menu_docs)

print("✅ Fake data seeded successfully!")
