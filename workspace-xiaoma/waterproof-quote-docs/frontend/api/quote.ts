// 防水补漏智能报价 - API 封装
// 文件: src/api/quote.ts

import axios, { AxiosInstance, AxiosResponse } from 'axios'
import { showToast } from 'vant'

// ============================================
// 类型定义
// ============================================

/** 建筑信息 */
export interface BuildingInfo {
  floor_level?: string
  house_age?: string
  area_range?: string
}

/** 表单数据 */
export interface QuoteForm {
  user_id?: string
  location_type: string
  location_label?: string
  building: BuildingInfo
  description: string
  files: any[]
}

/** 单个方案 */
export interface Plan {
  plan_id: number
  plan_code: string
  name: string
  description: string
  tags: string[]
  duration: string
  price_min: number
  price_max: number
}

/** 估价结果 */
export interface QuoteResult {
  request_id: string
  severity: 'light' | 'normal' | 'severe'
  severity_label: string
  severity_reason: string
  plans: Plan[]
}

/** 工单信息 */
export interface OrderInfo {
  order_id: string
  order_no: string
  status: string
  request_id: string
  location_type?: string
  severity?: string
  chosen_plan?: {
    plan_id: number
    name: string
    price_min: number
    price_max: number
  }
  created_at?: string
}

/** 响应包装 */
interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// ============================================
// API 实例
// ============================================

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加 token
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const { code, message } = response.data
    
    if (code !== 0 && code !== 200) {
      showToast(message || '请求失败')
      return Promise.reject(new Error(message))
    }
    
    return response.data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '网络错误'
    showToast(message)
    return Promise.reject(error)
  }
)

// ============================================
// API 接口
// ============================================

/**
 * 校验用户会话
 */
export function verifySession(userId: string, token: string): Promise<any> {
  return api.get<ApiResponse<any>>('/api/session/verify', {
    params: { user_id: userId, token }
  }).then(res => res.data.data)
}

/**
 * 上传图片
 * @param file File 对象
 */
export function uploadImage(file: File): Promise<string> {
  const formData = new FormData()
  formData.append('file', file)
  
  return api.post<ApiResponse<{ url: string }>>('/api/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(res => res.data.data.url)
}

/**
 * 批量上传图片
 * @param files File 对象数组
 */
export async function uploadImages(files: File[]): Promise<string[]> {
  const promises = files.map(file => uploadImage(file))
  return Promise.all(promises)
}

/**
 * 提交报价请求
 */
export function submitQuote(form: QuoteForm, imageUrls: string[]): Promise<QuoteResult> {
  const params = {
    user_id: form.user_id || 'anonymous',
    location_type: form.location_type,
    building_info: form.building,
    description: form.description,
    images: imageUrls
  }
  
  return api.post<ApiResponse<QuoteResult>>('/api/quote/estimate', params)
    .then(res => res.data.data)
}

/**
 * 查询报价结果
 */
export function getQuoteResult(requestId: string): Promise<QuoteResult> {
  return api.get<ApiResponse<QuoteResult>>(`/api/quote/result/${requestId}`)
    .then(res => res.data.data)
}

/**
 * 确认方案并生成工单
 */
export function confirmOrder(requestId: string, planId: number): Promise<OrderInfo> {
  return api.post<ApiResponse<OrderInfo>>('/api/quote/confirm', {
    request_id: requestId,
    plan_id: planId
  }).then(res => res.data.data)
}

/**
 * 查询工单详情
 */
export function getOrderDetail(orderId: string): Promise<OrderInfo> {
  return api.get<ApiResponse<OrderInfo>>(`/api/orders/${orderId}`)
    .then(res => res.data.data)
}

/**
 * 获取系统配置
 */
export function getConfig(): Promise<any> {
  return api.get<ApiResponse<any>>('/api/config')
    .then(res => res.data.data)
}

/**
 * 保存系统配置
 */
export function saveConfig(config: any): Promise<void> {
  return api.post<ApiResponse<void>>('/api/config', config)
    .then(res => res.data)
}

// ============================================
// 工具函数
// ============================================

/**
 * 获取严重程度标签
 */
export function getSeverityLabel(severity: string): string {
  const labels: Record<string, string> = {
    light: '轻微',
    normal: '普通',
    severe: '严重'
  }
  return labels[severity] || '未知'
}

/**
 * 获取严重程度样式类
 */
export function getSeverityClass(severity: string): string {
  const classes: Record<string, string> = {
    light: 'severity-light',
    normal: 'severity-normal',
    severe: 'severity-severe'
  }
  return classes[severity] || ''
}

/**
 * 获取漏点位置选项
 */
export function getLocationOptions() {
  return [
    { text: '卫生间', value: 'bathroom' },
    { text: '厨房', value: 'kitchen' },
    { text: '阳台', value: 'balcony' },
    { text: '屋顶', value: 'roof' },
    { text: '外墙', value: 'outer_wall' },
    { text: '飘窗', value: 'bay_window' },
    { text: '其他', value: 'other' }
  ]
}

/**
 * 获取楼层选项
 */
export function getFloorOptions() {
  return [
    { text: '低层', value: 'low' },
    { text: '中层', value: 'mid' },
    { text: '高层', value: 'high' }
  ]
}

/**
 * 获取房龄选项
 */
export function getHouseAgeOptions() {
  return [
    { text: '0-5 年', value: '0_5' },
    { text: '5-10 年', value: '5_10' },
    { text: '10 年以上', value: '10_plus' }
  ]
}

export default {
  verifySession,
  uploadImage,
  uploadImages,
  submitQuote,
  getQuoteResult,
  confirmOrder,
  getOrderDetail,
  getConfig,
  saveConfig,
  getSeverityLabel,
  getSeverityClass,
  getLocationOptions,
  getFloorOptions,
  getHouseAgeOptions
}
