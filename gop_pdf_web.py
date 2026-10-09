import streamlit as st
import os
import tempfile
from pypdf import PdfWriter

# ==================================================
# CAU HINH
# ==================================================
TEN_FILE_MAC_DINH = "TongHop_File.pdf"
# ==================================================

def lay_so_tu_ten_file(ten_file):
    """
    Lay so tu ten file de sap xep (1, 2, 3... 10, 11)
    """
    ten_khong_mo_rong = os.path.splitext(ten_file)[0]
    try:
        return int(ten_khong_mo_rong)
    except ValueError:
        return 999999

def gop_pdf(danh_sach_file, ten_file_dau_ra):
    """
    Gop cac file PDF thanh 1 file
    """
    merger = PdfWriter()
    
    for file in danh_sach_file:
        merger.append(file)
    
    # Luu file ket qua vao bo nho tam
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        merger.write(tmp)
        duong_dan_tmp = tmp.name
    
    merger.close()
    return duong_dan_tmp

# ==================================================
# GIAO DIEN WEB
# ==================================================

# Tieu de
st.set_page_config(page_title="Cong cu gop file PDF", page_icon="📄", layout="wide")
st.title("📄 Cong cu gop file PDF")
st.markdown("---")

# Phan tai len file
st.subheader("📤 Buoc 1: Tai len cac file PDF")
uploaded_files = st.file_uploader(
    "Chon cac file PDF (co the chon nhieu file cung luc)",
    type=["pdf"],
    accept_multiple_files=True
)

# Neu co file duoc tai len
if uploaded_files:
    st.success(f"✅ Da tai len {len(uploaded_files)} file PDF")
    
    # Hien thi danh sach file da tai len
    st.subheader("📋 Danh sach file da tai len:")
    
    # Tao danh sach ten file
    danh_sach_ten_file = [file.name for file in uploaded_files]
    
    # Sap xep theo so trong ten file
    danh_sach_ten_file_sap_xep = sorted(danh_sach_ten_file, key=lay_so_tu_ten_file)
    
    # Hien thi danh sach da sap xep
    for i, ten_file in enumerate(danh_sach_ten_file_sap_xep, 1):
        st.write(f"{i}. {ten_file}")
    
    st.markdown("---")
    
    # Phan cau hinh
    st.subheader("⚙️ Buoc 2: Cau hinh")
    
    # O nhap ten file ket qua
    ten_file_dau_ra = st.text_input(
        "Ten file ket qua:",
        value=TEN_FILE_MAC_DINH,
        help="Nhap ten file PDF sau khi gop"
    )
    
    # Dam bao ten file co duoi .pdf
    if not ten_file_dau_ra.lower().endswith(".pdf"):
        ten_file_dau_ra += ".pdf"
    
    st.markdown("---")
    
    # Phan gop file
    st.subheader("🚀 Buoc 3: Gop file")
    
    # Nut gop file
    if st.button("🔗 Gop file", type="primary", use_container_width=True):
        with st.spinner("Dang gop file..."):
            try:
                # Tao dictionary de anh xa ten file voi doi tuong file
                dict_file = {file.name: file for file in uploaded_files}
                
                # Sap xep cac file theo thu tu da sap xep
                danh_sach_file_sap_xep = [dict_file[ten_file] for ten_file in danh_sach_ten_file_sap_xep]
                
                # Gop file
                duong_dan_tmp = gop_pdf(danh_sach_file_sap_xep, ten_file_dau_ra)
                
                # Hien thi thanh cong
                st.success("✅ Gop file thanh cong!")
                
                # Nut tai xuong
                with open(duong_dan_tmp, "rb") as f:
                    st.download_button(
                        label="📥 Tai xuong file ket qua",
                        data=f,
                        file_name=ten_file_dau_ra,
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                # Xoa file tam
                os.unlink(duong_dan_tmp)
                
            except Exception as e:
                st.error(f"❌ Loi khi gop file: {e}")
                st.info("Vui long kiem tra lai cac file PDF co bi hong khong, hoac thu lai.")
else:
    # Neu chua co file nao duoc tai len
    st.info("👆 Vui long tai len cac file PDF de bat dau")
    
    # Hien thi vi du
    st.markdown("---")
    st.subheader("💡 Vi du:")
    st.markdown("""
    - Neu ban co cac file: `1.pdf`, `2.pdf`, `3.pdf`, `10.pdf`
    - He thong se tu dong sap xep theo thu tu: `1.pdf`, `2.pdf`, `3.pdf`, `10.pdf`
    - File ket qua se co 4 trang theo dung thu tu nay
    """)
#（注：内容由AI生成）
