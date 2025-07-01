import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.bundle.min.js"

// Components
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"

// Pages
import HomePage from "./pages/HomePage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import Dashboard from "./pages/Dashboard"
import AddItemPage from "./pages/AddItemPage"
import SearchPage from "./pages/SearchPage"
import ItemDetailsPage from "./pages/ItemDetailsPage"
import ChatPage from "./pages/ChatPage"
import OrdersPage from "./pages/OrdersPage"
import ProfilePage from "./pages/ProfilePage"
import AdminPanel from "./pages/AdminPanel"

// Context
import { AuthProvider } from "./context/AuthContext"

import "./App.css"

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/add-item" element={<AddItemPage />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/item/:id" element={<ItemDetailsPage />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/orders" element={<OrdersPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/admin" element={<AdminPanel />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
