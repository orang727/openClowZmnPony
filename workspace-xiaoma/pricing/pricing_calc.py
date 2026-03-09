"""
商业产品定价计算器
用于生成环氧地坪等服务类产品的定价Excel表格
"""

import pandas as pd

# ===== 配置区域 =====

# 地面基层处理统一价格
GROUND_PRICE = 7  # 元/㎡

# 产品配置：每个工艺类型的服务项、用量、单价、人工费、最低面积
CONFIGS = {
    '薄涂型': {
        'items': [
            ('地面基层处理', 0.2, 8),
            ('环氧渗透底漆', 0.15, 25),
            ('环氧面漆', 0.4, 30)
        ],
        'labor': 12,    # 人工费(元/㎡)
        'min_area': 67  # 最低施工面积(㎡)
    },
    '砂浆型': {
        'items': [
            ('地面基层处理', 0.2, 8),
            ('环氧渗透底漆', 0.15, 25),
            ('环氧砂浆中涂', 1.0, 28),
            ('环氧面漆', 0.4, 30)
        ],
        'labor': 15,
        'min_area': 54
    },
    '自流平型': {
        'items': [
            ('高强石膏自流平基层', 2.0, 15),
            ('环氧渗透底漆', 0.15, 25),
            ('环氧自流平面漆', 1.2, 35)
        ],
        'labor': 18,
        'min_area': 45
    },
    '彩砂型': {
        'items': [
            ('地面基层处理', 0.2, 8),
            ('环氧彩砂', 1.5, 45),
            ('环氧面漆', 0.5, 30)
        ],
        'labor': 20,
        'min_area': 40
    },
    '停车场': {
        'items': [
            ('地面基层处理', 0.2, 8),
            ('停车场底漆', 0.2, 20),
            ('停车场面漆', 0.5, 25),
            ('划线漆', 0.1, 30)
        ],
        'labor': 15,
        'min_area': 54
    }
}


def calculate_price(configs):
    """计算定价"""
    data1 = []  # 服务项定价
    data2 = []  # 材料用量组成
    data3 = []  # 施工费组成
    
    for tech, config in configs.items():
        items = config['items']
        labor = config['labor']
        min_area = config['min_area']
        
        # 计算材料成本（不含地面基层处理）
        mat_per_sqm = sum(d * p for _, d, p in items if d > 0 and '基层' not in _)
        
        # 售价 = (材料 + 人工) / 0.73
        price = round((mat_per_sqm + labor) / 0.73, 0)
        
        # 毛利率
        gross_rate = round((price - mat_per_sqm - labor) / price * 100, 1)
        
        # 净利率锁定8%
        net_rate = 8.0
        
        # 施工费按服务项数量分摊
        labor_per_item = labor / len(items)
        
        for i, (name, d, p) in enumerate(items):
            # 材料费
            if '基层' in name:
                item_price = GROUND_PRICE
                mc = 0
            else:
                mc = d * p if d > 0 else 0
                item_price = round((d * p) / mat_per_sqm * price, 0) if d > 0 else 0
            
            # 施工费分摊
            labor_cost = labor_per_item
            
            data1.append({
                '后台产品': tech + '环氧地坪',
                '服务项名称': name,
                '服务项单价(元/㎡)': item_price,
                '材料费(元/㎡)': mc,
                '施工费(元/㎡)': round(labor_cost, 2),
                '预估毛利(%)': f'{gross_rate}%',
                '预估净利(%)': f'{net_rate}%',
                '备注(起售面积)': f'{min_area}㎡起'
            })
            
            # 材料用量组成
            if d > 0:
                data2.append({
                    '后台产品': tech + '环氧地坪',
                    '服务项': name,
                    '材料名称': name,
                    '用量(kg/㎡)': d,
                    '单价(元/kg)': p,
                    '材料成本(元/㎡)': round(d * p, 2)
                })
        
        # 施工费组成
        data3.append({
            '后台产品': tech + '环氧地坪',
            '人工费(元/㎡)': labor,
            '最小施工面积(㎡)': min_area,
            '最低施工费(元)': min_area * labor,
            '施工人数': 2,
            '施工天数': 1,
            '人工成本(元/人/天)': 400,
            '备注': '2人1天上门'
        })
    
    return pd.DataFrame(data1), pd.DataFrame(data2), pd.DataFrame(data3)


def save_to_excel(filename='环氧地坪定价.xlsx'):
    """保存到Excel"""
    df1, df2, df3 = calculate_price(CONFIGS)
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='服务项定价', index=False)
        df2.to_excel(writer, sheet_name='材料用量组成', index=False)
        df3.to_excel(writer, sheet_name='施工费组成', index=False)
    
    print(f'已保存到: {filename}')


if __name__ == '__main__':
    save_to_excel()
