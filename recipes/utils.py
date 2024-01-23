# Update your utils.py file

from io import BytesIO
import base64
import matplotlib.pyplot as plt

# ...

def get_chart(chart_type, data, **kwargs):
    # switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    # AGG is the preferred solution to write PNG files
    plt.switch_backend('AGG')

    # specify figure size
    fig = plt.figure(figsize=(6, 3))

    if data is None or data.empty:  # handle the case where data is None or empty
        print('No data available for chart.')
        # generate a placeholder chart (you can customize this part)
        plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
    else:
        # select chart_type based on user input from the form
        if chart_type == '#1':
            # plot bar chart between cooking_time on x-axis and number of ingredients on y-axis
            plt.bar(data['cooking_time'], data['ingredients_count'])

        elif chart_type == '#2':
            # generate pie chart based on the number of unique ingredients.
            # The chart values are sent from the view
            values = kwargs.get('values')
            labels = ['Unique Ingredients']
            plt.pie(values, labels=labels)

        elif chart_type == '#3':
            # plot line chart based on cooking_time on x-axis and number of ingredients on y-axis
            plt.plot(data['cooking_time'], data['ingredients_count'])
        else:
            print('Unknown chart type')

    # specify layout details
    plt.tight_layout()

    # render the graph to file
    chart = get_graph()
    return chart
