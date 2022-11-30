# Restful API
This repository contains the Restful API and its associated data.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# Install pre-requisites

Start a terminal on tensorflow/RestfulAPI and choose one of the following options:

Make sure you have pip installed. On ubuntu, run,
```
apt install python3-pip
```
and, then install the dependencies with...
```
pip install -r requirements.txt
```
# How to Run
- To run through flask, use the following
```
flask run
```
- To run through python (not recommended)
``` 
python app.py
```

For the current version, the output must be the following.
```
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000 (or your own designated address)
Press CTRL+C to quit
```
If this is not the case, please follow the error message thrown by flask or contact us.

# Making Requests
After receiving the output, go to http://127.0.0.1:5000 (or your own designated address).
For the current version, you must see a static page stating the following.
```
Not Found
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
```
To make a request to the API, you should add your parameters next to the stated address above in the following format.
```
/predict/<int:AVAILABILITY>/<int:REPUTATION>/<string:INTEREST>
```
An example would be for 60 hours of availability, 1500 score of reputation with the interests of "Machine Learning", "Java" and "Python" in the context of natural languages;
```
http://127.0.0.1:5000/predict/60/1500/I%20am%20a%20machine%20learning%20engineer%20with%20python%20and%20java%20knowledge

```
Note: For INTEREST, you can just write "REPUTATION/I am a machine learning engineer", you do not need to add '%20' in between every word.

Once you send your request, the terminal where you started the application should give an output like the following
```
127.0.0.1 - - [21/Nov/2022 17:57:13] "GET /predict/4000/4000/Im%20a%20machine%20learning%20engineer HTTP/1.1" 200 -
127.0.0.1 - - [21/Nov/2022 18:08:25] "GET / HTTP/1.1" 404 -
Files are Updated                     : 3.922396421432495
Filtered on Reputation                : 0.0030298233032226562 Remaining Jobs: 17290
Filtered on Availability              : 0.0030007362365722656 Remaining Jobs: 650
The remaining task ID's are collected : 0.0020029544830322266
Embeddings are collected              : 8.887234210968018
Annoy is built                        : 4.6339452266693115
Preprocessing of INTEREST is done     : 0.8352389335632324

<Description of the Jobs>
```
The float values after ":" is the taken time.
"Remaining jobs" indicates the number of jobs remaining after filtering through the given parameters.

The tab where you executed your request must be looking in the following format 
```
{
"Availability": 60,
 "Reputation": 1500,
 "Interest": "I'm a machine learning engineer with python and java knowledge ",
 "Possible Jobs": [1172, 4200, 10291, 6088, 4297]
}
```
"Possible Jobs" yields the intended outcome. Each integer within the given list is the ID of the most correlated task to the provided parameters. These tasks' descriptions are shown in the terminal.

# TODO






