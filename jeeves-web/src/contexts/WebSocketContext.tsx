import { createContext, useContext, useEffect, useState, useCallback, ReactNode } from 'react'

interface WebSocketContextType {
  isConnected: boolean
  lastMessage: unknown
  sendMessage: (message: string) => void
}

const WebSocketContext = createContext<WebSocketContextType | null>(null)

export function WebSocketProvider({ children }: { children: ReactNode }) {
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<unknown>(null)

  useEffect(() => {
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'
    const websocket = new WebSocket(wsUrl)

    websocket.onopen = () => {
      console.log('WebSocket 已连接')
      setIsConnected(true)
    }

    websocket.onclose = () => {
      console.log('WebSocket 已断开')
      setIsConnected(false)
    }

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setLastMessage(data)
      } catch {
        setLastMessage(event.data)
      }
    }

    setWs(websocket)

    return () => {
      websocket.close()
    }
  }, [])

  const sendMessage = useCallback((message: string) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(message)
    }
  }, [ws])

  return (
    <WebSocketContext.Provider value={{ isConnected, lastMessage, sendMessage }}>
      {children}
    </WebSocketContext.Provider>
  )
}

export function useWebSocket() {
  const context = useContext(WebSocketContext)
  if (!context) {
    throw new Error('useWebSocket 必须在 WebSocketProvider 内使用')
  }
  return context
}
