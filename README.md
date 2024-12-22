# 🚀 **BE-HUMG-Chatbot** 🤖  
**A Backend Server for Retrieval-Augmented Generation (RAG) using Vector Database and Chatbot Integration**

---

## 📚 **Giới thiệu Dự Án**

**BE-HUMG-Chatbot** là backend server được thiết kế để hỗ trợ các ứng dụng Chatbot sử dụng kỹ thuật **Retrieval-Augmented Generation (RAG)**. Dự án kết hợp **Vector Database** để lưu trữ và truy xuất dữ liệu hiệu quả, đồng thời triển khai một server mạnh mẽ để xử lý yêu cầu từ phía người dùng.

---

## 🛠️ **Các Thành Phần Chính**

### 1️⃣ **Vector Database Notebook 📊**
- **Mục đích:** Lưu trữ và truy xuất dữ liệu dưới dạng vector để tối ưu hóa tìm kiếm ngữ nghĩa.  
- **Chức năng chính:**  
   - Chuyển đổi văn bản thành vector thông qua mô hình ngôn ngữ tiên tiến.  
   - Lưu trữ vector vào cơ sở dữ liệu vector.  
   - Truy vấn vector để tìm kiếm thông tin liên quan.

### 2️⃣ **Server RAG 🚦**
- **Mục đích:** Cung cấp API cho chatbot, xử lý các yêu cầu thông qua pipeline RAG.  
- **Chức năng chính:**  
   - Tiếp nhận truy vấn từ người dùng.  
   - Truy xuất thông tin từ Vector Database.  
   - Kết hợp thông tin truy xuất với mô hình ngôn ngữ để tạo phản hồi tự nhiên.  
   - Giao tiếp qua API endpoint.

---

## 💻 **Hướng Dẫn Cài Đặt**

### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/your-username/BE-HUMG-Chatbot.git
cd BE-HUMG-Chatbot
```

### 2️⃣ **Tạo Virtual Environment và Cài Đặt Thư Viện**
```bash
python -m venv venv
source venv/bin/activate   # Trên Linux/MacOS
venv\Scripts\activate      # Trên Windows
pip install -r requirements.txt
```

### 3️⃣ **Chạy Server**
```bash
cd server
python app.py
```

Server sẽ khởi chạy tại: `http://127.0.0.1:5000`

---

## 🚦 **API Endpoints**

| Method | Endpoint         | Mô tả                    |
|--------|-------------------|--------------------------|
| POST   | `/query`         | Nhận truy vấn từ người dùng và trả về kết quả RAG. |
| GET    | `/health`        | Kiểm tra trạng thái của server. |

**Ví dụ truy vấn API:**
```json
POST /query
{
  "question": "Hãy giải thích RAG là gì?"
}
```

**Phản hồi mẫu:**
```json
{
  "answer": "RAG (Retrieval-Augmented Generation) là kỹ thuật kết hợp giữa tìm kiếm thông tin và sinh văn bản tự động."
}
```

---

## 🚧 **Kế Hoạch Phát Triển**

- [ ] Tích hợp thêm bộ nhớ ngữ cảnh cho chatbot.  
- [ ] Cải thiện hiệu suất truy vấn Vector Database.  
- [ ] Thêm tính năng xác thực API.

---

## 🤝 **Đóng Góp**

Chúng tôi luôn chào đón các đóng góp từ cộng đồng!  
1. **Fork** dự án.  
2. Tạo nhánh mới: `git checkout -b feature/your-feature`.  
3. Commit thay đổi: `git commit -m "Add some feature"`.  
4. Push nhánh: `git push origin feature/your-feature`.  
5. Tạo **Pull Request**.

---

## 📝 **Giấy Phép**

Dự án này được phân phối theo giấy phép **MIT License**.

---

## 📧 **Liên Hệ**

- **Người phụ trách:** PhamHongHiep  
- **Email:** [phamhonghiep.humg@gmail.com]  
- **GitHub:** [github.com/Epchannel](https://github.com/Epchannel)  

---

⭐ **Nếu bạn thấy dự án hữu ích, hãy cho chúng tôi một ngôi sao trên GitHub!** ⭐
