function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    
    let totalQty = 0;
    cart.forEach(item => {
        totalQty += item.qty;
    });

    document.getElementById("cart-count").innerText = totalQty;
}

// run when page loads
window.addEventListener("load", updateCartCount);