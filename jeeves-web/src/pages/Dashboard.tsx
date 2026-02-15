import { useEffect, useState } from 'react'
import useSWR from 'swr'
import { 
  Lightbulb, 
  Thermometer, 
  Shield, 
  Activity,
  Home,
  Power
} from 'lucide-react'
import { systemApi, devicesApi } from '../services/api'

interface SystemInfo {
  version: string
  uptime: number
  devices_count: number
  automations_count: number
  conversations_count: number
}

interface Device {
  id: string
  name: string
  device_type: string
  state: string
  area: string
  is_available: boolean
}

function StatCard({ 
  icon: Icon, 
  title, 
  value, 
  color 
}: { 
  icon: React.ElementType
  title: string
  value: string | number
  color: string 
}) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center gap-4">
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon size={24} className="text-white" />
        </div>
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
        </div>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const { data: systemData } = useSWR('system-info', () => systemApi.info().then(r => r.data))
  const { data: devicesData } = useSWR('devices', () => devicesApi.list().then(r => r.data))
  
  const info: SystemInfo | undefined = systemData
  const devices: Device[] = devicesData?.devices || []

  // 统计在线设备
  const onlineDevices = devices.filter(d => d.is_available).length
  
  // 按类型分组
  const lightsOn = devices.filter(d => d.device_type === 'light' && d.state === 'on').length
  const climateOn = devices.filter(d => d.device_type === 'climate' && d.state !== 'off').length

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">仪表盘</h1>
          <p className="text-gray-500">欢迎回家，当前系统运行正常</p>
        </div>
        <div className="text-sm text-gray-400">
          版本: {info?.version || '--'}
        </div>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard 
          icon={Home} 
          title="设备总数" 
          value={info?.devices_count || 0} 
          color="bg-blue-500" 
        />
        <StatCard 
          icon={Power} 
          title="在线设备" 
          value={onlineDevices} 
          color="bg-green-500" 
        />
        <StatCard 
          icon={Lightbulb} 
          title="灯光开启" 
          value={lightsOn} 
          color="bg-yellow-500" 
        />
        <StatCard 
          icon={Thermometer} 
          title="空调运行" 
          value={climateOn} 
          color="bg-orange-500" 
        />
      </div>

      {/* 快速控制 */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">快速场景</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <QuickSceneButton 
            icon={Home} 
            label="回家模式" 
            onClick={() => console.log('回家模式')} 
          />
          <QuickSceneButton 
            icon={Power} 
            label="离家模式" 
            onClick={() => console.log('离家模式')} 
          />
          <QuickSceneButton 
            icon={Lightbulb} 
            label="睡眠模式" 
            onClick={() => console.log('睡眠模式')} 
          />
          <QuickSceneButton 
            icon={Shield} 
            label="安防模式" 
            onClick={() => console.log('安防模式')} 
          />
        </div>
      </div>

      {/* 最近活动 */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">最近活动</h2>
        <div className="space-y-3">
          <ActivityItem 
            icon={Lightbulb}
            text="客厅灯已开启"
            time="2分钟前"
          />
          <ActivityItem 
            icon={Thermometer}
            text="空调温度设置为24°C"
            time="5分钟前"
          />
          <ActivityItem 
            icon={Activity}
            text="回家模式已触发"
            time="10分钟前"
          />
        </div>
      </div>
    </div>
  )
}

function QuickSceneButton({ 
  icon: Icon, 
  label, 
  onClick 
}: { 
  icon: React.ElementType
  label: string
  onClick: () => void 
}) {
  return (
    <button
      onClick={onClick}
      className="flex flex-col items-center gap-2 p-4 rounded-xl bg-gray-50 hover:bg-jeeves-50 
                 border border-gray-200 hover:border-jeeves-300 transition-all"
    >
      <div className="p-3 rounded-full bg-white shadow-sm">
        <Icon size={24} className="text-jeeves-700" />
      </div>
      <span className="text-sm font-medium text-gray-700">{label}</span>
    </button>
  )
}

function ActivityItem({ 
  icon: Icon, 
  text, 
  time 
}: { 
  icon: React.ElementType
  text: string
  time: string 
}) {
  return (
    <div className="flex items-center gap-3 py-2">
      <div className="p-2 rounded-full bg-gray-100">
        <Icon size={16} className="text-gray-600" />
      </div>
      <div className="flex-1">
        <p className="text-gray-800">{text}</p>
      </div>
      <span className="text-sm text-gray-400">{time}</span>
    </div>
  )
}
