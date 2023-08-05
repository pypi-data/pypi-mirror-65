flask-cos
==========

腾讯云对象存储的Flask扩展, 基于 `codeif/qcos <https://github.com/codeif/qcos>`_

安装
----

通过pip安装::

    pip install flask-cos


使用
----

.. code-block:: python

    from flask_cos import COS
    cos = COS()
    cos.init_app(app)

    key = "test.txt"
    data = "content"
    cos.put_object(key, data)


配置项
------

================    ==================================================================
配置项              说明
================    ==================================================================
COS_SECRET_ID
COS_SECRET_KEY
COS_REGION
COS_APPID
COS_BUCKET
COS_HOST            选填，可以通过cos.host访问设置的值，用于组成文件url
================    ==================================================================
