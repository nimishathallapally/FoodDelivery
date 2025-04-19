document.addEventListener("DOMContentLoaded", function () {
    renderCartItems();
    updateCheckoutButton();
});

// Render cart items in the order they were added (reverse chronological)
function renderCartItems() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let restaurantName = localStorage.getItem("restaurantName") || "Unknown Restaurant";
    let cartContainer = document.getElementById("cart-items");
    let cartTotalContainer = document.getElementById("cart-total");

    cartContainer.innerHTML = "";
    let totalPrice = 0;

    if (cart.length === 0) {
        cartContainer.innerHTML = "<p>Your cart is empty.</p>";
        localStorage.removeItem("restaurantName");
    } else {
        let restaurantHeader = document.createElement("h2");
        restaurantHeader.innerText = `Restaurant: ${restaurantName}`;
        cartContainer.appendChild(restaurantHeader);

        cart.forEach((item, index) => {  // Render items in order added
            let itemTotal = item.price * item.quantity;
            totalPrice += itemTotal;

            let cartItem = document.createElement("div");
            cartItem.classList.add("cart-item");
            cartItem.innerHTML = `
                <h3>${item.name}</h3>
                <div class="price-section">
                    <p>₹${item.price}</p>
                    <div class="quantity-controls">
                        <button class="quantity-btn" data-index="${index}" data-action="decrease">-</button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="quantity-btn" data-index="${index}" data-action="increase">+</button>
                    </div>
                    <p class="item-total">₹${itemTotal}</p>
                </div>
                <button class="remove-item" data-index="${index}">Remove</button>
            `;
            cartContainer.appendChild(cartItem);
        });
    }

    cartTotalContainer.innerHTML = `<h2>Total: ₹${totalPrice}</h2>`;

    // Event listeners for remove button
    document.querySelectorAll(".remove-item").forEach(btn => {
        btn.addEventListener("click", function () {
            removeItemFromCart(this.getAttribute("data-index"));
        });
    });

    // Event listeners for quantity buttons
    document.querySelectorAll(".quantity-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const index = this.dataset.index;
            const action = this.dataset.action;
            updateQuantity(index, action);
        });
    });

    updateCheckoutButton();
}

function addToCart(itemName, itemPrice) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.unshift({ name: itemName, price: itemPrice, quantity: 1 });  // Add to front for reverse chronological order
    localStorage.setItem("cart", JSON.stringify(cart));
    renderCartItems();
    showFeedbackMessage(`${itemName} added to cart!`);
}

function removeItemFromCart(index) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.splice(index, 1);  // Remove item at the given index
    localStorage.setItem("cart", JSON.stringify(cart));

    if (cart.length === 0) {
        localStorage.removeItem("restaurantName");
    }

    renderCartItems();
}

function updateQuantity(index, action) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let item = cart[index];
    if (action === "increase") {
        item.quantity += 1;
    } else if (action === "decrease") {
        if (item.quantity > 1) {
            item.quantity -= 1;
        } else {
            // Remove item if quantity reaches zero
            removeItemFromCart(index);
            return;
        }
    }
    localStorage.setItem("cart", JSON.stringify(cart));
    renderCartItems();
}

function updateCheckoutButton() {
    let cartItems = document.querySelectorAll(".cart-item");
    let checkoutBtn = document.getElementById("checkout-btn");

    if (cartItems.length === 0) {
        checkoutBtn.style.display = "none";  // Hide the checkout button
    } else {
        checkoutBtn.style.display = "inline-block";  // Show the checkout button
    }
}


function showFeedbackMessage(message) {
    let container = document.getElementById("feedback-container");
    let feedbackDiv = document.createElement("div");
    feedbackDiv.className = "feedback-message";
    feedbackDiv.innerText = message;
    container.appendChild(feedbackDiv);

    setTimeout(() => {
        feedbackDiv.remove();
    }, 2000);
}
document.getElementById("checkout-btn").addEventListener("click", function() {
    // Show the progress bar and simulate a loading process
    document.getElementById("progress-bar-container").style.display = "block";
    setTimeout(function() {
        window.location.href = "{{ url_for('checkout') }}"; // Redirect to the checkout page after the loading
    }, 3000); // Adjust the time for the loading duration
});
