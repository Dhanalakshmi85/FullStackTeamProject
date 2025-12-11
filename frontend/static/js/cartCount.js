function updateCartCount() {
    let cart = [];
    try {
        cart = JSON.parse(localStorage.getItem("cart")) || [];
    } catch (e) {
        console.error("Cart parse error:", e);
        cart = [];
    }

    let total = 0;
    cart.forEach(item => {
        const qty = Number(item.qty || 0);
        if (!isNaN(qty)) total += qty;
    });

    const el = document.getElementById("cart-count");
    if (el) el.innerText = total;
}

// run after DOM ready
document.addEventListener("DOMContentLoaded", updateCartCount);
// Run on page load
//window.addEventListener("load", updateCartCount);