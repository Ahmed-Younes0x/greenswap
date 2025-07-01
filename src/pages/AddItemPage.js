"use client"

import { useState } from "react"
import { useNavigate } from "react-router-dom"
// import { useAuth } from "../context/AuthContext"

const AddItemPage = () => {
  // const { currentUser } = useAuth()
  const currentUser='hamada'
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "",
    condition: "",
    quantity: "",
    unit: "",
    price: "",
    priceType: "free",
    location: currentUser?.location || "",
    contactMethod: "both",
    images: [],
  })

  const categories = [
    { value: "furniture", label: "أثاث" },
    { value: "electronics", label: "إلكترونيات" },
    { value: "metals", label: "معادن" },
    { value: "plastic", label: "بلاستيك" },
    { value: "paper", label: "ورق وكرتون" },
    { value: "glass", label: "زجاج" },
    { value: "textiles", label: "منسوجات" },
    { value: "construction", label: "مواد بناء" },
    { value: "other", label: "أخرى" },
  ]

  const conditions = [
    { value: "excellent", label: "ممتاز" },
    { value: "good", label: "جيد" },
    { value: "fair", label: "مقبول" },
    { value: "poor", label: "يحتاج إصلاح" },
    { value: "scrap", label: "خردة" },
  ]

  const units = [
    { value: "piece", label: "قطعة" },
    { value: "kg", label: "كيلوجرام" },
    { value: "ton", label: "طن" },
    { value: "meter", label: "متر" },
    { value: "box", label: "صندوق" },
    { value: "bag", label: "كيس" },
  ]

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleImageChange = (e) => {
    const files = Array.from(e.target.files)
    setFormData((prev) => ({
      ...prev,
      images: files,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // محاكاة رفع البيانات
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // إظهار رسالة نجاح
      alert("تم إضافة المخلف بنجاح!")
      navigate("/dashboard")
    } catch (error) {
      alert("حدث خطأ أثناء إضافة المخلف")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container py-4">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-success text-white">
              <h4 className="mb-0">
                <i className="fas fa-plus me-2"></i>
                إضافة مخلف جديد
              </h4>
            </div>
            <div className="card-body p-4">
              <form onSubmit={handleSubmit}>
                {/* Basic Information */}
                <div className="mb-4">
                  <h5 className="text-success mb-3">المعلومات الأساسية</h5>

                  <div className="mb-3">
                    <label htmlFor="title" className="form-label">
                      عنوان الإعلان *
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="title"
                      name="title"
                      value={formData.title}
                      onChange={handleChange}
                      required
                      placeholder="مثال: أثاث مكتبي مستعمل"
                    />
                  </div>

                  <div className="mb-3">
                    <label htmlFor="description" className="form-label">
                      الوصف *
                    </label>
                    <textarea
                      className="form-control"
                      id="description"
                      name="description"
                      rows="4"
                      value={formData.description}
                      onChange={handleChange}
                      required
                      placeholder="اكتب وصفاً مفصلاً للمخلف..."
                    ></textarea>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="category" className="form-label">
                        الفئة *
                      </label>
                      <select
                        className="form-select"
                        id="category"
                        name="category"
                        value={formData.category}
                        onChange={handleChange}
                        required
                      >
                        <option value="">اختر الفئة</option>
                        {categories.map((cat) => (
                          <option key={cat.value} value={cat.value}>
                            {cat.label}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="col-md-6 mb-3">
                      <label htmlFor="condition" className="form-label">
                        الحالة *
                      </label>
                      <select
                        className="form-select"
                        id="condition"
                        name="condition"
                        value={formData.condition}
                        onChange={handleChange}
                        required
                      >
                        <option value="">اختر الحالة</option>
                        {conditions.map((cond) => (
                          <option key={cond.value} value={cond.value}>
                            {cond.label}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>

                {/* Quantity and Price */}
                <div className="mb-4">
                  <h5 className="text-success mb-3">الكمية والسعر</h5>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="quantity" className="form-label">
                        الكمية *
                      </label>
                      <input
                        type="number"
                        className="form-control"
                        id="quantity"
                        name="quantity"
                        value={formData.quantity}
                        onChange={handleChange}
                        required
                        min="1"
                      />
                    </div>

                    <div className="col-md-6 mb-3">
                      <label htmlFor="unit" className="form-label">
                        الوحدة *
                      </label>
                      <select
                        className="form-select"
                        id="unit"
                        name="unit"
                        value={formData.unit}
                        onChange={handleChange}
                        required
                      >
                        <option value="">اختر الوحدة</option>
                        {units.map((unit) => (
                          <option key={unit.value} value={unit.value}>
                            {unit.label}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">نوع السعر *</label>
                    <div className="row">
                      <div className="col-md-4">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="radio"
                            name="priceType"
                            id="free"
                            value="free"
                            checked={formData.priceType === "free"}
                            onChange={handleChange}
                          />
                          <label className="form-check-label" htmlFor="free">
                            مجاني
                          </label>
                        </div>
                      </div>
                      <div className="col-md-4">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="radio"
                            name="priceType"
                            id="fixed"
                            value="fixed"
                            checked={formData.priceType === "fixed"}
                            onChange={handleChange}
                          />
                          <label className="form-check-label" htmlFor="fixed">
                            سعر ثابت
                          </label>
                        </div>
                      </div>
                      <div className="col-md-4">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="radio"
                            name="priceType"
                            id="negotiable"
                            value="negotiable"
                            checked={formData.priceType === "negotiable"}
                            onChange={handleChange}
                          />
                          <label className="form-check-label" htmlFor="negotiable">
                            قابل للتفاوض
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>

                  {formData.priceType !== "free" && (
                    <div className="mb-3">
                      <label htmlFor="price" className="form-label">
                        السعر (جنيه مصري)
                      </label>
                      <input
                        type="number"
                        className="form-control"
                        id="price"
                        name="price"
                        value={formData.price}
                        onChange={handleChange}
                        min="0"
                        placeholder="أدخل السعر"
                      />
                    </div>
                  )}
                </div>

                {/* Location and Contact */}
                <div className="mb-4">
                  <h5 className="text-success mb-3">الموقع والتواصل</h5>

                  <div className="mb-3">
                    <label htmlFor="location" className="form-label">
                      المحافظة *
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

                  <div className="mb-3">
                    <label className="form-label">طريقة التواصل المفضلة</label>
                    <div className="row">
                      <div className="col-md-4">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="radio"
                            name="contactMethod"
                            id="phone"
                            value="phone"
                            checked={formData.contactMethod === "phone"}
                            onChange={handleChange}
                          />
                          <label className="form-check-label" htmlFor="phone">
                            هاتف فقط
                          </label>
                        </div>
                      </div>
                      <div className="col-md-4">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="radio"
                            name="contactMethod"
                            id="chat"
                            value="chat"
                            checked={formData.contactMethod === "chat"}
                            onChange={handleChange}
                          />
                          <label className="form-check-label" htmlFor="chat">
                            محادثة فقط
                          </label>
                        </div>
                      </div>
                      <div className="col-md-4">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="radio"
                            name="contactMethod"
                            id="both"
                            value="both"
                            checked={formData.contactMethod === "both"}
                            onChange={handleChange}
                          />
                          <label className="form-check-label" htmlFor="both">
                            كلاهما
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Images */}
                <div className="mb-4">
                  <h5 className="text-success mb-3">الصور</h5>

                  <div className="mb-3">
                    <label htmlFor="images" className="form-label">
                      إضافة صور (حتى 5 صور)
                    </label>
                    <input
                      type="file"
                      className="form-control"
                      id="images"
                      name="images"
                      multiple
                      accept="image/*"
                      onChange={handleImageChange}
                    />
                    <div className="form-text">الصور الواضحة تزيد من فرص نجاح الإعلان</div>
                  </div>

                  {formData.images.length > 0 && (
                    <div className="row">
                      {Array.from(formData.images)
                        .slice(0, 5)
                        .map((file, index) => (
                          <div key={index} className="col-md-3 mb-2">
                            <div className="card">
                              <div className="card-body p-2 text-center">
                                <i className="fas fa-image text-muted fs-4"></i>
                                <p className="small mb-0 mt-1">{file.name}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                    </div>
                  )}
                </div>

                {/* Terms */}
                <div className="mb-4">
                  <div className="form-check">
                    <input className="form-check-input" type="checkbox" id="terms" required />
                    <label className="form-check-label" htmlFor="terms">
                      أوافق على شروط النشر وأتحمل مسؤولية صحة البيانات المدخلة
                    </label>
                  </div>
                </div>

                {/* Submit Button */}
                <div className="d-flex gap-3">
                  <button type="submit" className="btn btn-success btn-lg flex-grow-1" disabled={loading}>
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        جاري النشر...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-plus me-2"></i>
                        نشر الإعلان
                      </>
                    )}
                  </button>
                  <button type="button" className="btn btn-outline-secondary" onClick={() => navigate("/dashboard")}>
                    إلغاء
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AddItemPage
