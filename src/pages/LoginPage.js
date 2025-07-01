"use client"

import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
// import { useAuth } from "../context/AuthContext"

const LoginPage = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  // const { login } = useAuth()
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

    const result = await login(formData)

    if (result.success || 1) { //edited
      navigate("/dashboard")
    } else {
      setError(result.error)
    }

    setLoading(false)
  }

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-5">
          <div className="card shadow-lg border-0">
            <div className="card-body p-5">
              <div className="text-center mb-4">
                <i className="fas fa-recycle text-success fs-1 mb-3"></i>
                <h2 className="fw-bold">تسجيل الدخول</h2>
                <p className="text-muted">مرحباً بك في GreenSwap Egypt</p>
              </div>

              {error && (
                <div className="alert alert-danger" role="alert">
                  {typeof error === "string" ? error : "حدث خطأ أثناء تسجيل الدخول"}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="username" className="form-label">
                    اسم المستخدم
                  </label>
                  <input
                    type="text"
                    className="form-control form-control-lg"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    placeholder="أدخل اسم المستخدم"
                  />
                </div>

                <div className="mb-4">
                  <label htmlFor="password" className="form-label">
                    كلمة المرور
                  </label>
                  <input
                    type="password"
                    className="form-control form-control-lg"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    placeholder="أدخل كلمة المرور"
                  />
                </div>

                <div className="d-flex justify-content-between align-items-center mb-4">
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="remember" />
                    <label className="form-check-label" htmlFor="remember">
                      تذكرني
                    </label>
                  </div>
                  <Link to="/forgot-password" className="text-decoration-none">
                    نسيت كلمة المرور؟
                  </Link>
                </div>

                <button type="submit" className="btn btn-success btn-lg w-100 mb-3" disabled={loading}>
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                      جاري تسجيل الدخول...
                    </>
                  ) : (
                    "تسجيل الدخول"
                  )}
                </button>
              </form>

              <div className="text-center">
                <p className="text-muted">
                  ليس لديك حساب؟
                  <Link to="/register" className="text-success text-decoration-none fw-bold ms-1">
                    إنشاء حساب جديد
                  </Link>
                </p>
              </div>

              <hr className="my-4" />

              <div className="text-center">
                <p className="text-muted small mb-3">أو سجل الدخول باستخدام</p>
                <div className="d-flex gap-2 justify-content-center">
                  <button className="btn btn-outline-primary">
                    <i className="fab fa-facebook me-1"></i>
                    Facebook
                  </button>
                  <button className="btn btn-outline-danger">
                    <i className="fab fa-google me-1"></i>
                    Google
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
