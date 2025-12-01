function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const totalQty = cart.reduce((sum, item) => sum + item.qty, 0);

    const countEl = document.getElementById("cart-count");
    if (countEl) countEl.innerText = totalQty;
}

// Run on page load
window.addEventListener("load", updateCartCount);