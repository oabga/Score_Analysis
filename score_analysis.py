import streamlit as st
import pandas as pd
# Most of the Matplotlib utilities lies under the pyplot submodule, and are usually imported under the plt alias:
import matplotlib.pyplot as plt 
import io 
from PIL import Image

def calculate_average(scores):
    return sum(scores) / len(scores)


def percentage_distribution(scores):
    bins = {'90-100': 0, '80-89': 0, '70-79': 0, '60-69': 0, '<60': 0}
    for score in scores:
        if score >= 90:
            bins['90-100'] += 1
        elif score >= 80:
            bins['80-89'] += 1
        elif score >= 70:
            bins['70-79'] += 1
        elif score >= 60:
            bins['60-69'] += 1
        else:
            bins['<60'] += 1
    
    return bins 

def main():
    st.title("Phân tích dữ liệu điểm số học sinh")
    uploaded_file = st.file_uploader(label='Chọn file Excel (có cột Điểm số)', type=['xlsx'])
    if uploaded_file:
        # Đọc file
        df = pd.read_excel(uploaded_file)
        
        # Xử lý danh sách điểm số
        scores = df['Điểm số'].dropna().astype(float).to_list()

        # Hiển thị các thông số
        st.write("Tổng số học sinh:", len(scores), "\t\tĐiểm trung bình:", round(calculate_average(scores), 2))

        dist = percentage_distribution(scores)

        # show distribution
        labels = dist.keys()
        values = dist.values()

        fig, ax = plt.subplots(figsize=(2, 2))
        ax.pie(x=values, labels=labels, startangle=90, autopct="%1.1f%%", textprops={'fontsize': 6.0})
        # ax.axis("equal")
        # ax.set_title("Phân bố bản điểm")
        # st.pyplot(fig)

        ax.axis('equal')
        plt.tight_layout(pad=0.1)

        # Tạo một vùng nhớ đệm(buffer) trong RAM kiểu nhị phân(BytesIO) để tạm thời lưu trữ dữ liệu
        buf = io.BytesIO()

        # lưu hình vẽ(figure vào buffer), dpi(dots per inch: độ phân giải cao)
        fig.savefig(buf, format='png', dpi=300)

        #Sau khi lưu ảnh, con trỏ đang ở cuối buffer.
        #seek(0) giúp chuẩn bị đọc dữ liệu từ đầu.
        buf.seek(0)

        # biến dữ liệu nhị phân trong buffer thành đối tượng image
        img = Image.open(buf)

        col1, col2, col3 = st.columns(spec=[1,2,1])
        with col2:
            st.image(img, width=250)
            st.markdown('**Biểu đồ phân bố điểm số**')
        

if __name__ == '__main__':
    main()
