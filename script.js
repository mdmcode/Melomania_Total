const ALBUMS_PER_PAGE = 12;
let albums = [];
let currentPage = 1;
let totalPages = 1;

function renderAlbums(page) {
    const container = document.getElementById("album-list");
    container.innerHTML = "";
  const start = (page - 1) * ALBUMS_PER_PAGE;
    const end = start + ALBUMS_PER_PAGE;
    const pageAlbums = albums.slice(start, end);
    pageAlbums.forEach((album) => {
    const albumDiv = document.createElement("div");
    albumDiv.className = "product";
    albumDiv.innerHTML = `
        <img src="${album.cover}" alt="Album Cover">
        <h3>${album.title}</h3>
        <p>${album.artist}</p>
        <p>$${album.price}</p>
        <button class="add-to-cart-btn" data-index="${start + pageAlbums.indexOf(album)}">Agregar al carrito</button>
    `;
    container.appendChild(albumDiv);
    });

    container.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const albumIndex = parseInt(this.getAttribute('data-index'));
        addToCart(albums[albumIndex]);
    });
});
}

function renderPagination() {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";
    for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    btn.style.padding = "8px 14px";
    btn.style.borderRadius = "5px";
    btn.style.border = "1px solid #ccc";
    btn.style.background = i === currentPage ? "#ffd700" : "#fff";
    btn.style.cursor = "pointer";
    btn.style.fontWeight = i === currentPage ? "bold" : "normal";
    btn.onclick = () => {
        currentPage = i;
        renderAlbums(currentPage);
        renderPagination();
        window.scrollTo({ top: 0, behavior: "smooth" });
    };
    pagination.appendChild(btn);
    }
}

fetch("albums.json")
    .then((response) => response.json())
    .then((data) => {
    albums = data;
    totalPages = Math.ceil(albums.length / ALBUMS_PER_PAGE);
    renderAlbums(currentPage);
    renderPagination();
});

function addToCart(album) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push(album);
    localStorage.setItem('cart', JSON.stringify(cart));
    alert('Álbum agregado al carrito');
}