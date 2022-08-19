import pandas as pd
import requests


def data_for_train(inputs, output=None):
    """Bring dfs to format suitable for the FCE Rest API data argument

    :param: inputs: Dataframe, column names are parameter names.
    :param: output: Series, name is parameter name.

    :return: List of Dictionaries, suitable to fill into the
             data argument as needed by train post
             calls to the FCE Rest API.
    """
    def make_data_dict(series, name, category='Input'):
        return {
            'Parameter': name,
            'Category': category,
            'Records': [
                {'Datetime': series.index[i].strftime('%Y-%m-%dT%H:%M:%S'),
                 'Value': series[i]}
                for i in range(len(series))]
        }

    ret = []
    if type(inputs) == type(pd.DataFrame()):
        for col in inputs:
            ret.append(make_data_dict(inputs[col], col, 'Input'))
    elif type(inputs) == type(pd.Series()):
        ret.append(make_data_dict(inputs, inputs.name, 'Input'))
    else:
        raise TypeError('inputs argument must be either DataFrame or Series')

    if output is not None:
        ret.append(make_data_dict(output, output.name, 'Output'))

    return ret


def data_for_evaluate(inputs):
    """Bring dfs to format suitable for the FCE Rest API data argument

    :param: inputs: Dataframe, column names are parameter names.

    :return: List of Dictionaries, suitable to fill into the
             data argument as needed by evaluate post
             calls to the FCE Rest API.
    """
    def make_data_dict(series, name, category='Input'):
        return {
            'Parameter': name,
            'Records': [
                {'Datetime': series.index[i].strftime('%Y-%m-%dT%H:%M:%S'),
                 'Value': series[i]}
                for i in range(len(series))]
        }

    ret = []
    if type(inputs) == type(pd.DataFrame()):
        for col in inputs:
            ret.append(make_data_dict(inputs[col], col))
    elif type(inputs) == type(pd.Series()):
        ret.append(make_data_dict(inputs, inputs.name))
    else:
        raise TypeError('inputs argument must be either DataFrame or Series')

    return ret


def json_to_series (json):
    """Builds Series from the FCE Rest API

    :param json: response.json() when response is the answer to
                 a call to the FCE Rest API
    :return: pandas.Series of the forecast.
    """
    forecast = json['forecast'][0]
    df = pd.DataFrame(forecast['records'])
    df.index = pd.to_datetime(df['datetime'], format='%Y%m%dT%H:%M:%S')
    ser = df['value'].sort_index()
    ser.name = forecast['parameter']

    return ser

