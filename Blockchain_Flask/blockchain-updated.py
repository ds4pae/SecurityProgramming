import hashlib
import json
import time
import os
from uuid import uuid4
from flask import Flask, jsonify, request, render_template, Blueprint, send_file
from Blockchain_Advanced_6th_updated import *  ## 수정됨....
from InfoSecModule_selfsigned import *
from InfoSecModule import rsaEncrypt, rsaDecrypt


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


# Creating the app node
app = Flask(__name__, template_folder='./templates')    ## flask 폴더 위치를 지정할 수 있음
node_identifier = str(uuid4()).replace('-','')

# Initializing blockchain
my_blockchain = Blockchain()

addPublicKeyOnBlockchain(my_blockchain, "Alice")
addPublicKeyOnBlockchain(my_blockchain, "Bob")
addPublicKeyOnBlockchain(my_blockchain, "Carol")

myPublicKey = getPublicKeyFromBlockchain(my_blockchain, "Alice")
print(f"Public Key Stored on Blockchain: {myPublicKey}")


@app.route('/')
def hello_world():  # put application's code here
    return '<h1>Hello World!!! Blockchain with Flask</h1>'

@app.route('/myname')
def myName():
    return 'hong gil dong'

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
    return render_template("aes_sample.html",
                           aes_message = message, aes_encryption_result = ciphertext.hex())


@app.route('/aes_get_post_sample', methods=['GET','POST'])
def aes_get_post_sample():
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
        return render_template("aes_sample.html",
                               aes_message = message, aes_encryption_result = ciphertext.hex())

    return render_template("aes_get_post_sample.html")


UPLOAD_FOLDER = os.getcwd() + '/upload'  # 절대 파일 경로
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

bp = Blueprint('fileupload', __name__, url_prefix='/fileupload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/fileupload', methods=['GET', 'POST'])
def fileupload():
    global UPLOAD_FILE

    if request.method == 'POST':
        print(request.files)
        file = request.files['savefile']
        if file and allowed_file(file.filename):
            filename = file.filename
            filepathtosave = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepathtosave)
            return render_template('fileupload.html')
    return render_template('fileupload.html')


@app.route('/download')
def download():
    hostname = "Server"
    myCertFile = hostname + "Cert.crt"
    myPrivateKeyFile = hostname + "Private.key"
    genCertificateToFile(hostname, myCertFile, myPrivateKeyFile)

    path =myCertFile
    print('downfile ' + path)
    return send_file(path, as_attachment=True)


@app.route('/rsa_get_post_sample', methods=['GET','POST'])
def rsa_get_post_sample():
    if request.method == 'POST':
        print("RSA 암호화 버튼 클릭!!!")
        input_value = request.form.to_dict(flat=False)
        print("Input Message: ", input_value)
        #웹 페이지로부터 message(plaintext)를 입력 받아서 RSA 암호화 과정을 수행
        message = input_value.get('message')[0]
        hostname = "Server"
        certFilename = hostname + "Cert.crt"
        print(message)
        myPublicKey = read_pub_key_from_cert(certFilename)
        print(myPublicKey)
        ciphertext = rsaEncrypt(message.encode(), myPublicKey)
        return render_template("rsa_sample.html",
                               rsa_message = message, rsa_encryption_result = ciphertext.hex())

    return render_template("rsa_get_post_sample.html")


@app.route('/rsa_dec_get_post_sample', methods=['GET','POST'])
def rsa_dec_get_post_sample():
    if request.method == 'POST':
        print("RSA 복호화 버튼 클릭!!!")
        #웹 페이지로부터 message(plaintext)를 입력 받아서 RSA 암호화 과정을 수행
        ciphertext = "{}".format(request.form['ciphertextArea'])
        hostname = "Server"
        privateKeyFilename = hostname + "Private.key"
        myPrivateKey = readFromCertFile(privateKeyFilename)
        print(ciphertext)
        message = rsaDecrypt(bytearray.fromhex(ciphertext), myPrivateKey)
        return render_template("rsa_dec_sample.html", rsa_ciphetext = ciphertext, rsa_decryption_result = message.decode())

    return render_template("rsa_get_post_sample.html")


#### blockchain with flask
@app.route('/mine', methods=['GET'])
def mine_block():
    addPublicKeyOnBlockchain(my_blockchain, 'Eve')
    myPublicKey = getPublicKeyFromBlockchain(my_blockchain, "Eve")
    print("Public Key: ", myPublicKey)
    last_block = my_blockchain.get_latest_block()
    response = {
        'message': f'Transaction Block No. {my_blockchain.get_latest_block().index}',
        'userName': last_block.userName,
        'data': last_block.data
    }
    return jsonify(response), 201

@app.route('/getPublicKey', methods=['GET'])
def get_publicKey():
    last_block = my_blockchain.get_latest_block()
    return last_block.data

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [ ]
    for block in my_blockchain.chain:
        chain_data.append({
            'index' : block.index,
            "UserName" : block.userName,
            'Data' : block.data,
            'hash': block.hash
        })
    return jsonify({'chain': chain_data, 'length': len(chain_data)}), 200


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)