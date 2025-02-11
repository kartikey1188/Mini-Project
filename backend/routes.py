from flask import current_app as app, render_template, send_from_directory

@app.get('/')
def begin():
    return render_template('index.html')

@app.route('/serve_image/<filename>', methods=['GET'])
def serve_image(filename):                         # for serving images from the 'pictures/images' folder
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

@app.route('/serve_graph/<filename>', methods=['GET'])
def serve_graph(filename):                         # for serving images from the 'pictures/graphs' folder
    return send_from_directory(app.config['GRAPH_FOLDER'], filename)




