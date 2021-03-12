from flask import Flask, request


app = Flask(__name__)


r = None
@app.route('/get_token/')
def token_request():
    #print('\n*********',request.args['code'],'\n************')
    
    return '''Received key. Sending it back to Python...
<script type="text/javascript">

var hash = false; 
checkHash();

function checkHash(){ 
    if(window.location.hash != hash) { 
        hash = window.location.hash; 
        processHash(hash.replace("#", "?")); 
    }
}

function processHash(hash){
    window.location.replace('http://localhost:8080/post_token/'+hash);
}
                
            </script> '''
            
@app.route('/post_token/')
def token_response():
    print('\n*********',request.args['access_token'],'\n************')
    
    return "Token received by Python. You can close this."

if __name__ == '__main__':
    app.run(port=8080)
    