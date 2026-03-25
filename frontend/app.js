// Configuration
// Auto-detect API URL based on environment
const getApiUrl = () => {
  // If on localhost, use local API
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:5000/api';
  }
  
  // If environment variable is set (via window variable), use it
  if (window.__API_URL__) {
    return window.__API_URL__;
  }
  
  // Otherwise, construct from current origin (for Railway/production)
  // Assumes API is on the same domain with /api prefix
  return window.location.origin + '/api';
};

const API_URL = getApiUrl();

// Debug: Log which API URL is being used
console.log('🌐 Using API URL:', API_URL);

let cart = [];
let allProducts = [];
let currentProduct = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    setupEventListeners();
    loadCartFromStorage();
});

// Setup event listeners
function setupEventListeners() {
    document.querySelector('.cart-link').addEventListener('click', (e) => {
        e.preventDefault();
        openCart();
    });
}

// Load products from API
async function loadProducts() {
    try {
        const response = await fetch(`${API_URL}/products?limit=20`);
        const data = await response.json();
        
        if (data.success) {
            allProducts = data.products;
            displayProducts(allProducts);
        } else {
            displayError('Failed to load products');
        }
    } catch (error) {
        console.error('Error loading products:', error);
        displayError('Error connecting to server. Using demo products.');
        displayDemoProducts();
    }
}

// Display products in grid
function displayProducts(products) {
    const grid = document.getElementById('products-grid');
    
    if (products.length === 0) {
        grid.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">No products found</p>';
        return;
    }
    
    grid.innerHTML = products.map(product => `
        <div class="product-card" onclick="viewProduct('${product._id}', '${product.name}', ${product.price}, '${product.character_name}', '${product.condition}', '${product.description}')">
            <div class="product-image">🧸</div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <p class="character">${product.character_name}</p>
                <p class="price">$${product.price.toFixed(2)}</p>
                <span class="product-condition">${product.condition}</span>
                <div class="product-actions">
                    <button onclick="event.stopPropagation(); quickAddToCart('${product._id}', '${product.name}', ${product.price})">Add to Cart</button>
                </div>
            </div>
        </div>
    `).join('');
}

// Display demo products when API is unavailable
function displayDemoProducts() {
    const demoProducts = [
        { _id: '1', name: 'Labubu Hot Spring Ver.', character_name: 'Labubu', price: 150, condition: 'Mint', description: 'Rare hot spring edition with pristine packaging', seller_id: 'seller1' },
        { _id: '2', name: 'Labubu Basquiat Ver.', character_name: 'Labubu', price: 280, condition: 'Like New', description: 'Limited Basquiat collaboration, highly sought after', seller_id: 'seller2' },
        { _id: '3', name: 'Labubu Molly Doll Peace Ver.', character_name: 'Molly', price: 95, condition: 'Good', description: 'Charming peace edition in excellent condition', seller_id: 'seller3' },
        { _id: '4', name: 'Labubu Porcelain Ver.', character_name: 'Labubu', price: 320, condition: 'Mint', description: 'Exclusive porcelain variant with special packaging', seller_id: 'seller1' },
        { _id: '5', name: 'Labubu Kabuki Ver.', character_name: 'Labubu', price: 200, condition: 'Mint', description: 'Japanese traditional Kabuki design limited edition', seller_id: 'seller4' },
        { _id: '6', name: 'Labubu Constellation Ver.', character_name: 'Labubu', price: 175, condition: 'Like New', description: 'Beautiful constellation series collectible', seller_id: 'seller5' }
    ];
    
    allProducts = demoProducts;
    displayProducts(demoProducts);
}

// View product details
function viewProduct(id, name, price, character, condition, description) {
    currentProduct = { id, name, price, character, condition, description };
    
    document.getElementById('detail-name').textContent = name;
    document.getElementById('detail-price').textContent = `$${price.toFixed(2)}`;
    document.getElementById('detail-character').textContent = character;
    document.getElementById('detail-condition').textContent = condition;
    document.getElementById('detail-description').textContent = description;
    document.getElementById('detail-seller').textContent = 'Verified Seller';
    document.getElementById('detail-image').textContent = '🧸';
    
    document.getElementById('product-modal').style.display = 'block';
}

// Close product modal
function closeProductModal() {
    document.getElementById('product-modal').style.display = 'none';
}

// Add to cart from product detail
function addToCart() {
    if (currentProduct) {
        quickAddToCart(currentProduct.id, currentProduct.name, currentProduct.price);
    }
}

// Quick add to cart
function quickAddToCart(productId, productName, productPrice) {
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: productPrice,
            quantity: 1
        });
    }
    
    saveCartToStorage();
    updateCartDisplay();
    showNotification(`${productName} added to cart!`);
    closeProductModal();
}

// Update cart display
function updateCartDisplay() {
    document.getElementById('cart-count').textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
}

// Save cart to localStorage
function saveCartToStorage() {
    localStorage.setItem('labubu-cart', JSON.stringify(cart));
}

// Load cart from localStorage
function loadCartFromStorage() {
    const saved = localStorage.getItem('labubu-cart');
    if (saved) {
        cart = JSON.parse(saved);
        updateCartDisplay();
    }
}

// Open cart modal
function openCart() {
    const cartItemsContainer = document.getElementById('cart-items');
    let totalPrice = 0;
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p style="text-align: center; padding: 2rem;">Your cart is empty</p>';
    } else {
        cartItemsContainer.innerHTML = cart.map((item, index) => {
            const itemTotal = item.price * item.quantity;
            totalPrice += itemTotal;
            
            return `
                <div class="cart-item">
                    <div class="cart-item-info">
                        <h4>${item.name}</h4>
                        <p>$${item.price.toFixed(2)} x ${item.quantity}</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span class="cart-item-price">$${itemTotal.toFixed(2)}</span>
                        <button onclick="removeFromCart(${index})" style="background: #ff6b6b; color: white; border: none; padding: 0.5rem 1rem; border-radius: 3px; cursor: pointer;">Remove</button>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    document.getElementById('total-price').textContent = totalPrice.toFixed(2);
    document.getElementById('cart-modal').style.display = 'block';
}

// Close cart modal
function closeCart() {
    document.getElementById('cart-modal').style.display = 'none';
}

// Remove from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    saveCartToStorage();
    updateCartDisplay();
    openCart();
}

// Checkout
async function checkout() {
    if (cart.length === 0) {
        alert('Your cart is empty');
        return;
    }
    
    // Create order
    const order = {
        user_id: 'user-' + Date.now(),
        items: cart,
        total_price: cart.reduce((sum, item) => sum + item.price * item.quantity, 0),
        shipping_address: 'Demo Address'
    };
    
    try {
        const response = await fetch(`${API_URL}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(order)
        });
        
        const data = await response.json();
        
        if (data.success) {
            cart = [];
            saveCartToStorage();
            updateCartDisplay();
            closeCart();
            showNotification(`Order placed! ID: ${data.order_id}`);
        } else {
            alert('Error placing order: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Checkout error:', error);
        showNotification('Order demo: Successfully placed (server offline)', 'success');
        cart = [];
        saveCartToStorage();
        updateCartDisplay();
        closeCart();
    }
}

// Search products
async function handleSearch() {
    const searchQuery = document.getElementById('search-input').value;
    
    if (!searchQuery) {
        displayProducts(allProducts);
        return;
    }
    
    // First, try API search
    try {
        const response = await fetch(`${API_URL}/products/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: searchQuery })
        });
        
        const data = await response.json();
        if (data.success) {
            displayProducts(data.products);
            return;
        }
    } catch (error) {
        console.error('Search error:', error);
    }
    
    // Fallback to local search
    const filtered = allProducts.filter(product =>
        product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.character_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (product.description && product.description.toLowerCase().includes(searchQuery.toLowerCase()))
    );
    
    displayProducts(filtered);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#ff6b6b' : '#667eea'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        z-index: 9999;
        animation: slideIn 0.3s;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Display error
function displayError(message) {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: #ff6b6b;">
            <p>${message}</p>
            <p style="font-size: 0.9rem; margin-top: 1rem;">Showing demo products instead</p>
        </div>
    `;
}

// Close modals when clicking outside
window.addEventListener('click', (event) => {
    const cartModal = document.getElementById('cart-modal');
    const productModal = document.getElementById('product-modal');
    
    if (event.target == cartModal) {
        cartModal.style.display = 'none';
    }
    
    if (event.target == productModal) {
        productModal.style.display = 'none';
    }
});
