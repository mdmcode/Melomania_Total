const ALBUMS_PER_PAGE = 12;
let albums = [];
let currentPage = 1;
let totalPages = 1;
let searchTerm = "";

function renderAlbums(page) {
    const container = document.getElementById("album-list");
    container.innerHTML = "";

    // Filtra los álbumes según el término de búsqueda
    const filteredAlbums = albums.filter(album =>
        album.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        album.artist.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    // Calcula la cantidad de paginas
    totalPages = Math.ceil(filteredAlbums.length / ALBUMS_PER_PAGE);
    if (page > totalPages) page = 1;
    currentPage = page;
    
    const start = (page - 1) * ALBUMS_PER_PAGE;
    const end = start + ALBUMS_PER_PAGE;
    const pageAlbums = filteredAlbums.slice(start, end);

    // Muestra los albums encontrados
    pageAlbums.forEach((album) => {
        const albumDiv = document.createElement("div");
        albumDiv.className = "product";
        albumDiv.innerHTML = `
        <a href="album.html?title=${encodeURIComponent(album.title)}&artist=${encodeURIComponent(album.artist)}">
            <img src="${album.cover}" alt="Album Cover">
            <h3>${album.title}</h3>
        </a>
        <p>${album.artist}</p>
        <p>$${album.price}</p>
        <div class = 'botones_product'>
            <button class="add-to-cart-btn" data-index="${start + pageAlbums.indexOf(album)}">Agregar al carrito</button>
            <button class="add-to-wishlist-btn" data-index="${start + pageAlbums.indexOf(album)}">❤️ Wishlist</button>
        </div>
    `;
        container.appendChild(albumDiv);
    });

    // Event listeners
    container.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const albumIndex = parseInt(this.getAttribute('data-index'));
            addToCart(albums[albumIndex]);
        });
    });

    container.querySelectorAll('.add-to-wishlist-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const albumIndex = parseInt(this.getAttribute('data-index'));
            addToWishlist(albums[albumIndex]);
        });
    });

    // Carga la paginacion segun la cantidad de albums
    renderPagination();
}

// Se encarga de la paginacion de la tienda
function renderPagination() {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";
    // Segun la cantidad total de paginas, crea los botones para acceder a cada pagina
    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement("button");
        btn.textContent = i;
        btn.style.padding = "8px 14px";
        btn.style.borderRadius = "5px";
        btn.style.border = "1px solid #ccc";
        btn.style.background = i === currentPage ? "#ffd700" : "#fff";
        btn.style.cursor = "pointer";
        btn.style.fontWeight = i === currentPage ? "bold" : "normal";
        // Cuando se hace click en cada boton, se carga la pagina correspondiente
        btn.onclick = () => {
            currentPage = i;
            renderAlbums(currentPage);
            renderPagination();
            window.scrollTo({ top: 0, behavior: "smooth" });
        };
        pagination.appendChild(btn);
    }
}

// Agrega un album al carrito
function addToCart(album) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push(album);
    localStorage.setItem('cart', JSON.stringify(cart));
    alert('Álbum agregado al carrito');
}

// Agrega a la wishlist
function addToWishlist(album) {
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    // Evita duplicados
    if (!wishlist.some(a => a.title === album.title && a.artist === album.artist)) {
        wishlist.push(album);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        alert('Álbum agregado a tu wishlist');
    } else {
        alert('Este álbum ya está en tu wishlist');
    }
}

// Carga los albums a partir del json
fetch("albums.json")
    .then((response) => response.json())
    .then((data) => {
        albums = data;
        totalPages = Math.ceil(albums.length / ALBUMS_PER_PAGE);
        renderAlbums(currentPage);
        renderPagination();
        // Permite la busqueda:
        const searchBar = document.getElementById('search-bar');
        if (searchBar) {
            searchBar.addEventListener('input', function() {
                searchTerm = this.value;
                renderAlbums(1);
            });
        }
    });