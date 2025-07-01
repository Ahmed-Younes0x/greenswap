"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
// import { useAuth } from "../context/AuthContext"

const OrdersPage = () => {
  // const { currentUser } = useAuth()
  const currentUser='hamada'
  const [activeTab, setActiveTab] = useState("received")
  const [orders, setOrders] = useState({
    received: [],
    sent: [],
    completed: [],
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // محاكاة تحميل الطلبات
    const mockOrders = {
      received: [
        {
          id: 1,
          item: {
            id: 1,
            title: "أثاث مكتبي مستعمل",
            image: "/placeholder.svg?height=100&width=100",
            category: "أثاث",
          },
          buyer: {
            id: 2,
            name: "أحمد محمد",
            avatar: "/placeholder.svg?height=50&width=50",
            rating: 4.5,
          },
          message: "أريد شراء هذا الأثاث، هل يمكن التفاوض على السعر؟",
          status: "pending",
          createdAt: "2024-01-15T10:30:00",
          price: "300",
        },
        {
          id: 2,
          item: {
            id: 2,
            title: "خردة معادن",
            image: "/placeholder.svg?height=100&width=100",
            category: "معادن",
          },
          buyer: {
            id: 3,
            name: "ورشة التدوير",
            avatar: "/placeholder.svg?height=50&width=50",
            rating: 4.8,
          },
          message: "نحن مهتمون بشراء هذه المعادن، ما هو السعر النهائي؟",
          status: "accepted",
          createdAt: "2024-01-14T15:45:00",
          price: "500 جنيه",
        },
      ],
      sent: [
        {
          id: 3,
          item: {
            id: 3,
            title: "بلاستيك للتدوير",
            image: "/placeholder.svg?height=100&width=100",
            category: "بلاستيك",
          },
          seller: {
            id: 4,
            name: "مصنع البلاستيك",
            avatar: "/placeholder.svg?height=50&width=50",
            rating: 4.6,
          },
          message: "أريد شراء كمية كبيرة من البلاستيك",
          status: "pending",
          createdAt: "2024-01-13T09:20:00",
          price: "200 جنيه",
        },
      ],
      completed: [
        {
          id: 4,
          item: {
            id: 4,
            title: "أجهزة إلكترونية قديمة",
            image: "/placeholder.svg?height=100&width=100",
            category: "إلكترونيات",
          },
          buyer: {
            id: 5,
            name: "محل الإلكترونيات",
            avatar: "/placeholder.svg?height=50&width=50",
            rating: 4.3,
          },
          message: "تم الاتفاق على الصفقة",
          status: "completed",
          createdAt: "2024-01-10T14:00:00",
          completedAt: "2024-01-12T16:30:00",
          price: "300 جنيه",
        },
      ],
    }

    setTimeout(() => {
      setOrders(mockOrders)
      setLoading(false)
    }, 1000)
  }, [])

  const getStatusLabel = (status) => {
    const statuses = {
      pending: { label: "في الانتظار", class: "warning" },
      accepted: { label: "مقبول", class: "success" },
      rejected: { label: "مرفوض", class: "danger" },
      completed: { label: "مكتمل", class: "info" },
    }
    return statuses[status] || { label: status, class: "secondary" }
  }

  const handleOrderAction = (orderId, action) => {
    // محاكاة تحديث حالة الطلب
    setOrders((prev) => ({
      ...prev,
      received: prev.received.map((order) => (order.id === orderId ? { ...order, status: action } : order)),
    }))

    alert(`تم ${action === "accepted" ? "قبول" : "رفض"} الطلب بنجاح`)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("ar-EG", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  if (loading) {
    return (
      <div className="container py-5">
        <div className="text-center">
          <div className="spinner-border text-success" role="status">
            <span className="visually-hidden">جاري التحميل...</span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container py-4">
      {/* Page Header */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card bg-success text-white">
            <div className="card-body">
              <h2 className="mb-0">
                <i className="fas fa-list-alt me-2"></i>
                إدارة الطلبات
              </h2>
              <p className="mb-0">تابع جميع طلباتك المرسلة والمستلمة</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="row mb-4">
        <div className="col-12">
          <ul className="nav nav-pills nav-fill">
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "received" ? "active" : ""}`}
                onClick={() => setActiveTab("received")}
              >
                <i className="fas fa-inbox me-2"></i>
                الطلبات المستلمة ({orders.received.length})
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "sent" ? "active" : ""}`}
                onClick={() => setActiveTab("sent")}
              >
                <i className="fas fa-paper-plane me-2"></i>
                الطلبات المرسلة ({orders.sent.length})
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "completed" ? "active" : ""}`}
                onClick={() => setActiveTab("completed")}
              >
                <i className="fas fa-check-circle me-2"></i>
                الطلبات المكتملة ({orders.completed.length})
              </button>
            </li>
          </ul>
        </div>
      </div>

      {/* Orders Content */}
      <div className="row">
        <div className="col-12">
          {/* Received Orders */}
          {activeTab === "received" && (
            <div>
              {orders.received.length === 0 ? (
                <div className="text-center py-5">
                  <i className="fas fa-inbox fs-1 text-muted mb-3"></i>
                  <h4 className="text-muted">لا توجد طلبات مستلمة</h4>
                  <p className="text-muted">عندما يرسل لك أحد طلباً، ستظهر هنا</p>
                </div>
              ) : (
                <div className="row">
                  {orders.received.map((order) => (
                    <div key={order.id} className="col-lg-6 mb-4">
                      <div className="card border-0 shadow-sm">
                        <div className="card-body">
                          <div className="d-flex align-items-start mb-3">
                            <img
                              src={order.item.image || "/placeholder.svg"}
                              alt={order.item.title}
                              className="rounded me-3"
                              style={{ width: "80px", height: "80px", objectFit: "cover" }}
                            />
                            <div className="flex-grow-1">
                              <h6 className="mb-1">{order.item.title}</h6>
                              <span className="badge bg-secondary mb-2">{order.item.category}</span>
                              <p className="text-success fw-bold mb-0">{order.price}</p>
                            </div>
                            <span className={`badge bg-${getStatusLabel(order.status).class}`}>
                              {getStatusLabel(order.status).label}
                            </span>
                          </div>

                          <div className="d-flex align-items-center mb-3">
                            <img
                              src={order.buyer.avatar || "/placeholder.svg"}
                              alt={order.buyer.name}
                              className="rounded-circle me-2"
                              style={{ width: "30px", height: "30px", objectFit: "cover" }}
                            />
                            <div>
                              <small className="fw-bold">{order.buyer.name}</small>
                              <div>
                                <i className="fas fa-star text-warning me-1"></i>
                                <small>{order.buyer.rating}</small>
                              </div>
                            </div>
                          </div>

                          <div className="mb-3">
                            <p className="text-muted small mb-1">رسالة المشتري:</p>
                            <p className="mb-0">{order.message}</p>
                          </div>

                          <div className="mb-3">
                            <small className="text-muted">
                              <i className="fas fa-clock me-1"></i>
                              {formatDate(order.createdAt)}
                            </small>
                          </div>

                          {order.status === "pending" && (
                            <div className="d-flex gap-2">
                              <button
                                className="btn btn-success btn-sm flex-grow-1"
                                onClick={() => handleOrderAction(order.id, "accepted")}
                              >
                                <i className="fas fa-check me-1"></i>
                                قبول
                              </button>
                              <button
                                className="btn btn-outline-danger btn-sm flex-grow-1"
                                onClick={() => handleOrderAction(order.id, "rejected")}
                              >
                                <i className="fas fa-times me-1"></i>
                                رفض
                              </button>
                              <Link to={`/chat?user=${order.buyer.id}`} className="btn btn-outline-primary btn-sm">
                                <i className="fas fa-comments"></i>
                              </Link>
                            </div>
                          )}

                          {order.status === "accepted" && (
                            <div className="d-flex gap-2">
                              <Link to={`/chat?user=${order.buyer.id}`} className="btn btn-primary btn-sm flex-grow-1">
                                <i className="fas fa-comments me-1"></i>
                                تواصل مع المشتري
                              </Link>
                              <button
                                className="btn btn-success btn-sm"
                                onClick={() => handleOrderAction(order.id, "completed")}
                              >
                                <i className="fas fa-check-circle me-1"></i>
                                إتمام الصفقة
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Sent Orders */}
          {activeTab === "sent" && (
            <div>
              {orders.sent.length === 0 ? (
                <div className="text-center py-5">
                  <i className="fas fa-paper-plane fs-1 text-muted mb-3"></i>
                  <h4 className="text-muted">لا توجد طلبات مرسلة</h4>
                  <p className="text-muted">عندما ترسل طلباً لأحد، ستظهر هنا</p>
                  <Link to="/search" className="btn btn-success">
                    تصفح المنتجات
                  </Link>
                </div>
              ) : (
                <div className="row">
                  {orders.sent.map((order) => (
                    <div key={order.id} className="col-lg-6 mb-4">
                      <div className="card border-0 shadow-sm">
                        <div className="card-body">
                          <div className="d-flex align-items-start mb-3">
                            <img
                              src={order.item.image || "/placeholder.svg"}
                              alt={order.item.title}
                              className="rounded me-3"
                              style={{ width: "80px", height: "80px", objectFit: "cover" }}
                            />
                            <div className="flex-grow-1">
                              <h6 className="mb-1">{order.item.title}</h6>
                              <span className="badge bg-secondary mb-2">{order.item.category}</span>
                              <p className="text-success fw-bold mb-0">{order.price}</p>
                            </div>
                            <span className={`badge bg-${getStatusLabel(order.status).class}`}>
                              {getStatusLabel(order.status).label}
                            </span>
                          </div>

                          <div className="d-flex align-items-center mb-3">
                            <img
                              src={order.seller.avatar || "/placeholder.svg"}
                              alt={order.seller.name}
                              className="rounded-circle me-2"
                              style={{ width: "30px", height: "30px", objectFit: "cover" }}
                            />
                            <div>
                              <small className="fw-bold">{order.seller.name}</small>
                              <div>
                                <i className="fas fa-star text-warning me-1"></i>
                                <small>{order.seller.rating}</small>
                              </div>
                            </div>
                          </div>

                          <div className="mb-3">
                            <p className="text-muted small mb-1">رسالتك:</p>
                            <p className="mb-0">{order.message}</p>
                          </div>

                          <div className="mb-3">
                            <small className="text-muted">
                              <i className="fas fa-clock me-1"></i>
                              {formatDate(order.createdAt)}
                            </small>
                          </div>

                          <div className="d-flex gap-2">
                            <Link to={`/item/${order.item.id}`} className="btn btn-outline-success btn-sm flex-grow-1">
                              <i className="fas fa-eye me-1"></i>
                              عرض المنتج
                            </Link>
                            <Link to={`/chat?user=${order.seller.id}`} className="btn btn-primary btn-sm">
                              <i className="fas fa-comments"></i>
                            </Link>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Completed Orders */}
          {activeTab === "completed" && (
            <div>
              {orders.completed.length === 0 ? (
                <div className="text-center py-5">
                  <i className="fas fa-check-circle fs-1 text-muted mb-3"></i>
                  <h4 className="text-muted">لا توجد طلبات مكتملة</h4>
                  <p className="text-muted">الصفقات المكتملة ستظهر هنا</p>
                </div>
              ) : (
                <div className="row">
                  {orders.completed.map((order) => (
                    <div key={order.id} className="col-lg-6 mb-4">
                      <div className="card border-0 shadow-sm">
                        <div className="card-body">
                          <div className="d-flex align-items-start mb-3">
                            <img
                              src={order.item.image || "/placeholder.svg"}
                              alt={order.item.title}
                              className="rounded me-3"
                              style={{ width: "80px", height: "80px", objectFit: "cover" }}
                            />
                            <div className="flex-grow-1">
                              <h6 className="mb-1">{order.item.title}</h6>
                              <span className="badge bg-secondary mb-2">{order.item.category}</span>
                              <p className="text-success fw-bold mb-0">{order.price}</p>
                            </div>
                            <span className="badge bg-success">
                              <i className="fas fa-check me-1"></i>
                              مكتمل
                            </span>
                          </div>

                          <div className="d-flex align-items-center mb-3">
                            <img
                              src={order.buyer.avatar || "/placeholder.svg"}
                              alt={order.buyer.name}
                              className="rounded-circle me-2"
                              style={{ width: "30px", height: "30px", objectFit: "cover" }}
                            />
                            <div>
                              <small className="fw-bold">{order.buyer.name}</small>
                              <div>
                                <i className="fas fa-star text-warning me-1"></i>
                                <small>{order.buyer.rating}</small>
                              </div>
                            </div>
                          </div>

                          <div className="mb-3">
                            <div className="row">
                              <div className="col-6">
                                <small className="text-muted d-block">تاريخ الطلب</small>
                                <small>{formatDate(order.createdAt)}</small>
                              </div>
                              <div className="col-6">
                                <small className="text-muted d-block">تاريخ الإتمام</small>
                                <small>{formatDate(order.completedAt)}</small>
                              </div>
                            </div>
                          </div>

                          <div className="d-flex gap-2">
                            <button className="btn btn-outline-warning btn-sm flex-grow-1">
                              <i className="fas fa-star me-1"></i>
                              تقييم المشتري
                            </button>
                            <button className="btn btn-outline-primary btn-sm">
                              <i className="fas fa-download me-1"></i>
                              فاتورة
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default OrdersPage
