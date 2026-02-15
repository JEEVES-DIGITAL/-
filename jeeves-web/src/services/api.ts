import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 系统接口
export const systemApi = {
  health: () => api.get('/system/health'),
  info: () => api.get('/system/info'),
}

// 设备接口
export const devicesApi = {
  list: (params?: { device_type?: string; area?: string }) => 
    api.get('/devices', { params }),
  get: (id: string) => api.get(`/devices/${id}`),
  create: (data: unknown) => api.post('/devices', data),
  update: (id: string, data: unknown) => api.patch(`/devices/${id}`, data),
  delete: (id: string) => api.delete(`/devices/${id}`),
  command: (id: string, data: unknown) => api.post(`/devices/${id}/command`, data),
}

// 对话接口
export const chatApi = {
  send: (message: string, sessionId?: string) => 
    api.post('/chat', { message, session_id: sessionId }),
}

// 自动化接口
export const automationsApi = {
  list: () => api.get('/automations'),
  get: (id: string) => api.get(`/automations/${id}`),
  create: (data: unknown) => api.post('/automations', data),
  update: (id: string, data: unknown) => api.patch(`/automations/${id}`, data),
  delete: (id: string) => api.delete(`/automations/${id}`),
  trigger: (id: string) => api.post(`/automations/${id}/trigger`),
}

export default api
