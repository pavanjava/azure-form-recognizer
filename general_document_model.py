# import libraries
import os
from dotenv import load_dotenv, find_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

_ = load_dotenv(find_dotenv())

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
endpoint = os.getenv("FORM_ENDPOINT")
key = os.getenv("FORM_KEY")


def analyze_general_documents():
    # sample document
    docUrl = "https://slicedinvoices.com/pdf/wordpress-pdf-invoice-plugin-sample.pdf"

    # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document", docUrl)
    result = poller.result()

    print("----Key-value pairs found in document----")
    data_dictionary = {}
    for kv_pair in result.key_value_pairs:
        if kv_pair.key and kv_pair.value:
            data_dictionary[kv_pair.key.content] = kv_pair.value.content

    print(data_dictionary)
    print("----------------------------------------")


if __name__ == "__main__":
    analyze_general_documents()
