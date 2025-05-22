from database import *# from datetime import datetime,timezone,timedelta,datetime
import datetime
import serial
from time import sleep
import sys
from typing import Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum

# 時區設定
TZ_OFFSET = datetime.timezone(datetime.timedelta(hours=8))
today = datetime.datetime.now(tz=TZ_OFFSET)
dtoday = datetime.datetime.strptime(today.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

# 常數定義
SERIAL_PORT = 'COM5'
BAUD_RATE = 9600
TIMEOUT_SECONDS = 900  # 15分鐘
PRICE_PER_HOUR = 20
PRICE_PER_HALF_HOUR = 10
MAX_DAILY_PRICE = 100
INITIAL_PRICE = 10

# 停車位狀態枚舉
class ParkingState(Enum):
    AVAILABLE = '0'
    RESERVED = '1'
    OCCUPIED = '2'
    MAINTENANCE = '3'
    DISABLED = '4'

# 停車位狀態管理類別
@dataclass
class ParkingSpot:
    number: str
    state: ParkingState

class ParkingSystem:
    def __init__(self):
        self.serial_port = None
        self.parking_states: Dict[str, str] = {'1': '0', '2': '0', '3': '0', '4': '0'}
        self._initialize_serial()

    def _initialize_serial(self) -> None:
        """初始化序列埠連接"""
        try:
            self.serial_port = serial.Serial(SERIAL_PORT, BAUD_RATE)
        except serial.SerialException as e:
            print(f"序列埠初始化失敗: {e}")
            self.serial_port = None

    def control_arduino(self, spot_number: str) -> bool:
        """控制 Arduino 閘門"""
        if not self.serial_port:
            print("序列埠未初始化")
            return False

        try:
            command = f"{spot_number}\n".encode()
            self.serial_port.write(command)
            sleep(0.5)

            while self.serial_port.in_waiting:
                feedback = self.serial_port.readline().decode().strip()
                print(f'控制板回應：{feedback}')
            return True
        except Exception as e:
            print(f"Arduino 控制失敗: {e}")
            return False
        finally:
            if self.serial_port:
                self.serial_port.close()

    def get_current_time(self) -> str:
        """獲取當前時間字串"""
        return today.strftime("%Y-%m-%d %H:%M:%S")

    def calculate_fee(self, unumber: str) -> int:
        """計算停車費用"""
        try:
            booking_data = ClientSearch(unumber)
            if not booking_data or booking_data[4] != ParkingState.OCCUPIED.value:
                return INITIAL_PRICE

            entry_time = datetime.datetime.strptime(booking_data[3], '%Y-%m-%d %H:%M:%S')
            time_diff = dtoday - entry_time

            if time_diff.days == 0:
                return INITIAL_PRICE + int(time_diff.seconds / 1800) * PRICE_PER_HALF_HOUR

            current_hourly_cost = dtoday.hour * PRICE_PER_HOUR + int(dtoday.minute / 30) * PRICE_PER_HALF_HOUR
            if current_hourly_cost > MAX_DAILY_PRICE:
                return (time_diff.days + 1) * MAX_DAILY_PRICE

            return (INITIAL_PRICE +
                   (time_diff.days * MAX_DAILY_PRICE) +
                   (dtoday.hour * PRICE_PER_HOUR) +
                   (int(dtoday.minute / 30) * PRICE_PER_HALF_HOUR))
        except Exception as e:
            print(f"費用計算錯誤: {e}")
            return INITIAL_PRICE

    def check_parking_states(self) -> None:
        """檢查並更新停車位狀態"""
        try:
            bookings = SearchAll()
            if not bookings:
                return

            for booking in bookings:
                if booking[4] == ParkingState.RESERVED.value:
                    booking_time = datetime.datetime.strptime(booking[3], '%Y-%m-%d %H:%M:%S')
                    time_diff = dtoday - booking_time

                    if time_diff.seconds > TIMEOUT_SECONDS:
                        RecordLogin(booking[0], booking[1], booking[2], None, None, None, '未報到')
                        AdminDelete(booking[2])
        except Exception as e:
            print(f"狀態檢查錯誤: {e}")

    def load_parking_states(self) -> Dict[str, str]:
        """載入停車位狀態"""
        try:
            bookings = SearchAll()
            if bookings:
                for booking in bookings:
                    self.parking_states[booking[1]] = booking[4]
            return self.parking_states
        except Exception as e:
            print(f"狀態載入錯誤: {e}")
            return self.parking_states

    def reset_parking_state(self, spot_number: str) -> None:
        """重置停車位狀態"""
        self.parking_states[spot_number] = ParkingState.AVAILABLE.value

    def change_parking_state(self, spot_number: str, new_state: str) -> None:
        """更改停車位狀態"""
        if new_state in [state.value for state in ParkingState]:
            self.parking_states[spot_number] = new_state

# 建立全域停車系統實例
parking_system = ParkingSystem()


def arduino(choice: str) -> None:
    parking_system.control_arduino(choice)

def DateControl() -> str:
    return parking_system.get_current_time()

def Compute(unumber: str) -> int:
    return parking_system.calculate_fee(unumber)

def Statechenk() -> None:
    parking_system.check_parking_states()

def Stateload() -> Dict[str, str]:
    return parking_system.load_parking_states()

def StateReset(pnumber: str) -> None:
    parking_system.reset_parking_state(pnumber)

def statechanage(pnumber: str, state: str) -> None:
    parking_system.change_parking_state(pnumber, state)

# 全域變數
BKstate = parking_system.parking_states
