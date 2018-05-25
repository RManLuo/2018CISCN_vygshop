from flask import Flask,request,jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/api/send_sms', methods=['GET', 'POST'])
def send_sms():
    if request.method == 'POST':
        if request.form.get('data'):
            tree1 = etree.fromstring(request.form['data'].encode('utf8'))
            print etree.tostring(tree1)
            return jsonify({'status':0,'msg':'Success','content':etree.tostring(tree1)})
        else:
            return jsonify({'status':1,'msg':'no params'})
    else:
        return jsonify({'status':1,'msg':'not post'})
        
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8200)
