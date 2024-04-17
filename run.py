from app import app
import os
x = 1
if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    # print (x or None)
    # print (x is not None)
    
from flask import request
print (request.remote_addr)