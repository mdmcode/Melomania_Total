function renderCart() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const container = document.getElementById('cart-list');
    const totalDiv = document.getElementById('cart-total');
    container.innerHTML = '';
    let total = 0;
    if (cart.length === 0) {
        container.innerHTML = '<p style="grid-column: 1 / -1; text-align:center; color: #f2f2ff;">Tu carrito está vacío.</p>';
        totalDiv.textContent = '';
        return;
    }
    cart.forEach(album => {
        total += Number(album.price);
        const albumDiv = document.createElement('div');
        albumDiv.className = 'product';
        albumDiv.innerHTML = `
                    <img src="${album.cover}" alt="Album Cover">
                    <h3>${album.title}</h3>
                    <p>${album.artist}</p>
                    <p>$${album.price}</p>
                `;
        container.appendChild(albumDiv);
    });
    totalDiv.textContent = 'Total: $' + total;
}
function clearCart() {
    localStorage.removeItem('cart');
    renderCart();
}
renderCart();