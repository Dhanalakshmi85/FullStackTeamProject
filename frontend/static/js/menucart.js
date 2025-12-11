// menucart.js - single source of truth for menu quantities & adding to cart

// menuQt keys are itemId strings (the same as item._id)
let menuQt = {};

// Increase/decrease quantity in menu UI
function changeMenuQty(itemId, amt) {
    if (!itemId) return;
    if (!menuQt[itemId]) menuQt[itemId] = 0;
    menuQt[itemId] = Number(menuQt[itemId]) + Number(amt);
    if (menuQt[itemId] < 0) menuQt[itemId] = 0;

    const qtyEl = document.getElementById(`qty-${itemId}`);
    if (qtyEl) qtyEl.innerText = menuQt[itemId];
}

// Add item to cart: itemId (string), itemPrice (number), itemName (string)
function addToCart(itemId, itemPrice, itemName) {
    // validate args
    if (!itemId || !itemName) {
        console.error("addToCart missing args", itemId, itemPrice, itemName);
        return;
    }

    // Ensure price is a number
    itemPrice = parseFloat(itemPrice.toString().replace("€", '').trim());
    if (isNaN(itemPrice)) {
        console.error("Invalid price for item:", itemName, itemPrice);
        alert("Cannot add item: invalid price.");
        return;
    }

    const qty = Number(menuQt[itemId] || 0);

    if (qty <= 0) {
        alert("Please choose a quantity before adding to cart.");
        return;
    }

    // load current cart
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    // find by id
    const existing = cart.find(it => it.id === itemId);

    if (existing) {
        existing.qty = Number(existing.qty || 0) + qty;
    } else {
        cart.push({
            id: String(itemId),
            name: itemName,
            price: itemPrice,
            qty: Number(qty)
        });
    }

    // persist and update UI
    localStorage.setItem("cart", JSON.stringify(cart));
    menuQt[itemId] = 0;
    const qtyEl = document.getElementById(`qty-${itemId}`);
    if (qtyEl) qtyEl.innerText = 0;

    if (typeof updateCartCount === "function") updateCartCount();
    console.log("Cart saved:", cart);
}

