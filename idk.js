document.addEventListener('DOMContentLoaded', () => {
    const products = [
        { id: 1, name: '1', price: 10, image: '' },
        { id: 2, name: '2', price: 15, image: '' },
        { id: 3, name: '3', price: 20, image: '' },
        { id: 4, name: '4', price: 25, image: '' },
        { id: 5, name: '5', price: 30, image: '' },
        { id: 6, name: '6', price: 35, image: '' },
        { id: 7, name: '7', price: 40, image: '' },
        { id: 8, name: '8', price: 45, image: '' },
        { id: 9, name: '9', price: 50, image: '' },
        { id: 10, name: '10', price: 55, image: '' },
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