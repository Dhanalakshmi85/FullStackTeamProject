// cart.js - render cart and place order

function loadCart() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const container = document.getElementById("cart-items");
    const totalEl = document.getElementById("cart-total");

    if (!container || !totalEl) return;

    let html = "";
    let total = 0;

    cart.forEach(item => {
        const subtotal = (Number(item.price) || 0) * (Number(item.qty) || 0);
        total += subtotal;
        const safeName = encodeURIComponent(item.name);

        html += `
          <div class="cart-row" data-id="${item.id}">
            <strong>${item.name}</strong> — €${subtotal.toFixed(2)}<br>
            Qty:
            <button onclick="updateQtyCart('${safeName}', -1)">-</button>
            <span id="cart-qty-${item.id}">${item.qty}</span>
            <button onclick="updateQtyCart('${safeName}', 1)">+</button>
          </div>
        `;
    });

    container.innerHTML = html;
    totalEl.innerText = total.toFixed(2);
}

// update qty from cart page (nameEncoded)
function updateQtyCart(nameEncoded, delta) {
    const name = decodeURIComponent(nameEncoded);
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    const idx = cart.findIndex(it => it.name === name);
    if (idx === -1) return;

    cart[idx].qty = Number(cart[idx].qty) + Number(delta);
    if (cart[idx].qty <= 0) cart.splice(idx, 1);

    localStorage.setItem("cart", JSON.stringify(cart));
    if (typeof updateCartCount === "function") updateCartCount();
    loadCart();
}

async function placeOrder() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    if (!cart.length) {
        alert("Cart is empty");
        return;
    }

    // defensive normalization: ensure price and qty are numbers
    const normalized = cart.map(c => ({
        id: c.id,
        name: c.name,
        price: Number(c.price) || 0,
        qty: Number(c.qty) || 0
    })).filter(c => c.qty > 0);

    try {
        const resp = await fetch("/place-order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cart: normalized })
        });

        const data = await resp.json();
        if (data.success) {
            localStorage.removeItem("cart");
            if (typeof updateCartCount === "function") updateCartCount();
            alert("Order placed!");
            window.location.href = "/menu";
        } else {
            alert("Order failed: " + (data.message || "unknown"));
        }
    } catch (err) {
        console.error("placeOrder error", err);
        alert("Error placing order");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const checkoutBtn = document.getElementById("checkout-btn");
    if (checkoutBtn) checkoutBtn.addEventListener("click", placeOrder);
    loadCart();
});
