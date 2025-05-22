from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
import logging
from flask import current_app
import re

def get_current_time() -> datetime:
    """獲取當前時間（考慮時區）"""
    return datetime.now(timezone(timedelta(hours=8)))

def format_datetime(dt: datetime) -> str:
    """格式化日期時間"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def validate_phone(phone: str) -> bool:
    """驗證手機號碼格式"""
    pattern = r'^09\d{8}$'
    return bool(re.match(pattern, phone))

def validate_booking_number(number: str) -> bool:
    """驗證預訂編號格式"""
    pattern = r'^BK\d{14}$'
    return bool(re.match(pattern, number))

def compute_parking_fee(start_time: datetime, end_time: Optional[datetime] = None) -> float:
    """計算停車費用"""
    if end_time is None:
        end_time = get_current_time()

    # 計算停車時數（向上取整）
    hours = (end_time - start_time).total_seconds() / 3600
    hours = int(hours) + (1 if hours % 1 > 0 else 0)

    # 獲取每小時費率
    rate = current_app.config.get('PARKING_RATE', 30)

    return hours * rate

def log_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """記錄錯誤日誌"""
    error_msg = f"Error: {str(error)}"
    if context:
        error_msg += f" Context: {context}"
    current_app.logger.error(error_msg)

def format_currency(amount: float) -> str:
    """格式化金額"""
    return f"${amount:,.2f}"

def get_booking_state_text(state: str) -> str:
    """獲取預訂狀態文字描述"""
    states = {
        '0': '已取消',
        '1': '預訂中',
        '2': '使用中',
        '3': '已完成',
        '4': '已取消'
    }
    return states.get(state, '未知狀態')

def get_spot_state_text(state: str) -> str:
    """獲取停車位狀態文字描述"""
    states = {
        '0': '空閒',
        '1': '已預訂',
        '2': '使用中',
        '3': '維護中'
    }
    return states.get(state, '未知狀態')

def validate_admin_password(password: str) -> bool:
    """驗證管理員密碼強度"""
    if len(password) < 8:
        return False

    # 檢查是否包含數字
    if not re.search(r'\d', password):
        return False

    # 檢查是否包含大寫字母
    if not re.search(r'[A-Z]', password):
        return False

    # 檢查是否包含小寫字母
    if not re.search(r'[a-z]', password):
        return False

    # 檢查是否包含特殊字符
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True

def sanitize_input(text: str) -> str:
    """清理輸入文字"""
    # 移除 HTML 標籤
    text = re.sub(r'<[^>]+>', '', text)
    # 移除特殊字符
    text = re.sub(r'[^\w\s-]', '', text)
    return text.strip()

def generate_booking_number() -> str:
    """生成預訂編號"""
    return f"BK{get_current_time().strftime('%Y%m%d%H%M%S')}"