"use client"

import { useState } from "react"

const RatingSystem = ({ userId, userName, onRatingSubmit, existingRating = null }) => {
  const [rating, setRating] = useState(existingRating?.rating || 0)
  const [comment, setComment] = useState(existingRating?.comment || "")
  const [hoveredRating, setHoveredRating] = useState(0)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (rating === 0) {
      alert("يرجى اختيار تقييم")
      return
    }

    setLoading(true)
    try {
      // محاكاة إرسال التقييم
      await new Promise((resolve) => setTimeout(resolve, 1000))

      const ratingData = {
        userId,
        rating,
        comment,
        createdAt: new Date().toISOString(),
      }

      onRatingSubmit?.(ratingData)
      alert("تم إرسال التقييم بنجاح!")
    } catch (error) {
      alert("حدث خطأ أثناء إرسال التقييم")
    } finally {
      setLoading(false)
    }
  }

  const renderStars = () => {
    return Array.from({ length: 5 }, (_, index) => {
      const starValue = index + 1
      const isActive = starValue <= (hoveredRating || rating)

      return (
        <button
          key={index}
          type="button"
          className={`btn btn-link p-0 me-1 ${isActive ? "text-warning" : "text-muted"}`}
          onClick={() => setRating(starValue)}
          onMouseEnter={() => setHoveredRating(starValue)}
          onMouseLeave={() => setHoveredRating(0)}
          style={{ fontSize: "1.5rem", textDecoration: "none" }}
        >
          <i className={`fas fa-star`}></i>
        </button>
      )
    })
  }

  return (
    <div className="card border-0 shadow-sm">
      <div className="card-header">
        <h5 className="mb-0">
          <i className="fas fa-star text-warning me-2"></i>
          تقييم {userName}
        </h5>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">التقييم</label>
            <div className="d-flex align-items-center">
              {renderStars()}
              <span className="ms-2 text-muted">
                {rating > 0 && (
                  <>
                    {rating === 1 && "ضعيف"}
                    {rating === 2 && "مقبول"}
                    {rating === 3 && "جيد"}
                    {rating === 4 && "جيد جداً"}
                    {rating === 5 && "ممتاز"}
                  </>
                )}
              </span>
            </div>
          </div>

          <div className="mb-3">
            <label htmlFor="comment" className="form-label">
              تعليق (اختياري)
            </label>
            <textarea
              className="form-control"
              id="comment"
              rows="3"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="اكتب تعليقك هنا..."
            ></textarea>
          </div>

          <button type="submit" className="btn btn-warning" disabled={loading || rating === 0}>
            {loading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                جاري الإرسال...
              </>
            ) : (
              <>
                <i className="fas fa-star me-2"></i>
                إرسال التقييم
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

export default RatingSystem
