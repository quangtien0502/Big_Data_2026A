# Hướng dẫn chạy Dự án Web Server FastAPI (Big Data) trên PyCharm

Tài liệu này được viết chi tiết từng bước, dành cho thành viên mới để có thể dễ dàng thiết lập và chạy dự án Backend này bằng **PyCharm**.

---

## 1. Yêu cầu cài đặt trước (Prerequisites)
Trước khi bắt đầu, hãy đảm bảo máy tính của bạn đã cài đặt:
- **Python 3.12+** (Hoặc phiên bản Python 3.10 trở lên).
- **Docker Desktop** (để chạy Database PostgreSQL mà không cần cài rườm rà vào máy).
- **PyCharm** (Khuyên dùng bản Professional hoặc Community đều được).

---

## 2. Mở dự án trong PyCharm
1. Mở phần mềm PyCharm.
2. Chọn **Open** và tìm đến thư mục `backend` của dự án (Lưu ý: Mở thẳng thư mục `backend` làm root project sẽ giúp PyCharm nhận diện môi trường tốt nhất).
3. Đợi một chút để PyCharm quét các file.

---

## 3. Tạo môi trường ảo (Virtual Environment) và Cài thư viện
Chúng ta cần một môi trường ảo để các thư viện không bị xung đột với máy thật.
1. Ở góc dưới cùng bên phải của PyCharm, bạn sẽ thấy chữ `<No interpreter>` hoặc tên phiên bản Python. Hãy bấm vào đó -> Chọn **Add New Interpreter** -> **Add Local Interpreter...**
2. Cửa sổ hiện ra, chọn mục **Virtualenv Environment** (ở thanh bên trái).
3. Chọn **New environment**:
   - Location: Giữ nguyên mặc định (thường là đường dẫn dự án cộng thêm `/.venv`).
   - Base interpreter: Chọn bản Python 3.12 của bạn.
4. Bấm **OK** và chờ PyCharm tạo môi trường.
5. Khi tạo xong, PyCharm sẽ báo có file `requirements.txt`. Nó sẽ hiện ra một thanh vàng ở góc trên báo "Requirements plugins missing...". Bạn chỉ cần bấm vào **Install requirements** để tải toàn bộ thư viện về.
   *(Nếu không thấy thanh vàng, hãy mở tab **Terminal** ở góc dưới màn hình, gõ `pip install -r requirements.txt` rồi Enter).*

---

## 4. Khởi động Database (PostgreSQL qua Docker)
Ứng dụng cần có Database để lưu trữ. Chúng ta sẽ dùng Docker.
1. Mở phần mềm **Docker Desktop** trên máy bạn lên (chỉ cần bật cho nó chạy ngầm).
2. Trở lại PyCharm, mở tab **Terminal** ở góc dưới cùng (đảm bảo bạn đang ở thư mục `backend`).
3. Gõ lệnh sau để tải và bật database:
   ```bash
   docker-compose up -d
   ```
4. Đợi một lát để Docker tải image và khởi động. (Chữ `-d` giúp database chạy ngầm không chiếm màn hình).

*(Lưu ý: File cấu hình kết nối DB đã được tạo sẵn trong `backend/.env.example`. Hãy copy file đó thành file `.env` nếu bạn muốn tuỳ chỉnh).*

---

## 5. Chạy Migrations (Tạo Bảng trong Database)
Lúc này Database đã chạy, nhưng nó đang trống rỗng. Ta cần bảo hệ thống tạo các bảng (Roads, Traffic, Weather...).
1. Mở tab **Terminal** trong PyCharm (nếu thấy có chữ `(.venv)` ở đầu dòng lệnh là tốt nhất).
2. Chạy lệnh để quét code và sinh file kịch bản tạo bảng:
   ```bash
   alembic revision --autogenerate -m "init"
   ```
   *(Kết quả sẽ báo là phát hiện các bảng mới).*
3. Chạy lệnh để áp dụng kịch bản đó vào Database thực tế:
   ```bash
   alembic upgrade head
   ```
Lúc này toàn bộ cấu trúc bảng đã được tạo thành công!

---

## 6. Khởi chạy Server FastAPI
Bây giờ mọi thứ đã sẵn sàng. Ta sẽ chạy ứng dụng:
1. Nhìn sang cây thư mục bên trái của PyCharm, mở file `app/main.py`.
2. Kéo xuống dòng cuối cùng của file, bạn sẽ thấy đoạn code:
   ```python
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
   ```
3. Bạn sẽ thấy một **nút Play (tam giác xanh lá)** nho nhỏ nằm ở ngoài cùng lề trái (ngay cạnh dòng `if __name__ == "__main__":`).
4. Bấm vào nút Play đó -> Chọn **Run 'main'**.
5. Nhìn xuống cửa sổ Run ở dưới cùng, nếu thấy dòng chữ:
   `INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)`
   nghĩa là server đã chạy thành công!

*(Chế độ `reload=True` giúp server tự động khởi động lại mỗi khi bạn sửa và lưu file code).*

---

## 7. Trải nghiệm API bằng Swagger
FastAPI tự động tạo sẵn giao diện web cực kỳ trực quan để thử nghiệm API.
1. Mở trình duyệt web (Chrome, Edge, Safari...).
2. Truy cập vào địa chỉ: [http://localhost:8000/docs](http://localhost:8000/docs)
3. Bạn sẽ thấy danh sách tất cả các API. Để test:
   - Bấm vào một API bất kỳ, ví dụ `GET /api/v1/health/db`.
   - Bấm nút **Try it out** ở góc trên bên phải của box đó.
   - Bấm nút **Execute** màu xanh.
   - Xem kết quả trả về ở mục **Response body**.

---
**Chúc bạn code vui vẻ!** Mọi thắc mắc về luồng dữ liệu (Data Pipeline, PySpark) sẽ được cập nhật ở các Phase tiếp theo.
