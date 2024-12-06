import requests
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2 import service_account

project_id = "craftify-capstone"
collection = "diy_project"
key_file = "craftify-capstone-firebase-adminsdk-z38iz-5372c7f45c.json"

def get_access_token():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            key_file,
            scopes=["https://www.googleapis.com/auth/datastore"],
        )
        request_instance = Request()
        if not credentials.valid or credentials.expired:
            credentials.refresh(request_instance)
        return credentials.token
    except Exception as e:
        print("Error getting access token:", e)
        raise

def get_data():
    try:
        access_token = get_access_token()
        url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection}"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        documents = []
        if "documents" in data:
            print("Documents retrieved from Firestore:")
            for document in data["documents"]:
                if "fields" in document:
                    document_id = document["name"].split("/")[-1]
                    fields = document["fields"]
                    flattened_fields = {
                        field: int(list(value.values())[0]) if list(value.values())[0].isdigit() else list(value.values())[0]
                        for field, value in fields.items()
                    }
                    flattened_fields["Document ID"] = document_id
                    documents.append(flattened_fields)
                else:
                    print(f"Skipping document without fields: {document['name']}")
        else:
            print("No documents found in the response.")

        if documents:
            df = pd.DataFrame(documents)
            numeric_columns = [
                'other_plastic_wrapper', 'metal_bottle_cap',
                'single_use_carrier_bag', 'broken_glass', 'glass_bottle', 'pop_tab',
                'styrofoam', 'drink_can', 'carton',
                'plastic_straw', 'normal_paper', 'plastic_lid',
                'plastic_bottle', 'plastic_film', 'aluminium_foil',
                'other_plastic', 'plastic_bottle_cap', 'paper_cup',
                'disposable_plastic_cup'
            ]
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

            print("DataFrame created:")
            print(df.head())
            return df
        else:
            print("No valid documents to include in the DataFrame.")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print("Error getting data:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


if __name__ == "__main__":
    df = get_data()
    df.to_csv('project.csv')
