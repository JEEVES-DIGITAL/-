import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { SWRConfig } from 'swr'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './index.css'
import { WebSocketProvider } from './contexts/WebSocketContext'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <SWRConfig
        value={{
          refreshInterval: 5000,
          revalidateOnFocus: true,
        }}
      >
        <WebSocketProvider>
          <App />
          <Toaster position="top-right" />
        </WebSocketProvider>
      </SWRConfig>
    </BrowserRouter>
  </React.StrictMode>,
)
