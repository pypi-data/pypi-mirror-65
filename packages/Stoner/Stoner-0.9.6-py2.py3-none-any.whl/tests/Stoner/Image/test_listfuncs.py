# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 19:21:48 2016

@author: phyrct
"""
from Stoner.Image import ImageArray,ImageFile
from Stoner.HDF5 import STXMImage
import unittest
from os.path import dirname,join
import numpy as np
from lmfit.models import LorentzianModel
import matplotlib.pyplot as plt

thisdir=dirname(__file__)

def mag(x):
    return np.sqrt(np.dot(x,x))

class FuncsTest(unittest.TestCase):

    def setUp(self):
        self.a=ImageArray(join(thisdir,'coretestdata/im2_noannotations.png'))
        self.a1=ImageArray(join(thisdir,'coretestdata/im1_annotated.png'))
        self.a2=STXMImage(join(thisdir,"..","..","..","sample-data","Sample_Image_2017-10-15_100.hdf5"))
        self.a3=STXMImage(join(thisdir,"..","..","..","sample-data","Sample_Image_2017-10-15_101.hdf5"))


    def test_imagefile_ops(self):
        self.a2.gridimage()
        self.a3.gridimage()
        self.a2.crop(5,-15,5,-5,_=True)
        self.a3.crop(5,-15,5,-5,_=True)
        self.b=self.a2//self.a3
        self.assertEqual(self.b.shape,(90,80),"Failure to crop image correctly.")
        self.assertGreater(self.b.max(),0.047,"XMCD Ratio calculation failed")
        self.assertLess(self.b.min(),-0.05,"XMCD Ratio calculation failed")
        self.b.normalise()
        self.assertEqual(self.b.max(),1.0,"Normalise Image failed")
        self.assertEqual(self.b.min(),-1.0,"Normalise Image failed")
        self.profile=self.b.profile_line((0,0),(100,100))
        self.profile.plot()
        self.b.mask=self.a2.image>25E3
        self.hist=self.b.hist(bins=200)
        self.hist.column_headers=["XMCD Signal","Frequency"]
        self.hist.labels=None
        g1=LorentzianModel(prefix="g1_")
        g2=LorentzianModel(prefix="g2_")
        params=g1.make_params()
        params.update(g2.make_params())
        double_peak=g1+g2
        g1=np.argmax(self.hist.y[:100]) # Location of first peak
        g2=np.argmax(self.hist.y[100:])+100
        for k, p in zip(params,[0.25,self.hist.x[g1],self.hist.y[g1]/np.sqrt(2),0.5,self.hist.y[g1],
            0.25,self.hist.x[g2],self.hist.y[g2]/np.sqrt(2),0.5,self.hist.y[g2]]):
            params[k].value=p
        print(g1,g2,params)
        self.res=self.hist.lmfit(double_peak,p0=params,output="report")
        self.hist.add_column(self.res.init_fit,header="Initial Fit")
        self.hist.add_column(self.res.best_fit,header="Best Fit")
        self.hist.setas="xyyy"
        self.hist.plot(fmt=["b+","b--","r-"])
        plt.close("all")


        #self.b.adnewjust_contrast((0.1,0.9),percent=True)z

    def test_funcs(self):
        b=self.a.translate((2.5,3))
        self.c=b.correct_drift(ref=self.a)
        self.d=b.align(self.a,method="scharr")
        tv=np.array(self.d["tvec"])*10
        cd=np.array(self.c["correct_drift"])*10
        shift=np.array([25,30])
        d1=mag(cd-shift)
        d2=mag(tv-shift)
        self.assertLess(d1,1.5,"Drift Correct off by more than 0.1 pxiels.")
        self.assertLess(d2,1.5,"Scharr Alignment off by more than 0.1 pxiels.")
#        print("#"*80)
#        print(self.a.metadata)
#        print(self.a1.metadata)
#        print(all([k in self.a.metadata.keys() for k in self.a1.metadata.keys()]))

    def test_imagefuncs(self):
        self.a2.subtract_image(self.a2.image,offset=0)
        self.assertTrue(np.all(self.a2.image<=0.0001),"Failed to subtract image from itself")
        x=np.linspace(-3*np.pi,3*np.pi,101)
        X,Y=np.meshgrid(x,x)
        i=ImageFile(np.sin(X)*np.cos(Y))
        i2=i.clone
        j=i.fft()
        self.assertTrue(np.all(np.unique(np.argmax(j,axis=1))==np.array([47,53])),"FFT of image test failed")
        j.imshow()
        self.assertTrue(len(plt.get_fignums())==1,"Imshow didn't open one window")
        plt.close("all")
        self.a2.imshow(title=None,figure=None)
        self.a2.imshow(title="Hello",figure=1)
        self.assertTrue(len(plt.get_fignums())==1,"Imshow with arguments didn't open one window")
        plt.close("all")
        i=i2
        k=i+0.2*X-0.1*Y+0.2
        k.level_image(mode="norm")
        j=k-i
        self.assertLess(np.max(j),0.01,"Level Image failed")
        i2=i.clone
        i2.quantize([-0.5,0,0.5])
        self.assertTrue(np.all(np.unique(i2.data)==np.array([-0.5,0,0.5])),"Quantise levels failed")
        i2=i.clone
        i2.quantize([-0.5,0,0.5],levels=[-0.25,0.25])
        self.assertTrue(np.all(np.unique(i2.data)==np.array([-0.5,0,0.5])),"Quantise levels failed")
        i2=i.clone
        i2.rotate(np.pi/4)
        i2.fft()
        self.assertTrue(np.all(np.unique(np.argmax(i2,axis=1))==np.array([46, 47, 49, 50, 51, 53])),"FFT of image test failed")




if __name__=="__main__": # Run some tests manually to allow debugging
    test=FuncsTest("test_funcs")
    test.setUp()
    #test.test_imagefile_ops()
    #test.test_imagefuncs()
    unittest.main()

