import streamlit as st
import json
import os
from utils.helpers import format_rupiah, hitung_total_belanja, format_ukuran
import time
from datetime import datetime
import streamlit.components.v1 as components 

# Konfigurasi page
st.set_page_config(
    page_title="SepatuKu Store",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data sepatu
@st.cache_data
def load_sepatu_data():
    try:
        with open('data/sepatu_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("File data/sepatu_data.json tidak ditemukan!")
        return []

# Initialize session state
def init_session_state():
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'selected_shoe' not in st.session_state:
        st.session_state.selected_shoe = None
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'sort_option' not in st.session_state:
        st.session_state.sort_option = "Sort by"
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'users' not in st.session_state:
        st.session_state.users = {}  # Simple user storage
    if 'checkout_data' not in st.session_state:
        st.session_state.checkout_data = {}
    if 'order_history' not in st.session_state:
        st.session_state.order_history = []

def show_snackbar(message, type="success"):
    """Show snackbar notification"""
    if type == "success":
        st.success(message)
    else:
        st.error(message)
    time.sleep(2)
    st.rerun()

def navigate_to(page, shoe_id=None):
    """Navigasi ke halaman tertentu"""
    st.session_state.current_page = page
    if shoe_id:
        st.session_state.selected_shoe = shoe_id
    st.rerun()

def add_to_cart(sepatu, ukuran):
    """Tambah item ke keranjang"""
    item = {
        'id': sepatu['id'],
        'nama': sepatu['nama'],
        'ukuran': ukuran,
        'harga': sepatu['harga'],
        'quantity': 1
    }
    
    existing_item = None
    for cart_item in st.session_state.cart:
        if cart_item['id'] == item['id'] and cart_item['ukuran'] == ukuran:
            existing_item = cart_item
            break
    
    if existing_item:
        existing_item['quantity'] += 1
    else:
        st.session_state.cart.append(item)

def toggle_favorite(shoe_id):
    """Toggle favorit sepatu"""
    if shoe_id in st.session_state.favorites:
        st.session_state.favorites.remove(shoe_id)
    else:
        st.session_state.favorites.append(shoe_id)

def get_shoe_by_id(sepatu_data, shoe_id):
    """Ambil data sepatu berdasarkan ID"""
    for sepatu in sepatu_data:
        if sepatu['id'] == shoe_id:
            return sepatu
    return None

def filter_and_sort_shoes(sepatu_data, search_query, sort_option):
    """Filter dan sort sepatu berdasarkan pencarian dan sorting"""
    filtered_shoes = []
    if search_query:
        for sepatu in sepatu_data:
            if search_query.lower() in sepatu['nama'].lower() or search_query.lower() in sepatu['bahan'].lower():
                filtered_shoes.append(sepatu)
    else:
        filtered_shoes = sepatu_data.copy()
    
    if sort_option == "Nama A-Z":
        filtered_shoes.sort(key=lambda x: x['nama'].lower())
    elif sort_option == "Nama Z-A":
        filtered_shoes.sort(key=lambda x: x['nama'].lower(), reverse=True)
    elif sort_option == "Harga Terendah":
        filtered_shoes.sort(key=lambda x: x['harga'])
    elif sort_option == "Harga Tertinggi":
        filtered_shoes.sort(key=lambda x: x['harga'], reverse=True)
    
    return filtered_shoes

def generate_order_id():
    """Generate unique order ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"ORD-{timestamp}"

def render_login_page():
    """Render halaman login"""
    
    with st.form("login_form", clear_on_submit=False):
        st.markdown("**Username**")
        username = st.text_input("", placeholder="masukkan username", key="login_username", label_visibility="collapsed")
        
        st.markdown("**Password**")
        password = st.text_input("", placeholder="masukkan password", type="password", key="login_password", label_visibility="collapsed")
        
        login_button = st.form_submit_button("Masuk", use_container_width=True)
        
        if login_button:
            if username and password:
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.is_logged_in = True
                    st.session_state.username = username
                    st.session_state.current_page = 'home'
                    show_snackbar("✅ Berhasil masuk!", "success")
                else:
                    show_snackbar("❌ Username atau password salah!", "error")
            else:
                show_snackbar("❌ Mohon lengkapi semua data!", "error")
    
    st.markdown("""
    <div class="auth-footer">
        <span>Belum punya akun? </span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Daftar", key="goto_register"):
        navigate_to('register')

def render_register_page():
    """Render halaman register"""
    
    with st.form("register_form", clear_on_submit=False):
        st.markdown("**Username**")
        username = st.text_input("", placeholder="masukkan username", key="register_username", label_visibility="collapsed")
        
        st.markdown("**Password**")
        password = st.text_input("", placeholder="masukkan password", type="password", key="register_password", label_visibility="collapsed")
        
        register_button = st.form_submit_button("Daftar", use_container_width=True)
        
        if register_button:
            if username and password:
                if username not in st.session_state.users:
                    st.session_state.users[username] = password
                    show_snackbar("✅ Berhasil daftar! Silakan masuk.", "success")
                    navigate_to('login')
                else:
                    show_snackbar("❌ Username sudah digunakan!", "error")
            else:
                show_snackbar("❌ Mohon lengkapi semua data!", "error")
    
    st.markdown("""
    <div class="auth-footer">
        <span>Sudah punya akun? </span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Masuk", key="goto_login"):
        navigate_to('login')

def render_app_bar():
    """Render app bar dengan navigasi"""
    st.markdown("""
    <div class="app-bar">
        <div class="app-bar-content">
            <div class="app-title">👟 SepatuKu</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation controls
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍", placeholder="Cari sepatu...", 
                                   value=st.session_state.search_query, 
                                   key="search_input", label_visibility="collapsed")
        if search_query != st.session_state.search_query:
            st.session_state.search_query = search_query
            st.rerun()
    
    with col2:
        sort_options = ["Sort by", "Nama A-Z", "Nama Z-A", "Harga Terendah", "Harga Tertinggi"]
        sort_option = st.selectbox("Filter", sort_options, 
                                 index=sort_options.index(st.session_state.sort_option),
                                 key="sort_select", label_visibility="collapsed")
        if sort_option != st.session_state.sort_option:
            st.session_state.sort_option = sort_option
            st.rerun()
    
    with col3:
        if st.button("🏠 Beranda", key="nav_home"):
            navigate_to('home')
    
    with col4:
        fav_count = len(st.session_state.favorites)
        fav_text = f"❤️ Favorit" 
        if st.button(fav_text, key="nav_favorites"):
            navigate_to('favorites')
    
    with col5:
        cart_count = len(st.session_state.cart)
        cart_text = f"🛒 Keranjang" 
        if st.button(cart_text, key="nav_cart"):
            navigate_to('cart')


def render_home_page(sepatu_data):
    """Render halaman utama dengan promo banner dan grid layout"""
    # Promo Banner
    st.markdown("""
    <div class="promo-banner">
        <div class="promo-content">
            <div class="promo-discount">50%</div>
            <div class="promo-text">
                <h3>Upgrade Gayamu Mulai dari Kaki</h3>
                <p>Promo Gila Akhir Pekan!</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Sepatu Populer")
    
    # Filter dan sort sepatu
    filtered_shoes = filter_and_sort_shoes(sepatu_data, st.session_state.search_query, st.session_state.sort_option)
    
    if not filtered_shoes:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔍</div>
            <h3>Tidak Ada Sepatu Ditemukan</h3>
            <p>Coba ubah kata kunci pencarian atau filter Anda</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Grid layout - 3 columns
    cols = st.columns(3)
    
    for idx, sepatu in enumerate(filtered_shoes):
        col_idx = idx % 3
        
        with cols[col_idx]:
            # Product card dengan styling baru
            st.markdown(f"""
            <div class="product-card-home">
                <img src="{sepatu['gambar']}" class="product-image-home" alt="{sepatu['nama']}">
                <div class="product-info-home">
                    <div class="product-name-home">{sepatu['nama']}</div>
                    <div class="product-price-home">{format_rupiah(sepatu['harga'])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            btn_col1, btn_col2 = st.columns([1, 1])
            
            with btn_col1:
                if st.button("Lihat", key=f"view_{sepatu['id']}", help="Lihat detail"):
                    navigate_to('detail', sepatu['id'])

def render_detail_page(sepatu_data):
    """Render halaman detail sepatu dengan styling baru"""
    if not st.session_state.selected_shoe:
        st.error("Sepatu tidak ditemukan!")
        return
    
    sepatu = get_shoe_by_id(sepatu_data, st.session_state.selected_shoe)
    if not sepatu:
        st.error("Data sepatu tidak ditemukan!")
        return
    
    # Detail card layout sesuai mockup
    st.markdown(f"""
    <div class="detail-card-new">
        <div class="detail-image-section">
            <img src="{sepatu['gambar']}" class="detail-image-new" alt="{sepatu['nama']}">
        </div>
        <div class="detail-info-section">
            <h2 class="detail-name-new">{sepatu['nama']}</h2>
            <div class="detail-price-new">{format_rupiah(sepatu['harga'])}</div>
    """, unsafe_allow_html=True)
    
    # Size selection buttons
    selected_size = st.session_state.get('selected_size', sepatu['ukuran'][0])
    
    size_cols = st.columns(len(sepatu['ukuran']))
    for idx, ukuran in enumerate(sepatu['ukuran']):
        with size_cols[idx]:
            if st.button(f"{ukuran}", key=f"size_{ukuran}_{sepatu['id']}"):
                st.session_state.selected_size = ukuran
                st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🛒 Tambah ke keranjang", key=f"add_cart_{sepatu['id']}", use_container_width=True):
            add_to_cart(sepatu, selected_size)
            st.success(f"✅ {sepatu['nama']} ukuran {selected_size} ditambahkan ke keranjang!")
    
    with col2:
        is_favorite = sepatu['id'] in st.session_state.favorites
        fav_text = "💖 Favorit" if is_favorite else "🤍 Favorit"
        if st.button(fav_text, key=f"fav_detail_{sepatu['id']}", use_container_width=True):
            toggle_favorite(sepatu['id'])
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Back button
    if st.button("← Kembali", key="back_home"):
        navigate_to('home')

def render_favorites_page(sepatu_data):
    """Render halaman favorit"""
    st.markdown("## ❤️ Daftar Favorit")
    
    if not st.session_state.favorites:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">❤️</div>
            <h3>Daftar Favorit Masih Kosong</h3>
            <p>Tambahkan sepatu favorit Anda dengan menekan tombol love!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    favorite_shoes = [shoe for shoe in sepatu_data if shoe['id'] in st.session_state.favorites]
    
    cols = st.columns(3)
    
    for idx, sepatu in enumerate(favorite_shoes):
        col_idx = idx % 3
        
        with cols[col_idx]:
            st.markdown(f"""
            <div class="product-card-home">
                <img src="{sepatu['gambar']}" class="product-image-home" alt="{sepatu['nama']}">
                <div class="product-info-home">
                    <div class="product-name-home">{sepatu['nama']}</div>
                    <div class="product-price-home">{format_rupiah(sepatu['harga'])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns([1, 1])
            
            with btn_col1:
                if st.button("Lihat", key=f"fav_detail_{sepatu['id']}", help="Lihat detail"):
                    navigate_to('detail', sepatu['id']) 

def render_cart_page():
    """Render halaman keranjang"""
    st.markdown("## 🛒 Keranjang Belanja")
    
    if not st.session_state.cart:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🛒</div>
            <h3>Keranjang Belanja Kosong</h3>
            <p>Silakan pilih sepatu untuk dibeli dari halaman utama!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for i, item in enumerate(st.session_state.cart):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="cart-item-detail">
                <strong>{item['nama']}</strong><br>
                Ukuran: {item['ukuran']}<br>
                Harga: {format_rupiah(item['harga'])}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**Qty:** {item['quantity']}")
            st.markdown(f"**Total:** {format_rupiah(item['harga'] * item['quantity'])}")
        
        with col3:
            if st.button("🗑️", key=f"remove_cart_{i}", help="Hapus dari keranjang"):
                st.session_state.cart.pop(i)
                st.rerun()
        
        st.markdown("---")
    
    total_harga = hitung_total_belanja(st.session_state.cart)
    st.markdown(f"""
    <div class="total-price">
        <strong>Total Pembayaran: {format_rupiah(total_harga)}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💳 Checkout Sekarang", key="checkout_now"):
        navigate_to('checkout')

def render_checkout_page():
    """Render halaman checkout dan pembayaran"""
    st.markdown("## 💳 Checkout & Pembayaran")
    
    if not st.session_state.cart:
        st.error("Keranjang belanja kosong!")
        if st.button("← Kembali ke Beranda"):
            navigate_to('home')
        return
    
    # Ringkasan pesanan
    st.markdown("### 📋 Ringkasan Pesanan")
    
    total_harga = hitung_total_belanja(st.session_state.cart)
    
    st.markdown(f"""
    <div class="order-summary">
        <h4>Items dalam keranjang:</h4>
    """, unsafe_allow_html=True)
    
    for item in st.session_state.cart:
        st.markdown(f"""
        <div class="checkout-item">
            <span><strong>{item['nama']}</strong> (Ukuran: {item['ukuran']})</span>
            <span>{item['quantity']} x {format_rupiah(item['harga'])} = {format_rupiah(item['harga'] * item['quantity'])}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="checkout-total">
            <strong>Total: {format_rupiah(total_harga)}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Form pembayaran
    st.markdown("### 📝 Informasi Pembayaran")
    
    with st.form("checkout_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Nama Lengkap**")
            nama = st.text_input("", placeholder="Masukkan nama lengkap", key="checkout_nama", label_visibility="collapsed")
            
            st.markdown("**Nomor Telepon**")
            telepon = st.text_input("", placeholder="Masukkan nomor telepon", key="checkout_telepon", label_visibility="collapsed")
        
        with col2:
            st.markdown("**Alamat Lengkap**")
            alamat = st.text_area("", placeholder="Masukkan alamat lengkap", key="checkout_alamat", label_visibility="collapsed", height=100)
            
            st.markdown("**Pilih Bank**")
            bank_options = ["Pilih Bank", "Bank BCA", "Bank Mandiri", "Bank BRI"]
            bank = st.selectbox("", bank_options, key="checkout_bank", label_visibility="collapsed")
        
        st.markdown("**Kode Bank**")
        kode_bank = st.text_input("", placeholder="Masukkan kode bank", key="checkout_kode_bank", label_visibility="collapsed")
        
        submit_button = st.form_submit_button("🔒 Proses Pembayaran", use_container_width=True)
        
        if submit_button:
            if nama and telepon and alamat and bank != "Pilih Bank" and kode_bank:
                # Simpan data checkout
                order_id = generate_order_id()
                order_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                checkout_data = {
                    'order_id': order_id,
                    'order_date': order_date,
                    'nama': nama,
                    'telepon': telepon,
                    'alamat': alamat,
                    'bank': bank,
                    'kode_bank': kode_bank,
                    'items': st.session_state.cart.copy(),
                    'total': total_harga,
                    'username': st.session_state.username
                }
                
                st.session_state.checkout_data = checkout_data
                st.session_state.order_history.append(checkout_data)
                
                # Redirect ke halaman struk
                navigate_to('receipt')
            else:
                st.error("❌ Mohon lengkapi semua data pembayaran!")
    
    # Back button
    if st.button("← Kembali ke Keranjang"):
        navigate_to('cart')

def render_receipt_page():
    """Render halaman struk pembelian"""
    if not st.session_state.get('checkout_data'):
        st.error("Data pembelian tidak ditemukan!")
        if st.button("← Kembali ke Beranda"):
            navigate_to('home')
        return

    data = st.session_state.checkout_data

    st.markdown("## 🧾 Struk Pembelian")

    html = f"""
    <html>
    <head>
    <style>
    body {{ font-family: Poppins, sans-serif; color: #333; }}
    .receipt-container {{
        background: white; border-radius: 15px; padding: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 600px;
        margin: 2rem auto; color: #333;
    }}
    .receipt-header {{ text-align: center; margin-bottom: 1rem; border-bottom: 2px solid #8FBC8F; }}
    .receipt-row {{ display: flex; justify-content: space-between; margin: 0.5rem 0; }}
    .receipt-item {{ display: flex; justify-content: space-between; background: #f9f9f9; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }}
    .receipt-total {{ border-top: 2px solid #8FBC8F; padding-top: 1rem; font-weight: bold; font-size: 1.2rem; }}
    .receipt-footer {{ text-align: center; color: #666; margin-top: 2rem; }}
    </style>
    </head>
    <body>
    <div class="receipt-container">
        <div class="receipt-header">
            <h2>👟 SepatuKu Store</h2>
            <p>Struk Pembelian</p>
        </div>
        <div class="receipt-info">
            <div class="receipt-row"><span><strong>Order ID:</strong></span><span>{data['order_id']}</span></div>
            <div class="receipt-row"><span><strong>Tanggal:</strong></span><span>{data['order_date']}</span></div>
            <div class="receipt-row"><span><strong>Nama:</strong></span><span>{data['nama']}</span></div>
            <div class="receipt-row"><span><strong>Telepon:</strong></span><span>{data['telepon']}</span></div>
            <div class="receipt-row"><span><strong>Alamat:</strong></span><span>{data['alamat']}</span></div>
            <div class="receipt-row"><span><strong>Bank:</strong></span><span>{data['bank']}</span></div>
            <div class="receipt-row"><span><strong>Kode Bank:</strong></span><span>{data['kode_bank']}</span></div>
        </div>

        <div class="receipt-items">
            <h4>Detail Pembelian:</h4>
    """

    for item in data['items']:
        html += f"""
        <div class="receipt-item">
            <div>
                <strong>{item['nama']}</strong><br>
                Ukuran: {item['ukuran']}
            </div>
            <div>
                {item['quantity']} x {format_rupiah(item['harga'])}<br>
                <strong>{format_rupiah(item['harga'] * item['quantity'])}</strong>
            </div>
        </div>
        """

    html += f"""
        </div>
        <div class="receipt-total">
            <div class="receipt-row">
                <span><strong>TOTAL PEMBAYARAN:</strong></span>
                <span><strong>{format_rupiah(data['total'])}</strong></span>
            </div>
        </div>
        <div class="receipt-footer">
            <p>Terima kasih telah berbelanja di SepatuKu Store!</p>
            <p>Barang akan dikirim dalam 1–3 hari kerja</p>
        </div>
    </div>
    </body>
    </html>
    """

    # GANTI st.markdown dengan components.html
    components.html(html, height=800)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Kembali ke Beranda", use_container_width=True):
            st.session_state.cart = []
            st.session_state.checkout_data = {}
            navigate_to('home')

    with col2:
        if st.button("🛒 Belanja Lagi", use_container_width=True):
            st.session_state.cart = []
            st.session_state.checkout_data = {}
            navigate_to('home')

    st.balloons()
    st.success("🎉 Pembelian berhasil! Terima kasih telah berbelanja di SepatuKu Store!")

def render_history_page():
    """Render halaman riwayat pembelian user"""
    st.markdown("## 🗂️ Riwayat Pembelian")

    user = st.session_state.username
    orders = [order for order in st.session_state.order_history if order['username'] == user]

    if not orders:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📦</div>
            <h3>Belum ada riwayat pembelian</h3>
            <p>Kamu belum pernah melakukan transaksi.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for order in reversed(orders):
        with st.expander(f"📟 Order ID: {order['order_id']} — {order['order_date']}"):
            st.markdown(f"""
            **Nama:** {order['nama']}  
            **Telepon:** {order['telepon']}  
            **Alamat:** {order['alamat']}  
            **Bank:** {order['bank']}  
            **Kode Bank:** {order['kode_bank']}  
            **Total Pembayaran:** {format_rupiah(order['total'])}
            """)
            st.markdown("**Detail Barang:**")
            for item in order['items']:
                st.markdown(f"- {item['nama']} (Ukuran {item['ukuran']}) x {item['quantity']} = {format_rupiah(item['harga'] * item['quantity'])}")


def render_app_bar():
    """Render app bar dengan navigasi"""
    st.markdown("""
    <div class="app-bar">
        <div class="app-bar-content">
            <div class="app-title">👟 SepatuKu</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    with col1:
        search_query = st.text_input("🔍", placeholder="Cari sepatu...",
            value=st.session_state.search_query,
            key="search_input", label_visibility="collapsed")
        if search_query != st.session_state.search_query:
            st.session_state.search_query = search_query
            st.rerun()

    with col2:
        sort_options = ["Sort by", "Nama A-Z", "Nama Z-A", "Harga Terendah", "Harga Tertinggi"]
        sort_option = st.selectbox("Filter", sort_options,
            index=sort_options.index(st.session_state.sort_option),
            key="sort_select", label_visibility="collapsed")
        if sort_option != st.session_state.sort_option:
            st.session_state.sort_option = sort_option
            st.rerun()

    with col3:
        if st.button("🏠 Beranda", key="nav_home"):
            navigate_to('home')

    with col4:
        if st.button("❤️ Favorit", key="nav_favorites"):
            navigate_to('favorites')

    with col5:
        if st.button("🛒 Keranjang", key="nav_cart"):
            navigate_to('cart')

    with col6:
        if st.button("🗂️ Riwayat", key="nav_history"):
            navigate_to('history')

    if st.button("🚪 Keluar", key="logout"):
        st.session_state.is_logged_in = False
        st.session_state.username = ""
        st.session_state.cart = []
        st.session_state.favorites = []
        navigate_to('login')


def main():
    load_css()
    init_session_state()
    sepatu_data = load_sepatu_data()

    if not st.session_state.is_logged_in:
        if st.session_state.current_page == 'register':
            render_register_page()
        else:
            render_login_page()
    else:
        render_app_bar()

        if st.session_state.current_page == 'home':
            render_home_page(sepatu_data)
        elif st.session_state.current_page == 'detail':
            render_detail_page(sepatu_data)
        elif st.session_state.current_page == 'favorites':
            render_favorites_page(sepatu_data)
        elif st.session_state.current_page == 'cart':
            render_cart_page()
        elif st.session_state.current_page == 'checkout':
            render_checkout_page()
        elif st.session_state.current_page == 'receipt':
            render_receipt_page()
        elif st.session_state.current_page == 'history':
            render_history_page()

        st.markdown("---")
        st.markdown("""
        <div class="footer">
            <p>© 2024 SepatuKu Store</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
