# Author: manas.tri@gmail.com

import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import re
#from azure.mgmt.cognitiveservices.operations  import AccountsOperations




# create array of azure regions
regions = [
    "southindia",
    "australiaeast",
    "brazilsouth",
    "westus",
    "westus2",
    "westeurope",
    "northeurope",
    "southeastasia",
    "eastasia",
    "westcentralus",
    "southcentralus",
    "eastus",
    "eastus2",
    "canadacentral",
    "japaneast",
    "centralindia",
    "uksouth",
    "japanwest",
    "koreacentral",
    "francecentral",
    "northcentralus",
    "centralus",
    "southafricanorth",
    "uaenorth",
    "swedencentral",
    "switzerlandnorth",
    "switzerlandwest",
    "germanywestcentral",
    "norwayeast",
    "westus3",
    "jioindiawest",
    "qatarcentral",
    "canadaeast" ]

class Deployment:
    def __init__(self, name, model, capacity, region, resource_group, resource):
        self.name = name
        self.model = model
        self.capacity = capacity
        self.region = region
        self.resource_group = resource_group
        self.resource = resource

def main():
    sub_id = input("Enter AZURE_SUBSCRIPTION_ID: ")
    #sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not sub_id:
        raise Exception("AZURE_SUBSCRIPTION_ID is not provided")

    client = CognitiveServicesManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=sub_id
    )

    # get all the deployments
    deployments = []
    # sample account ID '/subscriptions/abcd1234-1234-5678-9012-098330bfffff/resourceGroups/OpenAI/providers/Microsoft.CognitiveServices/accounts/myaccount'
    # Regex pattern to extract resource group name
    pattern = r'resourceGroups\/(.*?)\/providers'

    accounts_response = client.accounts.list()
    for account in accounts_response:
        #print(account.name)
        # get resource group from account
        match = re.search(pattern, account.id)
        resource_group_name = match.group(1)
        deployments_response = client.deployments.list(
            resource_group_name = resource_group_name,
            account_name = account.name
        )
        # Get keys
        #Get old Key
        oldkeys = client.accounts.list_keys(resource_group_name=resource_group_name,account_name=account.name)
        # Extract and print keys
        oldprimary_key = oldkeys.key1
        oldsecondary_key = oldkeys.key2

        print(f"\nResource Group: {resource_group_name} Resource: {account.name}")
        print(f"OldPrimary Key: {oldprimary_key}")
        print(f"OldSecondary Key: {oldsecondary_key}")        
        #generate Key
        regenkeys1 = client.accounts.regenerate_key(resource_group_name=resource_group_name,account_name=account.name,key_name="Key1")
        regenkeys2 = client.accounts.regenerate_key(resource_group_name=resource_group_name,account_name=account.name,key_name="Key2")
        #Get new Key
        keys = client.accounts.list_keys(resource_group_name=resource_group_name,account_name=account.name)

        # Extract and print keys
        newprimary_key = keys.key1
        newsecondary_key = keys.key2

        print(f"\nResource Group: {resource_group_name} Resource: {account.name}")
        print(f"NewPrimary Key: {newprimary_key}")
        print(f"NewSecondary Key: {newsecondary_key}")

if __name__ == "__main__":
    # Ask for confirmation
    confirmation = input("Do you want to regenerate the OpenAI Key? (yes/no): ").lower()

if confirmation == 'yes':
    main()
    print("Script execution Successful.")
else:
    print("Answer other than Yes, Script Could not be executed.")
    