

import numpy as np
from scipy.optimize import minimize
from functools import partial


from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import pysptools.eea.eea
import math
from tqdm import tqdm
        


"""All intitialisation methods to extract the endmembers"""
################################################################################################################################

class KmeansInit: #Kmeans initialisation
    @classmethod
    def initialisation(cls, x, nb_c, n_init=10):

        s = KMeans(n_clusters=nb_c, n_init = n_init).fit(x).cluster_centers_

        return s

################################################################################################################################

class MBKmeansInit: #Mini Batch Kmeans (plus rapide mais moins robuste)
    @classmethod
    def initialisation(cls, x, nb_c):
        
        ctr_k = MiniBatchKMeans(n_clusters = nb_c).fit(x)
        s = ctr_k.cluster_centers_
        
        return s
################################################################################################################################

class NFindrInit:
    @classmethod
    def initialisation(cls, x, nb_c):
        size0 = x.shape[0]
        size1 = x.shape[1]
        xr = np.reshape(x, (1, size0, size1) ) # NFindr travaille avec des jeux de données 3D...
        s = pysptools.eea.NFINDR.extract(cls, xr, nb_c)
        
        return s

################################################################################################################################
   
class RobustNFindrInit:
    @classmethod
    def initialisation(cls, x, nb_c, fraction = 0.1, min_spectra = 50, nb_i = 50): # Initialisaiton KMeans + NMF / Voir avec Ryan Gosselin pour les explications et évolutions
        """
        fraction : Fraction du jeu de données par échantillon
        min_spectra : minimum de spectre pour garder un échantillong
        nb_i : nombre d'échantillons à créer
        """
        
        
        def km(x, nb_c):
            k = KMeans(n_clusters=nb_c).fit(x)
            IDX = k.labels_
            C = k.cluster_centers_
            return IDX, C
        
        
        s1 = x.shape[0]
        
        fX = math.ceil(s1*fraction)

        
        BESTC = np.array(())
       
        DETC = 0
        for i in tqdm(range(nb_i)):
            
            randomVector = np.random.choice(s1, fX, replace = False)# Create random vector with unique values
            sampX = x[randomVector,:]#Pick a sample in x according to the randomVector
            
            #Run Kmeans
            IDX, C = km(sampX, nb_c)
            
            #Check Number of pixels in each kmeans centroid
            U, nbU = np.unique(IDX, return_counts=True);
            
            
            if min(nbU) > min_spectra: #Do not keep this bootstrap if too few pixels fall in a category
                a = np.zeros((nb_c,1)) + 1 #Start NMF
                C1 = np.column_stack((a, C))
                CC = C1@C1.T
                detc = np.linalg.det(CC)
                if detc > DETC:
                    DETC = detc
                    BESTC = np.copy(C)
                    #print(nbU)
                                           
        return BESTC
    
################################################################################################################################

class RobustNFindrV2Init:
    @classmethod
    def initialisation(cls, x, nb_c, fraction = 0.1, min_spectra = 50, nb_i = 50):
        """
        fraction : Fraction du jeu de données par échantillon
        min_spectra : minimum de spectre pour garder un échantillong
        nb_i : nombre d'échantillons à créer
        """
        
        def km(x, nb_c):
            k = KMeans(n_clusters=nb_c).fit(x)
            IDX = k.labels_
            C = k.cluster_centers_
            return IDX, C
        
        s1 = x.shape[0]
        f = fraction # Fraction to keep in each bootstrap
        fX = math.ceil(s1*f)

        allS = np.array(())


        for i in tqdm(range(nb_i)):
            randomVector = np.random.choice(s1, fX, replace = False)# Create random vector with unique values
            sampX = x[randomVector,:]#Pick a sample in x according to the randomVector
    
        #Run Kmeans
            IDX, C = km(sampX, nb_c)
        
            #Check Number of pixels in each kmeans centroid
            U, nbU = np.unique(IDX, return_counts=True);

            #print(nbU)
            if min(nbU) > min_spectra: #Do not keep this bootstrap if too few pixels fall in a category
                try:
                    allS = np.vstack((allS, C));
                except ValueError:
                    allS = np.copy(C)
        
        size0 = allS.shape[0]
        size1 = allS.shape[1]
        allS = np.reshape(allS, (1, size0, size1) ) # NFindr travaille avec des jeux de données 3D...
        s = pysptools.eea.NFINDR.extract(cls, allS, nb_c)
                    
        return s
    
################################################################################################################################

class AtgpInit: # Automatic Target Generation Process
    @classmethod
    def initialisation(cls, x, nb_c):
        
        s = pysptools.eea.eea.ATGP(x, nb_c)
        
        return s[0]
    
################################################################################################################################
    
class FippiInit: # Fast Iterative Pixel Purity Index
    @classmethod
    def initialisation(cls, x, nb_c):
        
        t = pysptools.eea.eea.FIPPI(x, q = nb_c)
        
        s = t[0]
        s = s[:nb_c, :]
        
        return s
  
################################################################################################################################
    
class PpiInit: # Pixel Purity Index
    @classmethod
    def initialisation(cls, x, nb_c):
        numSkewers = 10000
        s = pysptools.eea.eea.PPI(x, nb_c, numSkewers)
        
        return s[0]   
 
    
################################################################################################################################
class nKmeansInit:    
    @classmethod
    def initialisation(cls, x, nb_c, n = 15): 
        
        """Sometimes it's necessary to run Kmeans for more component than we want, to get the expected spectras, this version runs
        the initialisation for nb_c + n components, and keep the nb_c centroids containing the most pixels"""

        
        nb_ci = nb_c + n 
        
        init = KMeans(nb_ci).fit(x)
        s = init.cluster_centers_
        lab = init.labels_
        
        U, nbU = np.unique(lab, return_counts=True);# nbU is the number of pixels in each centroid
        
        ind = nbU.argsort()[-nb_c:] # Get the indices of the nb_c centroids containing the most pixels
        
        s = s[ind,:] # Keep only the nb_c spectra
        
        
        return s



    
    
    





def pcanipals(Xh,A,it=1000,tol=1e-4):
   
    
    obsCount,varCount = np.shape(Xh);
    T = np.zeros([obsCount,A]);
    P = np.zeros([varCount,A]);
    nr = 0;
    
    for a in range(A):
        
        th = np.array([Xh[:,0]]).T;
        ende = False;
    
        while(ende==False):
            
            nr+=1
            ph=Xh.T@th/np.linalg.inv(th.T@th)
            ph=ph/np.linalg.norm(ph)
            thnew=Xh@ph
            prec = (thnew-th).T@(thnew-th)
            th=thnew
            
            if(prec<=tol**2):
                ende=True
            elif(it<=nr):
                ende=True
    
        Xh = Xh - th@ph.T
        T[:,a] = th[:,0]
        P[:,a] = ph[:,0]
    
    return T,P
    
    





class mcrllm:
    
    
    def __init__(self,X,nb_c,method="standard",fact_ini=.5):
        
        # Save Xraw and normalize data
        self.Xraw = X.copy()
        self.Xsum = np.sum(X,axis=1)
        self.X = X/np.array([np.sum(X,axis=1)]).T
        
        self.pix,self.var = np.shape(self.X)
        self.nb_c = nb_c
        self.method = "phi" ################## self.method = method
        self.expvar = np.inf
        self.fact_ini = .5
        
        # History initialization
        self.allC = []
        self.allS = []
        self.allphi = []
        
        
        self.C = np.ones([self.pix,self.nb_c])/nb_c
        
        # PCA reconstruction
        X_m = np.array([np.mean(self.X,axis=0)])
        X_s = np.array([np.std(self.X,axis=0)])
        Xpca = (self.X - X_m)/X_s
        T,P = pcanipals(Xpca,nb_c-1)
        self.Xrec = (T@P.T)*X_s+X_m
            
        # Initialization
        self.Sini = KmeansInit.initialisation(self.X, nb_c)
        #if(np.sum(self.Sini <= 0)>0):
        #    raise("Bas initialization")
        self.S = self.Sini.copy()
        
        
    
    def iterate(self,nb_iter=1):
        
        for iteration in range(nb_iter):
            #print("Iteration {:.0f}".format(len(self.allS)+1))
            self.C_plm()
            self.S_plm()
            
            
            
    
    def C_plm(self):
        
        c_new = np.zeros((self.pix,self.nb_c))
        

        # on calcule les concentrations optimales pour chaque pixel par maximum likelihood 
        for pix in range(self.pix):
            sraw = self.S*self.Xsum[pix]
            c_new[pix,:] = self.pyPLM(sraw, self.Xraw[pix,:], self.C[pix,:])
                
                
        # avoid errors (this part should not be necessary)
        c_new[np.isnan(c_new)] = 1/self.nb_c
        c_new[np.isinf(c_new)] = 1/self.nb_c
        c_new[c_new<0] = 0
        c_sum1 = np.array([np.sum(c_new,axis=1)]).T
        c_new = c_new/c_sum1

        self.C = c_new.copy()
        self.allC.append( c_new.copy() )
    
            
        
        
    
    def Sphi(self,phi,h):
    
        C_m = self.C**phi
            
        S = np.linalg.inv(C_m[h,:].T@C_m[h,:])@C_m[h,:].T@self.X[h,:]
        S[S<1e-15] = 1e-15
        S = S/np.array([np.sum(S,axis=1)]).T
        
        return S
    
    
    
    
    def S_plm(self):
        
        
        h = np.random.permutation(len(self.X))
        phi_optimal = 1
        
        if self.method == "phi":
            allMSE = []
            all_phis = np.arange(.1,10.1,.1)
            
            for phi in all_phis:
                S = self.Sphi(phi,h)
                allMSE.append(np.sum( (S-self.S)**2 ))
                
            phi_optimal = all_phis[np.argmin(allMSE)]
            self.S = self.Sphi(phi_optimal,h)
            
            
                    
        else: # Standard
            
            self.S =  self.Sphi(phi_optimal,h)
            
            
        self.allS.append( self.S.copy() )
        self.allphi.append(phi_optimal)
        
        
        
    
    
    def pyPLM(self, sraw, xrawPix, c_old):
        

        # sum of every value is equal to 1
        def con_one(c_old):
            return 1-sum(c_old) 
        
        
        
        def regressLLPoisson(sraw,  xrawPix, c_pred):
            
            #compute prediction of counts
            yPred = c_pred @ sraw
            nb_lev = len(yPred) #?
            # avoid errors, should (may?) not be necessary
            yPred[yPred < 1/1000000] = 1/1000000
            logLik = -np.sum(xrawPix*np.log(yPred)-yPred)
            return (logLik)
        
        
        
        def jacobians(nb_c, xrawPix, sraw, c_pred):

            #compute prediction of counts
            yPred = c_pred @ sraw
            
            #compute jacobians
            jacC = np.zeros(nb_c)
            
            for phase in range(nb_c):    
                jacC[phase] = -np.sum(((xrawPix*sraw[phase,:])/yPred)-sraw[phase,:])    
            return(jacC) 
        
        
        
        # all values are positive
        bnds = ((0.0, 1.0),) * self.nb_c
        cons = [{'type': 'eq', 'fun': con_one}]
   
                
        # Run the minimizer    
        results = minimize(partial(regressLLPoisson, sraw,  xrawPix), c_old,\
                           method='SLSQP', bounds=bnds, constraints=cons, \
                           jac = partial(jacobians, self.nb_c, xrawPix, sraw))
        results = np.asarray(results.x)
        

        c_new = results.reshape(int(len(results) / self.nb_c), self.nb_c)
        
        
        return c_new
        
        
    
    

        