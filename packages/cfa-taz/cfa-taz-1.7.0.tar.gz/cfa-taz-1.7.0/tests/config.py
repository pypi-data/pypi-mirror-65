keyvault = {
    "name": "kvdvldev",
    "secret_name": "REGISTRY-PASSWORD",
    "tenant_id": "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9",
    "client_id": "9d6f83f7-af2f-4a8d-b692-e2329dbbef9d",
    "client_secret": "C89nigG4BeonI",
}

auth = {
    "resource_group": "RG-APPLI-RED-DEV",
    "managed_identity": "mi-aci-wag-dev-01",
    "subscription_id": "5f82da32-5cad-49a4-aec5-5ba8806e6d9c",
    "tenant_id": "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9",
    "client_id": "1300f1b6-1bc2-4658-a504-86a1850805d2",
    "client_secret": "E.ZmS5LjjYpqjsb38=DgAn5WtIibBd.@",
}

blob = {
    "storage_account_name": "zstalrsdvllogdev01",
    "storage_key": "z++1cFPTnrNBNIM6QONcnjYUXa1VZuCs6DpsP+x9ELEuItoAZyM/W+FQLqlxsy/DWfjxywsJu5FjW2O7Wc3P1A==",
    "storage_connection_string": "DefaultEndpointsProtocol=https;AccountName=zstalrsdvllogdev01;AccountKey=z++1cFPTnrNBNIM6QONcnjYUXa1VZuCs6DpsP+x9ELEuItoAZyM/W+FQLqlxsy/DWfjxywsJu5FjW2O7Wc3P1A==;EndpointSuffix=core.windows.net",
    "sas_key": "?sv=2019-02-02&ss=bfqt&srt=sco&sp=rwdlacup&se=2019-12-05T02:24:33Z&st=2019-12-04T18:24:33Z&spr=https&sig=MssPnv0uBl%2BoWxplggnsUBlZLRi8lBWgMd1dy%2BnVo3Q%3D",
    "container_name": "unittest-taz",
    "path": "test.csv",
    "localpath": "/tmp/test.csv",
    "gzip_path": "test.csv.gz",
    "data": "col1,col2,col3\nval11,val12,val13\nval21,val22,val23",
}

acr = {
    "resource_group": "RG-APPLI-RED-DEV",
    "registry_name": "crreddev",
    "subscription_id": "5f82da32-5cad-49a4-aec5-5ba8806e6d9c",
    "image_name": "hello-world",
}

aci = {
    "resource_group": "RG-APPLI-RED-DEV",
    "container_group_name": "cg-taz-test-unit",
    "location": "northeurope",
    "subscription_id": "5f82da32-5cad-49a4-aec5-5ba8806e6d9c",
}

dls = {
    "dls_name": "lemanhprod",
    "tenant_id": "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9",
    "client_id": "e3952129-496b-416b-a244-67c43bd5bddd",
    "client_secret": "/KauQDlt2yiL34n9xsCxPLJMgKVzf.==",
    # "https_proxy": "host.docker.internal:3128",
    "https_proxy": "localhost:3128",
    "path": "SNCF/landing/input/METEOFRANCE/data_files/OBSERVATIONS_5MN/2019",
    "glob_path": "SNCF/landing/input/METEOFRANCE/data_files/OBSERVATIONS_5MN/2019/matriceSNCF_20191212*",
    "file_name": "matriceSNCF_201905201520.csv",
    "gz_file_name": "SNCF/landing/input/METEOFRANCE/data_files/PREVISIONS/20190123/previsions_20190123_J1.csv.gz",
    "tmp_file_name": "/tmp/taz.tmp",
}

dls_glob = {}
