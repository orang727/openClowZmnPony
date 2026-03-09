# UI 设计稿 v2.1 - 设计标注

> **版本**: v2.1  
> **创建时间**: 2026-03-08 18:45  
> **设计师**: 小爱 (xiaoi)  
> **目标读者**: 前端开发工程师  
> **开发框架**: 移动端 H5 / 小程序  

---

## 📐 全局规范

### 设计稿尺寸

```
宽度：375px（iPhone X）
高度：812px
适配：响应式布局，适配主流手机屏幕
```

### 基础栅格

```
页面边距：16px（左右）
卡片内边距：16px
模块间距：24px
元素间距：8px / 16px
```

### 色彩规范

```css
/* 主色 */
--primary: #1E88E5;
--primary-dark: #1565C0;
--primary-light: #E3F2FD;

/* 功能色 */
--success: #43A047;
--warning: #FB8C00;
--error: #E53935;
--info: #1E88E5;

/* 中性色 */
--text-primary: #333333;
--text-secondary: #666666;
--text-hint: #999999;
--border: #CCCCCC;
--background: #F5F5F5;
--card-bg: #FFFFFF;
```

### 字体规范

```css
/* 字号 */
--text-xs: 12px;    /* 提示文字 */
--text-sm: 14px;    /* 辅助文字 */
--text-base: 16px;  /* 正文 */
--text-lg: 20px;    /* 中标题 */
--text-xl: 24px;    /* 大标题 */
--text-2xl: 32px;   /* 超大标题 */

/* 字重 */
--font-normal: 400;
--font-medium: 500;
--font-bold: 700;
```

---

## 📊 全局组件 - 6 步进度条

### 组件结构

```html
<div class="progress-bar">
  <div class="step-text">步骤 3/6</div>
  <div class="progress-indicator">
    <div class="dot completed">✓</div>
    <div class="line completed"></div>
    <div class="dot completed">✓</div>
    <div class="line completed"></div>
    <div class="dot active">3</div>
    <div class="line"></div>
    <div class="dot"></div>
    <div class="line"></div>
    <div class="dot"></div>
    <div class="line"></div>
    <div class="dot"></div>
  </div>
</div>
```

### 样式规格

```css
.progress-bar {
  height: 60px;
  padding: 8px 16px;
  background: #FFFFFF;
  border-bottom: 1px solid #F5F5F5;
}

.step-text {
  font-size: 14px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 8px;
}

.progress-indicator {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  font-size: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  flex-shrink: 0;
}

.dot.completed {
  background: #43A047;
}

.dot.active {
  background: #1E88E5;
}

.dot:not(.completed):not(.active) {
  background: #CCCCCC;
}

.line {
  width: 48px;
  height: 2px;
  background: #CCCCCC;
  flex-grow: 1;
  margin: 0 4px;
}

.line.completed {
  background: #43A047;
}

.line.active {
  background: linear-gradient(to right, #43A047 50%, #CCCCCC 50%);
}
```

### Props 参数

```typescript
interface ProgressBarProps {
  currentStep: number;  // 1-6
  totalSteps?: number;  // 默认 6
}
```

### 使用示例

```vue
<!-- P1 -->
<ProgressBar :currentStep="1" />

<!-- P2 -->
<ProgressBar :currentStep="2" />

<!-- P3 -->
<ProgressBar :currentStep="3" />
```

---

## 📱 P1 - 漏点位置选择

### 页面结构

```
导航栏 (44px)
进度条 (60px)
页面标题 + 说明 (56px)
位置卡片列表 (7 个 × 116px = 812px)
社会证明卡片 (76px)
底部按钮区域 (80px)
─────────────────────
总高度：约 1128px（可滚动）
```

### 社会证明卡片

```css
.social-proof {
  margin: 16px;
  padding: 12px 16px;
  background: #E8F5E9;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.social-proof-icon {
  font-size: 20px;
}

.social-proof-text {
  font-size: 14px;
  color: #666666;
}

.social-proof-subtext {
  font-size: 12px;
  color: #999999;
  margin-left: 28px;
}
```

---

## 📱 P2 - 图片上传

### 数量提示

```css
.upload-count {
  font-size: 14px;
  color: #666666;
  margin: 16px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.upload-count.success {
  color: #43A047;
}

.upload-count .check-icon {
  color: #43A047;
}
```

### 上传区域禁用状态

```css
.upload-area.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.upload-area.disabled .upload-icon {
  color: #CCCCCC;
}

.upload-limit-hint {
  font-size: 12px;
  color: #999999;
  margin-top: 8px;
  text-align: center;
}
```

### 交互逻辑

```javascript
const MAX_IMAGES = 5;
const MIN_IMAGES = 1;

function handleImageUpload(file) {
  if (images.value.length >= MAX_IMAGES) {
    showToast('已达上限，无法继续上传');
    return;
  }
  // 上传逻辑
}

function handleImageDelete(index) {
  images.value.splice(index, 1);
  // 更新计数器
}

// 计算属性
const uploadCountText = computed(() => {
  const count = images.value.length;
  if (count >= MAX_IMAGES) {
    return `已上传 ${count}/${MAX_IMAGES} 张 ✅`;
  }
  return `已上传 ${count}/${MAX_IMAGES} 张`;
});

const isUploadDisabled = computed(() => {
  return images.value.length >= MAX_IMAGES;
});
```

---

## 📱 P3 - 面积估算 + AI 分析

### 默认状态

```javascript
// 默认选中手动输入模式
const selectedMode = ref('manual'); // 'manual' | 'ai'

// AI 模式默认收起
const isAiExpanded = ref(false);
```

### 提示文案

```css
.ai-hint {
  margin: 16px;
  padding: 12px 16px;
  background: #FFF3E0;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.ai-hint-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.ai-hint-text {
  font-size: 12px;
  color: #FB8C00;
  line-height: 1.5;
}
```

### AI 加载进度

```css
.ai-loading {
  padding: 24px 16px;
  text-align: center;
}

.loading-animation {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 16px;
  color: #333333;
  margin-bottom: 24px;
}

.step-list {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 40px;
  font-size: 14px;
}

.step-item.completed .step-icon {
  color: #43A047;
}

.step-item.completed .step-text {
  color: #333333;
}

.step-item.processing .step-icon {
  color: #1E88E5;
  animation: pulse 1s ease-in-out infinite;
}

.step-item.processing .step-text {
  color: #1E88E5;
  font-weight: 500;
}

.step-item.pending .step-icon {
  color: #CCCCCC;
}

.step-item.pending .step-text {
  color: #999999;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.progress-bar-wrapper {
  margin-bottom: 8px;
}

.progress-bar-fill {
  height: 6px;
  background: #F5F5F5;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-value {
  height: 100%;
  background: #1E88E5;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-percentage {
  font-size: 14px;
  font-weight: 700;
  color: #1E88E5;
  text-align: center;
  margin-bottom: 8px;
}

.eta-text {
  font-size: 12px;
  color: #999999;
}
```

### 交互逻辑

```javascript
const aiProgress = ref(0);
const aiSteps = ref([
  { text: '识别漏水位置', status: 'pending' },
  { text: '分析严重程度', status: 'pending' },
  { text: '估算面积', status: 'pending' },
  { text: '生成施工方案', status: 'pending' }
]);

async function startAiAnalysis() {
  isAiExpanded.value = true;
  
  // 模拟进度更新
  const updateProgress = (progress: number, stepIndex: number) => {
    aiProgress.value = progress;
    aiSteps.value.forEach((step, index) => {
      if (index < stepIndex) {
        step.status = 'completed';
      } else if (index === stepIndex) {
        step.status = 'processing';
      } else {
        step.status = 'pending';
      }
    });
  };
  
  // 实际项目中对接真实 API
  updateProgress(25, 0);
  await sleep(2000);
  updateProgress(50, 1);
  await sleep(2000);
  updateProgress(75, 2);
  await sleep(2000);
  updateProgress(100, 3);
  aiSteps.value[3].status = 'completed';
}
```

---

## 📱 P4 - 方案推荐

### 用户评价卡片

```css
.user-reviews {
  margin: 16px;
  background: #F5F5F5;
  border-radius: 8px;
  padding: 16px;
}

.reviews-title {
  font-size: 16px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 16px;
}

.review-item {
  padding: 16px 0;
  border-bottom: 1px solid #CCCCCC;
}

.review-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.review-stars {
  color: #FFC107;
  font-size: 16px;
  margin-bottom: 8px;
}

.review-text {
  font-size: 14px;
  color: #666666;
  font-style: italic;
  line-height: 1.6;
  margin-bottom: 8px;
}

.review-author {
  font-size: 12px;
  color: #999999;
  text-align: right;
}
```

---

## 📱 P5 - 价格显示 + 留资

### 价格说明

```css
.price-container {
  text-align: center;
  padding: 24px 16px;
}

.price-amount {
  font-size: 32px;
  font-weight: 700;
  color: #1E88E5;
  margin-bottom: 8px;
}

.price-hint {
  font-size: 12px;
  color: #999999;
  line-height: 1.5;
  margin-bottom: 16px;
}

.price-hint-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background: #F5F5F5;
  border-radius: 4px;
  margin-bottom: 16px;
}

.price-hint-badge-icon {
  font-size: 14px;
}

.price-hint-badge-text {
  font-size: 12px;
  color: #999999;
}
```

### 预约顾问按钮

```css
.consult-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 16px;
  background: #E3F2FD;
  border: 1px solid #1E88E5;
  border-radius: 8px;
  margin-bottom: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.consult-btn:hover {
  background: #BBDEFB;
}

.consult-btn-icon {
  font-size: 16px;
  color: #1E88E5;
}

.consult-btn-text {
  font-size: 14px;
  color: #1E88E5;
  font-weight: 500;
}
```

### 表单进度提示

```css
.form-progress {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.form-progress-title {
  font-size: 16px;
  font-weight: 500;
  color: #333333;
}

.form-progress-step {
  font-size: 14px;
  color: #666666;
}

.form-progress-bar {
  height: 2px;
  background: #F5F5F5;
  border-radius: 1px;
  margin-top: 8px;
  overflow: hidden;
}

.form-progress-fill {
  height: 100%;
  background: #1E88E5;
  transition: width 0.3s ease;
}

.address-hint {
  font-size: 12px;
  color: #999999;
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.address-hint-icon {
  font-size: 12px;
}
```

### 表单字段

```javascript
// P5 表单字段（v2.1 简化为 2 个）
const formFields = ref({
  name: '',
  phone: '',
  agreeTerms: false
});

// 校验规则
const validationRules = {
  name: {
    required: true,
    minLength: 2,
    message: '请输入您的姓名'
  },
  phone: {
    required: true,
    pattern: /^1[3-9]\d{9}$/,
    message: '请输入正确的手机号'
  },
  agreeTerms: {
    required: true,
    message: '请阅读并同意用户协议'
  }
};

// 计算表单进度
const formProgress = computed(() => {
  let filled = 0;
  if (formFields.value.name) filled++;
  if (formFields.value.phone) filled++;
  return filled / 2; // 2 个字段
});
```

---

## 📱 P6 - 确认下单

### 地址字段

```css
.address-field {
  margin: 16px;
}

.address-label {
  font-size: 16px;
  font-weight: 500;
  color: #333333;
  margin-bottom: 8px;
}

.address-label .required {
  color: #E53935;
  margin-left: 4px;
}

.address-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  border: 1px solid #CCCCCC;
  border-radius: 4px;
  font-size: 16px;
  color: #333333;
  transition: border-color 0.2s ease;
}

.address-input:focus {
  border-color: #1E88E5;
  outline: none;
}

.address-input::placeholder {
  color: #999999;
}

.address-error {
  font-size: 12px;
  color: #E53935;
  margin-top: 4px;
}
```

### 校验逻辑

```javascript
const addressField = ref('');

function validateAddress() {
  if (!addressField.value.trim()) {
    return {
      valid: false,
      message: '请输入详细地址'
    };
  }
  
  if (addressField.value.trim().length < 10) {
    return {
      valid: false,
      message: '地址太短，请输入完整地址'
    };
  }
  
  return { valid: true };
}

async function submitOrder() {
  const validation = validateAddress();
  if (!validation.valid) {
    showToast(validation.message);
    return;
  }
  
  // 提交订单逻辑
  isLoading.value = true;
  try {
    await api.submitOrder({
      ...formFields.value,
      address: addressField.value
    });
    // 跳转成功页
  } catch (error) {
    showToast('提交失败，请重试');
  } finally {
    isLoading.value = false;
  }
}
```

---

## 🎯 通用组件

### Toast 提示

```css
.toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.8);
  color: #FFFFFF;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  z-index: 9999;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

### 按钮状态

```css
.btn {
  height: 48px;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #1E88E5;
  color: #FFFFFF;
}

.btn-primary:hover {
  background: #1565C0;
}

.btn-primary:disabled {
  background: #CCCCCC;
  cursor: not-allowed;
}

.btn-secondary {
  background: #FFFFFF;
  color: #1E88E5;
  border: 1px solid #1E88E5;
}

.btn-secondary:disabled {
  background: #F5F5F5;
  color: #CCCCCC;
  border-color: #CCCCCC;
  cursor: not-allowed;
}
```

---

## 📱 响应式适配

### 断点设置

```css
/* 手机 <768px */
@media (max-width: 767px) {
  .container {
    padding: 0 16px;
  }
}

/* 平板 768px-1024px */
@media (min-width: 768px) and (max-width: 1023px) {
  .container {
    max-width: 768px;
    margin: 0 auto;
    padding: 0 24px;
  }
}

/* 桌面 >1024px */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
    margin: 0 auto;
    padding: 0 32px;
  }
}
```

### 字体适配

```css
html {
  font-size: 16px;
}

/* 小屏幕适配 */
@media (max-width: 374px) {
  html {
    font-size: 14px;
  }
}

/* 大屏幕适配 */
@media (min-width: 414px) {
  html {
    font-size: 18px;
  }
}
```

---

## 🔧 开发注意事项

### 1. 进度条组件复用

```vue
<!-- 所有页面统一使用 ProgressBar 组件 -->
<template>
  <ProgressBar :currentStep="currentStep" />
</template>

<script setup>
const props = defineProps({
  currentStep: {
    type: Number,
    required: true,
    validator: (value) => value >= 1 && value <= 6
  }
});
</script>
```

### 2. 表单校验统一处理

```javascript
// 使用统一的表单校验工具
import { validateForm } from '@/utils/validator';

const errors = validateForm(formFields, validationRules);
if (errors.length > 0) {
  showToast(errors[0].message);
  return;
}
```

### 3. 图片上传限制

```javascript
// 全局常量
export const IMAGE_UPLOAD_CONFIG = {
  MAX_COUNT: 5,
  MIN_COUNT: 1,
  MAX_SIZE: 8 * 1024 * 1024, // 8MB
  ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/jpg']
};
```

### 4. AI 分析进度对接

```javascript
// 实际项目中对接真实 API
async function analyzeImages(images) {
  const response = await api.aiAnalyze({ images });
  
  // 进度回调
  response.onProgress((progress) => {
    updateAiProgress(progress);
  });
  
  return response.result;
}
```

---

## ✅ 验收清单

### 视觉验收

- [ ] 所有页面顶部显示 6 步进度条
- [ ] 进度条状态正确（已完成/进行中/未完成）
- [ ] 色彩符合设计规范
- [ ] 字体大小、字重正确
- [ ] 间距符合 8px 栅格系统
- [ ] 圆角符合规范（4px/8px）

### 交互验收

- [ ] P3 默认显示手动输入模式
- [ ] AI 模式可切换展开/收起
- [ ] AI 加载显示进度条 + 百分比
- [ ] P5 表单仅 2 个字段
- [ ] P6 地址字段必填校验
- [ ] P2 图片上传达到 5 张禁用
- [ ] 所有按钮状态正确（默认/hover/disabled）

### 功能验收

- [ ] 进度条随页面切换更新
- [ ] 表单校验正确
- [ ] 图片上传限制生效
- [ ] AI 分析进度实时更新
- [ ] 预约顾问按钮可点击
- [ ] 订单提交流程正常

---

> **版本**: v2.1  
> **创建时间**: 2026-03-08 18:45  
> **设计师**: 小爱 (xiaoi)  
> **目标读者**: 前端开发工程师  
> **下次更新**: 开发完成后根据实际调整更新
