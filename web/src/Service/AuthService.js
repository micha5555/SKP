class AuthService {
    getToken() {
        return localStorage.getItem('token');
    }
  
    setToken(token) {
        localStorage.setItem('token', token);
    }
  
    removeToken() {
        localStorage.removeItem('token');
    }
  
    isAuthenticated() {
        const token = this.getToken();
        return !!token;
    }
}
  
export default new AuthService();
  