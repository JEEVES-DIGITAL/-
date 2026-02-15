import { NavLink, Outlet } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Lightbulb, 
  MessageSquare, 
  Zap, 
  Settings,
  Wifi,
  WifiOff
} from 'lucide-react'
import { useWebSocket } from '../contexts/WebSocketContext'

const navItems = [
  { path: '/', icon: LayoutDashboard, label: '仪表盘' },
  { path: '/devices', icon: Lightbulb, label: '设备' },
  { path: '/chat', icon: MessageSquare, label: 'AI助手' },
  { path: '/automations', icon: Zap, label: '自动化' },
  { path: '/settings', icon: Settings, label: '设置' },
]

export default function Layout() {
  const { isConnected } = useWebSocket()

  return (
    <div className="flex h-screen bg-gray-50">
      {/* 侧边栏 */}
      <aside className="w-64 bg-jeeves-950 text-white flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-jeeves-900">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-accent-500 rounded-lg flex items-center justify-center">
              <span className="text-xl font-bold text-white">J</span>
            </div>
            <div>
              <h1 className="text-lg font-bold">基维斯</h1>
              <p className="text-xs text-jeeves-300">Jeeves OS</p>
            </div>
          </div>
        </div>

        {/* 导航 */}
        <nav className="flex-1 py-4">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-6 py-3 transition-colors ${
                  isActive
                    ? 'bg-jeeves-900 text-accent-400 border-r-2 border-accent-400'
                    : 'text-jeeves-300 hover:bg-jeeves-900 hover:text-white'
                }`
              }
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        {/* 连接状态 */}
        <div className="p-4 border-t border-jeeves-900">
          <div className="flex items-center gap-2 text-sm">
            {isConnected ? (
              <>
                <Wifi size={16} className="text-green-400" />
                <span className="text-green-400">已连接</span>
              </>
            ) : (
              <>
                <WifiOff size={16} className="text-red-400" />
                <span className="text-red-400">未连接</span>
              </>
            )}
          </div>
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
