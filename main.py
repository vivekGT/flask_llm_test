from flask_cors import CORS
from pypdf import PdfReader
from flask import Flask, request
import json



app = Flask(__name__)

CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

def get_pdf_texts(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text


@app.route('/ping',methods = ["GET"])
def ping():
        return json.dumps({"Response": "Getting response from the PING"})



@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        print(request)
        print("Request Method:", request.method)
        print("Request URL:", request.url)
        print("Request Headers:", request.headers)
        request_body = request.data
        print("Request Body:", request_body)

        # Print out query parameters
        print("Query Parameters:", request.args)

        # Print out form data
        print("Form Data:", request.form)

        print(request.files.keys())
        req = request.files
        print(req)        
        
        
        pdf_docs = request.files.getlist("pdf_docs")
        print(pdf_docs)

        if pdf_docs == None:
            return json.dumps({'success':False}), 401, {'ContentType':'application/json'}             
        
        # get pdf text
        try:
            raw_text = get_pdf_texts(pdf_docs)
            print(raw_text)
        except:
            return "error in reading pdf"   
        
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 



if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
