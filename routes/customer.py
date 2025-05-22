from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db, ParkingSpot, Booking
from datetime import datetime
from typing import Dict, Optional
import logging

customer_bp = Blueprint('customer', __name__)

def get_booking_data(booking_number: str) -> Optional[Dict]:
    """獲取預訂資料"""
    try:
        booking = Booking.query.filter_by(number=booking_number).first()
        if not booking:
            return None
        return {
            'phone': booking.phone,
            'spot_number': booking.spot.number,
            'time': booking.time,
            'state': booking.state
        }
    except Exception as e:
        current_app.logger.error(f"Error getting booking data: {str(e)}")
        return None

@customer_bp.route('/')
def index():
    """首頁"""
    return render_template('customer/index.html')

@customer_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    """預訂停車位"""
    if request.method == 'POST':
        try:
            phone = request.form.get('phone')
            spot_number = request.form.get('spot_number')

            if not phone or not spot_number:
                flash('請填寫所有必要資訊', 'error')
                return redirect(url_for('customer.book'))

            spot = ParkingSpot.query.filter_by(number=spot_number).first()
            if not spot or spot.state != '0':
                flash('該停車位不可預訂', 'error')
                return redirect(url_for('customer.book'))

            booking = Booking(
                phone=phone,
                spot_id=spot.id,
                number=f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
                time=datetime.now(),
                state='1'
            )

            spot.state = '1'
            db.session.add(booking)
            db.session.commit()

            flash('預訂成功！', 'success')
            return redirect(url_for('customer.booking_success', booking_number=booking.number))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Booking error: {str(e)}")
            flash('預訂失敗，請稍後再試', 'error')
            return redirect(url_for('customer.book'))

    available_spots = ParkingSpot.query.filter_by(state='0').all()
    return render_template('customer/book.html', spots=available_spots)

@customer_bp.route('/booking/<booking_number>')
@login_required
def booking_success(booking_number):
    """預訂成功頁面"""
    booking_data = get_booking_data(booking_number)
    if not booking_data:
        flash('找不到預訂資料', 'error')
        return redirect(url_for('customer.index'))
    return render_template('customer/booking_success.html', booking=booking_data)

@customer_bp.route('/payment/<booking_number>', methods=['GET', 'POST'])
@login_required
def payment(booking_number):
    """付款頁面"""
    booking = Booking.query.filter_by(number=booking_number).first()
    if not booking:
        flash('找不到預訂資料', 'error')
        return redirect(url_for('customer.index'))

    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            if amount < booking.compute_fee():
                flash('付款金額不足', 'error')
                return redirect(url_for('customer.payment', booking_number=booking_number))

            booking.state = '3'  # 已付款
            booking.spot.state = '0'  # 釋放停車位
            db.session.commit()

            flash('付款成功！', 'success')
            return redirect(url_for('customer.payment_success', booking_number=booking_number))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Payment error: {str(e)}")
            flash('付款失敗，請稍後再試', 'error')
            return redirect(url_for('customer.payment', booking_number=booking_number))

    return render_template('customer/payment.html',
                         booking=booking,
                         fee=booking.compute_fee())

@customer_bp.route('/payment/success/<booking_number>')
@login_required
def payment_success(booking_number):
    """付款成功頁面"""
    booking_data = get_booking_data(booking_number)
    if not booking_data:
        flash('找不到預訂資料', 'error')
        return redirect(url_for('customer.index'))
    return render_template('customer/payment_success.html', booking=booking_data)

@customer_bp.route('/search')
@login_required
def search():
    """搜尋預訂"""
    booking_number = request.args.get('booking_number')
    if not booking_number:
        return render_template('customer/search.html')

    booking_data = get_booking_data(booking_number)
    if not booking_data:
        flash('找不到預訂資料', 'error')
        return render_template('customer/search.html')

    return render_template('customer/search.html', booking=booking_data)