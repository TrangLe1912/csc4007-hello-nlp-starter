# Phát bài CSC4007 cho lớp KHMT 17-01

Workflow tạo một repository **private** cho mỗi sinh viên trong organization
`CSC-17-01`, chép nội dung bài tập từ `TrangLe1912/csc4007-hello-nlp-starter`,
sau đó mời GitHub username tương ứng với quyền `push`.

Các file quản trị trong `.github/classroom` và workflow phát bài không được chép
sang repo sinh viên, nhằm bảo vệ danh sách lớp và tránh chạy nhầm.

Tên repository: `csc4007-hello-nlp-<MSSV>`.

## Chuẩn bị một lần

1. Tạo fine-grained personal access token cho tài khoản có quyền quản trị
   organization `CSC-17-01`.
2. Chọn resource owner `CSC-17-01`, repository access `All repositories`, và
   cấp `Administration: Read and write`.
3. Trong repo starter, vào **Settings → Secrets and variables → Actions → New
   repository secret**; đặt tên `CLASSROOM_PAT` và dán token.

Không ghi token vào file CSV, workflow, issue hoặc nội dung commit.

## Chạy

1. Mở **Actions → Distribute CSC4007 to KHMT 17-01 → Run workflow**.
2. Lần đầu giữ `dry_run = true` để kiểm tra 19 tài khoản.
3. Nếu bảng Summary không có lỗi, chạy lại với `dry_run = false`.
4. Kiểm tra bảng Summary để biết repo đã tạo, lời mời đã gửi hoặc lỗi cần sửa.

Workflow có thể chạy lại an toàn: repo đã tồn tại sẽ không được tạo trùng.
