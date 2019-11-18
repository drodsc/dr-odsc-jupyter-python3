# DataRobot & scikit-learn with Python3.7
FROM python:3.7-slim
ENV LC_ALL=en_US.UTF-8 TERM=xterm COLS=132 ROWS=43 DEBIAN_FRONTEND=noninteractive
LABEL maintainer “Qian Zhao <qian.zhao@datarobot>”

# Install Python library for Data Science
RUN pip --no-cache-dir install \
        datarobot \
        flask \
        sklearn \
        jupyter \
        ipykernel \
		scipy \
        matplotlib \
        wtforms\
        seaborn \
        numpy \
        pandas \
        && \
    python -m ipykernel.kernelspec

# Set up Jupyter Notebook config
ENV CONFIG /root/.jupyter/jupyter_notebook_config.py
ENV CONFIG_IPYTHON /root/.ipython/profile_default/ipython_config.py 

RUN jupyter notebook --generate-config --allow-root && \
    ipython profile create

RUN echo "c.NotebookApp.ip = '0.0.0.0'" >>${CONFIG} && \
    echo "c.NotebookApp.port = 8890" >>${CONFIG} && \
    echo "c.NotebookApp.open_browser = False" >>${CONFIG} && \
    echo "c.NotebookApp.iopub_data_rate_limit=10000000000" >>${CONFIG} && \
    echo "c.MultiKernelManager.default_kernel_name = 'python3'" >>${CONFIG} 

RUN echo "c.InteractiveShellApp.exec_lines = ['%matplotlib inline']" >>${CONFIG_IPYTHON} 

# Copy sample notebooks.
#ADD DataRobot_ODSC /DataRobot_ODSC

COPY DataRobot_ODSC/ /DataRobot_ODSC/
RUN ls -la /DataRobot_ODSC/*

# Port
EXPOSE 8890

VOLUME /DataRobot_ODSC

# Run Jupyter Notebook
WORKDIR "/DataRobot_ODSC"
CMD ["jupyter","notebook", "--allow-root"]