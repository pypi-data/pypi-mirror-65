<h1>sklearnkernels</h1>

<b>sklearn-kernels:</b> extend functionality SVM and ANN classification and regression implementation <br/>
with alternative kernels proposed by Belanche.

the kernel hyperparameter manage is similar to SVM kernel parameter of sklearn library and could be some<br/>
member in brackets of  next list
<ul>
    <li>Gausian     (mrbf)</li>
    <li>Canberra    (can)</li>
    <li>Truncated   (tru)</li>
    <li>Hyperbolic  (hyperbolic)</li>
    <li>Triangular  (triangle)</li>
    <li>Radial Basic(radial_basic)</li>
    <li>Rational Quadratic(rquadratic)</li>
</ul>




<h1>Install</h1>


To install the library use pip:

    pip install sklearn-kernels


or clone the repo and just type the following on your shell:

    python setup.py install

<h1>Usage examples</h1>



Example of usage:



```python
from sklearnkernels.KSVM import KSVC, KSVR
from sklearnkernels.KANN import KANNC,KANNR
```


```python
from sklearn import  datasets
from sklearn.model_selection import train_test_split
iris = datasets.load_iris()
Xc = iris.data
yc = iris.target
X_fc, X_tc, y_fc, y_tc = train_test_split(Xc, yc, test_size=0.25, random_state=0)
svc=KSVC(kernel='tru', C=100,gamma=0.001,degree=2)
svc.fit(X_fc, y_fc)
print('cmlfc',svc.score(X_tc,y_tc))

```

    cmlfc 0.9210526315789473
    


```python
Xr, yr = datasets.load_boston(return_X_y=True)
X_fr, X_tr, y_fr, y_tr = train_test_split(Xr, yr, test_size=0.25, random_state=0)
svr=KSVR(kernel='can', C=10,  gamma=300)
svr.fit(X_fr, y_fr)
print('clflr',svr.score(X_tr,y_tr))
```

    clflr 0.7079035547838508
    


```python
annc=KANNC(kernel='rbf',gamma=.25,random_state=0)
annc.fit(X_fc, y_fc)
print('clfk',annc.score(X_tc,y_tc)) 
```

    clfk 0.8947368421052632
    


```python
annr=KANNR(kernel='linear', gamma=1, early_stopping=True, max_iter=5000, random_state=0)
annr.fit(X_fr, y_fr)
print('clfk',annr.score(X_tr,y_tr))
```

    clfk 0.5629257343580683
    
