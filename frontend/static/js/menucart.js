let cart = JSON.parse(localStorage.getItem("cart")) || [];

let menuQt = {};

function changeMenuQty(itemName, amt) {
    if (!menuQt[itemName]) {
        menuQt[itemName] = 0;
    }   
    menuQt[itemName] += amt;

    if (menuQt[itemName] < 0) {
        menuQt[itemName] = 0;
    }   

    document.getElementById(`qty-${itemName}`).innerText = menuQt[itemName];
}


function addToCart(itemName, itemPrice) {

    itemPrice = parseFloat(itemPrice);
    const quantity = menuQt[itemName] || 0;
    
    if (quantity === 0) {
        return;
    }                                                                       
  
     let existing = cart.find(item => item.name === itemName);

         if (existing) {
             existing.qty += quantity;  // item exists → increase qty
        } else {
            cart.push({ name: itemName, price: itemPrice, qty: quantity }); // new item
        }
 

   


    menuQt[itemName] = 0;
    document.getElementById(`qty-${itemName}`).innerText = 0;

    localStorage.setItem("cart", JSON.stringify(cart));


    updateCartCount();

    console.log("Cart:", cart);



}