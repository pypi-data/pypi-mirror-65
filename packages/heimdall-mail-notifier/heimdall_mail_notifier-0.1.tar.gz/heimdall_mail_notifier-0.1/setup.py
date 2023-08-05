#  Copyright (c) 2020 Jean-François MARQUIS
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from setuptools import setup

setup(
    name='heimdall_mail_notifier',
    version='0.1',
    packages=['heimdall'],
    url='',
    license='MIT',
    install_requires=[
        "mailjet_rest>=1.3.3",
        "google-cloud-secret-manager>=0.2.0",
        "google-api-python-client>=1.7.11",
        "google-auth>=1.9.0",
        "google-cloud-bigquery>=1.23.1",
        "google-cloud-core>=1.1.0",
        "google-cloud-logging>=1.14.0",
        "google-cloud-pubsub>=1.1.0",
        "google-cloud-storage>=1.23.0"
        ],
    author='Jean-Francois MARQUIS',
    author_email='jeanfrancois.marquis@gmail.com',
    description='This module allow user to execute an SQL request in Bigquery and send the result in a mail attachment send by mailjet'
)
