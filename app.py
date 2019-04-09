import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import fitz
import pytesseract
import numpy as np
from PIL import Image
import io


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True



server = app.server



#US_STATES_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv'



#US_AG_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv'

baseheight = 1240
UPLOAD_DIRECTORY = "/assets"

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server)
templateDir = os.path.dirname(__file__)
TEMPLATE_DIRS = (os.path.join(templateDir, "templates"))
    


app.layout = html.Div(
    [
        html.H1("File Browser"),
        html.H2("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.H2("File List"),
        html.H3(id="file-list"),
    ],
    style={"max-width": "500px"},
)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(TEMPLATE_DIRS, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(templateDir):
        path = os.path.join(TEMPLATE_DIRS, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            if('.pdf' in name):
                #print('Filetype is perfect')
                save_file(name, data)
                #print('jghjghjg hjhjhjh hhkhhjhj bnbjbnb')
                path = os.path.join(TEMPLATE_DIRS, name)
                doc = fitz.open(path) 
                page = doc.loadPage(0)
                img=page.getPixmap()
                img2=img.getPNGData()
                stream = io.BytesIO(img2)
                img3 = Image.open(stream)
                hpercent = (baseheight / float(img3.size[1]))
                wsize = int((float(img3.size[0]) * float(hpercent)))
                img4 = img3.resize((wsize, baseheight), Image.ANTIALIAS)
                imagetext = pytesseract.image_to_string(img4)
                return imagetext
                
            else:
                return "filetype is Wrong"  
  

if __name__ == '__main__':

    app.run_server(debug=True)
