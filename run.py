from flask import Flask, render_template, request,redirect, url_for
from werkzeug.utils import secure_filename
from src import get_reference
import os



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/paper/'

@app.route('/')
def a():
    return redirect(url_for('index'))

@app.route('/index',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        # print(request.form)
        paper = request.form['paper']
        if paper == 'add':
            return  redirect(url_for('upload_file'))
        else:
            return redirect(url_for("show_reference",paper = paper))
    else:
        papers=[]
        for root,dirs,files in os.walk('data/paper'):
            papers = files
        return  render_template("index.html",papers=papers)

@app.route('/upload')
def upload_file():
    return render_template("upload.html")

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename !='':
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            get_reference.mulit_get_reference(f.filename)

        return redirect(url_for('index'))

    else:

        return render_template('upload.html')

@app.route('/reference/<paper>/<reference>')
def show_bib(paper,reference):
    str =''
    with open ('./data/reference/'+paper[0:-4]+'/'+reference) as f:
        list = f.readlines()
        str = "\n".join(list)
    return render_template('bib.html',reference=reference,str=str)

@app.route('/reference/<paper>',methods =['POST','GET'])
def jump(paper):
    if request.method == 'POST':
        reference = request.form.get('reference')

        return redirect(url_for('show_bib',paper=paper,reference=reference))

@app.route('/paper/<paper>')
def show_reference(paper):

    references = []
    for root, dirs, files in os.walk('data/reference/'+paper[0:-4]+'/'):
        references = files
    return  render_template('show_reference.html',paper=paper,references=references)



if __name__ == '__main__':
   app.run(debug=True)