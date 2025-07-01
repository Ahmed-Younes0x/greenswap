"use client"

import { useState, useEffect } from "react"

const MapComponent = ({ location, onLocationSelect, height = "300px", interactive = false }) => {
  const [mapLoaded, setMapLoaded] = useState(false)
  const [selectedLocation, setSelectedLocation] = useState(location)

  // محاكاة تحميل الخريطة
  useEffect(() => {
    const timer = setTimeout(() => {
      setMapLoaded(true)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  const handleLocationClick = (event) => {
    if (!interactive) return

    const rect = event.currentTarget.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top

    // محاكاة إحداثيات الموقع
    const mockLocation = {
      lat: 30.0444 + (y / rect.height - 0.5) * 0.1,
      lng: 31.2357 + (x / rect.width - 0.5) * 0.1,
      address: "موقع مختار على الخريطة",
    }

    setSelectedLocation(mockLocation)
    onLocationSelect?.(mockLocation)
  }

  const egyptianCities = [
    { name: "القاهرة", lat: 30.0444, lng: 31.2357 },
    { name: "الجيزة", lat: 30.0131, lng: 31.2089 },
    { name: "الإسكندرية", lat: 31.2001, lng: 29.9187 },
    { name: "الدقهلية", lat: 31.0409, lng: 31.3785 },
    { name: "الشرقية", lat: 30.5965, lng: 31.5041 },
  ]

  return (
    <div className="map-container">
      <div
        className="position-relative bg-light border rounded"
        style={{ height, cursor: interactive ? "crosshair" : "default" }}
        onClick={handleLocationClick}
      >
        {!mapLoaded ? (
          <div className="d-flex align-items-center justify-content-center h-100">
            <div className="text-center">
              <div className="spinner-border text-success mb-2" role="status">
                <span className="visually-hidden">جاري تحميل الخريطة...</span>
              </div>
              <p className="text-muted">جاري تحميل الخريطة...</p>
            </div>
          </div>
        ) : (
          <>
            {/* محاكاة خريطة مصر */}
            <div
              className="position-absolute top-0 start-0 w-100 h-100 bg-gradient"
              style={{
                background: "linear-gradient(45deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%)",
              }}
            >
              {/* رسم محاكاة لخريطة مصر */}
              <svg className="w-100 h-100" viewBox="0 0 400 300">
                {/* شكل مبسط لخريطة مصر */}
                <path
                  d="M100 50 L300 50 L320 80 L310 150 L280 200 L200 250 L120 240 L80 180 L90 120 Z"
                  fill="#4caf50"
                  fillOpacity="0.3"
                  stroke="#2e7d32"
                  strokeWidth="2"
                />

                {/* المدن */}
                {egyptianCities.map((city, index) => (
                  <g key={city.name}>
                    <circle cx={150 + index * 30} cy={100 + index * 20} r="4" fill="#f44336" />
                    <text x={150 + index * 30} y={90 + index * 20} textAnchor="middle" fontSize="10" fill="#333">
                      {city.name}
                    </text>
                  </g>
                ))}

                {/* الموقع المحدد */}
                {selectedLocation && <circle cx="200" cy="150" r="8" fill="#2196f3" stroke="#fff" strokeWidth="2" />}
              </svg>
            </div>

            {/* معلومات الموقع */}
            {selectedLocation && (
              <div className="position-absolute bottom-0 start-0 m-2 bg-white rounded p-2 shadow-sm">
                <small className="text-muted">
                  <i className="fas fa-map-marker-alt text-danger me-1"></i>
                  {selectedLocation.address || selectedLocation.name || "موقع محدد"}
                </small>
              </div>
            )}

            {/* أدوات التحكم */}
            <div className="position-absolute top-0 end-0 m-2">
              <div className="btn-group-vertical">
                <button className="btn btn-sm btn-light">
                  <i className="fas fa-plus"></i>
                </button>
                <button className="btn btn-sm btn-light">
                  <i className="fas fa-minus"></i>
                </button>
              </div>
            </div>

            {interactive && (
              <div className="position-absolute bottom-0 end-0 m-2">
                <small className="bg-white rounded p-1 text-muted">انقر لتحديد الموقع</small>
              </div>
            )}
          </>
        )}
      </div>

      {/* معلومات إضافية */}
      {location && (
        <div className="mt-2">
          <small className="text-muted">
            <i className="fas fa-info-circle me-1"></i>
            الموقع: {location.address || location.name || "غير محدد"}
          </small>
        </div>
      )}
    </div>
  )
}

export default MapComponent
