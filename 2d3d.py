import numpy as np
import pydicom
import os
import scipy.ndimage
from skimage import measure
from plotly.offline import plot
from plotly.tools import FigureFactory as FF


class Plot3d:
    def __init__(self, path):
        self.path = path
        self.slices = None
        self.slice_thickness = None
        self.images = None
        self.verts = None
        self.faces = None
        self.norm = None
        self.val = None
        self.div = None


        print('loading images')
        self.load_scan()
        print('pre-processing images')
        self.get_pixels_hu()
        print('making a mesh')
        self.make_mesh()
        print('plotting a 3D model')
        self.plotly_3d()
  

    def load_scan(self):
        self.slices = [pydicom.read_file(self.path + '/' + s) for s in os.listdir(self.path)]
        self.slices.sort(key = lambda x: int(x.InstanceNumber))
        try:
            self.slice_thickness = np.abs(self.slices[0].ImagePositionPatient[2] - self.slices[1].ImagePositionPatient[2])
        except:
            self.slice_thickness = np.abs(self.slices[0].SliceLocation - self.slices[1].SliceLocation)
            
        for s in self.slices:
            s.SliceThickness = self.slice_thickness
  

    def get_pixels_hu(self):
        image = np.stack([s.pixel_array for s in self.slices])
        
        image = image.astype(np.int16)

        image[image == -2000] = 0
        
        intercept = self.slices[0].RescaleIntercept
        slope = self.slices[0].RescaleSlope
        
        if slope != 1:
            image = slope * image.astype(np.float64)
            image = image.astype(np.int16)
            
        image += np.int16(intercept)
        
        self.images = np.array(image, dtype=np.int16)

        new_spacing = [1, 1, 1]

        spacing = map(float, ([self.slices[0].SliceThickness] + list(self.slices[0].PixelSpacing)))
        spacing = np.array(list(spacing))

        resize_factor = spacing / new_spacing
        new_real_shape = self.images.shape * resize_factor
        new_shape = np.round(new_real_shape)
        real_resize_factor = new_shape / self.images.shape
        new_spacing = spacing / real_resize_factor
        
        self.images = scipy.ndimage.zoom(self.images, real_resize_factor)


    def make_mesh(self, threshold=300, step_size=2):
        p = self.images.transpose(2,1,0)

        self.verts, self.faces, self.norm, self.val = measure.marching_cubes(p, threshold, step_size=step_size, allow_degenerate=True)
        return self.verts, self.faces
  

    def plotly_3d(self):
        x, y, z = zip(*self.verts)

        colormap = ['rgb(236, 236, 212)', 'rgb(236, 236, 212)']

        fig = FF.create_trisurf(
            x=x,
            y=y,
            z=z,
            plot_edges=False,
            colormap=colormap,
            simplices=self.faces,
            backgroundcolor='rgb(64, 64, 64)',
            title="Interactive Visualization"
        )

        self.div = plot(fig, include_plotlyjs=False, output_type='div')



from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import shutil

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__, template_folder='templates/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 900*1000*1000


@app.route("/")
def home():
    folder = 'uploads'
    if os.path.isdir(os.path.join(os.getcwd(), folder)):
        shutil.rmtree(os.path.join(os.getcwd(), folder))
        os.mkdir(os.path.join(os.getcwd(), folder))
    path = os.getcwd()
    UPLOAD_FOLDER = os.path.join(path, 'uploads')
    return render_template('index.html')

@app.route("/plot", methods=['POST'])
def file():
    files = request.files.getlist('file[]')
    for f in files:
        fname = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))

    obj = Plot3d(UPLOAD_FOLDER)
    
    obj.div = obj.div.replace('height:800px; width:800px;', 'width:50%; margin: 0 auto') 
    
    return render_template('plot.html', data=obj.div)


app.run()