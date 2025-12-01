function sanitizeName(name) {
    return name.replace(/\s+/g, '-').replace(/[^a-zA-Z0-9-_]/g, '');
}

// Load cart from localStorage and render it
function loadCart() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    let html = "";
    let total = 0;

    cart.forEach(item => {
        total += item.price * item.qty;
        const safeName = sanitizeName(item.name);

        html += `
        <div class="cart-row">
            <strong>${item.name}</strong>
            — €${(item.price * item.qty).toFixed(2)}
            <br>
            Qty:
            <button onclick="updateQty('${item.name}', -1)">-</button>
            <span id="qty-${safeName}">${item.qty}</span>
            <button onclick="updateQty('${item.name}', 1)">+</button>
            <br>
        </div>
        `;
    });

    document.getElementById("cart-items").innerHTML = html;
    document.getElementById("cart-total").innerText = total.toFixed(2);
}

// Update quantity for a cart item
function updateQty(name, amt) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let item = cart.find(i => i.name === name);
    if (!item) return;

    item.qty += amt;

    // Optional: remove item if quantity < 1
    if (item.qty < 1) {
        cart = cart.filter(i => i.name !== name);
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    loadCart();
    updateCartCount();
}


document.getElementById("checkout-btn").addEventListener("click", () => {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    if(cart.length === 0){
        alert("Your cart is empty!");
        return;
    }

    // Here you can redirect to a checkout page or payment flow
    alert("Proceeding to checkout...\nTotal: €" + cart.reduce((sum, item) => sum + item.price * item.qty, 0).toFixed(2));
    // window.location.href = "/checkout"; // example redirect
});

// Initial load
window.addEventListener("load", loadCart);