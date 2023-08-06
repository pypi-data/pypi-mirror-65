pyzafa
===============================================================================

Python自用小功能。安装:

.. code-block:: text

    pip install pyzafa

数据编码
------------------------------------------------------------------------------

1. unicode字符与base64字符相互转换
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pyzafa.data_encoding import base64encode, base64decode

    base64encode('你好，世界')
    base64decode('5L2g5aW977yM5LiW55WM')