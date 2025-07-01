"use client"

import { useState } from "react"
import { useAuth } from "../context/AuthContext"

const ProfilePage = () => {
  // const { currentUser, login } = useAuth()
  const currentUser='hamada'
  const [activeTab, setActiveTab] = useState("profile")
  const [loading, setLoading] = useState(false)
  const [profileData, setProfileData] = useState({
    name: currentUser?.name || "",
    email: currentUser?.email || "",
    phone: currentUser?.phone || "",
    location: currentUser?.location || "",
    organization: currentUser?.organization || "",
    bio: currentUser?.bio || "",
    userType: currentUser?.userType || "individual",
  })
  const [passwordData, setPasswordData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  })

  const handleProfileChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value,
    })
  }

  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value,
    })
  }

  const handleProfileSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // محاكاة تحديث البيانات
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // تحديث بيانات المستخدم في السياق
      const updatedUser = { ...currentUser, ...profileData }
      login(updatedUser)

      alert("تم تحديث البيانات بنجاح!")
    } catch (error) {
      alert("حدث خطأ أثناء تحديث البيانات")
    } finally {
      setLoading(false)
    }
  }

  const handlePasswordSubmit = async (e) => {
    e.preventDefault()

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      alert("كلمات المرور الجديدة غير متطابقة")
      return
    }

    setLoading(true)

    try {
      // محاكاة تغيير كلمة المرور
      await new Promise((resolve) => setTimeout(resolve, 1000))

      alert("تم تغيير كلمة المرور بنجاح!")
      setPasswordData({
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
      })
    } catch (error) {
      alert("حدث خطأ أثناء تغيير كلمة المرور")
    } finally {
      setLoading(false)
    }
  }

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

  const stats = {
    totalItems: 12,
    activeItems: 8,
    completedDeals: 15,
    rating: 4.6,
    reviewsCount: 23,
  }

  return (
    <div className="container py-4">
      {/* Profile Header */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card bg-success text-white">
            <div className="card-body">
              <div className="row align-items-center">
                <div className="col-md-2 text-center">
                  <img
                    src={currentUser?.avatar || "/placeholder.svg"}
                    alt="الصورة الشخصية"
                    className="rounded-circle border border-white border-3"
                    style={{ width: "100px", height: "100px", objectFit: "cover" }}
                  />
                </div>
                <div className="col-md-6">
                  <h2 className="mb-2">{currentUser?.name}</h2>
                  <p className="mb-1">
                    <i className="fas fa-user-tag me-2"></i>
                    {getUserTypeLabel(currentUser?.userType)}
                  </p>
                  <p className="mb-1">
                    <i className="fas fa-map-marker-alt me-2"></i>
                    {currentUser?.location}
                  </p>
                  <p className="mb-0">
                    <i className="fas fa-calendar me-2"></i>
                    عضو منذ يناير 2024
                  </p>
                </div>
                <div className="col-md-4">
                  <div className="row text-center">
                    <div className="col-6">
                      <h4 className="mb-0">{stats.rating}</h4>
                      <small>التقييم</small>
                      <div>
                        <i className="fas fa-star"></i>
                        <i className="fas fa-star"></i>
                        <i className="fas fa-star"></i>
                        <i className="fas fa-star"></i>
                        <i className="fas fa-star-half-alt"></i>
                      </div>
                    </div>
                    <div className="col-6">
                      <h4 className="mb-0">{stats.completedDeals}</h4>
                      <small>صفقة مكتملة</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <div className="card text-center border-0 shadow-sm">
            <div className="card-body">
              <i className="fas fa-box text-success fs-2 mb-2"></i>
              <h4 className="text-success">{stats.totalItems}</h4>
              <p className="text-muted mb-0">إجمالي الإعلانات</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center border-0 shadow-sm">
            <div className="card-body">
              <i className="fas fa-eye text-info fs-2 mb-2"></i>
              <h4 className="text-info">{stats.activeItems}</h4>
              <p className="text-muted mb-0">إعلانات نشطة</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center border-0 shadow-sm">
            <div className="card-body">
              <i className="fas fa-handshake text-warning fs-2 mb-2"></i>
              <h4 className="text-warning">{stats.completedDeals}</h4>
              <p className="text-muted mb-0">صفقات مكتملة</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center border-0 shadow-sm">
            <div className="card-body">
              <i className="fas fa-star text-warning fs-2 mb-2"></i>
              <h4 className="text-warning">{stats.reviewsCount}</h4>
              <p className="text-muted mb-0">تقييم</p>
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
                className={`nav-link ${activeTab === "profile" ? "active" : ""}`}
                onClick={() => setActiveTab("profile")}
              >
                <i className="fas fa-user me-2"></i>
                الملف الشخصي
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "security" ? "active" : ""}`}
                onClick={() => setActiveTab("security")}
              >
                <i className="fas fa-lock me-2"></i>
                الأمان
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "notifications" ? "active" : ""}`}
                onClick={() => setActiveTab("notifications")}
              >
                <i className="fas fa-bell me-2"></i>
                الإشعارات
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === "privacy" ? "active" : ""}`}
                onClick={() => setActiveTab("privacy")}
              >
                <i className="fas fa-shield-alt me-2"></i>
                الخصوصية
              </button>
            </li>
          </ul>

          {/* Profile Tab */}
          {activeTab === "profile" && (
            <div className="card border-0 shadow-sm">
              <div className="card-header">
                <h5 className="mb-0">تحديث الملف الشخصي</h5>
              </div>
              <div className="card-body">
                <form onSubmit={handleProfileSubmit}>
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="name" className="form-label">
                        الاسم الكامل
                      </label>
                      <input
                        type="text"
                        className="form-control"
                        id="name"
                        name="name"
                        value={profileData.name}
                        onChange={handleProfileChange}
                        required
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="email" className="form-label">
                        البريد الإلكتروني
                      </label>
                      <input
                        type="email"
                        className="form-control"
                        id="email"
                        name="email"
                        value={profileData.email}
                        onChange={handleProfileChange}
                        required
                      />
                    </div>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="phone" className="form-label">
                        رقم الهاتف
                      </label>
                      <input
                        type="tel"
                        className="form-control"
                        id="phone"
                        name="phone"
                        value={profileData.phone}
                        onChange={handleProfileChange}
                        required
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="location" className="form-label">
                        المحافظة
                      </label>
                      <select
                        className="form-select"
                        id="location"
                        name="location"
                        value={profileData.location}
                        onChange={handleProfileChange}
                        required
                      >
                        <option value="">اختر المحافظة</option>
                        <option value="القاهرة">القاهرة</option>
                        <option value="الجيزة">الجيزة</option>
                        <option value="الإسكندرية">الإسكندرية</option>
                        <option value="الدقهلية">الدقهلية</option>
                        <option value="الشرقية">الشرقية</option>
                        <option value="القليوبية">القليوبية</option>
                        <option value="كفر الشيخ">كفر الشيخ</option>
                        <option value="الغربية">الغربية</option>
                        <option value="المنوفية">المنوفية</option>
                        <option value="البحيرة">البحيرة</option>
                      </select>
                    </div>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="userType" className="form-label">
                        نوع المستخدم
                      </label>
                      <select
                        className="form-select"
                        id="userType"
                        name="userType"
                        value={profileData.userType}
                        onChange={handleProfileChange}
                        required
                      >
                        <option value="individual">فرد</option>
                        <option value="workshop">ورشة تدوير</option>
                        <option value="collector">جامع خردة</option>
                        <option value="organization">جمعية بيئية</option>
                        <option value="company">شركة</option>
                      </select>
                    </div>
                    {profileData.userType !== "individual" && (
                      <div className="col-md-6 mb-3">
                        <label htmlFor="organization" className="form-label">
                          اسم المؤسسة
                        </label>
                        <input
                          type="text"
                          className="form-control"
                          id="organization"
                          name="organization"
                          value={profileData.organization}
                          onChange={handleProfileChange}
                        />
                      </div>
                    )}
                  </div>

                  <div className="mb-3">
                    <label htmlFor="bio" className="form-label">
                      نبذة تعريفية
                    </label>
                    <textarea
                      className="form-control"
                      id="bio"
                      name="bio"
                      rows="3"
                      value={profileData.bio}
                      onChange={handleProfileChange}
                      placeholder="اكتب نبذة مختصرة عنك..."
                    ></textarea>
                  </div>

                  <button type="submit" className="btn btn-success" disabled={loading}>
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        جاري الحفظ...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-save me-2"></i>
                        حفظ التغييرات
                      </>
                    )}
                  </button>
                </form>
              </div>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === "security" && (
            <div className="card border-0 shadow-sm">
              <div className="card-header">
                <h5 className="mb-0">تغيير كلمة المرور</h5>
              </div>
              <div className="card-body">
                <form onSubmit={handlePasswordSubmit}>
                  <div className="mb-3">
                    <label htmlFor="currentPassword" className="form-label">
                      كلمة المرور الحالية
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="currentPassword"
                      name="currentPassword"
                      value={passwordData.currentPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label htmlFor="newPassword" className="form-label">
                      كلمة المرور الجديدة
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="newPassword"
                      name="newPassword"
                      value={passwordData.newPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label htmlFor="confirmPassword" className="form-label">
                      تأكيد كلمة المرور الجديدة
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="confirmPassword"
                      name="confirmPassword"
                      value={passwordData.confirmPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </div>

                  <button type="submit" className="btn btn-warning" disabled={loading}>
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        جاري التحديث...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-key me-2"></i>
                        تغيير كلمة المرور
                      </>
                    )}
                  </button>
                </form>
              </div>
            </div>
          )}

          {/* Notifications Tab */}
          {activeTab === "notifications" && (
            <div className="card border-0 shadow-sm">
              <div className="card-header">
                <h5 className="mb-0">إعدادات الإشعارات</h5>
              </div>
              <div className="card-body">
                <div className="mb-3">
                  <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="emailNotifications" defaultChecked />
                    <label className="form-check-label" htmlFor="emailNotifications">
                      إشعارات البريد الإلكتروني
                    </label>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="smsNotifications" />
                    <label className="form-check-label" htmlFor="smsNotifications">
                      إشعارات الرسائل النصية
                    </label>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="orderNotifications" defaultChecked />
                    <label className="form-check-label" htmlFor="orderNotifications">
                      إشعارات الطلبات الجديدة
                    </label>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="messageNotifications" defaultChecked />
                    <label className="form-check-label" htmlFor="messageNotifications">
                      إشعارات الرسائل
                    </label>
                  </div>
                </div>

                <button className="btn btn-success">
                  <i className="fas fa-save me-2"></i>
                  حفظ الإعدادات
                </button>
              </div>
            </div>
          )}

          {/* Privacy Tab */}
          {activeTab === "privacy" && (
            <div className="card border-0 shadow-sm">
              <div className="card-header">
                <h5 className="mb-0">إعدادات الخصوصية</h5>
              </div>
              <div className="card-body">
                <div className="mb-3">
                  <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="showPhone" defaultChecked />
                    <label className="form-check-label" htmlFor="showPhone">
                      إظهار رقم الهاتف للمستخدمين
                    </label>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="showEmail" />
                    <label className="form-check-label" htmlFor="showEmail">
                      إظهار البريد الإلكتروني للمستخدمين
                    </label>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="allowMessages" defaultChecked />
                    <label className="form-check-label" htmlFor="allowMessages">
                      السماح بالرسائل من المستخدمين
                    </label>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="form-check form-switch">
                    <input className="form-check-input" type="checkbox" id="showActivity" defaultChecked />
                    <label className="form-check-label" htmlFor="showActivity">
                      إظهار آخر نشاط
                    </label>
                  </div>
                </div>

                <button className="btn btn-success">
                  <i className="fas fa-save me-2"></i>
                  حفظ الإعدادات
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
