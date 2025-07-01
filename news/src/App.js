"use client"

import { useEffect } from "react"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { AuthProvider } from "./contexts/AuthContext"
import { ThemeProvider } from "./contexts/ThemeContext"
import { LanguageProvider } from "./contexts/LanguageContext"
import { GamificationProvider } from "./contexts/GamificationContext"

// Components
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"
import ProtectedRoute from "./components/ProtectedRoute"

// Pages
import HomePage from "./pages/HomePage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import Dashboard from "./pages/Dashboard"
import SearchPage from "./pages/SearchPage"
import AddItemPage from "./pages/AddItemPage"
import ItemDetailsPage from "./pages/ItemDetailsPage"
import ChatPage from "./pages/ChatPage"
import OrdersPage from "./pages/OrdersPage"
import ProfilePage from "./pages/ProfilePage"
import AdminPanel from "./pages/AdminPanel"

// Services
import pwaService from "./services/pwaService"

// Styles
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.bundle.min.js"
import "@fortawesome/fontawesome-free/css/all.min.css"
import "./App.css"

function App() {
  useEffect(() => {
    // تهيئة PWA
    pwaService.init()

    // إضافة skip link للوصولية
    const skipLink = document.createElement("a")
    skipLink.href = "#main-content"
    skipLink.className = "skip-link"
    skipLink.textContent = "تخطي إلى المحتوى الرئيسي"
    document.body.insertBefore(skipLink, document.body.firstChild)

    // تحسين الأداء - تحميل الخطوط مسبقاً
    const fontLink = document.createElement("link")
    fontLink.rel = "preload"
    fontLink.href = "https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap"
    fontLink.as = "style"
    fontLink.onload = function () {
      this.onload = null
      this.rel = "stylesheet"
    }
    document.head.appendChild(fontLink)

    // إضافة meta tags للـ SEO
    const metaDescription = document.createElement("meta")
    metaDescription.name = "description"
    metaDescription.content = "منصة GreenSwap Egypt - ربط الأفراد والمؤسسات لإعادة تدوير المخلفات وحماية البيئة"
    document.head.appendChild(metaDescription)

    const metaKeywords = document.createElement("meta")
    metaKeywords.name = "keywords"
    metaKeywords.content = "إعادة تدوير, مخلفات, بيئة, مصر, تدوير, استدامة"
    document.head.appendChild(metaKeywords)

    // إضافة structured data للـ SEO
    const structuredData = {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      name: "GreenSwap Egypt",
      description: "منصة رقمية لربط الأفراد والمؤسسات لإعادة تدوير المخلفات",
      url: window.location.origin,
      applicationCategory: "EnvironmentalApplication",
      operatingSystem: "Web Browser",
      offers: {
        "@type": "Offer",
        price: "0",
        priceCurrency: "EGP",
      },
    }

    const script = document.createElement("script")
    script.type = "application/ld+json"
    script.textContent = JSON.stringify(structuredData)
    document.head.appendChild(script)

    // تحسين الأداء - lazy loading للصور
    if ("IntersectionObserver" in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const img = entry.target
            img.src = img.dataset.src
            img.classList.remove("lazy")
            imageObserver.unobserve(img)
          }
        })
      })

      // مراقبة الصور الجديدة
      const observeImages = () => {
        document.querySelectorAll("img[data-src]").forEach((img) => {
          imageObserver.observe(img)
        })
      }

      // مراقبة التغييرات في DOM
      const mutationObserver = new MutationObserver(observeImages)
      mutationObserver.observe(document.body, {
        childList: true,
        subtree: true,
      })

      observeImages()
    }

    // تحسين الأداء - preload للصفحات المهمة
    const preloadPages = ["/search", "/dashboard", "/add-item"]
    preloadPages.forEach((page) => {
      const link = document.createElement("link")
      link.rel = "prefetch"
      link.href = page
      document.head.appendChild(link)
    })
  }, [])

  return (
    <LanguageProvider>
      <ThemeProvider>
        <AuthProvider>
          <GamificationProvider>
            <Router>
              <div className="App">
                <Navbar />

                <main id="main-content" className="main-content" role="main">
                  <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/search" element={<SearchPage />} />
                    <Route path="/item/:id" element={<ItemDetailsPage />} />

                    {/* Protected Routes */}
                    <Route
                      path="/dashboard"
                      element={
                        <ProtectedRoute>
                          <Dashboard />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/add-item"
                      element={
                        <ProtectedRoute>
                          <AddItemPage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/chat"
                      element={
                        <ProtectedRoute>
                          <ChatPage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/orders"
                      element={
                        <ProtectedRoute>
                          <OrdersPage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/profile"
                      element={
                        <ProtectedRoute>
                          <ProfilePage />
                        </ProtectedRoute>
                      }
                    />

                    {/* Admin Routes */}
                    <Route
                      path="/admin"
                      element={
                        <ProtectedRoute adminOnly>
                          <AdminPanel />
                        </ProtectedRoute>
                      }
                    />
                  </Routes>
                </main>

                <Footer />
              </div>
            </Router>
          </GamificationProvider>
        </AuthProvider>
      </ThemeProvider>
    </LanguageProvider>
  )
}

export default App
