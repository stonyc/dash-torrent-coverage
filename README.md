Dash app to calculate and visualize theoretical multiplexed coverage from Ion Torrent sequencing with options for chip, median read length, and genome size.

**Local Installation**

First install the necessary dependencies:

```bash
conda install -c anaconda -c conda-forge "python>=3.7.6" plotly dash pandas numpy
```

Then clone the `seqcover` repository:

```bash
git clone https://github.com/stonyc/dash-torrent-coverage.git
```

Then to run the application, go to the cloned `seqcover` repository and enter:

```bash
python app.py
```

Finally, open a Chrome browser window to your computer IP address to access the application:

```bash
http://<your-ip-address>:8051
```

**Example**

![screenshot](assets/seqcover.png)
