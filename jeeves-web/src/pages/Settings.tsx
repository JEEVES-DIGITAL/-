import { useState } from 'react'
import { 
  Server, 
  Database, 
  Cpu, 
  Shield, 
  Bell, 
  Moon, 
  Sun,
  Save
} from 'lucide-react'
import toast from 'react-hot-toast'

export default function Settings() {
  const [darkMode, setDarkMode] = useState(false)
  const [notifications, setNotifications] = useState(true)

  const handleSave = () => {
    toast.success('设置已保存')
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div>
        <h1 className="text-2xl font-bold text-gray-800">设置</h1>
        <p className="text-gray-500">配置系统参数和偏好设置</p>
      </div>

      {/* 设置卡片 */}
      <div className="grid gap-6">
        {/* 系统信息 */}
        <SettingsCard 
          icon={Server} 
          title="系统信息"
          description="查看系统版本和运行状态"
        >
          <div className="space-y-3">
            <InfoRow label="系统版本" value="Jeeves OS v0.1.0" />
            <InfoRow label="API版本" value="v1" />
            <InfoRow label="运行时间" value="3天 4小时" />
          </div>
        </SettingsCard>

        {/* 数据库 */}
        <SettingsCard 
          icon={Database} 
          title="数据库"
          description="数据库连接配置"
        >
          <div className="space-y-3">
            <InfoRow label="类型" value="PostgreSQL" />
            <InfoRow label="状态" value="已连接" valueColor="text-green-500" />
            <InfoRow label="主机" value="localhost:5432" />
          </div>
        </SettingsCard>

        {/* AI配置 */}
        <SettingsCard 
          icon={Cpu} 
          title="AI配置"
          description="本地AI和云端增强设置"
        >
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">本地模型</label>
              <select className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-jeeves-500">
                <option value="phi4">Phi-4 (推荐)</option>
                <option value="llama3">Llama 3</option>
                <option value="qwen">Qwen 2.5</option>
              </select>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-700">云端增强</span>
              <button
                className="w-12 h-6 bg-gray-300 rounded-full relative transition-colors"
              >
                <span className="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform" />
              </button>
            </div>
          </div>
        </SettingsCard>

        {/* 偏好设置 */}
        <SettingsCard 
          icon={Shield} 
          title="偏好设置"
          description="个性化您的使用体验"
        >
          <div className="space-y-4">
            <ToggleSetting
              icon={darkMode ? Moon : Sun}
              label="深色模式"
              checked={darkMode}
              onChange={setDarkMode}
            />
            <ToggleSetting
              icon={Bell}
              label="消息通知"
              checked={notifications}
              onChange={setNotifications}
            />
          </div>
        </SettingsCard>
      </div>

      {/* 保存按钮 */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          className="flex items-center gap-2 px-6 py-2 bg-jeeves-700 text-white rounded-lg hover:bg-jeeves-800 transition-colors"
        >
          <Save size={18} />
          保存设置
        </button>
      </div>
    </div>
  )
}

function SettingsCard({ 
  icon: Icon, 
  title, 
  description, 
  children 
}: { 
  icon: React.ElementType
  title: string
  description: string
  children: React.ReactNode
}) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-start gap-4 mb-4">
        <div className="p-3 rounded-lg bg-jeeves-50">
          <Icon size={20} className="text-jeeves-700" />
        </div>
        <div>
          <h2 className="font-semibold text-gray-800">{title}</h2>
          <p className="text-sm text-gray-500">{description}</p>
        </div>
      </div>
      <div className="pl-16">
        {children}
      </div>
    </div>
  )
}

function InfoRow({ 
  label, 
  value, 
  valueColor = 'text-gray-800' 
}: { 
  label: string
  value: string
  valueColor?: string
}) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-gray-500">{label}</span>
      <span className={`font-medium ${valueColor}`}>{value}</span>
    </div>
  )
}

function ToggleSetting({ 
  icon: Icon, 
  label, 
  checked, 
  onChange 
}: { 
  icon: React.ElementType
  label: string
  checked: boolean
  onChange: (checked: boolean) => void
}) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-3">
        <Icon size={18} className="text-gray-400" />
        <span className="text-gray-700">{label}</span>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`w-12 h-6 rounded-full relative transition-colors ${
          checked ? 'bg-accent-500' : 'bg-gray-300'
        }`}
      >
        <span className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
          checked ? 'left-7' : 'left-1'
        }`} />
      </button>
    </div>
  )
}
