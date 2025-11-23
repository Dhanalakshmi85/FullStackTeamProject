function loadCart() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];

    let html = "";
    let total = 0;

    cart.forEach(item => {
        total += item.price * item.qty;

        html += `
            <div class="cart-row">
                <strong>${item.name}</strong> (x${item.qty})  
                — €${item.price * item.qty}
            </div>
        `;
    });

    document.getElementById("cart-items").innerHTML = html;
    document.getElementById("cart-total").innerText = total.toFixed(2);
}

window.onload = loadCart;