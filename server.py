from flask import Flask, request
from threading import Thread
import time


app = Flask(__name__)

token_received = None

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
    global token_received
    token_received = request.args['access_token']

    shutdown_thread = Thread(target=shutdown_server)
    shutdown_thread.start()
    return "Token received by Python. You can close this."

def shutdown_server():
    time.sleep(1)
    raise RuntimeError('End this!')



def run_server():
    try:
        app.run(port=8080)
    except:
        print('Ended this server')
        
    

if __name__ == '__main__':
    run_server()