# 👟 SepatuKu

Aplikasi web toko sepatu sederhana yang dibuat dengan Streamlit. Aplikasi ini menampilkan daftar sepatu dengan fitur keranjang belanja yang interaktif.

## 🎨 Fitur

- **Tampilan Modern**: Desain aesthetic dengan font Poppins dan skema warna oranye, hitam, putih
- **Daftar Produk**: Menampilkan sepatu dengan informasi lengkap (nama, ukuran, bahan, harga, gambar)
- **Keranjang Belanja**: Sistem keranjang yang interaktif dengan penghitungan total otomatis
- **Responsive Design**: Tampilan yang optimal di berbagai ukuran layar
- **Animasi Hover**: Efek visual yang menarik saat hover pada kartu produk

## 📁 Struktur Folder

```
toko-sepatu/
├── app.py                 # File utama aplikasi Streamlit
├── style.css             # File styling CSS
├── requirements.txt      # Dependencies
├── data/
│   └── sepatu_data.json  # Data sepatu
└── utils/
    └── helpers.py        # Fungsi helper
```

## 🚀 Cara Menjalankan

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Jalankan aplikasi:**
   ```
   streamlit run app.py
   ```

3. **Buka browser** dan akses ``

## 📊 Data Sepatu

Data sepatu disimpan dalam format JSON dengan struktur:
```json
{
  "id": 1,
  "nama": "Nama Sepatu",
  "ukuran": [39, 40, 41, 42],
  "bahan": "Bahan Sepatu",
  "harga": 1000000,
  "gambar": "https://link-gambar.com"
}
```

## 🔧 Kustomisasi

- **Tambah Produk**: Edit file `data/sepatu_data.json`
- **Ubah Styling**: Modifikasi file `style.css`
- **Tambah Fitur**: Edit file `app.py` dan `utils/helpers.py`

## 🌐 Deploy ke Streamlit Cloud

1. Push code ke GitHub repository
2. Kunjungi [share.streamlit.io](https://share.streamlit.io)
3. Connect repository GitHub Anda
4. Deploy aplikasi

## 📱 Screenshot

Aplikasi menampilkan:
- Header dengan gradient oranye yang menarik
- Grid produk sepatu dengan gambar dan informasi lengkap
- Keranjang belanja real-time di sidebar
- Tombol yang responsive dengan animasi hover

## 🛠️ Teknologi

- **Frontend**: Streamlit + Custom CSS
- **Data**: JSON
- **Styling**: Google Fonts (Poppins)
- **Images**: Unsplash (placeholder)

---

**Selamat berbelanja di ShoeCraft Store! 👟✨**