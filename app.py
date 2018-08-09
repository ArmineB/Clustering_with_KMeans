
import pandas as pandas

import pandas.io.formats.style
from io import BytesIO
import numpy as np
from flask import Flask,  render_template, request
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message


from kMeans import kMeans, getIdWithClusters, describeData
from optimalK import getOptimalK

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'armine.baghdasaryan7@gmail.com'
app.config['MAIL_PASSWORD'] = '******'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
ADMINS=['armine.baghdasaryan7@gmail.com']

mail = Mail(app)


dataFrame = None
data = None
features = None
selectedFeatures = None
maxK = None
dataFrame1 = None
dataFrame2 = None
filename = None

@app.route('/')
def homePage():
    return render_template('temp/index.html')


@app.route('/upload', methods=['POST'])
def upload():

   file = request.files.get('fileToUpload')
   global filename
   filename = secure_filename(file.filename)
   file_content = BytesIO(file.read())
   global dataFrame
   dataFrame = pandas.read_csv(file_content)
   global features
   features = list(dataFrame.columns.values)
   features1 = features
   del features1[0]

   return render_template('temp/features.html', features=features1)


@app.route('/features', methods=['GET', 'POST'])
def getFeatures():
    global selectedFeatures
    selectedFeatures = request.form.getlist('fe')
    global data
    data = dataFrame[selectedFeatures].values
    uniqueData = np.unique(data)
    global maxK
    maxK = min(len(uniqueData),20)

    return render_template('temp/optimalK.html', maxK=maxK)


@app.route('/clustering', methods=['GET', 'POST'])
def clustering():
    k = request.form.get('k')
    clusters = kMeans(dataFrame, selectedFeatures, int(k))
    global dataFrame1
    dataFrame1 = getIdWithClusters(clusters, dataFrame)
    global dataFrame2
    dataFrame2 = describeData(selectedFeatures, dataFrame, clusters)

    return render_template("temp/analysis.html", numberOfClusters=k, data1=dataFrame1.to_html(index=False, table_id='ID1'), data2=dataFrame2.to_html(table_id='ID2'))


@app.route('/optimalClustering', methods=['GET', 'POST'])
def optimalClustering():
    optimalK = getOptimalK(data, maxK)

    clusters = kMeans(dataFrame, selectedFeatures, optimalK)
    global dataFrame1
    dataFrame1 = getIdWithClusters(clusters, dataFrame)
    global dataFrame2
    dataFrame2 = describeData(selectedFeatures, dataFrame, clusters)

    return render_template("temp/analysis.html", numberOfClusters=str(optimalK), data1=dataFrame1.to_html(index=False, table_id='ID1'), data2=dataFrame2.to_html(table_id='ID2'))


@app.route("/mail", methods=['POST', 'GET'])
def index():
    m = request.form.get('mail')
    path = 'C:\\dataframes\\'
    dataFrame1.to_csv(path+'_clusters'+filename)
    dataFrame2.to_csv(path+'_description'+filename)
    msg = Message("Message from site",
                  sender='armine.baghdasaryan7@gmail.com',
                  recipients=[m])

    msg.attach('_clusters'+filename, 'text/csv', str(dataFrame1))
    msg.attach('_description'+filename, 'text/csv', str(dataFrame2))
    mail.send(msg)
    return render_template("temp/end.html")


if __name__ == '__main__':
    app.run()


