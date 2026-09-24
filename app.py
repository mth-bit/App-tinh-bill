import streamlit as st
from datetime import datetime

# ==============================
# CẤU HÌNH APP
# ==============================
st.set_page_config(
    page_title="Restaurant Bill",
    page_icon="🍽️",
    layout="wide"
)

# ==============================
# MENU NHÀ HÀNG
# ==============================
MENU = {
    "🍜 Mì Ý Bò Bằm": 65000,
    "🍗 Gà Rán": 55000,
    "🍔 Hamburger": 60000,
    "🍕 Pizza Hải Sản": 120000,
    "🍚 Cơm Chiên Dương Châu": 50000,
    "🥩 Bò Lúc Lắc": 95000,
    "🍟 Khoai Tây Chiên": 35000,
    "🥗 Salad": 40000,
    "🥤 Coca Cola": 15000,
    "🧋 Trà Sữa": 30000,
    "☕ Cà Phê": 25000,
    "🍊 Nước Cam": 30000,
}

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("🍽️ RESTAURANT BILL")
st.caption("Ứng dụng tính tiền nhà hàng")

st.divider()

# ==============================
# THÔNG TIN KHÁCH HÀNG
# ==============================
col1, col2 = st.columns(2)

with col1:
    customer = st.text_input(
        "👤 Tên khách hàng",
        placeholder="Nhập tên khách hàng..."
    )

with col2:
    table = st.text_input(
        "🪑 Số bàn",
        placeholder="Ví dụ: Bàn 05"
    )

st.divider()

# ==============================
# CHỌN MÓN
# ==============================
st.subheader("🍴 Chọn món")

selected_items = []

cols = st.columns(3)

for index, (food, price) in enumerate(MENU.items()):

    with cols[index % 3]:

        st.markdown(f"### {food}")
        st.write(f"**{price:,.0f} VNĐ**")

        quantity = st.number_input(
            f"Số lượng",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key=f"quantity_{index}"
        )

        if quantity > 0:
            selected_items.append({
                "name": food,
                "price": price,
                "quantity": quantity,
                "total": price * quantity
            })

st.divider()

# ==============================
# TÍNH BILL
# ==============================
st.subheader("🧾 HÓA ĐƠN")

if not selected_items:

    st.info("Chưa có món nào được chọn.")

else:

    subtotal = sum(
        item["total"]
        for item in selected_items
    )

    # ==============================
    # GIẢM GIÁ
    # ==============================
    discount_percent = st.selectbox(
        "🎁 Mức giảm giá",
        [0, 5, 10, 15, 20]
    )

    discount = subtotal * discount_percent / 100

    after_discount = subtotal - discount

    # ==============================
    # VAT
    # ==============================
    vat_percent = 10

    vat = after_discount * vat_percent / 100

    total = after_discount + vat

    # ==============================
    # HIỂN THỊ BILL
    # ==============================

    st.markdown("### 📋 Chi tiết đơn hàng")

    for item in selected_items:

        col1, col2, col3, col4 = st.columns(
            [4, 2, 1, 2]
        )

        with col1:
            st.write(item["name"])

        with col2:
            st.write(
                f"{item['price']:,.0f} VNĐ"
            )

        with col3:
            st.write(item["quantity"])

        with col4:
            st.write(
                f"{item['total']:,.0f} VNĐ"
            )

    st.divider()

    # ==============================
    # TỔNG TIỀN
    # ==============================

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("Tạm tính:")
        st.write(f"Giảm giá ({discount_percent}%):")
        st.write(f"VAT ({vat_percent}%):")

        st.markdown("### 💰 TỔNG THANH TOÁN")

    with col2:
        st.write(f"{subtotal:,.0f} VNĐ")
        st.write(f"- {discount:,.0f} VNĐ")
        st.write(f"{vat:,.0f} VNĐ")

        st.markdown(
            f"### {total:,.0f} VNĐ"
        )

    st.divider()

    # ==============================
    # PHƯƠNG THỨC THANH TOÁN
    # ==============================

    payment = st.radio(
        "💳 Phương thức thanh toán",
        [
            "Tiền mặt",
            "Chuyển khoản",
            "Thẻ ngân hàng",
            "Ví điện tử"
        ],
        horizontal=True
    )

    st.divider()

    # ==============================
    # XUẤT HÓA ĐƠN
    # ==============================

    invoice = f"""
========================================
           RESTAURANT BILL
========================================

Khách hàng: {customer if customer else "Khách lẻ"}
Số bàn: {table if table else "Không xác định"}
Thời gian: {datetime.now().strftime("%d/%m/%Y %H:%M")}

----------------------------------------
MÓN ĂN
----------------------------------------
"""

    for item in selected_items:
        invoice += (
            f"{item['name']}\n"
            f"  {item['price']:,.0f} x "
            f"{item['quantity']} = "
            f"{item['total']:,.0f} VNĐ\n"
        )

    invoice += f"""
----------------------------------------
Tạm tính:       {subtotal:,.0f} VNĐ
Giảm giá:       -{discount:,.0f} VNĐ
VAT:             {vat:,.0f} VNĐ
----------------------------------------
TỔNG CỘNG:      {total:,.0f} VNĐ

Thanh toán: {payment}

========================================
       CẢM ƠN QUÝ KHÁCH!
========================================
"""

    st.download_button(
        label="📥 Tải hóa đơn",
        data=invoice,
        file_name="restaurant_bill.txt",
        mime="text/plain"
    )

    st.success(
        f"✅ Thanh toán thành công: "
        f"{total:,.0f} VNĐ"
    )
