from flask import Flask, render_template, url_for,request, redirect,session,send_file
from pymongo import MongoClient
from captcha.image import ImageCaptcha
import os
import random
import string

app = Flask(__name__)
app.secret_key = '12345' 

# app = Flask(__name__)

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017")  # Replace with your Mongo URI
db = client["restaurant_app"]

@app.route("/")
def home():
    restaurants_collection = db.restaurants
    restaurants_data = restaurants_collection.find()

    restaurants = []
    for r in restaurants_data:
        restaurants.append({
            "id": r["id"],
            "name": r["name"],
            "image": url_for('static', filename=f'/{r["image"]}')
        })

    return render_template("home.html", restaurants=restaurants)

@app.route('/menu/<int:restaurant_id>', methods=['GET'])
def menu(restaurant_id):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["restaurant_app"]
    menu_col = db["menus"]
    
    # Find the restaurant's menu based on the restaurant_id
    restaurant_menu = menu_col.find_one({"restaurant_id": restaurant_id})
    
    if restaurant_menu:
        menu_items = restaurant_menu["menu"]
    else:
        menu_items = []

    # Get the restaurant information
    restaurant_info = db["restaurant_info"].find_one({"id": restaurant_id})

    # Render the menu page with restaurant info and menu items
    return render_template('menu.html', menu_items=menu_items, restaurant=restaurant_info)


@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/profile')
def profile():
    user = db.users.find_one({"email": "john@example.com"})  # Simulating a logged-in user

    if not user:
        user = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
        db.users.insert_one(user)

    orders = list(db.orders.find({"user_email": user["email"]}))
    payment_methods = list(db.payments.find({"user_email": user["email"]}))

    return render_template("profile.html", user=user, orders=orders, payment_methods=payment_methods)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Here, you would process the checkout form data and handle the order.
        # For simplicity, let's just print the received data.
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        
        # Simulating order placement logic
        print(f"Order placed for: {name}, {address}, {email}, {phone}")

        # After processing, you can redirect or show a confirmation page.
        return redirect(url_for('order_confirmation'))

    return render_template('checkout.html')
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # You can access form data here
        name = request.form['name']
        # Do something with the data (e.g., save it, show confirmation, etc.)
        return render_template('payment.html')  # Your payment options page

    # fallback for GET (e.g., redirect if accessed directly)
    return redirect(url_for('checkout'))




@app.route('/place_order', methods=['POST'])
def place_order():
    # Ensure the captcha directory exists
    captcha_dir = 'static/captcha'
    if not os.path.exists(captcha_dir):
        os.makedirs(captcha_dir)

    # Generate a random CAPTCHA text (6 digits)
    captcha_text = ''.join(random.choices(string.digits, k=7))

    # Create the CAPTCHA image
    image = ImageCaptcha()
    captcha_image = image.generate_image(captcha_text)
    
    # Save the CAPTCHA image
    captcha_filename = f"{captcha_text}.png"
    captcha_image.save(os.path.join(captcha_dir, captcha_filename))

    # Render the template with the CAPTCHA filename
    return render_template('card.html', method=payment, captcha_filename=captcha_filename)

@app.route('/profile/edit')
def edit_profile():
    return "Edit Profile Page (Under Construction)"  # Replace with actual template later

def generate_captcha_image():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session['captcha_text'] = captcha_text

    # Create CAPTCHA image
    image = ImageCaptcha(width=280, height=90)

    # Save the CAPTCHA image in the 'static/captcha' folder
    captcha_filename = f"captcha_{captcha_text}.png"
    captcha_path = os.path.join(app.static_folder, 'captcha', captcha_filename)
    
    # Ensure the 'captcha' folder exists
    if not os.path.exists(os.path.dirname(captcha_path)):
        os.makedirs(os.path.dirname(captcha_path))

    image.write(captcha_text, captcha_path)
    
    return captcha_filename  # Return the file name for use in HTML


@app.route('/order-confirmation', methods=['POST'])
def order_confirmation():
    user_input = request.form['captcha']
    actual_captcha = session.get('captcha_text', '')

    if user_input != actual_captcha:
        # CAPTCHA incorrect – regenerate a new one
        captcha_text = ''.join(random.choices(string.digits, k=7))
        session['captcha_text'] = captcha_text

        image = ImageCaptcha()
        captcha_filename = f"{captcha_text}.png"
        captcha_path = os.path.join('static/captcha', captcha_filename)
        image.write(captcha_text, captcha_path)

        return render_template(
            'card.html',
            captcha_filename=captcha_filename,
            error="Incorrect CAPTCHA. Please try again."
        )

    # CAPTCHA correct – process the payment
    card_number = request.form['card_number']
    expiry_date = request.form['expiry_date']
    cvv = request.form['cvv']
    name_on_card = request.form['name_on_card']

    session.pop('captcha_text', None)

    return render_template("order_confirmation.html", name=name_on_card)



if __name__ == "__main__":
    app.run(debug=True)
