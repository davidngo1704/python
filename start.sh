if [ ! -d "/root/python_daint/data" ]; then
    mkdir -p /root/python_daint/data
    chmod 777 /root/python_daint/data
fi

# Create file /root/python_daint/data/data.db if not exists
if [ ! -f "/root/python_daint/data/data.db" ]; then
    touch /root/python_daint/data/data.db
    chmod 666 /root/python_daint/data/data.db
fi

# Create folder /root/python_daint/huggingfacemodels if not exists
if [ ! -d "/root/python_daint/huggingfacemodels" ]; then
    mkdir -p /root/python_daint/huggingfacemodels
    chmod 777 /root/python_daint/huggingfacemodels
fi