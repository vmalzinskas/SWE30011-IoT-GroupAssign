from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)

# Initialize variables
current_temp = 'No connection'
target_temp = 'Device Default 0 C'

@app.route('/', methods=['GET'])
def index():
    # Serve HTML template with current and target temperatures
    return render_template('index.html', current_temp=current_temp, target_temp=target_temp)

@app.route('/api/endpoint', methods=['GET', 'POST'])
def handle_api_request():
    global current_temp, target_temp

    if request.method == 'GET':
        # Return target temperature and current temperature in JSON format
        return jsonify({'target_temp': target_temp, 'current_temp': current_temp})
    elif request.method == 'POST':
        # Update target temperature and current temperature from POST request
        new_target_temp = request.form.get('new_target_temp')
        current_temp = request.form.get('current_temp')
        if new_target_temp and current_temp:
            target_temp = float(new_target_temp)
            # Redirect back to the original page after update
            return redirect(url_for('index'))
        else:
            return 'No new target temperature provided'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
