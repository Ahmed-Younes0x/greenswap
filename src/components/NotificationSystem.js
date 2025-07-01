"use client"

import { useState, useEffect } from "react"
import { useAuth } from "../context/AuthContext"

const NotificationSystem = () => {
  const { currentUser } = useAuth()
  const [notifications, setNotifications] = useState([])
  const [showDropdown, setShowDropdown] = useState(false)
  const [unreadCount, setUnreadCount] = useState(0)

  useEffect(() => {
    if (currentUser) {
      // محاكاة تحميل الإشعارات
      const mockNotifications = [
        {
          id: 1,
          type: "new_order",
          title: "طلب جديد",
          message: "لديك طلب جديد على منتج الأثاث المكتبي",
          read: false,
          createdAt: "2024-01-16T10:30:00",
          icon: "fas fa-shopping-cart",
          color: "success",
        },
        {
          id: 2,
          type: "message",
          title: "رسالة جديدة",
          message: "رسالة جديدة من أحمد محمد",
          read: false,
          createdAt: "2024-01-16T09:15:00",
          icon: "fas fa-envelope",
          color: "primary",
        },
        {
          id: 3,
          type: "deal_completed",
          title: "صفقة مكتملة",
          message: "تم إتمام صفقة بنجاح مع ورشة التدوير",
          read: true,
          createdAt: "2024-01-15T16:45:00",
          icon: "fas fa-check-circle",
          color: "info",
        },
      ]

      setNotifications(mockNotifications)
      setUnreadCount(mockNotifications.filter((n) => !n.read).length)
    }
  }, [currentUser])

  const markAsRead = (notificationId) => {
    setNotifications((prev) =>
      prev.map((notification) => (notification.id === notificationId ? { ...notification, read: true } : notification)),
    )
    setUnreadCount((prev) => Math.max(0, prev - 1))
  }

  const markAllAsRead = () => {
    setNotifications((prev) => prev.map((notification) => ({ ...notification, read: true })))
    setUnreadCount(0)
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInHours = (now - date) / (1000 * 60 * 60)

    if (diffInHours < 1) {
      return "منذ دقائق"
    } else if (diffInHours < 24) {
      return `منذ ${Math.floor(diffInHours)} ساعة`
    } else {
      return date.toLocaleDateString("ar-EG")
    }
  }

  if (!currentUser) return null

  return (
    <div className="dropdown">
      <button
        className="btn btn-link text-white position-relative"
        onClick={() => setShowDropdown(!showDropdown)}
        style={{ textDecoration: "none" }}
      >
        <i className="fas fa-bell fs-5"></i>
        {unreadCount > 0 && (
          <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
            {unreadCount > 99 ? "99+" : unreadCount}
          </span>
        )}
      </button>

      {showDropdown && (
        <div className="dropdown-menu dropdown-menu-end show" style={{ width: "350px", maxHeight: "400px" }}>
          <div className="dropdown-header d-flex justify-content-between align-items-center">
            <h6 className="mb-0">الإشعارات</h6>
            {unreadCount > 0 && (
              <button className="btn btn-sm btn-link text-primary p-0" onClick={markAllAsRead}>
                تحديد الكل كمقروء
              </button>
            )}
          </div>

          <div className="dropdown-divider"></div>

          <div style={{ maxHeight: "300px", overflowY: "auto" }}>
            {notifications.length === 0 ? (
              <div className="text-center py-4">
                <i className="fas fa-bell-slash text-muted fs-3 mb-2"></i>
                <p className="text-muted mb-0">لا توجد إشعارات</p>
              </div>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`dropdown-item ${!notification.read ? "bg-light" : ""}`}
                  onClick={() => markAsRead(notification.id)}
                  style={{ cursor: "pointer", whiteSpace: "normal" }}
                >
                  <div className="d-flex align-items-start">
                    <div className={`text-${notification.color} me-3 mt-1`}>
                      <i className={notification.icon}></i>
                    </div>
                    <div className="flex-grow-1">
                      <h6 className="mb-1 fs-6">{notification.title}</h6>
                      <p className="mb-1 text-muted small">{notification.message}</p>
                      <small className="text-muted">{formatTime(notification.createdAt)}</small>
                    </div>
                    {!notification.read && (
                      <div className="bg-primary rounded-circle" style={{ width: "8px", height: "8px" }}></div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="dropdown-divider"></div>
          <div className="dropdown-item text-center">
            <button className="btn btn-sm btn-outline-primary">عرض جميع الإشعارات</button>
          </div>
        </div>
      )}

      {showDropdown && (
        <div
          className="position-fixed top-0 start-0 w-100 h-100"
          style={{ zIndex: -1 }}
          onClick={() => setShowDropdown(false)}
        ></div>
      )}
    </div>
  )
}

export default NotificationSystem
