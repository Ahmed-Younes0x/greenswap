"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { itemsAPI } from "../services/api"

const SearchPage = () => {
  const [items, setItems] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    search: "",
    category: "",
    location: "",
    condition: "",
    price_type: "",
    ordering: "-created_at",
  })

  const locations = [
    "القاهرة",
    "الجيزة",
    "الإسكندرية",
    "الدقهلية",
    "الشرقية",
    "القليوبية",
    "كفر الشيخ",
    "الغربية",
    "المنوفية",
    "البحيرة",
  ]

  useEffect(() => {
    loadCategories()
  }, [])

  useEffect(() => {
    loadItems()
  }, [filters])

  const loadCategories = async () => {
    try {
      const response = await itemsAPI.getCategories()
      setCategories(response.data)
    } catch (error) {
      console.error("Error loading categories:", error)
    }
  }

  const loadItems = async () => {
    setLoading(true)
    try {
      const params = {}
      Object.keys(filters).forEach((key) => {
        if (filters[key]) {
          params[key] = filters[key]
        }
      })

      const response = await itemsAPI.getItems(params)
      setItems(response.data.results || response.data)
    } catch (error) {
      console.error("Error loading items:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (e) => {
    const { name, value } = e.target
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const clearFilters = () => {
    setFilters({
      search: "",
      category: "",
      location: "",
      condition: "",
      price_type: "",
      ordering: "-created_at",
    })
  }

  const getConditionLabel = (condition) => {
    const conditions = {
      excellent: "ممتاز",
      good: "جيد",
      fair: "مقبول",
      poor: "يحتاج إصلاح",
      scrap: "خردة",
    }
    return conditions[condition] || condition
  }

  return (
    <div className="container py-4">
      {/* Search Header */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card bg-success text-white">
            <div className="card-body">
              <h2 className="mb-3">البحث في المخلفات</h2>
              <div className="row">
                <div className="col-md-8">
                  <input
                    type="text"
                    className="form-control form-control-lg"
                    placeholder="ابحث عن المخلفات..."
                    name="search"
                    value={filters.search}
                    onChange={handleFilterChange}
                  />
                </div>
                <div className="col-md-4">
                  <button className="btn btn-light btn-lg w-100 mt-2 mt-md-0" onClick={loadItems}>
                    <i className="fas fa-search me-2"></i>
                    بحث
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        {/* Filters Sidebar */}
        <div className="col-lg-3 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="mb-0">تصفية النتائج</h5>
                <button className="btn btn-sm btn-outline-secondary" onClick={clearFilters}>
                  مسح الكل
                </button>
              </div>
            </div>
            <div className="card-body">
              {/* Category Filter */}
              <div className="mb-3">
                <label className="form-label fw-bold">الفئة</label>
                <select className="form-select" name="category" value={filters.category} onChange={handleFilterChange}>
                  <option value="">جميع الفئات</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name_ar}
                    </option>
                  ))}
                </select>
              </div>

              {/* Location Filter */}
              <div className="mb-3">
                <label className="form-label fw-bold">المحافظة</label>
                <select className="form-select" name="location" value={filters.location} onChange={handleFilterChange}>
                  <option value="">جميع المحافظات</option>
                  {locations.map((location) => (
                    <option key={location} value={location}>
                      {location}
                    </option>
                  ))}
                </select>
              </div>

              {/* Condition Filter */}
              <div className="mb-3">
                <label className="form-label fw-bold">الحالة</label>
                <select
                  className="form-select"
                  name="condition"
                  value={filters.condition}
                  onChange={handleFilterChange}
                >
                  <option value="">جميع الحالات</option>
                  <option value="excellent">ممتاز</option>
                  <option value="good">جيد</option>
                  <option value="fair">مقبول</option>
                  <option value="poor">يحتاج إصلاح</option>
                  <option value="scrap">خردة</option>
                </select>
              </div>

              {/* Price Type Filter */}
              <div className="mb-3">
                <label className="form-label fw-bold">نوع السعر</label>
                <select
                  className="form-select"
                  name="price_type"
                  value={filters.price_type}
                  onChange={handleFilterChange}
                >
                  <option value="">جميع الأنواع</option>
                  <option value="free">مجاني</option>
                  <option value="fixed">سعر ثابت</option>
                  <option value="negotiable">قابل للتفاوض</option>
                </select>
              </div>

              {/* Sort Filter */}
              <div className="mb-3">
                <label className="form-label fw-bold">ترتيب حسب</label>
                <select className="form-select" name="ordering" value={filters.ordering} onChange={handleFilterChange}>
                  <option value="-created_at">الأحدث</option>
                  <option value="created_at">الأقدم</option>
                  <option value="-views">الأكثر مشاهدة</option>
                  <option value="price">السعر (الأقل)</option>
                  <option value="-price">السعر (الأعلى)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="col-lg-9">
          {/* Results Header */}
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5>{loading ? "جاري التحميل..." : `${items.length} نتيجة`}</h5>
            <div className="d-flex gap-2">
              <button className="btn btn-outline-secondary btn-sm">
                <i className="fas fa-th"></i>
              </button>
              <button className="btn btn-outline-secondary btn-sm">
                <i className="fas fa-list"></i>
              </button>
            </div>
          </div>

          {/* Loading */}
          {loading && (
            <div className="text-center py-5">
              <div className="spinner-border text-success" role="status">
                <span className="visually-hidden">جاري التحميل...</span>
              </div>
            </div>
          )}

          {/* No Results */}
          {!loading && items.length === 0 && (
            <div className="text-center py-5">
              <i className="fas fa-search fs-1 text-muted mb-3"></i>
              <h4 className="text-muted">لا توجد نتائج</h4>
              <p className="text-muted">جرب تغيير معايير البحث</p>
              <button className="btn btn-success" onClick={clearFilters}>
                مسح جميع المرشحات
              </button>
            </div>
          )}

          {/* Results Grid */}
          {!loading && items.length > 0 && (
            <div className="row">
              {items.map((item) => (
                <div key={item.id} className="col-md-6 col-xl-4 mb-4">
                  <div className="card border-0 shadow-sm h-100">
                    <div className="position-relative">
                      <img
                        src={item.primary_image || "/placeholder.svg?height=200&width=300"}
                        className="card-img-top"
                        alt={item.title}
                        style={{ height: "200px", objectFit: "cover" }}
                      />
                      <span className="badge bg-success position-absolute top-0 start-0 m-2">
                        {item.category.name_ar}
                      </span>
                      <span className="badge bg-secondary position-absolute top-0 end-0 m-2">
                        {getConditionLabel(item.condition)}
                      </span>
                    </div>

                    <div className="card-body">
                      <h6 className="card-title">{item.title}</h6>
                      <p className="text-muted small mb-2">{item.description.substring(0, 80)}...</p>

                      <div className="mb-2">
                        <small className="text-muted">
                          <i className="fas fa-map-marker-alt me-1"></i>
                          {item.location}
                        </small>
                      </div>

                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <span className="fw-bold text-success">
                          {item.price_type === "free" ? "مجاني" : `${item.price} جنيه`}
                        </span>
                        <small className="text-muted">
                          <i className="fas fa-eye me-1"></i>
                          {item.views}
                        </small>
                      </div>

                      <div className="d-flex justify-content-between align-items-center">
                        <div>
                          <small className="text-muted d-block">
                            {item.user.first_name} {item.user.last_name}
                          </small>
                          <small className="text-muted">
                            <i className="fas fa-star text-warning me-1"></i>
                            {item.user.rating}
                          </small>
                        </div>
                        <Link to={`/item/${item.id}`} className="btn btn-sm btn-success">
                          عرض التفاصيل
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SearchPage
