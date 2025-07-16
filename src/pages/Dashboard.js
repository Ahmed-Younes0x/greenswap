"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

const Dashboard = () => {
  const { currentUser } = useAuth()
  const [stats, setStats] = useState({
    myItems: 12,
    activeOrders: 5,
    completedDeals: 8,
    messages: 3,
  })
  const [recentActivity, setRecentActivity] = useState([])

  useEffect(() => {
    // محاكاة تحميل النشاط الأخير
    setRecentActivity([
      {
        id: 1,
        type: "new_order",
        message: "طلب جديد على أثاث المكتب",
        time: "منذ ساعتين",
        icon: "fas fa-shopping-cart",
        color: "success",
      },
      {
        id: 2,
        type: "message",
        message: "رسالة جديدة من أحمد محمد",
        time: "منذ 4 ساعات",
        icon: "fas fa-envelope",
        color: "primary",
      },
      {
        id: 3,
        type: "item_viewed",
        message: "تم عرض إعلانك 15 مرة اليوم",
        time: "منذ 6 ساعات",
        icon: "fas fa-eye",
        color: "info",
      },
      {
        id: 4,
        type: "deal_completed",
        message: "تم إتمام صفقة بنجاح",
        time: "أمس",
        icon: "fas fa-check-circle",
        color: "success",
      },
    ])
  }, [])

  const getUserTypeLabel = (type) => {
    const types = {
      individual: "فرد",
      workshop: "ورشة تدوير",
      collector: "جامع خردة",
      organization: "جمعية بيئية",
      company: "شركة",
    }
    return types[type] || "غير محدد"
  }

  return (
    <div className="container py-4">
      {/* Welcome Section */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card bg-success text-white">
            <div className="card-body">
              <div className="row align-items-center">
                <div className="col-md-8">
                  <h2 className="mb-2">مرحباً، {currentUser?.name}</h2>
                  <p className="mb-0">
                    <i className="fas fa-user-tag me-2"></i>
                    {getUserTypeLabel(currentUser?.userType)}
                  </p>
                  <p className="mb-0">
                    <i className="fas fa-map-marker-alt me-2"></i>
                    {currentUser?.location}
                  </p>
                </div>
                <div className="col-md-4 text-center">
                  <img
                    src={currentUser?.avatar || "/placeholder.svg"}
                    alt="الصورة الشخصية"
                    className="rounded-circle"
                    style={{ width: "80px", height: "80px", objectFit: "cover" }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row mb-4">
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center">
              <i className="fas fa-box text-success fs-1 mb-3"></i>
              <h3 className="text-success">{stats.myItems}</h3>
              <p className="text-muted mb-0">إعلاناتي</p>
            </div>
          </div>
        </div>
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center">
              <i className="fas fa-shopping-cart text-warning fs-1 mb-3"></i>
              <h3 className="text-warning">{stats.activeOrders}</h3>
              <p className="text-muted mb-0">طلبات نشطة</p>
            </div>
          </div>
        </div>
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center">
              <i className="fas fa-handshake text-info fs-1 mb-3"></i>
              <h3 className="text-info">{stats.completedDeals}</h3>
              <p className="text-muted mb-0">صفقات مكتملة</p>
            </div>
          </div>
        </div>
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center">
              <i className="fas fa-envelope text-primary fs-1 mb-3"></i>
              <h3 className="text-primary">{stats.messages}</h3>
              <p className="text-muted mb-0">رسائل جديدة</p>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        {/* Quick Actions */}
        <div className="col-lg-4 mb-4">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-header bg-white">
              <h5 className="mb-0">إجراءات سريعة</h5>
            </div>
            <div className="card-body">
              <div className="d-grid gap-2">
                <Link to="/add-item" className="btn btn-success">
                  <i className="fas fa-plus me-2"></i>
                  إضافة مخلف جديد
                </Link>
                <Link to="/search" className="btn btn-outline-success">
                  <i className="fas fa-search me-2"></i>
                  البحث عن مواد
                </Link>
                <Link to="/orders" className="btn btn-outline-primary">
                  <i className="fas fa-list me-2"></i>
                  إدارة الطلبات
                </Link>
                <Link to="/chat" className="btn btn-outline-info">
                  <i className="fas fa-comments me-2"></i>
                  المحادثات
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="col-lg-8 mb-4">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 className="mb-0">النشاط الأخير</h5>
              <Link to="/activity" className="btn btn-sm btn-outline-success">
                عرض الكل
              </Link>
            </div>
            <div className="card-body">
              {recentActivity.length > 0 ? (
                <div className="list-group list-group-flush">
                  {recentActivity.map((activity) => (
                    <div key={activity.id} className="list-group-item border-0 px-0">
                      <div className="d-flex align-items-center">
                        <div className={`text-${activity.color} me-3`}>
                          <i className={`${activity.icon} fs-5`}></i>
                        </div>
                        <div className="flex-grow-1">
                          <p className="mb-1">{activity.message}</p>
                          <small className="text-muted">{activity.time}</small>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center text-muted py-4">
                  <i className="fas fa-inbox fs-1 mb-3"></i>
                  <p>لا يوجد نشاط حديث</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Tips Section */}
      <div className="row">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <h5 className="mb-0">
                <i className="fas fa-lightbulb text-warning me-2"></i>
                نصائح للاستفادة القصوى من المنصة
              </h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-4 mb-3">
                  <div className="d-flex align-items-start">
                    <i className="fas fa-camera text-success me-3 mt-1"></i>
                    <div>
                      <h6>أضف صور واضحة</h6>
                      <p className="text-muted small mb-0">الصور الواضحة تزيد من فرص البيع</p>
                    </div>
                  </div>
                </div>
                <div className="col-md-4 mb-3">
                  <div className="d-flex align-items-start">
                    <i className="fas fa-edit text-success me-3 mt-1"></i>
                    <div>
                      <h6>اكتب وصف مفصل</h6>
                      <p className="text-muted small mb-0">الوصف المفصل يجذب المشترين</p>
                    </div>
                  </div>
                </div>
                <div className="col-md-4 mb-3">
                  <div className="d-flex align-items-start">
                    <i className="fas fa-reply text-success me-3 mt-1"></i>
                    <div>
                      <h6>رد بسرعة</h6>
                      <p className="text-muted small mb-0">الرد السريع يزيد من ثقة العملاء</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
