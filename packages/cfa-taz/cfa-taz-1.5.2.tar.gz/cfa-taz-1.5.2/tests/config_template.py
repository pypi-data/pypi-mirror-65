
keyvault = {
    name: "kvdvldev"
    secret_name: "REGISTRY-PASSWORD"
    tenant_id: "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9"
    client_id: "9d6f83f7-af2f-4a8d-b692-e2329dbbef9d"
    client_secret: "<secured string>"
}

auth = {
    resource_group: "RG-APPLI-RED-DEV"
    managed_identity: "mi-aci-wag-dev-01"
    subscription_id: "5f82da32-5cad-49a4-aec5-5ba8806e6d9c"
    tenant_id: "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9"
    client_id: "1300f1b6-1bc2-4658-a504-86a1850805d2"
    client_secret: "<secured string>"
}

blob = {
    storage_account_name: "zstalrsdvllogdev01"
    storage_key: "<secured string>"
    sas_key: "<secured string>"
    container_name: "unittest-taz"
    path: "test.csv"
    gzip_path: "test.csv.gz"
    data: "col1,col2,col3
val11,val12,val13
val21,val22,val23"
}

acr = {
    resource_group: "RG-APPLI-RED-DEV"
    registry_name: "crreddev"
    subscription_id: "5f82da32-5cad-49a4-aec5-5ba8806e6d9c"
    image_name: "hello-world"
}

aci = {
    resource_group: "RG-APPLI-RED-DEV"
    container_group_name: "cg-taz-test-unit"
    location: "northeurope"
    subscription_id: "5f82da32-5cad-49a4-aec5-5ba8806e6d9c"
}

dls = {
    dls_name: "lemanhprod"
    tenant_id: "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9"
    client_id: "e3952129-496b-416b-a244-67c43bd5bddd"
    client_secret: "<secured string>"
    https_proxy: "localhost:3128"
    path: "SNCF/landing/input/METEOFRANCE/data_files/OBSERVATIONS_5MN/2019"
    glob_path: "SNCF/landing/input/METEOFRANCE/data_files/OBSERVATIONS_5MN/2019/matriceSNCF_20191212*"
    file_name: "matriceSNCF_201905201520.csv"
    gz_file_name: "SNCF/landing/input/METEOFRANCE/data_files/PREVISIONS/20190123/previsions_20190123_J1.csv.gz"
    tmp_file_name: "/tmp/taz.tmp"
}

dls_glob = {
}
