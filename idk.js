document.addEventListener('DOMContentLoaded', () => {
    const products = [
        { id: 1, name: 'normal cool cat', price: 10, image: 'images/1.jpg' },
        { id: 2, name: 'abnormal cool cat', price: 15, image: 'images/2.jpg' },
        { id: 3, name: 'he doesnt know he cool', price: 20, image: 'images/3.jpg' },
        { id: 4, name: 'bro so cat', price: 25, image: 'images/4.jpg' },
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