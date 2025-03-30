document.addEventListener('DOMContentLoaded', () => {
    const products = [
        { id: 1, name: 'Product 1', price: 10, image: 'https://via.placeholder.com/150' },
        { id: 2, name: 'Product 2', price: 15, image: 'https://via.placeholder.com/150' },
        { id: 3, name: 'Product 3', price: 20, image: 'https://via.placeholder.com/150' },
        { id: 4, name: 'Product 4', price: 25, image: 'https://via.placeholder.com/150' },
        { id: 5, name: 'Product 5', price: 30, image: 'https://via.placeholder.com/150' },
        { id: 6, name: 'Product 6', price: 35, image: 'https://via.placeholder.com/150' },
        { id: 7, name: 'Product 7', price: 40, image: 'https://via.placeholder.com/150' },
        { id: 8, name: 'Product 8', price: 45, image: 'https://via.placeholder.com/150' },
        { id: 9, name: 'Product 9', price: 50, image: 'https://via.placeholder.com/150' },
        { id: 10, name: 'Product 10', price: 55, image: 'https://via.placeholder.com/150' },
    ];

    const cart = [];
    const productsContainer = document.getElementById('products');
    const cartContainer = document.getElementById('cart');
    const totalContainer = document.getElementById('total');

    const renderProducts = () => {
        products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.classList.add('product');
            productElement.innerHTML = `
                <img src="${product.image}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p>$${product.price}</p>
                <button onclick="addToCart(${product.id})">Add to Cart</button>
            `;
            productsContainer.appendChild(productElement);
        });
    };

    const renderCart = () => {
        cartContainer.innerHTML = '';
        let total = 0;
        cart.forEach(item => {
            const cartItem = document.createElement('li');
            cartItem.textContent = `${item.name} - $${item.price}`;
            cartContainer.appendChild(cartItem);
            total += item.price;
        });
        totalContainer.textContent = `Total: $${total}`;
    };

    window.addToCart = (id) => {
        const product = products.find(p => p.id === id);
        if (product) {
            cart.push(product);
            renderCart();
        }
    };

    renderProducts();
});