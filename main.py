#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_google import GoogleProvider
from imports import network
from imports import cloudNat
from imports import projectFactory
from imports import serviceAccounts

GCP_PROJECT_ID = "sr-cdktf-test"
GCP_NETWORK_NAME = "sr-cdktf-test-vpc"
TF_SERVICE_ACCOUNT = "sr-cdktf-test-tf-sa@sr-cdktf-test.iam.gserviceaccount.com"
GCP_REGION = "us-central1"
GCP_ZONE = "us-central1-a"

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        GoogleProvider(self,
            id = "sr-cdktf-test",
            impersonate_service_account = TF_SERVICE_ACCOUNT, 
            project = GCP_PROJECT_ID, 
            region = GCP_REGION, 
            zone = GCP_ZONE
        )
        
        project_apis = projectFactory.ProjectFactory(self, 
            id = "project_apis",
            project_id = GCP_PROJECT_ID, 
            activate_apis = ["compute.googleapis.com"]
        )

        test_vpc = network.Network(self,
            id = "test_vpc",
            project_id = GCP_PROJECT_ID,
            network_name = GCP_NETWORK_NAME,
            routing_mode = "GLOBAL",
            subnets = [{
                "subnet_name" : "subnet01",
                "subnet_region" : GCP_REGION,
                "subnet_ip" : "10.1.1.0/24"}]
        )

        test_nat = cloudNat.CloudNat(self,
            id = "test_cloud_nat",
            project_id = GCP_PROJECT_ID,
            network = GCP_NETWORK_NAME,
            region = GCP_REGION,
            create_router = True,
            router = "sr-cdktf-test-vpc-usc1-natrtr01",
            name = "sr-cdktf-test-vpc-usc1-natgw01"
        )

app = App()
MyStack(app, "sr-cdktf-test")

app.synth()
