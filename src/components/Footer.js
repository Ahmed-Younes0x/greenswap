const Footer = () => {
  return (
    <footer className="bg-dark text-light py-5 mt-5">
      <div className="container">
        <div className="row">
          <div className="col-md-4 mb-4">
            <h5 className="text-success">
              <i className="fas fa-recycle me-2"></i>
              GreenSwap Egypt
            </h5>
            <p className="text-muted">منصة رقمية لربط الأفراد والمؤسسات لإعادة تدوير المخلفات وحماية البيئة</p>
          </div>

          <div className="col-md-2 mb-4">
            <h6>روابط سريعة</h6>
            <ul className="list-unstyled">
              <li>
                <a href="/" className="text-muted text-decoration-none">
                  الرئيسية
                </a>
              </li>
              <li>
                <a href="/search" className="text-muted text-decoration-none">
                  البحث
                </a>
              </li>
              <li>
                <a href="/register" className="text-muted text-decoration-none">
                  إنشاء حساب
                </a>
              </li>
            </ul>
          </div>

          <div className="col-md-3 mb-4">
            <h6>الفئات</h6>
            <ul className="list-unstyled">
              <li>
                <span className="text-muted">أثاث مستعمل</span>
              </li>
              <li>
                <span className="text-muted">أجهزة إلكترونية</span>
              </li>
              <li>
                <span className="text-muted">معادن وبلاستيك</span>
              </li>
              <li>
                <span className="text-muted">مواد بناء</span>
              </li>
            </ul>
          </div>

          <div className="col-md-3 mb-4">
            <h6>تواصل معنا</h6>
            <div className="d-flex gap-3">
              <a href="#" className="text-success fs-4">
                <i className="fab fa-facebook"></i>
              </a>
              <a href="#" className="text-success fs-4">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="#" className="text-success fs-4">
                <i className="fab fa-instagram"></i>
              </a>
              <a href="#" className="text-success fs-4">
                <i className="fab fa-whatsapp"></i>
              </a>
            </div>
          </div>
        </div>

        <hr className="my-4" />

        <div className="row align-items-center">
          <div className="col-md-6">
            <p className="text-muted mb-0">© 2024 GreenSwap Egypt. جميع الحقوق محفوظة</p>
          </div>
          <div className="col-md-6 text-md-end">
            <a href="#" className="text-muted text-decoration-none me-3">
              سياسة الخصوصية
            </a>
            <a href="#" className="text-muted text-decoration-none">
              شروط الاستخدام
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
