"""Sarus library to leverage sensitive data withou revealing them

This lib contains classes and method to browse, learn from & explore sensitive datasets.
It connects to a Sarus server, which acts as a gateway, to ensure no results/analysis coming out of this lib are sensitive.
"""

import requests
import tempfile
import tarfile
import cloudpickle, pickle
import tensorflow as tf
import io
import re
import json
import matplotlib.pyplot as plt
from tensorflow.keras.utils import Progbar
import time
import getpass


class Dataset():
    """
    A class based on tf.data.dataset to provide a representation of datasets used by Sarus, remotely.
    To be shared by client & server.
    """
    def __init__(self, name,id, type_metadata=None, URI=None, human_description=None, marginals=None, columns=None):
        self.name=name
        self.id=id
        self.parquet_dataset=None #TO BE REMOVED ??
        try:
            self.type_metadata=json.loads(type_metadata)
        except:
            self.type_metadata=None
        self.URI=URI
        self.columns=columns
        self.human_description=human_description
        self.synthetic=None
        try:
            self.marginals=json.loads(marginals)
        except:
            self.marginals=None

    def _inputs():
        return None
    def element_spec():
        return None

    def set_real_data(self,parquet_dataset):
        """ upload the data into the dataset
        """
        self.parquet_dataset=parquet_dataset

    def set_synthetic_data(self,data):
        """ upload the data into the dataset
        """
        self.synthetic=data

    def set_set_marginals(self,data):
        """ upload the data into the dataset
        """
        self.marginals=data

    def _plot_marginal_feature(self, marginal_feature, width=1.5, heigth=1.5):
        if "statistics" not in marginal_feature:
          return None

        # text-based representations
        # count for categories
        distrib= marginal_feature['statistics'].get('distribution')
        if distrib:
            html_response="<p><div>"
            distrib_s=sorted(distrib, key= lambda x:-x['probability'])
            if len(distrib_s)>5:
                others_count=len(distrib_s)-5          
                others_sum = sum([x['probability'] for x in distrib_s[5:]])
                distrib_s=distrib_s[0:5]

                distrib_s.append({'name':f'Other ({others_count})','probability':others_sum})
            for item in distrib_s:
                html_response+=f"<div class='category'>\
                  <div class='category_name'>\
                    {item['name']}\
                  </div>\
                  <div class='category_proba'> {round(100*item['probability'],2)}%</div>\
                </div>"
            html_response+="</div></p>"
            return html_response

        # Graph-based representation
        plt.figure(figsize=(width,heigth))
        # cumulDistribution for real
        cumul=marginal_feature['statistics'].get('cumulativeDistribution')
        if cumul:
            try:
              plt.fill_between([vp['value'] for vp in cumul], [vp['probability'] for vp in cumul])
            except:
              pass
        fi = io.BytesIO()
        plt.tight_layout()
        plt.savefig(fi, format = "svg")
        plt.clf()
        svg_dta = fi.getvalue()  # this is svg data
        return (svg_dta.decode())
    
    def to_html(self):
        """
        return a HTML representation of this dataset, to be displayed in a Notebook for example.
        We'd like to render something like: https://www.kaggle.com/fmejia21/demographics-of-academy-awards-oscars-winners
        Typical usage in a Jupyter Notebook is: 
           TODO
        """
        css="<style> table { \
        border-collapse: collapse;\
        } \
        .category {\
        width:100%;\
        display:block;\
        }\
        .category_name {\
        font-weight: 700;\
        width:60%;\
        float: left;\
        }\
        .category_proba {margin-left: 8px;\
        color: rgb(0, 138, 188);\
        float:right}\
        th {min-width:160px;}\
        table, th, td { \
         border: 1px solid rgb(222, 223, 224); \
         }</style>"

        synthethic_bool=(self.synthetic != None)
        table=f"<table><tr>\n"
        columns=self.type_metadata['features']
        for c in columns:
          table+=f"<th>{c['name']}</th>\n"

        table+="</tr><tr>"

        columns=self.type_metadata['features']
        for c in self.marginals['features']:
            table+=f"<td>{self._plot_marginal_feature(c)}</td>\n"
        table+="</tr><tr>"
        for c in columns:
          table+=f"<td>{c['type']}</td>\n"

        table+=f"</tr></table>"

        return f"<html>{css}<body>\n \
                    Dataset: {self.name} \n \
                    <p>Available synthetic data:{synthethic_bool}</p>\n \
                    <p>Descrition of the data:{self.human_description}</p>\n \
                   {table}\
                 </body></html>"

"""
class Projection(Dataset):
    #sub-dataset, to define X and Y
    
    def __init__(self, dataset, columns):
        self.dataset=dataset
        self.columns=columns
"""

class Client:

    def _url_validator(self, url):
        """
        From https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
        """
        regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return (re.match(regex, url) is not None) 

    def __init__(self, url="http://0.0.0.0:5000", username=None, password=None, verify=True):
        # verify: if False, doesn't check SSL certificate if protocol is https
        # for future use: TODO : self.progress_bar = Progbar(100, stateful_metrics=None)


        if self._url_validator(url):
            self.base_url=url
        else:
            raise Exception(f'Bad url')
        self.verify=verify
        if not password:
            password=getpass.getpass(prompt='Password: ', stream=None) 
        try:
            request = requests.post(f'{self.base_url}/login',
            json={'username':username,'password':password},
            headers={'Content-Type': 'application/json'}, verify=self.verify)
            self.cookies=request.cookies
            request.raise_for_status()
        except:
            raise Exception(f'Error during login')
        
    def available_datasets(self):
        request = requests.get(f'{self.base_url}/datasets', cookies=self.cookies, verify=self.verify)
        return [ds["name"] for ds in request.json()]

    def fetch_dataset_by_id(self, id):
        """ Return a dataset

        Used to get access to the object
        """
        try:
            request = requests.get(f'{self.base_url}/datasets/{id}', cookies=self.cookies, verify=self.verify)
            dataset = pickle.loads(request.content)
            return dataset
        except Exception as e:
            raise Exception(f'Dataset not available')

    def fetch_dataset_by_name(self, name):
        """ Return a dataset

        Used to get access to the object
        """
        try:
            request = requests.get(f'{self.base_url}/datasets/name/{name}', cookies=self.cookies, verify=self.verify)
            dataset = pickle.loads(request.content)
            return dataset
        except Exception as e:
            raise Exception(f'Dataset not available')

    def fit_v1(self,transform_def,keras_model_def, dataset, non_DP_training=False):
        """ Return a training task ID

        Launches remotely the training of a model, passed in keras_model_def
        """
        request = requests.post(f'{self.base_url}/fit_v1',
            data=cloudpickle.dumps((transform_def, keras_model_def, dataset.id, non_DP_training)),
            headers={'Content-Type': 'application/octet-stream'}, cookies=self.cookies, verify=self.verify)
        # for future use: TODO self.progress_bar.update(1, values=None)
        if request.status_code>200:
            raise Exception(f"Error while training the model. Full Gateway answer was:{request}")
        task_id=request.json()['task']
        self.poll_training_status(task_id)
        return task_id

    def fit(self,transform_def, keras_model_def, x=None, y=None, non_DP_training=False, **kwargs):
        """ NEW SIGNATURE!
        X and Y are columns
        non_DP_training: allows to also train the model without Differential Privacy, to assess performance difference
         Returns a training task ID

        Launches remotely the training of a model, passed in keras_model_def
        """
        request = requests.post(f'{self.base_url}/fit',
            data=cloudpickle.dumps((transform_def, keras_model_def, x, y, non_DP_training, kwargs)),
            headers={'Content-Type': 'application/octet-stream'}, cookies=self.cookies, verify=self.verify)
        if request.status_code>200:
            raise Exception(f"Error while training the model. Full Gateway answer was:{request}")
        task_id=request.json()['task']
        self.poll_training_status(task_id)
        return task_id

    def training_status(self, id):
        """ Return a string with the status of a training tasks

        id is the task ID provided by the fit method
        """

        request = requests.get(f'{self.base_url}/tasks/{id}', cookies=self.cookies, verify=self.verify)
        return request.json()

    def poll_training_status(self, id, timeout=1000): #timeout in sec
        """ Return a string with the status of a training tasks

        id is the task ID provided by the fit method
        """
        import base64
        elapsed_time=0.0
        while elapsed_time<timeout:
            elapsed_time+=0.5
            request = requests.get(f'{self.base_url}/tasks/{id}', cookies=self.cookies, verify=self.verify)
            response_dict=request.json()
            if 'progress' in response_dict:
                progress=base64.b64decode(response_dict['progress'].encode('ascii')).decode('ascii')
                print (progress, end='\r')
            else:
                # this is the end of the training
                break
            time.sleep(0.5)

    def fetch_model(self, id):
        """ Return a model

        For naming convention, see https://stackoverflow.com/questions/2141818/method-names-for-getting-data
        """
        response = requests.get(f'{self.base_url}/models/{id}', cookies=self.cookies, verify=self.verify)
        # apparently we need to save to a temp file, this is stupid but...
        # https://github.com/keras-team/keras/issues/9343
        with tempfile.TemporaryDirectory() as _dir:
            f = tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz")
            f.extractall(_dir)

            return tf.keras.models.load_model(_dir)
