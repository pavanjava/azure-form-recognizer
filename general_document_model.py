# import libraries
import os
import csv
from dotenv import load_dotenv, find_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

_ = load_dotenv(find_dotenv())
"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
"""
endpoint = os.getenv("FORM_ENDPOINT")
key = os.getenv("FORM_KEY")


def analyze_general_documents():
    # real time financial report of honeywell
    docUrl = "https://www.mitsubishicorp.com/jp/en/ir/library/earnings/pdf/202305e.pdf"

    # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document", docUrl)
    result = poller.result()

    print("----Key-value pairs found in document----")
    data_dictionary = {}
    # for kv_pair in result.key_value_pairs:
    #     if kv_pair.key and kv_pair.value:
    #         data_dictionary[kv_pair.key.content] = kv_pair.value.content

    for page in result.pages:
        for line_idx, line in enumerate(page.lines):
            print("...Line # {} has text content '{}'".format(line_idx, line.content))

    for table_idx, table in enumerate(result.tables):
        fields = []
        rows = []
        curr_row_index = 0
        row_shift_index = 0
        for cell in table.cells:
            curr_row_index = cell.row_index
            if cell.kind == "columnHeader":
                # field names
                fields.append(cell.content)
            if cell.kind == "content":
                if cell.column_index == 0:
                    row_data = [str(cell.content)]
                else:
                    row_data.append(str(cell.content))
                if curr_row_index != row_shift_index:
                    row_shift_index = curr_row_index
                    rows.append(row_data)

        print(f"----Writing to data-{table_idx}: start----")

        with open(f'./data/data-{table_idx}.csv', 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(fields)

            # writing the data rows
            csvwriter.writerows(rows)
        print(f"--------Writing to data-{table_idx}: end------")


if __name__ == "__main__":
    analyze_general_documents()



