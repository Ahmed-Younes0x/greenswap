import axios from "axios"

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api"

// إنشاء instance من axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// إضافة interceptor للتوكن
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// إضافة interceptor للاستجابة
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem("refresh_token")
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          })

          const { access } = response.data
          localStorage.setItem("access_token", access)

          // إعادة المحاولة مع التوكن الجديد
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // فشل في تجديد التوكن - تسجيل خروج
        localStorage.removeItem("access_token")
        localStorage.removeItem("refresh_token")
        localStorage.removeItem("user")
        window.location.href = "/login"
      }
    }

    return Promise.reject(error)
  },
)

// Auth API
export const authAPI = {
  register: (userData) => api.post("/auth/register/", userData),
  login: (credentials) => api.post("/auth/login/", credentials),
  logout: (refreshToken) => api.post("/auth/logout/", { refresh: refreshToken }),
  getCurrentUser: () => api.get("/auth/current-user/"),
  updateProfile: (userData) => api.patch("/auth/profile/", userData),
}

// Items API
export const itemsAPI = {
  getCategories: () => api.get("/items/categories/"),
  getItems: (params) => api.get("/items/", { params }),
  getItem: (id) => api.get(`/items/${id}/`),
  createItem: (itemData) => {
    const formData = new FormData()
    Object.keys(itemData).forEach((key) => {
      if (key === "images") {
        itemData[key].forEach((image) => {
          formData.append("images", image)
        })
      } else {
        formData.append(key, itemData[key])
      }
    })
    return api.post("/items/create/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },
  updateItem: (id, itemData) => api.patch(`/items/${id}/update/`, itemData),
  deleteItem: (id) => api.delete(`/items/${id}/update/`),
  getMyItems: () => api.get("/items/my-items/"),
  markInterested: (itemId) => api.post(`/items/${itemId}/interested/`),
  reportItem: (reportData) => api.post("/items/report/", reportData),
  searchItems: (params) => api.get("/items/search/", { params }),
  getFeaturedItems: () => api.get("/items/featured/"),
  getStats: () => api.get("/items/stats/"),
}

// Orders API
export const ordersAPI = {
  getOrders: (params) => api.get("/orders/", { params }),
  createOrder: (orderData) => api.post("/orders/", orderData),
  updateOrder: (id, orderData) => api.patch(`/orders/${id}/`, orderData),
  getMyOrders: () => api.get("/orders/my-orders/"),
}

// Chat API
export const chatAPI = {
  getConversations: () => api.get("/chat/conversations/"),
  getMessages: (conversationId) => api.get(`/chat/conversations/${conversationId}/messages/`),
  sendMessage: (conversationId, messageData) =>
    api.post(`/chat/conversations/${conversationId}/messages/`, messageData),
  createConversation: (userData) => api.post("/chat/conversations/", userData),
}

// Notifications API
export const notificationsAPI = {
  getNotifications: () => api.get("/notifications/"),
  markAsRead: (id) => api.patch(`/notifications/${id}/`, { is_read: true }),
  markAllAsRead: () => api.post("/notifications/mark-all-read/"),
}

// Reviews API
export const reviewsAPI = {
  getReviews: (userId) => api.get(`/reviews/?user=${userId}`),
  createReview: (reviewData) => api.post("/reviews/", reviewData),
  updateReview: (id, reviewData) => api.patch(`/reviews/${id}/`, reviewData),
}

export default api
