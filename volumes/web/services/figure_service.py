import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from models.figure import Figure
from repo.figure_repo import FigureRepository

# pass Figure, return base64 encoded image
def create_chart(figure: Figure) -> str:
    '''Creates a chart from a Figure object and returns it as a base64 encoded image.'''
    # Create the plot
    plt.figure(figsize=(10, 6))

    plt.plot(figure.xaxis_value, figure.yaxis_value, marker='o')
    plt.title(figure.description)
    plt.xlabel(figure.xaxis_title)
    plt.ylabel(figure.yaxis_title)
    
    # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    
    # Encode the image to base64
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
    return img_base64


