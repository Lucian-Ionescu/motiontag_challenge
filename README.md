# Hi guys!
Initially I was wondering why that GPS track absolutely does not align to any street or subway network. Nice one!
I did not use that geo-stuff for a long time, so indeed it was a challenge to get used to it again.

Does anyone of you live in Katharinenholzstr. 26b in Potsdam? That one outlier looks far too intentional!

# What I did
I implemented the dynamic thresholding for accuracy and velocity and a simple decision tree model. For this small data sample with just two features, results are almost identical – except one of the rear legs.  

1. Most importantly, see the notebook
```./notebooks/analysis.ipynb```
for retracing the process and my comments ([Click here for the HTML version](./notebooks/analysis.html)).


2. I created the dockerized Flask API. You can select whether you want to use simple thresholding or decision tree for classification.
   Also, you can send labels along with the data, which triggers an evaluation in the server side console output. 
   Ok, I feel that you know all of this, but here are some instructions:
   For building the Docker image, run:
   ```docker build . -t motiontag_challenge```
   Run the container:
   ```docker run -p 10400:10400 -t -i motiontag_challenge:latest```
   Or simply use the bash script:
   ```./start_service.sh```.


3. For testing the API there are multiple ways to do that:
    - Again, have a look at ```./notebooks/analysis.ipynb```, it retrieves filtered data from the API and draws (a rather expressionistic version of) the bear.   
    - A demo Python script, wrapped in ```./demo.sh```: make sure you have the packages installed, e.g. by:
      ```conda env create -f environment.yml; conda activate motiontag-challenge```.


# What I did not do
1. All the good stuff: unit testing, docstrings. I will do that with great pleasure once I am paid for it :)
2. The API won't win a prize for being failsafe or verbose.
3. The API is not that efficient (0.5sec for filtering the given dataset) since I re-used analytical code from the Jupyter notebook (especially geopandas dataframes).
You know, the usual nasty data science code that makes its way into production...
   
### So far, see you soon!