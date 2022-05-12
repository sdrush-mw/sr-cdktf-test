#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_google import GoogleProvider
from imports import google
from imports import network
from imports import projectFactory
from imports import serviceAccounts

GCP_PROJECT_ID = "sr-cdktf-test"
TF_SERVICE_ACCOUNT= "sr-cdktf-test-tf-sa@sr-cdktf-test.iam.gserviceaccount.com"

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        GoogleProvider(self,
            id= "sr-cdktf-test",
            impersonate_service_account=TF_SERVICE_ACCOUNT, 
            project= GCP_PROJECT_ID, 
            region= "us-central1", 
            zone= "us-central1-a"
        )
        
        project_apis = projectFactory.ProjectFactory(self, 
            id="project_apis",
            project_id=GCP_PROJECT_ID, 
            activate_apis=["compute.googleapis.com"]
        )

        test_vpc = network.Network(self,
            id= "test_vpc",
            project_id= GCP_PROJECT_ID,
            network_name= "sr-cdktf-test-vpc",
            routing_mode= "GLOBAL",
            subnets=[["subnet01","us-central1","10.1.1.0/24"]]
        )


app = App()
MyStack(app, "sr-cdktf-test")

app.synth()