import kagglehub
import pandas as pd
import streamlit as st
import re
import numpy as np
path = kagglehub.dataset_download("kazanova/sentiment140")

print("Path to dataset files:", path)


def clean_code(df):
    # re.split

    return df