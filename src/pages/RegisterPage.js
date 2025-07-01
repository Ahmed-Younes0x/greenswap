"use client"

import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
// import { useAuth } from "../context/AuthContext"

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password_confirm: "",
    first_name: "",
    last_name: "",
    user_type: "individual",
    phone: "",
    location: "",
    organization: "",
    bio: "",
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  // const { register } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    if (formData.password !== formData.password_confirm) {
      setError("كلمات المرور غير متطابقة")
      setLoading(false)
      return
    }

    // const result = await register(formData)

    if (result.success || 1) { // edited for prototype
      navigate("/dashboard")
    } else {
      setError(result.error)
    }

    setLoading(false)
  }

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
          <div className="card shadow-lg border-0">
            <div className="card-body p-5">
              <div className="text-center mb-4">
                <i className="fas fa-recycle text-success fs-1 mb-3"></i>
                <h2 className="fw-bold">إنشاء حساب جديد</h2>
                <p className="text-muted">انضم إلى مجتمع GreenSwap Egypt</p>
              </div>

              {error && (
                <div className="alert alert-danger" role="alert">
                  {typeof error === "object" ? JSON.stringify(error) : error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="username" className="form-label">
                      اسم المستخدم
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="username"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      required
                      placeholder="أدخل اسم المستخدم"
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
                      value={formData.email}
                      onChange={handleChange}
                      required
                      placeholder="أدخل بريدك الإلكتروني"
                    />
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="first_name" className="form-label">
                      الاسم الأول
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="first_name"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleChange}
                      required
                      placeholder="أدخل اسمك الأول"
                    />
                  </div>

                  <div className="col-md-6 mb-3">
                    <label htmlFor="last_name" className="form-label">
                      الاسم الأخير
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="last_name"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                      required
                      placeholder="أدخل اسمك الأخير"
                    />
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="password" className="form-label">
                      كلمة المرور
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      placeholder="أدخل كلمة المرور"
                    />
                  </div>

                  <div className="col-md-6 mb-3">
                    <label htmlFor="password_confirm" className="form-label">
                      تأكيد كلمة المرور
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="password_confirm"
                      name="password_confirm"
                      value={formData.password_confirm}
                      onChange={handleChange}
                      required
                      placeholder="أعد إدخال كلمة المرور"
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label htmlFor="user_type" className="form-label">
                    نوع المستخدم
                  </label>
                  <select
                    className="form-select"
                    id="user_type"
                    name="user_type"
                    value={formData.user_type}
                    onChange={handleChange}
                    required
                  >
                    <option value="individual">فرد</option>
                    <option value="workshop">ورشة تدوير</option>
                    <option value="collector">جامع خردة</option>
                    <option value="organization">جمعية بيئية</option>
                    <option value="company">شركة</option>
                  </select>
                </div>

                {formData.user_type !== "individual" && (
                  <div className="mb-3">
                    <label htmlFor="organization" className="form-label">
                      اسم المؤسسة/الورشة
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="organization"
                      name="organization"
                      value={formData.organization}
                      onChange={handleChange}
                      placeholder="أدخل اسم المؤسسة أو الورشة"
                    />
                  </div>
                )}

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
                      value={formData.phone}
                      onChange={handleChange}
                      required
                      placeholder="أدخل رقم الهاتف"
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
                      value={formData.location}
                      onChange={handleChange}
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

                <div className="mb-3">
                  <label htmlFor="bio" className="form-label">
                    نبذة تعريفية (اختياري)
                  </label>
                  <textarea
                    className="form-control"
                    id="bio"
                    name="bio"
                    rows="3"
                    value={formData.bio}
                    onChange={handleChange}
                    placeholder="اكتب نبذة مختصرة عنك..."
                  ></textarea>
                </div>

                <div className="mb-4">
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="terms" required />
                    <label className="form-check-label" htmlFor="terms">
                      أوافق على{" "}
                      <Link to="/terms" className="text-success">
                        شروط الاستخدام
                      </Link>{" "}
                      و
                      <Link to="/privacy" className="text-success ms-1">
                        سياسة الخصوصية
                      </Link>
                    </label>
                  </div>
                </div>

                <button type="submit" className="btn btn-success btn-lg w-100 mb-3" disabled={loading}>
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                      جاري إنشاء الحساب...
                    </>
                  ) : (
                    "إنشاء الحساب"
                  )}
                </button>
              </form>

              <div className="text-center">
                <p className="text-muted">
                  لديك حساب بالفعل؟
                  <Link to="/login" className="text-success text-decoration-none fw-bold ms-1">
                    تسجيل الدخول
                  </Link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
