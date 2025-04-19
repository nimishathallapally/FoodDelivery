document.addEventListener("DOMContentLoaded", function () {
  updateCartCount();
  renderCartItems();

  // Attach event listeners to all "ADD" buttons on page load
  document.querySelectorAll(".add-to-cart").forEach((button) => {
    button.addEventListener("click", function () {
      let itemName = this.getAttribute("data-name");
      let itemPrice = parseFloat(this.getAttribute("data-price"));
      let restaurantName = this.getAttribute("data-restaurant");
      addToCart(this, itemName, itemPrice, restaurantName);
    });
  });
});

function renderCartItems() {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  let cartItemsHTML = "";

  cart.forEach((item) => {
    cartItemsHTML += `
            <div class="cart-item">
                <span class="item-name">${item.name}</span>
                <span class="item-quantity">${item.quantity}</span>
                <span class="item-price">₹${item.price * item.quantity}</span>
            </div>
        `;
  });

  const cartItemsContainer = document.getElementById("cart-items");
  if (cartItemsContainer) {
    cartItemsContainer.innerHTML = cartItemsHTML;
  } else {
    console.error("Cart items container not found!");
  }

  updateCartTotal();
}
function addToCart(button, itemName, itemPrice, restaurantName) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  let storedRestaurant = localStorage.getItem("restaurantName");

  // Debugging logs
  console.log("Cart:", cart);
  console.log("Stored Restaurant:", storedRestaurant);
  console.log("Attempting to add item from restaurant:", restaurantName);

  // If the cart has items from a different restaurant, alert and stop further action
  if (
    cart.length > 0 &&
    storedRestaurant &&
    storedRestaurant !== restaurantName
  ) {
    console.log(
      `Cart contains items from ${storedRestaurant}. New restaurant is ${restaurantName}.`
    );
    alert(
      `Your cart contains items from ${storedRestaurant}. Clear the cart to order from ${restaurantName}.`
    );
    return; // Stop further action (return early)
  }

  // If the restaurant name is not yet stored, store it
  if (!storedRestaurant) {
    console.log(
      "No restaurant in cart, storing the restaurant name:",
      restaurantName
    );
    localStorage.setItem("restaurantName", restaurantName);
  }

  // Add item to cart
  let itemIndex = cart.findIndex((item) => item.name === itemName);
  if (itemIndex !== -1) {
    cart[itemIndex].quantity += 1;
    console.log(`${itemName} quantity updated to ${cart[itemIndex].quantity}`);
  } else {
    cart.push({ name: itemName, price: itemPrice, quantity: 1 });
    console.log(`Added new item to cart: ${itemName}`);
  }

  // Store the updated cart in localStorage
  localStorage.setItem("cart", JSON.stringify(cart));

  // Update the cart count (you can also log this to see the change)
  updateCartCount();

  // Replace the "ADD" button with quantity selector
  const quantityControl = document.createElement("div");
  quantityControl.classList.add("quantity-control");
  quantityControl.innerHTML = `
        <div class="quantity-selector">
            <button class="decrease-btn">−</button>
            <span class="quantity">1</span>
            <button class="increase-btn">+</button>
        </div>
    `;

  button.replaceWith(quantityControl);

  // Attach event listeners to the new buttons
  quantityControl
    .querySelector(".decrease-btn")
    .addEventListener("click", function () {
      updateQuantity(itemName, -1, quantityControl);
    });

  quantityControl
    .querySelector(".increase-btn")
    .addEventListener("click", function () {
      updateQuantity(itemName, 1, quantityControl);
    });

  // Show feedback popup
  showFeedbackPopUp(itemName);
}

function updateQuantity(itemName, change, quantityControl) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  let itemIndex = cart.findIndex((item) => item.name === itemName);

  if (itemIndex !== -1) {
    cart[itemIndex].quantity += change;

    if (cart[itemIndex].quantity <= 0) {
      cart.splice(itemIndex, 1);

      // Restore "ADD" button when quantity reaches 0
      const addButton = document.createElement("button");
      addButton.classList.add("add-to-cart");
      addButton.textContent = "ADD";
      addButton.setAttribute("data-name", itemName);
      addButton.setAttribute("data-price", cart[itemIndex]?.price || 0);
      addButton.addEventListener("click", function () {
        addToCart(this, itemName, itemPrice);
      });

      quantityControl.replaceWith(addButton);
    } else {
      quantityControl.querySelector(".quantity").textContent =
        cart[itemIndex].quantity;
    }
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  updateCartCount();
  renderCartItems();
}

function updateCartCount() {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  let cartCountElement = document.getElementById("cart-count");

  if (cartCountElement) {
    cartCountElement.textContent = cart.length;
  }
}

function showFeedbackPopUp(itemName) {
  const feedbackPopup = document.getElementById("feedback-popup");
  const feedbackMessage = document.getElementById("feedback-message");

  feedbackMessage.textContent = `${itemName} added to cart!`;

  feedbackPopup.style.display = "block";

  feedbackPopup.classList.add("show");

  setTimeout(function () {
    feedbackPopup.classList.remove("show");
  }, 2000);
}

// Function to calculate the total price of cart items
function updateCartTotal() {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  let total = 0;

  // Calculate total price of all cart items
  cart.forEach((item) => {
    total += item.price * item.quantity;
  });

  // Update the cart total display
  const cartTotalElement = document.getElementById("cart-total");
  if (cartTotalElement) {
    cartTotalElement.textContent = `Total: ₹${total.toFixed(2)}`;
  }
}

