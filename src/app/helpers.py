import base64
import dash_html_components as html
import io
import pandas as pd


def parse_contents(contents, filename):
    """Parse the contents of a reaction file into a DataFrame."""
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

        elif 'txt' in filename:
            df = pd.read_fwf(io.StringIO(decoded.decode('utf-8')))

        else:
            raise Exception("File should be xls(x), txt, or csv")

        return df

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
