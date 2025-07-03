# main_app.py
import streamlit as st
import datetime
import pandas as pd
import locale

# Atur locale untuk format mata uang
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Indonesian_Indonesia.1252')
    except:
        print("Locale id_ID/Indonesian tidak tersedia.")

def format_rp(angka):
    try:
        return locale.currency(angka or 0, grouping=True, symbol='Rp ')[:-3]
    except:
        return f"Rp {angka or 0:,.0f}".replace(",", ".")

# Import modul internal
try:
    from model import Transaksi
    from manajer_anggaran import AnggaranHarian
    from konfigurasi import KATEGORI_PENGELUARAN
    import database # <-- TAMBAHKAN ATAU PASTIKAN BARIS INI ADA
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}. Pastikan file .py lain ada.")
    st.stop()

st.set_page_config(page_title="Catatan Pengeluaran", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi objek anggaran
@st.cache_resource
def get_anggaran_manager():
    print(">>> STREAMLIT: (Cache Resource) Menginisialisasi AnggaranHarian...")
    return AnggaranHarian()

anggaran = get_anggaran_manager()

# --- Halaman Input ---
def halaman_input(anggaran: AnggaranHarian):
    st.header("Tambah Pengeluaran Baru")
    with st.form("form_transaksi_baru", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            deskripsi = st.text_input("Deskripsi*", placeholder="Contoh: Makan siang")
        with col2:
            kategori = st.selectbox("Kategori*:", KATEGORI_PENGELUARAN, index=0)

        col3, col4 = st.columns(2)
        with col3:
            jumlah = st.number_input("Jumlah (Rp)*:", min_value=0.01, step=1000.0, format="%.0f")
        with col4:
            tanggal = st.date_input("Tanggal*:", value=datetime.date.today())

        submitted = st.form_submit_button("Simpan Transaksi")
        if submitted:
            if not deskripsi:
                st.warning("Deskripsi wajib!")
            elif jumlah is None or jumlah <= 0:
                st.warning("Jumlah wajib!")
            else:
                with st.spinner("Menyimpan..."):
                    tx = Transaksi(deskripsi, float(jumlah), kategori, tanggal)
                    if anggaran.tambah_transaksi(tx):
                        st.success("OK! Simpan.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Gagal simpan.")

# --- Halaman Riwayat ---
# main_app.py atau streamlit_app.py

# ... (kode import dan fungsi lain yang sudah ada)

def halaman_riwayat(anggaran: AnggaranHarian):
    st.subheader("Detail Semua Transaksi")

    # Kolom untuk menampung fungsionalitas hapus dan refresh
    col1, col2 = st.columns([3, 1])
    with col1:
        # Fungsionalitas Hapus
        with st.expander(" Hapus Transaksi"):
            # Ambil semua ID transaksi yang ada untuk validasi
            # Ini bisa di-cache agar tidak query terus menerus
            @st.cache_data(ttl=60)
            def get_all_transaction_ids():
                # Kita butuh query baru di database.py atau metode di manajer_anggaran.py
                # Untuk kesederhanaan, kita panggil query langsung di sini
                query = "SELECT id FROM transaksi"
                rows = database.fetch_query(query, fetch_all=True)
                return [row['id'] for row in rows] if rows else []

            list_id_transaksi = get_all_transaction_ids()

            if not list_id_transaksi:
                st.info("Tidak ada transaksi yang bisa dihapus.")
            else:
                id_to_delete = st.selectbox("Pilih ID Transaksi yang akan dihapus:", options=list_id_transaksi)
                
                if st.button("Hapus Transaksi Terpilih", type="primary"):
                    if id_to_delete:
                        # Logika Konfirmasi
                        if f"confirm_delete_{id_to_delete}" not in st.session_state:
                            st.session_state[f"confirm_delete_{id_to_delete}"] = True
                            st.warning(f"Anda yakin ingin menghapus transaksi ID: {id_to_delete}? Aksi ini tidak dapat dibatalkan.", icon="⚠️")
    
    with col2:
        # Tombol Refresh
        if st.button("🔄 Refresh Riwayat"):
            st.cache_data.clear()
            st.rerun()

    # Logika setelah tombol konfirmasi ditekan
    if 'id_to_delete' in locals() and st.session_state.get(f"confirm_delete_{id_to_delete}"):
        if st.button(f"Ya, Hapus Transaksi ID {id_to_delete}"):
            with st.spinner("Menghapus..."):
                if anggaran.hapus_transaksi(id_to_delete):
                    st.success(f"Transaksi ID: {id_to_delete} berhasil dihapus.", icon="✅")
                    # Bersihkan cache dan state konfirmasi, lalu jalankan ulang aplikasi
                    del st.session_state[f"confirm_delete_{id_to_delete}"]
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Gagal menghapus transaksi dari database.", icon="❌")
                    del st.session_state[f"confirm_delete_{id_to_delete}"]


    st.markdown("---")
    
    # Menampilkan tabel riwayat transaksi
    with st.spinner("Memuat riwayat..."):
        # Query diubah untuk menyertakan ID agar pengguna tahu ID mana yang harus dipilih
        query = "SELECT id, tanggal, kategori, deskripsi, jumlah FROM transaksi ORDER BY tanggal DESC, id DESC"
        df_transaksi = database.get_dataframe(query)

    if df_transaksi is None:
        st.error("Gagal mengambil data riwayat.")
    elif df_transaksi.empty:
        st.info("Belum ada data transaksi yang tercatat.")
    else:
        # Format kolom jumlah ke Rupiah
        try:
            df_transaksi['Jumlah (Rp)'] = df_transaksi['jumlah'].apply(lambda x: locale.currency(x or 0, grouping=True, symbol='Rp ')[:-3])
            df_display = df_transaksi[['id', 'tanggal', 'kategori', 'deskripsi', 'Jumlah (Rp)']]
        except Exception:
            df_transaksi['Jumlah (Rp)'] = df_transaksi['jumlah'].apply(lambda x: f"Rp {x or 0:,.0f}".replace(",", "."))
            df_display = df_transaksi[['id', 'tanggal', 'kategori', 'deskripsi', 'Jumlah (Rp)']]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)

# ... (sisa kode aplikasi)

# --- Halaman Ringkasan ---
def halaman_ringkasan(anggaran: AnggaranHarian):
    st.subheader("Ringkasan Pengeluaran")
    col_filter1, col_filter2 = st.columns([1, 2])

    with col_filter1:
        pilihan_periode = st.selectbox("Filter Periode:", ["Semua Waktu", "Hari Ini", "Pilih Tanggal"], key="filter_periode", on_change=lambda: st.cache_data.clear())

    tanggal_filter = None
    label_periode = "(Semua Waktu)"

    if pilihan_periode == "Hari Ini":
        tanggal_filter = datetime.date.today()
        label_periode = f"({tanggal_filter.strftime('%d %b')})"
    elif pilihan_periode == "Pilih Tanggal":
        if 'tanggal_pilihan_state' not in st.session_state:
            st.session_state.tanggal_pilihan_state = datetime.date.today()
        tanggal_filter = st.date_input("Pilih Tanggal:", value=st.session_state.tanggal_pilihan_state,
                                       key="tanggal_pilihan",
                                       on_change=lambda: setattr(st.session_state, 'tanggal_pilihan_state', st.session_state.tanggal_pilihan) or st.cache_data.clear())
        label_periode = f"({tanggal_filter.strftime('%d %b %Y')})"

    with col_filter2:
        @st.cache_data(ttl=300)
        def hitung_total_cached(tgl_filter):
            return anggaran.hitung_total_pengeluaran(tanggal=tgl_filter)

        total_pengeluaran = hitung_total_cached(tanggal_filter)
        st.metric(label=f"Total Pengeluaran {label_periode}", value=format_rp(total_pengeluaran))

    st.divider()
    st.subheader(f"Pengeluaran per Kategori {label_periode}")

    @st.cache_data(ttl=300)
    def get_kategori_cached(tgl_filter):
        return anggaran.get_pengeluaran_per_kategori(tanggal=tgl_filter)

    with st.spinner("Memuat ringkasan kategori..."):
        dict_per_kategori = get_kategori_cached(tanggal_filter)

    if not dict_per_kategori:
        st.info(f"Tidak ada data untuk periode ini.")
    else:
        try:
            data_kategori = [{"Kategori": kat, "Total": jml} for kat, jml in dict_per_kategori.items()]
            df_kategori = pd.DataFrame(data_kategori).sort_values(by="Total", ascending=False).reset_index(drop=True)
            df_kategori['Total (Rp)'] = df_kategori['Total'].apply(format_rp)

            col_kat1, col_kat2 = st.columns(2)
            with col_kat1:
                st.write("Tabel:")
                st.dataframe(df_kategori[['Kategori', 'Total (Rp)']], hide_index=True, use_container_width=True)
            with col_kat2:
                st.write("Grafik:")
                st.bar_chart(df_kategori.set_index('Kategori')['Total'], use_container_width=True)
        except Exception as e:
            st.error(f"Gagal tampilkan ringkasan: {e}")

# --- Main ---
def main():
    st.sidebar.title("Catatan Pengeluaran")
    menu_pilihan = st.sidebar.radio("Pilih Menu:", ["Tambah", "Riwayat", "Ringkasan"], key="menu_utama")
    st.sidebar.markdown("---")
    st.sidebar.info("Jobsheet - Aplikasi Keuangan")

    manajer_anggaran = get_anggaran_manager()
    if menu_pilihan == "Tambah":
        halaman_input(manajer_anggaran)
    elif menu_pilihan == "Riwayat":
        halaman_riwayat(manajer_anggaran)
    elif menu_pilihan == "Ringkasan":
        halaman_ringkasan(manajer_anggaran)

    st.markdown("---")
    st.caption("Pengembangan Aplikasi Berbasis OOP")

if __name__ == "__main__":
    main()
