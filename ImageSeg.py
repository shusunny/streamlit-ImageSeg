from enum import auto
import streamlit as st
import numpy as np
import numpy.matlib
import random
from PIL import Image

def init_centroids(X,K):
    c = random.sample(list(X),K)
    return c

# compute the distance to the closest centroid
def closest_centroids(X,c):
    K = np.size(c,0)
    idx = np.zeros((np.size(X,0),1))
    arr = np.empty((np.size(X,0),1))
    for i in range(0,K):
        y = c[i]
        temp = np.ones((np.size(X,0),1))*y
        b = np.power(np.subtract(X,temp),2)
        a = np.sum(b,axis = 1)
        a = np.asarray(a)
        a.resize((np.size(X,0),1))
        arr = np.append(arr, a, axis=1)
    arr = np.delete(arr,0,axis=1)
    idx = np.argmin(arr, axis=1)
    return idx

# compute the new centroids
def compute_centroids(X,idx,K):
    n = np.size(X,1)
    centroids = np.zeros((K,n))
    for i in range(0,K):
        ci = idx==i
        ci = ci.astype(int)
        total_number = sum(ci)
        ci.resize((np.size(X,0),1))
        total_matrix = np.matlib.repmat(ci,1,n)
        ci = np.transpose(ci)
        total = np.multiply(X,total_matrix)
        centroids[i] = (1/total_number)*np.sum(total,axis=0)
    return centroids

# run kmeans function
def run_kMean(X,initial_centroids,max_iters):
    m = np.size(X,0)
    n = np.size(X,1)
    K = np.size(initial_centroids,0)
    centroids = initial_centroids
    previous_centroids = centroids
    idx = np.zeros((m,1))
    for i in range(1,max_iters):
        idx = closest_centroids(X,centroids)
        centroids = compute_centroids(X,idx,K)
    return centroids,idx


# Main function
def image_seg(img, K, max_iters):
    image = np.asarray(img)
    rows = image.shape[0]
    cols = image.shape[1]
    image = image/255
    X = image.reshape(image.shape[0]*image.shape[1],3)

    initial_centroids = init_centroids(X,K)
    centroids,idx = run_kMean(X,initial_centroids,max_iters)
    idx = closest_centroids(X,centroids)
    X_recovered = centroids[idx]
    X_recovered = np.reshape(X_recovered, (rows, cols, 3))
    result = Image.fromarray((X_recovered * 255).astype(np.uint8))
    return result


st.title("Image Segmentation with K-means")
st.markdown('Please assign clusters and upload a picture to start.')

# Upload and enter params
num_clusters = st.sidebar.slider("Number of clusters(colors)", 1, 24, 8)
num_iters = st.sidebar.slider("Number of iterations", 1, 100, 30)
img_upload = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg"])

if img_upload is not None:
    image = Image.open(img_upload)	
    st.subheader('Original Image:')
    st.image(img_upload, caption="Original Image", use_column_width= auto)

    res = image_seg(image, num_clusters, num_iters)
    st.subheader('Segmented result:')
    st.image(res, caption="Segmented Image",use_column_width= auto)
    im = res.save("result.jpg")
    
    with open("result.jpg", "rb") as file:
        btn = st.download_button(
                label="Download",
                data=file,
                file_name="result.jpg",
                mime="image/png"
            )