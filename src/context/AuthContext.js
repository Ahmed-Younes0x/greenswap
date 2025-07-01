"use client"

import { createContext, useContext, useState, useEffect } from "react"
import { authAPI } from "../services/api"

const AuthContext = createContext()

export const useAuth = () => {
  return useContext(AuthContext)
}

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    const token = localStorage.getItem("access_token")
    if (token) {
      try {
        const response = await authAPI.getCurrentUser()
        setCurrentUser(response.data)
      } catch (error) {
        console.error("Error checking auth status:", error)
        logout()
      }
    }
    setLoading(false)
  }

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials)
      const { user, tokens } = response.data

      localStorage.setItem("access_token", tokens.access)
      localStorage.setItem("refresh_token", tokens.refresh)
      localStorage.setItem("user", JSON.stringify(user))

      setCurrentUser(user)
      return { success: true, user }
    } catch (error) {
      console.error("Login error:", error)
      return {
        success: false,
        error: error.response?.data?.detail || "حدث خطأ أثناء تسجيل الدخول",
      }
    }
  }

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData)
      const { user, tokens } = response.data

      localStorage.setItem("access_token", tokens.access)
      localStorage.setItem("refresh_token", tokens.refresh)
      localStorage.setItem("user", JSON.stringify(user))

      setCurrentUser(user)
      return { success: true, user }
    } catch (error) {
      console.error("Registration error:", error)
      return {
        success: false,
        error: error.response?.data || "حدث خطأ أثناء إنشاء الحساب",
      }
    }
  }

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem("refresh_token")
      if (refreshToken) {
        await authAPI.logout(refreshToken)
      }
    } catch (error) {
      console.error("Logout error:", error)
    } finally {
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
      localStorage.removeItem("user")
      setCurrentUser(null)
    }
  }

  const updateProfile = async (userData) => {
    try {
      const response = await authAPI.updateProfile(userData)
      setCurrentUser(response.data)
      localStorage.setItem("user", JSON.stringify(response.data))
      return { success: true, user: response.data }
    } catch (error) {
      console.error("Update profile error:", error)
      return {
        success: false,
        error: error.response?.data || "حدث خطأ أثناء تحديث البيانات",
      }
    }
  }

  const value = {
    currentUser,
    login,
    register,
    logout,
    updateProfile,
    loading,
  }

  return <AuthContext.Provider value={value}>{!loading && children}</AuthContext.Provider>
}
