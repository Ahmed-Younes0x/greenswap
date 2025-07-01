"use client"

import { useState } from "react"

const DeliveryScheduler = ({ onScheduleSubmit, itemTitle }) => {
  const [scheduleData, setScheduleData] = useState({
    date: "",
    time: "",
    address: "",
    notes: "",
    deliveryType: "pickup", // pickup or delivery
  })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setScheduleData({
      ...scheduleData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // محاكاة إرسال طلب الجدولة
      await new Promise((resolve) => setTimeout(resolve, 1000))

      onScheduleSubmit?.(scheduleData)
      alert("تم جدولة الاستلام بنجاح!")
    } catch (error) {
      alert("حدث خطأ أثناء جدولة الاستلام")
    } finally {
      setLoading(false)
    }
  }

  // الحصول على التاريخ الحالي لتحديد الحد الأدنى
  const today = new Date().toISOString().split("T")[0]

  // أوقات متاحة
  const availableTimes = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

  return (
    <div className="card border-0 shadow-sm">
      <div className="card-header bg-primary text-white">
        <h5 className="mb-0">
          <i className="fas fa-calendar-alt me-2"></i>
          جدولة الاستلام
        </h5>
      </div>
      <div className="card-body">
        <div className="alert alert-info">
          <i className="fas fa-info-circle me-2"></i>
          جدولة استلام: <strong>{itemTitle}</strong>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">نوع الخدمة</label>
            <div className="row">
              <div className="col-6">
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="deliveryType"
                    id="pickup"
                    value="pickup"
                    checked={scheduleData.deliveryType === "pickup"}
                    onChange={handleChange}
                  />
                  <label className="form-check-label" htmlFor="pickup">
                    <i className="fas fa-hand-holding me-1"></i>
                    استلام من المكان
                  </label>
                </div>
              </div>
              <div className="col-6">
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="deliveryType"
                    id="delivery"
                    value="delivery"
                    checked={scheduleData.deliveryType === "delivery"}
                    onChange={handleChange}
                  />
                  <label className="form-check-label" htmlFor="delivery">
                    <i className="fas fa-truck me-1"></i>
                    توصيل للمكان
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="date" className="form-label">
                التاريخ المفضل *
              </label>
              <input
                type="date"
                className="form-control"
                id="date"
                name="date"
                value={scheduleData.date}
                onChange={handleChange}
                min={today}
                required
              />
            </div>

            <div className="col-md-6 mb-3">
              <label htmlFor="time" className="form-label">
                الوقت المفضل *
              </label>
              <select
                className="form-select"
                id="time"
                name="time"
                value={scheduleData.time}
                onChange={handleChange}
                required
              >
                <option value="">اختر الوقت</option>
                {availableTimes.map((time) => (
                  <option key={time} value={time}>
                    {time}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mb-3">
            <label htmlFor="address" className="form-label">
              العنوان التفصيلي *
            </label>
            <textarea
              className="form-control"
              id="address"
              name="address"
              rows="2"
              value={scheduleData.address}
              onChange={handleChange}
              required
              placeholder="أدخل العنوان التفصيلي للاستلام أو التوصيل..."
            ></textarea>
          </div>

          <div className="mb-3">
            <label htmlFor="notes" className="form-label">
              ملاحظات إضافية
            </label>
            <textarea
              className="form-control"
              id="notes"
              name="notes"
              rows="2"
              value={scheduleData.notes}
              onChange={handleChange}
              placeholder="أي ملاحظات أو تعليمات خاصة..."
            ></textarea>
          </div>

          <div className="alert alert-warning">
            <i className="fas fa-exclamation-triangle me-2"></i>
            <strong>ملاحظة:</strong> سيتم التواصل معك لتأكيد الموعد قبل الاستلام بـ 24 ساعة.
          </div>

          <div className="d-flex gap-2">
            <button type="submit" className="btn btn-primary flex-grow-1" disabled={loading}>
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                  جاري الجدولة...
                </>
              ) : (
                <>
                  <i className="fas fa-calendar-check me-2"></i>
                  تأكيد الجدولة
                </>
              )}
            </button>
            <button type="button" className="btn btn-outline-secondary">
              إلغاء
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default DeliveryScheduler
