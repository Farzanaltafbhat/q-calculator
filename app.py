from flask import Flask, render_template, request
import numpy as np
from scipy.special import erfc, erfcinv

app = Flask(__name__)

def q_function(x):
    return 0.5 * erfc(x / np.sqrt(2))

def inverse_q_function(q_value):
    return np.sqrt(2) * erfcinv(2 * q_value)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    inputs = {}

    if request.method == 'POST':
        mode = request.form.get('mode')
        
        try:
            if mode == 'Q(x)':
                x = float(request.form['x_value'])
                result = q_function(x)
                inputs = {'x_value': x}
                
            elif mode == 'Q^-1(y)':
                q = float(request.form['q_value'])
                if not 0 < q < 1:
                    raise ValueError("Q value must be between 0 and 1")
                result = inverse_q_function(q)
                inputs = {'q_value': q}
                
            elif mode == 'Find x for Pb':
                pb = float(request.form['pb_value'])
                if not 0 < pb < 1:
                    raise ValueError("Pb value must be between 0 and 1")
                result = inverse_q_function(pb)
                inputs = {'pb_value': pb}
                
        except ValueError as e:
            error = str(e)
        except:
            error = "Invalid input format"

    return render_template('index.html', result=result, error=error, **inputs)

if __name__ == "__main__":
    app.run(debug=True)