"use client"

import { useState, useEffect } from "react"
import { useParams, Link } from "react-router-dom"
// import { useAuth } from "../context/AuthContext"

const ItemDetailsPage = () => {
  const { id } = useParams()
  // const { currentUser } = useAuth()
  const currentUser='hamada'
  const [item, setItem] = useState(null)
  const [loading, setLoading] = useState(true)
  const [currentImageIndex, setCurrentImageIndex] = useState(0)
  const [showContactModal, setShowContactModal] = useState(false)

  useEffect(() => {
    // محاكاة تحميل بيانات المنتج
    const mockItem = {
      id: Number.parseInt(id),
      title: "أثاث مكتبي مستعمل",
      description: `مجموعة من الأثاث المكتبي المستعمل في حالة جيدة جداً. تشمل:
      - 5 مكاتب خشبية
      - 8 كراسي مكتبية
      - خزانة ملفات
      - طاولة اجتماعات
      
      الأثاث نظيف ومناسب للاستخدام المباشر أو إعادة التدوير. متاح للاستلام من المكتب.`,
      category: "furniture",
      condition: "good",
      location: "القاهرة - مدينة نصر",
      price: "مجاني",
      priceType: "free",
      quantity: "1",
      unit: "مجموعة",
      contactMethod: "both",
      images: [
        "/placeholder.svg?height=400&width=600",
        "/placeholder.svg?height=400&width=600",
        "/placeholder.svg?height=400&width=600",
      ],
      user: {
        id: 2,
        name: "شركة التطوير العقاري",
        type: "company",
        rating: 4.8,
        reviewsCount: 24,
        avatar: "/placeholder.svg?height=100&width=100",
        phone: "01234567890",
        joinDate: "2023-05-15",
        totalItems: 12,
        completedDeals: 8,
      },
      createdAt: "2024-01-15",
      updatedAt: "2024-01-15",
      views: 45,
      interested: 12,
      status: "available",
    }

    setTimeout(() => {
      setItem(mockItem)
      setLoading(false)
    }, 1000)
  }, [id])

  const getCategoryLabel = (category) => {
    const categories = {
      furniture: "أثاث",
      electronics: "إلكترونيات",
      metals: "معادن",
      plastic: "بلاستيك",
      paper: "ورق وكرتون",
      glass: "زجاج",
      textiles: "منسوجات",
      construction: "مواد بناء",
      other: "أخرى",
    }
    return categories[category] || category
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

  const getUserTypeLabel = (type) => {
    const types = {
      individual: "فرد",
      workshop: "ورشة تدوير",
      collector: "جامع خردة",
      organization: "جمعية بيئية",
      company: "شركة",
    }
    return types[type] || type
  }

  const handleInterest = () => {
    if (!currentUser) {
      alert("يجب تسجيل الدخول أولاً")
      return
    }
    alert("تم إرسال إشعار الاهتمام بنجاح!")
  }

  const handleContact = () => {
    if (!currentUser) {
      alert("يجب تسجيل الدخول أولاً")
      return
    }
    setShowContactModal(true)
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

  if (!item) {
    return (
      <div className="container py-5">
        <div className="text-center">
          <h4>المنتج غير موجود</h4>
          <Link to="/search" className="btn btn-success">
            العودة للبحث
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="container py-4">
      {/* Breadcrumb */}
      <nav aria-label="breadcrumb" className="mb-4">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/" className="text-decoration-none">
              الرئيسية
            </Link>
          </li>
          <li className="breadcrumb-item">
            <Link to="/search" className="text-decoration-none">
              البحث
            </Link>
          </li>
          <li className="breadcrumb-item active">{item.title}</li>
        </ol>
      </nav>

      <div className="row">
        {/* Images Section */}
        <div className="col-lg-8 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-body p-0">
              {/* Main Image */}
              <div className="position-relative">
                <img
                  src={item.images[currentImageIndex] || "/placeholder.svg"}
                  alt={item.title}
                  className="w-100"
                  style={{ height: "400px", objectFit: "cover" }}
                />
                <span className="badge bg-success position-absolute top-0 start-0 m-3">
                  {getCategoryLabel(item.category)}
                </span>
                <span className="badge bg-secondary position-absolute top-0 end-0 m-3">
                  {getConditionLabel(item.condition)}
                </span>
              </div>

              {/* Image Thumbnails */}
              {item.images.length > 1 && (
                <div className="p-3">
                  <div className="row g-2">
                    {item.images.map((image, index) => (
                      <div key={index} className="col-3">
                        <img
                          src={image || "/placeholder.svg"}
                          alt={`صورة ${index + 1}`}
                          className={`w-100 rounded cursor-pointer ${
                            index === currentImageIndex ? "border border-success border-3" : ""
                          }`}
                          style={{ height: "80px", objectFit: "cover" }}
                          onClick={() => setCurrentImageIndex(index)}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Description */}
          <div className="card border-0 shadow-sm mt-4">
            <div className="card-header">
              <h5 className="mb-0">تفاصيل المنتج</h5>
            </div>
            <div className="card-body">
              <h4 className="mb-3">{item.title}</h4>
              <div className="mb-3">
                <pre className="text-wrap">{item.description}</pre>
              </div>

              {/* Product Details */}
              <div className="row">
                <div className="col-md-6">
                  <ul className="list-unstyled">
                    <li className="mb-2">
                      <strong>الفئة:</strong> {getCategoryLabel(item.category)}
                    </li>
                    <li className="mb-2">
                      <strong>الحالة:</strong> {getConditionLabel(item.condition)}
                    </li>
                    <li className="mb-2">
                      <strong>الكمية:</strong> {item.quantity} {item.unit}
                    </li>
                  </ul>
                </div>
                <div className="col-md-6">
                  <ul className="list-unstyled">
                    <li className="mb-2">
                      <strong>الموقع:</strong> {item.location}
                    </li>
                    <li className="mb-2">
                      <strong>تاريخ النشر:</strong> {new Date(item.createdAt).toLocaleDateString("ar-EG")}
                    </li>
                    <li className="mb-2">
                      <strong>المشاهدات:</strong> {item.views}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="col-lg-4">
          {/* Price and Actions */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-body">
              <div className="text-center mb-4">
                <h3 className="text-success mb-0">{item.price}</h3>
                <small className="text-muted">{item.priceType === "negotiable" && "قابل للتفاوض"}</small>
              </div>

              <div className="d-grid gap-2">
                <button className="btn btn-success btn-lg" onClick={handleContact}>
                  <i className="fas fa-phone me-2"></i>
                  تواصل مع البائع
                </button>
                <button className="btn btn-outline-success" onClick={handleInterest}>
                  <i className="fas fa-heart me-2"></i>
                  أبدي اهتماماً ({item.interested})
                </button>
                <Link to={`/chat?user=${item.user.id}`} className="btn btn-outline-primary">
                  <i className="fas fa-comments me-2"></i>
                  إرسال رسالة
                </Link>
              </div>

              <hr />

              <div className="text-center">
                <small className="text-muted">
                  <i className="fas fa-shield-alt me-1"></i>
                  تواصل آمن عبر المنصة
                </small>
              </div>
            </div>
          </div>

          {/* Seller Info */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-header">
              <h6 className="mb-0">معلومات البائع</h6>
            </div>
            <div className="card-body">
              <div className="d-flex align-items-center mb-3">
                <img
                  src={item.user.avatar || "/placeholder.svg"}
                  alt={item.user.name}
                  className="rounded-circle me-3"
                  style={{ width: "50px", height: "50px", objectFit: "cover" }}
                />
                <div>
                  <h6 className="mb-0">{item.user.name}</h6>
                  <small className="text-muted">{getUserTypeLabel(item.user.type)}</small>
                </div>
              </div>

              <div className="mb-3">
                <div className="d-flex justify-content-between align-items-center mb-1">
                  <span>التقييم</span>
                  <span>
                    <i className="fas fa-star text-warning me-1"></i>
                    {item.user.rating} ({item.user.reviewsCount} تقييم)
                  </span>
                </div>
                <div className="progress" style={{ height: "5px" }}>
                  <div className="progress-bar bg-warning" style={{ width: `${(item.user.rating / 5) * 100}%` }}></div>
                </div>
              </div>

              <div className="row text-center">
                <div className="col-6">
                  <div className="border-end">
                    <h6 className="text-success mb-0">{item.user.totalItems}</h6>
                    <small className="text-muted">إعلان</small>
                  </div>
                </div>
                <div className="col-6">
                  <h6 className="text-success mb-0">{item.user.completedDeals}</h6>
                  <small className="text-muted">صفقة مكتملة</small>
                </div>
              </div>

              <hr />

              <div className="text-center">
                <small className="text-muted">عضو منذ {new Date(item.user.joinDate).toLocaleDateString("ar-EG")}</small>
              </div>
            </div>
          </div>

          {/* Safety Tips */}
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-warning text-dark">
              <h6 className="mb-0">
                <i className="fas fa-exclamation-triangle me-2"></i>
                نصائح الأمان
              </h6>
            </div>
            <div className="card-body">
              <ul className="list-unstyled small mb-0">
                <li className="mb-2">
                  <i className="fas fa-check text-success me-2"></i>
                  تأكد من حالة المنتج قبل الاستلام
                </li>
                <li className="mb-2">
                  <i className="fas fa-check text-success me-2"></i>
                  التقي في مكان عام وآمن
                </li>
                <li className="mb-2">
                  <i className="fas fa-check text-success me-2"></i>
                  لا تدفع مقدماً قبل المعاينة
                </li>
                <li className="mb-0">
                  <i className="fas fa-check text-success me-2"></i>
                  أبلغ عن أي سلوك مشبوه
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Modal */}
      {showContactModal && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: "rgba(0,0,0,0.5)" }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">معلومات التواصل</h5>
                <button type="button" className="btn-close" onClick={() => setShowContactModal(false)}></button>
              </div>
              <div className="modal-body">
                <div className="text-center mb-3">
                  <img
                    src={item.user.avatar || "/placeholder.svg"}
                    alt={item.user.name}
                    className="rounded-circle mb-2"
                    style={{ width: "80px", height: "80px", objectFit: "cover" }}
                  />
                  <h5>{item.user.name}</h5>
                </div>

                <div className="d-grid gap-2">
                  <a href={`tel:${item.user.phone}`} className="btn btn-success">
                    <i className="fas fa-phone me-2"></i>
                    اتصال: {item.user.phone}
                  </a>
                  <a
                    href={`https://wa.me/2${item.user.phone.substring(1)}`}
                    className="btn btn-outline-success"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <i className="fab fa-whatsapp me-2"></i>
                    واتساب
                  </a>
                  <Link to={`/chat?user=${item.user.id}`} className="btn btn-outline-primary">
                    <i className="fas fa-comments me-2"></i>
                    محادثة عبر المنصة
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ItemDetailsPage
