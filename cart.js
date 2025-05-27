/**
 * Renderiza el carrito de compras obteniendo los elementos del carrito desde localStorage,
 * mostrándolos en el DOM y calculando el precio total.
 * Si el carrito está vacío, muestra un mensaje indicándolo.
 */
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

/**
 * Vacía el carrito de compras eliminando los datos del carrito de localStorage
 * y vuelve a renderizar la vista del carrito.
 */
function clearCart() {
    localStorage.removeItem('cart');
    renderCart();
}
renderCart();