# -*- coding: utf-8 -*-

"""Untitled20.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EW7wuTHY-CwDlmS1XrFaqGlUk8miZS1u
"""

import numpy as np
import streamlit as st
import sklearn
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
import pandas as pd
import json

# Load your image files
demo_image_path = "demo.jpeg"
gif_image_path = "1.gif"

# Display demo.png image
st.image(demo_image_path, use_column_width=True)

# Neural network weights and biases
wei_prev = [6.53372226, 1.45266998, -1.31130261, -3.16864773, 0.39603089]
wei_cur = [1.74665619, -0.74696832, 2.84321548, -1.33783743]
wei_fb = [1.28461033]
wei_bias = [0.41829136]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def onehot_pos_cur(num):
    """Converts current POS tag index to one-hot encoding"""
    return np.eye(4)[num-1]

def onehot_pos_prev(num):
    """Converts previous POS tag index to one-hot encoding"""
    return np.eye(5)[num]

st.title("🌲 Recurrent Perceptron for Noun Chunk Identification 🌲")

user_input = st.text_input("Enter a POS tagged input", "")

tokens = word_tokenize(user_input)
tagged_words = nltk.pos_tag(tokens)

# Initialize a list to store filtered words and their tags
filtered_words = []
tags = []

for word, tag in tagged_words:
    if tag in ['NN', 'NNS', 'NNP', 'NNPS']:
        filtered_words.append(1)
        tags.append(tag)
    elif tag in ['DT', 'PDT', 'POS']:
        filtered_words.append(2)
        tags.append(tag)
    elif tag in ['JJ', 'JJR', 'JJS']:
        filtered_words.append(3)
        tags.append(tag)
    else:
        filtered_words.append(4)
        tags.append('OT')  # Other tags

user_input = np.array(filtered_words, dtype=int)

classify_button = st.button("Classify", key="classify_button", help="Click to classify")

if classify_button:
    output = []
    pos_tagged_output = []
    chunk_output = []

    for i in range(len(user_input)):
        if i == 0:
            x_prev = np.array([1, 0, 0, 0, 0])  # Initial previous POS tag
            y_prev = 0  # Initial previous output
        else:
            x_prev = onehot_pos_prev(output[i-1])

        x_cur = onehot_pos_cur(user_input[i])

        # Forward pass through the network using sigmoid activation function
        y_cur = sigmoid(np.dot(wei_fb, y_prev) + np.dot(wei_prev, x_prev) + np.dot(wei_cur, x_cur) - wei_bias)
    
        # Predict the label based on the output of the network
        output.append(1 if y_cur > 0.5 else 0)
    
        # Prepare formatted output
        pos_tagged_output.append(f"{tokens[i]}_{tags[i]}")
        chunk_output.append(f"{tokens[i]}_{tags[i]}_{output[i]}")

    # Combine all parts into the formatted output
    pos_tagged_str = "POS tagged: " + " ".join(pos_tagged_output)
    chunk_str = "Chunk: " + " ".join(chunk_output)
    st.write(pos_tagged_str)
    st.write(chunk_str)

# Add the message below the Classify button
st.markdown("• **Made by 4 IIT-Bombay students.**")
st.markdown("•Hosted by ❤️")

# Display 1.gif image
st.image(gif_image_path, use_column_width=True)
