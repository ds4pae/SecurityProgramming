from flask import Flask
from flask import  render_template
from Crypto.Cipher import AES
from Crypto import Random
from fl
ask import request

app = Flask(__name__)


posts = [
    {
        'name' : 'Brother',
        'title' : 'Professor',
        'role' : 'Research',
        'date_after' : "2003.03.01"
    },
{
        'name' : 'Sister',
        'title' : 'Student',
        'role' : 'Study',
        'date_after' : "2023.03.01"
    }
]

@app.route('/')
def hello_world():  # put application's code here
    return '<h1>Hello World!</h1>'


@app.route('/sample')
def html_sample():
    return render_template('sample.html', posts=posts)


@app.route('/backend_sample')
def backend_sample():
    return render_template("backend_sample.html", backend_result = "1000")


@app.route('/aes_sample')
def aes_sample():
    message = "Hello World"
    key = Random.new().read(AES.key_size[0])
    iv = Random.new().read(AES.block_size)
    aesCipher = AES.new(key, AES.MODE_OFB, iv)
    ciphertext = aesCipher.encrypt(message.encode())
    return render_template("aes_sample.html", aes_encryption_result = ciphertext.hex())


@app.route('/aes_get_post_sample', methods=['GET','POST'])
def aes_get_post_sample():
    # from flask import request 추가...
    if request.method == 'POST':
        print("AES 암호화 버튼 클릭!!!")
        input_value = request.form.to_dict(flat=False)
        print("Input Message: ", input_value)
        #웹 페이지로부터 message(plaintext)를 입력 받아서 AES 암호화 과정을 수행
        message = input_value.get('message')[0]
        key = Random.new().read(AES.key_size[0])
        iv = Random.new().read(AES.block_size)
        aesCipher = AES.new(key, AES.MODE_OFB, iv)
        ciphertext = aesCipher.encrypt(message.encode())
        return render_template("aes_sample.html", aes_message = message, aes_encryption_result = ciphertext.hex())

    return render_template("aes_get_post_sample.html")


if __name__ == '__main__':
    app.run()
