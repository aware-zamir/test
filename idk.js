document.addEventListener('DOMContentLoaded', () => {
    const products = [
        { id: 1, name: 'normal cool cat', price: 10, image: 'images/1.jpg' },
        { id: 2, name: 'abnormal cool cat', price: 15, image: 'images/2.jpg' },
        { id: 3, name: 'he doesnt know he cool', price: 20, image: 'images/3.jpg' },
        { id: 4, name: 'bro so cat', price: 25, image: 'images/4.jpg' },
        { id: 5, name: 'puss after rewatching mincraft movie two days in row', price: 30, image: 'images/5.webp' },
        { id: 6, name: 'witchcar', price: 35, image: 'images/6.webp' },
        { id: 7, name: 'we have business to miew', price: 40, image: 'images/7.webp' },
        { id: 8, name: 'fr?', price: 45, image: 'images/8.webp' },
        { id: 9, name: 'you siad you like bikers right', price: 50, image: 'images/9.webp' },
        { id: 10, name: 'catasrophic', price: 55, image: 'images/10.webp' },
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