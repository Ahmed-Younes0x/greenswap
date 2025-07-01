"use client"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"

import RatingSystem from "../src/components/RatingSystem"
import HomePage from "../src/pages/HomePage"
import Dashboard from "../src/pages/Dashboard"
import LoginPage from "../src/pages/LoginPage"
import RegisterPage from "../src/pages/RegisterPage"
import AddItemPage from "../src/pages/AddItemPage"
import SearchPage from "../src/pages/SearchPage"
import ItemDetailsPage from "../src/pages/ItemDetailsPage"
import ChatPage from "../src/pages/ChatPage"
import OrdersPage from "../src/pages/OrdersPage"
import ProfilePage from "../src/pages/ProfilePage"
import AdminPanel from "../src/pages/AdminPanel"
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from "D:/Development/gs/src/components/Navbar.js"
import Footer from "D:/Development/gs/src/components/Footer"

export default function SyntheticV0PageForDeployment() {
  return (
        <Router>
                <div className="App">
                  <Navbar />
                  <main className="main-content">
                    <Routes>
                      {/* <Route path="/" element={<HomePage />} /> */}
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
  
)
}