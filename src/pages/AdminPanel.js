"use client"

import { useState, useEffect } from "react"
// import { useAuth } from "../context/AuthContext"

const AdminPanel = () => {
  // const { currentUser } = useAuth()
  const currentUser='hamada'
  const [activeTab, setActiveTab] = useState("dashboard")
  const [stats, setStats] = useState({
    totalUsers: 1250,
    totalItems: 3420,
    activeItems: 2180,
    completedDeals: 890,
    pendingReports: 12,
    monthlyGrowth: 15.3,
  })
  const [users, setUsers] = useState([])
  const [items, setItems] = useState([])
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // محاكاة تحميل البيانات
    const mockUsers = [
      {
        id: 1,
        name: "أحمد محمد",
        email: "ahmed@example.com",
        type: "individual",
        status: "active",
        joinDate: "2024-01-15",
        itemsCount: 5,
        dealsCount: 3,
      },
      {
        id: 2,
        name: "ورشة التدوير الحديثة",
        email: "workshop@example.com",
        type: "workshop",
        status: "active",
        joinDate: "2024-01-10",
        itemsCount: 12,
        dealsCount: 8,
      },
      {
        id: 3,
        name: "مصنع البلاستيك",
        email: "plastic@example.com",
        type: "company",
        status: "suspended",
        joinDate: "2024-01-05",
        itemsCount: 0,
        dealsCount: 0,
      },
    ]

    const mockItems = [
      {
        id: 1,
        title: "أثاث مكتبي مستعمل",
        category: "furniture",
        user: "أحمد محمد",
        status: "active",
        createdAt: "2024-01-15",
        views: 45,
        reports: 0,
      },
      {
        id: 2,
        title: "خردة معادن",
        category: "metals",
        user: "ورشة التدوير",
        status: "pending",
        createdAt: "2024-01-14",
        views: 32,
        reports: 1,
      },
    ]

    const mockReports = [
      {
        id: 1,
        type: "inappropriate_content",
        itemId: 2,
        itemTitle: "خردة معادن",
        reporter: "محمد علي",
        reason: "محتوى غير مناسب",
        status: "pending",
        createdAt: "2024-01-16",
      },
      {
        id: 2,
        type: "fake_item",
        itemId: 3,
        itemTitle: "أجهزة مزيفة",
        reporter: "سارة أحمد",
        reason: "منتج مزيف",
        status: "pending",
        createdAt: "2024-01-15",
      },
    ]

    setTimeout(() => {
      setUsers(mockUsers)
      setItems(mockItems)
      setReports(mockReports)
      setLoading(false)
    }, 1000)
  }, [])

  const handleUserAction = (userId, action) => {
    setUsers((prev) => prev.map((user) => (user.id === userId ? { ...user, status: action } : user)))
    alert(`تم ${action === "active" ? "تفعيل" : "تعليق"} المستخدم بنجاح`)
  }

  const handleItemAction = (itemId, action) => {
    setItems((prev) => prev.map((item) => (item.id === itemId ? { ...item, status: action } : item)))
    alert(`تم ${action === "active" ? "الموافقة على" : "رفض"} المنتج`)
  }

  const handleReportAction = (reportId, action) => {
    setReports((prev) => prev.map((report) => (report.id === reportId ? { ...report, status: action } : report)))
    alert(`تم ${action === "resolved" ? "حل" : "رفض"} البلاغ`)
  }

  // التحقق من صلاحيات الإدارة
  if (currentUser?.userType !== "admin") {
    return (
      <div className="container py-5">
        <div className="text-center">
          <i className="fas fa-lock fs-1 text-danger mb-3"></i>
          <h4>غير مصرح لك بالوصول</h4>
          <p className="text-muted">هذه الصفحة مخصصة للمديرين فقط</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container-fluid py-4">
      {/* Header */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card bg-dark text-white">
            <div className="card-body">
              <h2 className="mb-0">
                <i className="fas fa-cogs me-2"></i>
                لوحة الإدارة
              </h2>
              <p className="mb-0">إدارة المنصة والمستخدمين</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row mb-4">
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body">
              <i className="fas fa-users text-primary fs-1 mb-3"></i>
              <h3 className="text-primary">{stats.totalUsers.toLocaleString()}</h3>
              <p className="text-muted mb-0">إجمالي المستخدمين</p>
            </div>
          </div>
        </div>
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body">
              <i className="fas fa-box text-success fs-1 mb-3"></i>
              <h3 className="text-success">{stats.totalItems.toLocaleString()}</h3>
              <p className="text-muted mb-0">إجمالي المنتجات</p>
            </div>
          </div>
        </div>
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body">
              <i className="fas fa-handshake text-info fs-1 mb-3"></i>
              <h3 className="text-info">{stats.completedDeals.toLocaleString()}</h3>
              <p className="text-muted mb-0">الصفقات المكتملة</p>
            </div>
          </div>
        </div>
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body">
              <i className="fas fa-exclamation-triangle text-warning fs-1 mb-3"></i>
              <h3 className="text-warning">{stats.pendingReports}</h3>
              <p className="text-muted mb-0">البلاغات المعلقة</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="row">
        <div className="col-12">
          <ul className="nav nav-tabs mb-4">
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "dashboard" ? "active" : ""}`}
                onClick={() => setActiveTab("dashboard")}
              >
                <i className="fas fa-chart-bar me-2"></i>
                الإحصائيات
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "users" ? "active" : ""}`}
                onClick={() => setActiveTab("users")}
              >
                <i className="fas fa-users me-2"></i>
                المستخدمين
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "items" ? "active" : ""}`}
                onClick={() => setActiveTab("items")}
              >
                <i className="fas fa-box me-2"></i>
                المنتجات
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "reports" ? "active" : ""}`}
                onClick={() => setActiveTab("reports")}
              >
                <i className="fas fa-flag me-2"></i>
                البلاغات ({stats.pendingReports})
              </button>
            </li>
          </ul>

          {/* Dashboard Tab */}
          {activeTab === "dashboard" && (
            <div className="row">
              <div className="col-lg-8 mb-4">
                <div className="card border-0 shadow-sm">
                  <div className="card-header">
                    <h5 className="mb-0">إحصائيات الاستخدام</h5>
                  </div>
                  <div className="card-body">
                    <div className="row">
                      <div className="col-md-6 mb-3">
                        <canvas id="usersChart" width="400" height="200"></canvas>
                      </div>
                      <div className="col-md-6 mb-3">
                        <canvas id="itemsChart" width="400" height="200"></canvas>
                      </div>
                    </div>
                    <div className="alert alert-info">
                      <i className="fas fa-info-circle me-2"></i>
                      نمو شهري: {stats.monthlyGrowth}%
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-lg-4 mb-4">
                <div className="card border-0 shadow-sm">
                  <div className="card-header">
                    <h5 className="mb-0">النشاط الأخير</h5>
                  </div>
                  <div className="card-body">
                    <div className="list-group list-group-flush">
                      <div className="list-group-item border-0 px-0">
                        <small className="text-muted">منذ 5 دقائق</small>
                        <p className="mb-0">مستخدم جديد انضم للمنصة</p>
                      </div>
                      <div className="list-group-item border-0 px-0">
                        <small className="text-muted">منذ 15 دقيقة</small>
                        <p className="mb-0">تم إضافة منتج جديد</p>
                      </div>
                      <div className="list-group-item border-0 px-0">
                        <small className="text-muted">منذ 30 دقيقة</small>
                        <p className="mb-0">تم إتمام صفقة جديدة</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Users Tab */}
          {activeTab === "users" && (
            <div className="card border-0 shadow-sm">
              <div className="card-header">
                <h5 className="mb-0">إدارة المستخدمين</h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>المستخدم</th>
                        <th>النوع</th>
                        <th>تاريخ الانضمام</th>
                        <th>المنتجات</th>
                        <th>الصفقات</th>
                        <th>الحالة</th>
                        <th>الإجراءات</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.map((user) => (
                        <tr key={user.id}>
                          <td>
                            <div>
                              <strong>{user.name}</strong>
                              <br />
                              <small className="text-muted">{user.email}</small>
                            </div>
                          </td>
                          <td>
                            <span className="badge bg-secondary">
                              {user.type === "individual"
                                ? "فرد"
                                : user.type === "workshop"
                                  ? "ورشة"
                                  : user.type === "company"
                                    ? "شركة"
                                    : user.type}
                            </span>
                          </td>
                          <td>{new Date(user.joinDate).toLocaleDateString("ar-EG")}</td>
                          <td>{user.itemsCount}</td>
                          <td>{user.dealsCount}</td>
                          <td>
                            <span className={`badge ${user.status === "active" ? "bg-success" : "bg-danger"}`}>
                              {user.status === "active" ? "نشط" : "معلق"}
                            </span>
                          </td>
                          <td>
                            <div className="btn-group btn-group-sm">
                              {user.status === "active" ? (
                                <button
                                  className="btn btn-outline-danger"
                                  onClick={() => handleUserAction(user.id, "suspended")}
                                >
                                  تعليق
                                </button>
                              ) : (
                                <button
                                  className="btn btn-outline-success"
                                  onClick={() => handleUserAction(user.id, "active")}
                                >
                                  تفعيل
                                </button>
                              )}
                              <button className="btn btn-outline-primary">عرض</button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Items Tab */}
          {activeTab === "items" && (
            <div className="card border-0 shadow-sm">
              <div className="card-header">
                <h5 className="mb-0">إدارة المنتجات</h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>المنتج</th>
                        <th>الفئة</th>
                        <th>المستخدم</th>
                        <th>تاريخ الإضافة</th>
                        <th>المشاهدات</th>
                        <th>البلاغات</th>
                        <th>الحالة</th>
                        <th>الإجراءات</th>
                      </tr>
                    </thead>
                    <tbody>
                      {items.map((item) => (
                        <tr key={item.id}>
                          <td>
                            <strong>{item.title}</strong>
                          </td>
                          <td>
                            <span className="badge bg-info">
                              {item.category === "furniture"
                                ? "أثاث"
                                : item.category === "metals"
                                  ? "معادن"
                                  : item.category}
                            </span>
                          </td>
                          <td>{item.user}</td>
                          <td>{new Date(item.createdAt).toLocaleDateString("ar-EG")}</td>
                          <td>{item.views}</td>
                          <td>{item.reports > 0 && <span className="badge bg-warning">{item.reports}</span>}</td>
                          <td>
                            <span
                              className={`badge ${
                                item.status === "active"
                                  ? "bg-success"
                                  : item.status === "pending"
                                    ? "bg-warning"
                                    : "bg-danger"
                              }`}
                            >
                              {item.status === "active" ? "نشط" : item.status === "pending" ? "في الانتظار" : "مرفوض"}
                            </span>
                          </td>
                          <td>
                            <div className="btn-group btn-group-sm">
                              {item.status === "pending" && (
                                <>
                                  <button
                                    className="btn btn-outline-success"
                                    onClick={() => handleItemAction(item.id, "active")}
                                  >
                                    موافقة
                                  </button>
                                  <button
                                    className="btn btn-outline-danger"
                                    onClick={() => handleItemAction(item.id, "rejected")}
                                  >
                                    رفض
                                  </button>
                                </>
                              )}
                              <button className="btn btn-outline-primary">عرض</button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Reports Tab */}
          {activeTab === "reports" && (
            <div className="card border-0 shadow-sm">
              <div className="card-header">
                <h5 className="mb-0">إدارة البلاغات</h5>
              </div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>المنتج</th>
                        <th>نوع البلاغ</th>
                        <th>المبلغ</th>
                        <th>السبب</th>
                        <th>التاريخ</th>
                        <th>الحالة</th>
                        <th>الإجراءات</th>
                      </tr>
                    </thead>
                    <tbody>
                      {reports.map((report) => (
                        <tr key={report.id}>
                          <td>
                            <strong>{report.itemTitle}</strong>
                          </td>
                          <td>
                            <span className="badge bg-warning">
                              {report.type === "inappropriate_content"
                                ? "محتوى غير مناسب"
                                : report.type === "fake_item"
                                  ? "منتج مزيف"
                                  : report.type}
                            </span>
                          </td>
                          <td>{report.reporter}</td>
                          <td>{report.reason}</td>
                          <td>{new Date(report.createdAt).toLocaleDateString("ar-EG")}</td>
                          <td>
                            <span
                              className={`badge ${
                                report.status === "pending"
                                  ? "bg-warning"
                                  : report.status === "resolved"
                                    ? "bg-success"
                                    : "bg-secondary"
                              }`}
                            >
                              {report.status === "pending" ? "معلق" : report.status === "resolved" ? "محلول" : "مرفوض"}
                            </span>
                          </td>
                          <td>
                            {report.status === "pending" && (
                              <div className="btn-group btn-group-sm">
                                <button
                                  className="btn btn-outline-success"
                                  onClick={() => handleReportAction(report.id, "resolved")}
                                >
                                  حل
                                </button>
                                <button
                                  className="btn btn-outline-danger"
                                  onClick={() => handleReportAction(report.id, "rejected")}
                                >
                                  رفض
                                </button>
                              </div>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminPanel
