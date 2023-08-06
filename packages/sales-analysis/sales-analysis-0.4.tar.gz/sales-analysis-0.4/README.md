# sales_analysis: web application to view sales data

## What is it?

sales_analysis is a lightweight tool for viewig sales data in web browser. **Note: The input data must be in the same format, as the `.csv` files in `sales_analysis/data_pipeline/data`** 

## Where to get it?

The package can be installed by running 

```
pip install sales_analysis
```

## Dependancies

* [Pandas](https://github.com/pandas-dev/pandas/tree/v1.0.3)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
* [pytest](https://docs.pytest.org/en/latest/)

## License

BSD 3

## How to run the app

After successfully installing `sales_analysis`. The app may be run without any modification to `sales_analysis/data_pipeline/data`. However, this will execute the sample data provided. In order to change the default behaviour, the data in `sales_analysis/data_pipeline/data` must be replaced with new data. **Note: It is imperative that this folder contains data formatted in the same way as provided**. 

Once the data has been imported, then follow the steps below.

1. Open a terminal and enter `python` to launch an interactive python session.
```
> python
Python 3.7.7 (default, Mar 23 2020, 16:19:08) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

2. Then enter the following
```
>>> from sales_analysis import sales_app
>>> app.run()
```

This will output the following.

```
* Serving Flask app "sales_analysis" (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

3. Then copy and paste `http://127.0.0.1:5000/` into a browser. The default page will return the message below

> ## Not Found

The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.

4. Add a valid date to the url. For example, add `2019-08-02` to the url i.e. `http://127.0.0.1:5000/2019-08-02`. This will output the following in the browser.

```python 
{"customers":10.0,
 "discount_rate_avg":0.12950211356271726,
 "items":3082.0,
 "order_total_avg":1341449.559055637,
 "total_discount_amount":20061245.64408109}
```

If an incorrectly formatted date is passed, the server will raise an error. For example, if `2019-08` is passed, the following error is raised.

```
ValueError: time data '2019-08' does not match format '%Y-%m-%d'
```