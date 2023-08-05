"""
MGSampler
=========

MGSampler is a simple class generating a sample of data following 
the distributions of a training sample as a function of a set of 
input variables. 

The objective is obtain a sample G(X,y) where the y variables are 
computed as a function of X to follow the distribution p(y|X) that
is learned from a reference sample R(X,y). 

The procedure can be logically split in three steps:
  1. Preprocessing of the input variables. The X variables are preprocessed
     using a FastQuantileLayer to avoid any assumption on the shape and 
     distribution of the input variables X.
     The preprocessing of the y variables is critical for the quality 
     of the obtained parametrization and can be obtained with the following 
     three strategies:
      * do nothing (`preprocessing=None`, default): the preprocessing is demanded 
        to the client application.
      * linear preprocessing (`preprocessing='linear'`): the y variables are 
        subtracted by their average and divided by their mean. 
        This ease the optimization without modifying the shape of the output 
        distribution. If the latter is vaguely similar to a Gaussian, linear 
        preprocessing is ideal. If the distributions include sharp boundaries, 
        the optimization upon linear preprocessing is likely to fail. 
      * Gaussian preprocessing (`preprocessing='normal'): the y variables are 
        mapped into normal distributions through sampled functions obtained 
        from the quantiles of the distribution. The inversion of this 
        function is performed at the training time to guarantee fast evaluation. 
        Both the direct and the inverse functions are approximated via 
        linear interpolation between adjacent samples, this makes the 
        computation of gradients through the approximated functions too noisy
        for any optimization procedure. The sample obtained MGSampler with 
        Gaussian preprocessing can show small artifacts in the distributions 
        due to imperfect approximations of the cumulative distribution and 
        of its inverse. Still, for modelling many real-life distributions 
        there is no better alternative to Gaussian preprocessisng. 
  2. Fit of the distributions of the target variables Y with a sum
     of Gaussians:  sum_i ( w * G_i (y, mu, sigma )
     The weights, the means and the standard deviations of each 
     of the Gaussians is defined to be a function of the condition variables X
     (sometimes also called watcher variables).
  3. Random generation of a normally distributed dataset and 
     trasformation into the target dataset through:
      * shift (according to mu(X);
      * scaling (according to sigma(X);
      * random selection (according to  w(X)). 


Example
-------
The code snippet below trains a sampler on a random dataset and generates
a random sample of y variables on top of the same X variables used for training.
```
import numpy as np

## Generate a random dataset as an example
nSamples = 1000 
X = np.random.uniform ( -20, 10,  (nSamples,4)).astype (np.float32) 
y = np.random.uniform ( 0, 1,     (nSamples,2)).astype (np.float32) 

#from multigaussampler import MGSampler
## Creates and configure the MGSampler object
gp = MGSampler(X,y) 

## Train the MGSampler on the training dataset
from tqdm import trange
progress_bar = trange ( 100 )
for iEpoch in progress_bar:
  l = gp.train ( X,y ) 
  progress_bar.set_description ( "Loss: %.1f " % l ) 

## Sample the obtained parametrization
gp.sample (X) 
```


Saving the sampler
------------------
The `MGSampler` inherits from the `tf.Module` the serialization abilities.
```
## Compile the sample function to be run 4 input variables in float32 
gp.sample.get_concrete_function(tf.TensorSpec(shape=(None,X.shape[1]), dtype=np.float32)

## Save the model to an `export_dir`
import tensorflow as tf
tf.saved_model.save (gp, '/tmp/export_dir') 
```

To reload the model, from an environment where multigaussampler in installed, 
```
gp.sample.get_concrete_function(tf.TensorSpec(shape=(None,X.shape[1]), dtype=np.float32)

import tensorflow as tf
gp = tf.saved_model.load ('/tmp/export_dir') 
```

"""
import numpy as np 
import tensorflow as tf 
from FastQuantileLayer import FastQuantileLayer

class MGSampler ( tf.Module ):
  "Sampler based on an explicit pdf model trained using TensorFlow"
  def __init__ (self, X, y, nGaussians=10, preprocessing=None):
    """
    Initialize and configure the MGSampler.

    Arguments
    ---------
    
    X, y - *numpy.ndarray*
      A fraction of the training dataset used to compute the 
      preprocessing constant. The larger the fraction the more 
      accurate will be the obtained parametrization, but the slower
      the procedure will be (especially for `normal` preprocesisng).

    nGaussians - *integer, default: 10*
      Number of Gaussians *pdf* summed up to describe the input dataset 

    preprocessing - *string* or *None*, *default: `None`* 
      Type of preprocessing of the *y* variables, can be:
        * `None` or `'none'` to disable preprocessing, handled externally 
        * `'linear'` to shift the dataset by its mean and divide it by its std
        * `'normal'` to map the y variable into a normal distribution. Can be slow.
    """
    super(MGSampler,self).__init__() 

    if preprocessing is None: preprocessing = 'none' 
    if preprocessing.lower() not in ['none','linear','normal']:
      raise ValueError("Unexpected preprocessing mode: %s" % preprocessing )

    if len ( y.shape ) == 1: y = np.expand_dims(y, -1) 

    self._nvarsX = X.shape[1]
    self._nvarsY = y.shape[1] 
    self._preprocessing = preprocessing

    fastqlX = FastQuantileLayer (output_distribution='normal') 
    fastqlX . fit ( X ) 

    self.net = tf.keras.models.Sequential() 
    self.net . add (fastqlX) 

    self.net.add ( tf.keras.layers.Dense ( 128, activation = 'relu' ) )
    self.net.add ( tf.keras.layers.Dense ( 3*nGaussians*self._nvarsY ) )
    self.net.add ( tf.keras.layers.Reshape ( (nGaussians, 3, self._nvarsY) ) )

    ## Preprocessing setup 
    if preprocessing.lower() == 'normal':  
      self.fastqlY = FastQuantileLayer (output_distribution='normal')
      self.fastqlY . fit ( y ) 
    elif preprocessing.lower() == 'linear':  
      self._ymu  = np.mean(y,axis=0) 
      self._ys   = np.std (y,axis=0) 

    
  @tf.function
  def _yTransf (self, y, backward=False):
    "Internal. Preprocessing of the y variable according to self._preprocessing" 
    if self._preprocessing.lower() == 'none': return y 
    elif self._preprocessing.lower() == 'linear' : 
      if backward is True: return (y*self._ys + self._ymu) 
      return (y - self._ymu)/self._ys
    elif self._preprocessing.lower() == 'normal' : 
      return self.fastqlY.transform(y, inverse=backward)

  @tf.function
  def getPars (self, X):
    "Return the weight, means and sigmas of the y distribution at X."
    pars = tf.transpose (tf.cast( self.net(X), tf.float32), [1,0,2,3] ) 
    w  = tf.abs(pars[:,:,0,0])
    w /= tf.reduce_sum ( w, axis=0 ) #sum over gaussians 
    w  = tf.expand_dims ( w, -1 ) 
    mu = pars[:,:,1,:]
    s  = tf.clip_by_value ( tf.abs(pars[:,:,2,:]), 1e-8, 1e3 ) 

    return w, mu, s 

  @tf.function 
  def pdf (self, X, y):
    "Return the value of the multigaussian pdf computed in y at given X"
    yt = self._yTransf(y) 
    w, mu, s = self.getPars(X)
    return tf.reduce_sum (axis=0,
          input_tensor = w * ( 1./np.sqrt(2.*np.pi)/s * tf.exp ( -0.5 * tf.square((yt-mu)/s)) )
        )

  @tf.function
  def nll (self, X, y,  mean=False):
    """
    Return the Negative LogLikelihood of the multigaussian pdf for y at given X.

    Arguments
    ---------
      X, y: *tensorflow tensors*
        input dataset
      
      mean: *bool*
        Flag steering the computation of the loss. If True, the loss is divided by 
        the number of entries in (X, y). 
    """
    rf = tf.reduce_mean if mean is True else tf.reduce_sum
    return - rf( tf.math.log (tf.clip_by_value(self. pdf (X, y), 1e-12,1e12) ) )

  @tf.function #(input_signature = [tf.TensorSpec((None,None), tf.float32)])
  def sample (self, X):
    "Sample the multigaussian pdf" 
    w, mu, s = self.getPars(X)
    allG = tf.random.normal(tf.shape(mu),0,1) * s + mu
    ret = allG[0] 
    rnd = tf.random.uniform(tf.shape(ret),0,1) 
    w = tf.cumsum (w, axis=0) 

    for iGaus in range(1,tf.shape(mu)[0]):
      ret = tf.where ( rnd > w[iGaus-1], allG[iGaus], ret ) 

    return self._yTransf(ret , backward=True) 
      

  def train (self, X, y, learning_rate = 0.001):
    "Single-step in the maximum-likelihood fit procedure. Returns the loss." 
    with tf.GradientTape() as tape:
      loss = 2 * self.nll ( X, y ) 

    grads = tape.gradient(loss, self.net.trainable_variables) 
    optimizer = tf.keras.optimizers.Adam (learning_rate)

    optimizer . apply_gradients ( zip (grads, self.net.trainable_variables) )
    return loss 





if __name__ == '__main__':
  print ("TensorFlow version: ", tf.__version__) 

  ## Generate a random dataset as an example
  nSamples = 1000 
  X = np.random.uniform ( -20, 10,  (nSamples,4)).astype (np.float32) 
  y = np.random.uniform ( 0, 1,     (nSamples,2)).astype (np.float32) 

  #from multigaussampler import MGSampler
  ## Creates and configure the MGSampler object
  gp = MGSampler(X,y) 

  try: 
    from tqdm import trange
    with_tqdm = True
  except ImportError:
    trange = range
    with_tqdm = False

  ## Train the MGSampler on the training dataset
  progress_bar = trange ( 100 )
  for iEpoch in progress_bar:
    l = gp.train ( X,y ) 
    if with_tqdm: progress_bar.set_description ( "Loss: %.1f " % l ) 

  ## Sample the obtained parametrization
  gp.sample (X) 


