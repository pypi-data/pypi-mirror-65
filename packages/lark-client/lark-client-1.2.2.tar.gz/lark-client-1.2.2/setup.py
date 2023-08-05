from setuptools import setup, find_packages

setup(
    name="lark-client",
    version="1.2.2",
    keywords=("lark", "飞书", "feishu"),
    description="飞书OpenAPI的客户端",
    long_description="飞书OpenAPI的客户端，由于时间关系该版本只包含目前本人会使用到的方法",
    license="MIT Licence",

    url="",
    author="刘星辰",
    author_email="tbyes@foxmail.com",
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'ujson',
        'requests',
        'gevent==1.4.0',
    ]
)
