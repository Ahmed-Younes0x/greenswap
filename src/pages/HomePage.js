"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { itemsAPI } from "../services/api"

const HomePage = () => {
  const [recentItems, setRecentItems] = useState([])
  const [stats, setStats] = useState({
    total_items: 0,
    total_users: 0,
    completed_deals: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    // try {
    //   const [itemsResponse, statsResponse] = await Promise.all([itemsAPI.getFeaturedItems(), itemsAPI.getStats()])

    //   setRecentItems(itemsResponse.data)
    //   setStats(statsResponse.data)
    // } catch (error) {
    //   console.error("Error loading data:", error)
    // } finally {
    //   setLoading(false)
    // }
    const recentItems = [
  {
    id: 1,
    title: "كتاب تعلم البرمجة بلغة بايثون",
    primary_image: "/books/python-book.jpg",
    category: {
      name_ar: "كتب"
    },
    location: "القاهرة، مصر",
    user: {
      first_name: "أحمد",
      last_name: "محمد"
    },
    price_type: "fixed",
    price: 75
  },
  {
    id: 2,
    title: "جهاز لابتوب مستعمل بحالة جيدة",
    primary_image: "/electronics/laptop.jpg",
    category: {
      name_ar: "إلكترونيات"
    },
    location: "الإسكندرية، مصر",
    user: {
      first_name: "مريم",
      last_name: "علي"
    },
    price_type: "fixed",
    price: 4500
  },
  {
    id: 3,
    title: "أريكة خشب مزخرفة",
    primary_image: "/furniture/sofa.jpg",
    category: {
      name_ar: "أثاث"
    },
    location: "الجيزة، مصر",
    user: {
      first_name: "خالد",
      last_name: "عبد الرحمن"
    },
    price_type: "free"
  },
  {
    id: 4,
    title: "دراجة هوائية للبيع",
    primary_image: "/sports/bicycle.jpg",
    category: {
      name_ar: "رياضة"
    },
    location: "المنصورة، مصر",
    user: {
      first_name: "يوسف",
      last_name: "سعيد"
    },
    price_type: "fixed",
    price: 1200
  },
  {
    id: 5,
    title: "مجموعة أدوات مطبخ كاملة",
    primary_image: "/home/kitchen-tools.jpg",
    category: {
      name_ar: "أدوات منزلية"
    },
    location: "أسوان، مصر",
    user: {
      first_name: "فاطمة",
      last_name: "زكريا"
    },
    price_type: "fixed",
    price: 350
  },
  {
    id: 6,
    title: "لعبة أطفال تعليمية",
    primary_image: "/toys/educational-toy.jpg",
    category: {
      name_ar: "ألعاب أطفال"
    },
    location: "بورسعيد، مصر",
    user: {
      first_name: "نور",
      last_name: "حسين"
    },
    price_type: "free"
  },
  {
    id: 7,
    title: "كاميرا كانون مستعملة",
    primary_image: "/photography/camera.jpg",
    category: {
      name_ar: "تصوير"
    },
    location: "الأقصر، مصر",
    user: {
      first_name: "عمرو",
      last_name: "أحمد"
    },
    price_type: "fixed",
    price: 2800
  },
  {
    id: 8,
    title: "مجموعة كتب دينية",
    primary_image: "/books/religious-books.jpg",
    category: {
      name_ar: "كتب دينية"
    },
    location: "المنيا، مصر",
    user: {
      first_name: "عبد الله",
      last_name: "محمود"
    },
    price_type: "fixed",
    price: 150
  }
];
setLoading(false)
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
    <div>
      {/* Hero Section */}
      <section className="hero-section bg-success text-white py-5">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-6">
              <h1 className="display-4 fw-bold mb-4">GreenSwap Egypt</h1>
              <p className="lead mb-4">
                منصة رقمية لربط الأفراد والمؤسسات التي تمتلك مخلفات قابلة لإعادة الاستخدام مع ورش أو أفراد يعملون في
                إعادة التدوير
              </p>
              <div className="d-flex gap-3">
                <Link to="/register" className="btn btn-light btn-lg">
                  ابدأ الآن
                </Link>
                <Link to="/search" className="btn btn-outline-light btn-lg">
                  تصفح العروض
                </Link>
              </div>
            </div>
            <div className="col-lg-6">
              <img src="/placeholder.svg?height=400&width=500" alt="إعادة التدوير" className="img-fluid rounded" />
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-5 bg-light">
        <div className="container">
          <div className="row text-center">
            <div className="col-md-4 mb-4">
              <div className="card border-0 shadow-sm h-100">
                <div className="card-body">
                  <i className="fas fa-box text-success fs-1 mb-3"></i>
                  <h3 className="text-success">{stats.total_items.toLocaleString()}</h3>
                  <p className="text-muted">إجمالي المخلفات المعروضة</p>
                </div>
              </div>
            </div>
            <div className="col-md-4 mb-4">
              <div className="card border-0 shadow-sm h-100">
                <div className="card-body">
                  <i className="fas fa-users text-success fs-1 mb-3"></i>
                  <h3 className="text-success">{stats.total_users.toLocaleString()}</h3>
                  <p className="text-muted">المستخدمين النشطين</p>
                </div>
              </div>
            </div>
            <div className="col-md-4 mb-4">
              <div className="card border-0 shadow-sm h-100">
                <div className="card-body">
                  <i className="fas fa-handshake text-success fs-1 mb-3"></i>
                  <h3 className="text-success">{stats.completed_deals.toLocaleString()}</h3>
                  <p className="text-muted">الصفقات المكتملة</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-5">
        <div className="container">
          <h2 className="text-center mb-5">الفئات الرئيسية</h2>
          <div className="row">
            <div className="col-md-3 mb-4">
              <div className="card text-center border-0 shadow-sm h-100">
                <div className="card-body">
                  <i className="fas fa-couch text-success fs-1 mb-3"></i>
                  <h5>أثاث</h5>
                  <p className="text-muted">أثاث مستعمل قابل للإصلاح</p>
                </div>
              </div>
            </div>
            <div className="col-md-3 mb-4">
              <div className="card text-center border-0 shadow-sm h-100">
                <div className="card-body">
                  <i className="fas fa-laptop text-success fs-1 mb-3"></i>
                  <h5>إلكترونيات</h5>
                  <p className="text-muted">أجهزة إلكترونية ومعدات</p>
                </div>
              </div>
            </div>
            <div className="col-md-3 mb-4">
              <div className="card text-center border-0 shadow-sm h-100">
                <div className="card-body">
                  <i className="fas fa-industry text-success fs-1 mb-3"></i>
                  <h5>معادن</h5>
                  <p className="text-muted">خردة معادن وحديد</p>
                </div>
              </div>
            </div>
            <div className="col-md-3 mb-4">
              <div className="card text-center border-0 shadow-sm h-100">
                <div className="card-body">
                  <i className="fas fa-recycle text-success fs-1 mb-3"></i>
                  <h5>بلاستيك</h5>
                  <p className="text-muted">مواد بلاستيكية قابلة للتدوير</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Recent Items Section */}
      <section className="py-5 bg-light">
        <div className="container">
          <div className="d-flex justify-content-between align-items-center mb-5">
            <h2>أحدث العروض</h2>
            <Link to="/search" className="btn btn-success">
              عرض الكل
            </Link>
          </div>

          <div className="row">
            {recentItems.map((item) => (
              <div key={item.id} className="col-lg-3 col-md-6 mb-4">
                <div className="card border-0 shadow-sm h-100">
                  <img
                    src={item.primary_image || "/placeholder.svg?height=200&width=300"}
                    className="card-img-top"
                    alt={item.title}
                    style={{ height: "200px", objectFit: "cover" }}
                  />
                  <div className="card-body">
                    <span className="badge bg-success mb-2">{item.category.name_ar}</span>
                    <h6 className="card-title">{item.title}</h6>
                    <p className="text-muted small mb-2">
                      <i className="fas fa-map-marker-alt me-1"></i>
                      {item.location}
                    </p>
                    <p className="text-muted small mb-2">
                      <i className="fas fa-user me-1"></i>
                      {item.user.first_name} {item.user.last_name}
                    </p>
                    <div className="d-flex justify-content-between align-items-center">
                      <span className="fw-bold text-success">
                        {item.price_type === "free" ? "مجاني" : `${item.price} جنيه`}
                      </span>
                      <Link to={`/item/${item.id}`} className="btn btn-sm btn-outline-success">
                        عرض التفاصيل
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="py-5">
        <div className="container">
          <h2 className="text-center mb-5">كيف يعمل الموقع؟</h2>
          <div className="row">
            <div className="col-md-4 text-center mb-4">
              <div
                className="bg-success text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3"
                style={{ width: "80px", height: "80px" }}
              >
                <span className="fs-2 fw-bold">1</span>
              </div>
              <h5>سجل حسابك</h5>
              <p className="text-muted">أنشئ حساب جديد واختر نوع المستخدم المناسب لك</p>
            </div>
            <div className="col-md-4 text-center mb-4">
              <div
                className="bg-success text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3"
                style={{ width: "80px", height: "80px" }}
              >
                <span className="fs-2 fw-bold">2</span>
              </div>
              <h5>أضف أو ابحث</h5>
              <p className="text-muted">أضف مخلفاتك أو ابحث عن المواد التي تحتاجها</p>
            </div>
            <div className="col-md-4 text-center mb-4">
              <div
                className="bg-success text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3"
                style={{ width: "80px", height: "80px" }}
              >
                <span className="fs-2 fw-bold">3</span>
              </div>
              <h5>تواصل واتفق</h5>
              <p className="text-muted">تواصل مع الطرف الآخر واتفق على التفاصيل</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
