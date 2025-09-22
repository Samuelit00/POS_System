// POS XYZ System - API Client
class APIClient {
    constructor() {
        this.baseURL = '';
        this.token = localStorage.getItem('access_token');
    }

    // Set auth token
    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('access_token', token);
        } else {
            localStorage.removeItem('access_token');
        }
    }

    // Get auth headers
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    // Generic request method
    async request(url, options = {}) {
        const config = {
            headers: this.getHeaders(),
            ...options
        };

        try {
            const response = await fetch(this.baseURL + url, config);
            
            if (!response.ok) {
                if (response.status === 401) {
                    this.setToken(null);
                    window.location.href = '/login';
                    return;
                }
                
                let errorMessage = 'Error en la petición';
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorMessage;
                } catch (e) {
                    errorMessage = response.statusText || errorMessage;
                }
                
                throw new Error(errorMessage);
            }

            // Handle no content responses
            if (response.status === 204) {
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    // GET request
    async get(url) {
        return this.request(url, { method: 'GET' });
    }

    // POST request
    async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // PUT request
    async put(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // DELETE request
    async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }

    // PATCH request
    async patch(url, data) {
        return this.request(url, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }

    // Auth endpoints
    async login(email, password) {
        const response = await this.post('/api/usuarios/login', {
            email,
            password
        });
        
        if (response.access_token) {
            this.setToken(response.access_token);
        }
        
        return response;
    }

    async logout() {
        this.setToken(null);
        window.location.href = '/login';
    }

    // User endpoints
    async getUsers() {
        return this.get('/api/usuarios/');
    }

    async createUser(userData) {
        return this.post('/api/usuarios/', userData);
    }

    async getUser(userId) {
        return this.get(`/api/usuarios/${userId}`);
    }

    async deleteUser(userId) {
        return this.delete(`/api/usuarios/${userId}`);
    }

    // Product endpoints
    async getProducts() {
        return this.get('/api/productos/');
    }

    async createProduct(productData) {
        return this.post('/api/productos/', productData);
    }

    async getProduct(productId) {
        return this.get(`/api/productos/${productId}`);
    }

    async updateProduct(productId, productData) {
        return this.patch(`/api/productos/${productId}`, productData);
    }

    async deleteProduct(productId) {
        return this.delete(`/api/productos/${productId}`);
    }

    // Sales endpoints
    async getSales(params = {}) {
        const searchParams = new URLSearchParams(params);
        const queryString = searchParams.toString();
        return this.get(`/api/ventas/${queryString ? '?' + queryString : ''}`);
    }

    async createSale(saleData) {
        return this.post('/api/ventas/', saleData);
    }

    async getSale(saleId) {
        return this.get(`/api/ventas/${saleId}`);
    }

    async deleteSale(saleId) {
        return this.delete(`/api/ventas/${saleId}`);
    }

    // Dashboard endpoints
    async getDashboardMetrics() {
        return this.get('/api/dashboard/metrics');
    }
}

// Create global API instance
const api = new APIClient();
