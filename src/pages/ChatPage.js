"use client"

import { useState, useEffect, useRef } from "react"
// import { useAuth } from "../context/AuthContext"

const ChatPage = () => {
  // const { currentUser } = useAuth()
  const currentUser='hamada'
  const [conversations, setConversations] = useState([])
  const [activeConversation, setActiveConversation] = useState(null)
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState("")
  const [loading, setLoading] = useState(true)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // محاكاة تحميل المحادثات
    const mockConversations = [
      {
        id: 1,
        user: {
          id: 2,
          name: "أحمد محمد",
          avatar: "/placeholder.svg?height=50&width=50",
          type: "individual",
        },
        lastMessage: "هل المنتج ما زال متاحاً؟",
        lastMessageTime: "2024-01-15T10:30:00",
        unreadCount: 2,
        item: {
          id: 1,
          title: "أثاث مكتبي مستعمل",
          image: "/placeholder.svg?height=50&width=50",
        },
      },
      {
        id: 2,
        user: {
          id: 3,
          name: "ورشة التدوير",
          avatar: "/placeholder.svg?height=50&width=50",
          type: "workshop",
        },
        lastMessage: "شكراً لك، سأتواصل معك غداً",
        lastMessageTime: "2024-01-14T15:45:00",
        unreadCount: 0,
        item: {
          id: 2,
          title: "خردة معادن",
          image: "/placeholder.svg?height=50&width=50",
        },
      },
      {
        id: 3,
        user: {
          id: 4,
          name: "مصنع البلاستيك",
          avatar: "/placeholder.svg?height=50&width=50",
          type: "company",
        },
        lastMessage: "ما هي كمية البلاستيك المتاحة؟",
        lastMessageTime: "2024-01-13T09:20:00",
        unreadCount: 1,
        item: {
          id: 3,
          title: "بلاستيك للتدوير",
          image: "/placeholder.svg?height=50&width=50",
        },
      },
    ]

    setTimeout(() => {
      setConversations(mockConversations)
      setActiveConversation(mockConversations[0])
      setLoading(false)
    }, 1000)
  }, [])

  useEffect(() => {
    if (activeConversation) {
      // محاكاة تحميل الرسائل
      const mockMessages = [
        {
          id: 1,
          senderId: activeConversation.user.id,
          senderName: activeConversation.user.name,
          content: "السلام عليكم، أريد الاستفسار عن المنتج",
          timestamp: "2024-01-15T09:00:00",
          type: "text",
        },
        {
          id: 2,
          senderId: currentUser.id,
          senderName: currentUser.name,
          content: "وعليكم السلام، أهلاً بك. ما الذي تريد معرفته؟",
          timestamp: "2024-01-15T09:05:00",
          type: "text",
        },
        {
          id: 3,
          senderId: activeConversation.user.id,
          senderName: activeConversation.user.name,
          content: "هل المنتج ما زال متاحاً؟ وما هي حالته بالضبط؟",
          timestamp: "2024-01-15T09:10:00",
          type: "text",
        },
        {
          id: 4,
          senderId: currentUser.id,
          senderName: currentUser.name,
          content: "نعم ما زال متاحاً. الحالة جيدة جداً كما هو موضح في الصور",
          timestamp: "2024-01-15T09:15:00",
          type: "text",
        },
        {
          id: 5,
          senderId: activeConversation.user.id,
          senderName: activeConversation.user.name,
          content: "ممتاز، متى يمكنني المعاينة؟",
          timestamp: "2024-01-15T10:30:00",
          type: "text",
        },
      ]

      setMessages(mockMessages)
    }
  }, [activeConversation, currentUser])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSendMessage = (e) => {
    e.preventDefault()
    if (!newMessage.trim()) return

    const message = {
      id: Date.now(),
      senderId: currentUser.id,
      senderName: currentUser.name,
      content: newMessage,
      timestamp: new Date().toISOString(),
      type: "text",
    }

    setMessages((prev) => [...prev, message])
    setNewMessage("")

    // تحديث آخر رسالة في المحادثة
    setConversations((prev) =>
      prev.map((conv) =>
        conv.id === activeConversation.id
          ? { ...conv, lastMessage: newMessage, lastMessageTime: message.timestamp }
          : conv,
      ),
    )
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInHours = (now - date) / (1000 * 60 * 60)

    if (diffInHours < 24) {
      return date.toLocaleTimeString("ar-EG", {
        hour: "2-digit",
        minute: "2-digit",
      })
    } else {
      return date.toLocaleDateString("ar-EG", {
        month: "short",
        day: "numeric",
      })
    }
  }

  const getUserTypeLabel = (type) => {
    const types = {
      individual: "فرد",
      workshop: "ورشة",
      collector: "جامع خردة",
      organization: "جمعية",
      company: "شركة",
    }
    return types[type] || type
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
    <div className="container-fluid py-4">
      <div className="row">
        {/* Conversations List */}
        <div className="col-lg-4 col-xl-3">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-header bg-success text-white">
              <h5 className="mb-0">
                <i className="fas fa-comments me-2"></i>
                المحادثات
              </h5>
            </div>
            <div className="card-body p-0">
              {conversations.length === 0 ? (
                <div className="text-center py-5">
                  <i className="fas fa-inbox fs-1 text-muted mb-3"></i>
                  <p className="text-muted">لا توجد محادثات</p>
                </div>
              ) : (
                <div className="list-group list-group-flush">
                  {conversations.map((conversation) => (
                    <div
                      key={conversation.id}
                      className={`list-group-item list-group-item-action cursor-pointer ${
                        activeConversation?.id === conversation.id ? "active" : ""
                      }`}
                      onClick={() => setActiveConversation(conversation)}
                    >
                      <div className="d-flex align-items-center">
                        <div className="position-relative me-3">
                          <img
                            src={conversation.user.avatar || "/placeholder.svg"}
                            alt={conversation.user.name}
                            className="rounded-circle"
                            style={{ width: "50px", height: "50px", objectFit: "cover" }}
                          />
                          {conversation.unreadCount > 0 && (
                            <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                              {conversation.unreadCount}
                            </span>
                          )}
                        </div>
                        <div className="flex-grow-1 min-width-0">
                          <div className="d-flex justify-content-between align-items-start">
                            <h6 className="mb-1 text-truncate">{conversation.user.name}</h6>
                            <small className="text-muted">{formatTime(conversation.lastMessageTime)}</small>
                          </div>
                          <p className="mb-1 text-muted small text-truncate">{conversation.lastMessage}</p>
                          <div className="d-flex align-items-center">
                            <img
                              src={conversation.item.image || "/placeholder.svg"}
                              alt={conversation.item.title}
                              className="rounded me-2"
                              style={{ width: "20px", height: "20px", objectFit: "cover" }}
                            />
                            <small className="text-muted text-truncate">{conversation.item.title}</small>
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

        {/* Chat Area */}
        <div className="col-lg-8 col-xl-9">
          {activeConversation ? (
            <div className="card border-0 shadow-sm h-100">
              {/* Chat Header */}
              <div className="card-header bg-light">
                <div className="d-flex align-items-center">
                  <img
                    src={activeConversation.user.avatar || "/placeholder.svg"}
                    alt={activeConversation.user.name}
                    className="rounded-circle me-3"
                    style={{ width: "40px", height: "40px", objectFit: "cover" }}
                  />
                  <div className="flex-grow-1">
                    <h6 className="mb-0">{activeConversation.user.name}</h6>
                    <small className="text-muted">{getUserTypeLabel(activeConversation.user.type)}</small>
                  </div>
                  <div className="d-flex align-items-center">
                    <img
                      src={activeConversation.item.image || "/placeholder.svg"}
                      alt={activeConversation.item.title}
                      className="rounded me-2"
                      style={{ width: "30px", height: "30px", objectFit: "cover" }}
                    />
                    <small className="text-muted">{activeConversation.item.title}</small>
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div className="card-body" style={{ height: "400px", overflowY: "auto" }}>
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`d-flex mb-3 ${
                      message.senderId === currentUser.id ? "justify-content-end" : "justify-content-start"
                    }`}
                  >
                    <div
                      className={`max-width-70 ${
                        message.senderId === currentUser.id ? "bg-success text-white" : "bg-light"
                      } rounded p-3`}
                      style={{ maxWidth: "70%" }}
                    >
                      <p className="mb-1">{message.content}</p>
                      <small className={`${message.senderId === currentUser.id ? "text-white-50" : "text-muted"}`}>
                        {formatTime(message.timestamp)}
                      </small>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>

              {/* Message Input */}
              <div className="card-footer">
                <form onSubmit={handleSendMessage}>
                  <div className="input-group">
                    <input
                      type="text"
                      className="form-control"
                      placeholder="اكتب رسالتك..."
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                    />
                    <button type="submit" className="btn btn-success" disabled={!newMessage.trim()}>
                      <i className="fas fa-paper-plane"></i>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          ) : (
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body d-flex align-items-center justify-content-center">
                <div className="text-center">
                  <i className="fas fa-comments fs-1 text-muted mb-3"></i>
                  <h5 className="text-muted">اختر محادثة للبدء</h5>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChatPage
