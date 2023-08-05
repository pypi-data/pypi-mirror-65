
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

from mailjet_rest import Client

def sendmail(mailjet_api_key,mailjet_secret_key,sender,subject,recipient,text,attachment):
    """
        Send an email with mailjet api.
        :param mailjet_api_key,mailjet_secret_key api key and secret required for mailjet access
        :param sender : sender email and name
        :param subject,recipient,text,attachment
        :return: The blob object
    """
    mailjet = Client(auth=(mailjet_api_key, mailjet_secret_key), version='v3.1')

    data = {
        'Messages': [
            {
                "From": sender,
                "To": [
                    recipient
                ],
                "Subject": subject,
                "TextPart": text,
                "Attachments": [
                    attachment
                ]
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    return result