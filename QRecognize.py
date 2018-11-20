from preprocess import *
from align import *
from absl import app
from absl import flags
FLAGS = flags.FLAGS
flags.DEFINE_bool('rotate', False, 'if the QR direction is not standard.')

def main(argv):
    if FLAGS.rotate:
        path = "image/QR_rotated.jpeg"
        corners = [np.array([254, 124]), 
           np.array([106, 910]),
           np.array([1038, 288]),
           np.array([847, 993])]
    else:
        path = "image/QR.jpeg"
        corners = [np.array([168, 106]), 
           np.array([86, 847]),
           np.array([955, 254]),
           np.array([790, 1037])]
    
    image = ReadImage(path, threshold=90)
    H = GetTransform(corners)
    wrapped = WrapImage(image, H)
    # ShowImage(wrapped)

    _TYPE = RecReco(wrapped)
    rotated = RotateImage(wrapped, _TYPE)
    ShowImage(rotated)


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')    

    app.run(main)