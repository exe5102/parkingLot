from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db, ParkingSpot, Booking, User
from datetime import datetime
from typing import List, Dict
import logging

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """管理員權限檢查裝飾器"""
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('需要管理員權限', 'error')
            return redirect(url_for('customer.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """管理員儀表板"""
    try:
        total_spots = ParkingSpot.query.count()
        available_spots = ParkingSpot.query.filter_by(state='0').count()
        active_bookings = Booking.query.filter_by(state='1').count()
        completed_bookings = Booking.query.filter_by(state='3').count()

        return render_template('admin/dashboard.html',
                             total_spots=total_spots,
                             available_spots=available_spots,
                             active_bookings=active_bookings,
                             completed_bookings=completed_bookings)
    except Exception as e:
        current_app.logger.error(f"Dashboard error: {str(e)}")
        flash('載入儀表板失敗', 'error')
        return redirect(url_for('customer.index'))

@admin_bp.route('/spots')
@admin_required
def manage_spots():
    """管理停車位"""
    try:
        spots = ParkingSpot.query.all()
        return render_template('admin/spots.html', spots=spots)
    except Exception as e:
        current_app.logger.error(f"Manage spots error: {str(e)}")
        flash('載入停車位資料失敗', 'error')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/spots/<int:spot_id>/toggle', methods=['POST'])
@admin_required
def toggle_spot(spot_id):
    """切換停車位狀態"""
    try:
        spot = ParkingSpot.query.get_or_404(spot_id)
        spot.state = '0' if spot.state == '1' else '1'
        db.session.commit()
        flash('停車位狀態已更新', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Toggle spot error: {str(e)}")
        flash('更新停車位狀態失敗', 'error')
    return redirect(url_for('admin.manage_spots'))

@admin_bp.route('/bookings')
@admin_required
def manage_bookings():
    """管理預訂"""
    try:
        bookings = Booking.query.order_by(Booking.time.desc()).all()
        return render_template('admin/bookings.html', bookings=bookings)
    except Exception as e:
        current_app.logger.error(f"Manage bookings error: {str(e)}")
        flash('載入預訂資料失敗', 'error')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/bookings/<booking_number>/cancel', methods=['POST'])
@admin_required
def cancel_booking(booking_number):
    """取消預訂"""
    try:
        booking = Booking.query.filter_by(number=booking_number).first_or_404()
        if booking.state == '1':  # 只有未完成的預訂可以取消
            booking.state = '4'  # 已取消
            booking.spot.state = '0'  # 釋放停車位
            db.session.commit()
            flash('預訂已取消', 'success')
        else:
            flash('無法取消此預訂', 'error')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Cancel booking error: {str(e)}")
        flash('取消預訂失敗', 'error')
    return redirect(url_for('admin.manage_bookings'))

@admin_bp.route('/users')
@admin_required
def manage_users():
    """管理用戶"""
    try:
        users = User.query.all()
        return render_template('admin/users.html', users=users)
    except Exception as e:
        current_app.logger.error(f"Manage users error: {str(e)}")
        flash('載入用戶資料失敗', 'error')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    """切換管理員權限"""
    try:
        if user_id == current_user.id:
            flash('無法修改自己的權限', 'error')
            return redirect(url_for('admin.manage_users'))

        user = User.query.get_or_404(user_id)
        user.is_admin = not user.is_admin
        db.session.commit()
        flash('用戶權限已更新', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Toggle admin error: {str(e)}")
        flash('更新用戶權限失敗', 'error')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/reports')
@admin_required
def reports():
    """報表頁面"""
    try:
        # 獲取今日預訂統計
        today = datetime.now().date()
        today_bookings = Booking.query.filter(
            db.func.date(Booking.time) == today
        ).all()

        # 計算收入
        total_income = sum(booking.compute_fee() for booking in today_bookings if booking.state == '3')

        # 獲取熱門停車位
        popular_spots = db.session.query(
            ParkingSpot.number,
            db.func.count(Booking.id)
        ).join(Booking).group_by(ParkingSpot.number).order_by(
            db.func.count(Booking.id).desc()
        ).limit(5).all()

        return render_template('admin/reports.html',
                             today_bookings=len(today_bookings),
                             total_income=total_income,
                             popular_spots=popular_spots)
    except Exception as e:
        current_app.logger.error(f"Reports error: {str(e)}")
        flash('載入報表失敗', 'error')
        return redirect(url_for('admin.dashboard'))