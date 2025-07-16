import { useState } from "react"
import axios from "axios"

const ChatBot = () => {
  const [messages, setMessages] = useState([
    { role: "system", content: "مرحبًا! أنا مساعد GreenSwap. كيف يمكنني مساعدتك اليوم؟" }
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim()) return
    const newMessages = [...messages, { role: "user", content: input }]
    setMessages(newMessages)
    setInput("")
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post(
        "https://api.openai.com/v1/chat/completions",
        {
          model: "gpt-3.5-turbo",
          messages: newMessages.map(({ role, content }) => ({ role, content })),
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer placeholder_token`, // Replace with your actual OpenAI API key
          },
        }
      )
      const reply = response.data.choices[0].message.content
      setMessages([...newMessages, { role: "assistant", content: reply }])
    } catch (err) {
      if (err.response && err.response.status === 429) {
        setError("لقد تجاوزت الحد المسموح به من الطلبات. الرجاء الانتظار قليلاً ثم المحاولة مرة أخرى.")
      } else if (err.response && err.response.data && err.response.data.error && err.response.data.error.message) {
        setError(err.response.data.error.message)
      } else {
        setError("حدث خطأ أثناء الاتصال بالمساعد. حاول مرة أخرى.")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card shadow-sm mb-4" style={{ maxWidth: 400, position: "fixed", bottom: 24, right: 24, zIndex: 9999 }}>
      <div className="card-header bg-success text-white">مساعد GreenSwap</div>
      <div className="card-body" style={{ maxHeight: 300, overflowY: "auto", background: "#f9f9f9" }}>
        {messages.filter(m => m.role !== "system").map((msg, idx) => (
          <div key={idx} className={`mb-2 text-${msg.role === "user" ? "end" : "start"}`}>
            <span className={`badge bg-${msg.role === "user" ? "light text-dark" : "success"}`}>{msg.content}</span>
          </div>
        ))}
        {loading && <div className="text-center text-muted small">جاري الكتابة...</div>}
        {error && <div className="text-danger small">{error}</div>}
      </div>
      <form className="card-footer d-flex gap-2" onSubmit={handleSend} autoComplete="off">
        <input
          type="text"
          className="form-control"
          placeholder="اكتب سؤالك..."
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={loading}
        />
        <button className="btn btn-success" type="submit" disabled={loading || !input.trim()}>
          إرسال
        </button>
      </form>
    </div>
  )
}

export default ChatBot
