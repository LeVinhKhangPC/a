from flask import Flask, render_template, request, send_file, make_response
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    content = request.form.get('content')
    link = request.form.get('link')

    # Kiểm tra nếu cả nội dung và liên kết đều trống
    if not content and not link:
        return render_template('index.html', qr_generated=False, error_message='Please enter content or link.')

    # Tạo mã QR từ nội dung và liên kết
    qr_content = f'{content}\n' if content else ''
    qr_link = f'{link}' if link else ''

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content + qr_link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Tạo hình ảnh tạm thời trong bộ nhớ
    img_buffer = io.BytesIO()
    img.save(img_buffer)
    img_buffer.seek(0)

    response = make_response(send_file(img_buffer, mimetype='image/png', as_attachment=True, download_name='qr_code.png'))
    return response

if __name__ == '__main__':
    app.run(debug=True)
