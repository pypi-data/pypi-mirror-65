
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

def get_secret(project_id, secret_id):
    """
    get a secret into secret manager
    :param project_id:
    :param secret_id:
    :return:
    """
    # Import the Secret Manager client library.
    from google.cloud import secretmanager_v1beta1 as secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the parent name from the project.
    parent = client.project_path(project_id)
    # on liste les secrets présent dans le vault
    secrets = client.list_secrets(parent)
    for secret in secrets:
        # on recherche notre secret dans la liste
        if secret_id in secret.name:
            response = client.access_secret_version(secret.name + '/versions/latest')
            secretvalue = response.payload.data.decode('UTF-8')
            return (secretvalue)
