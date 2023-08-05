# openProduction
An opensource framework to model device production

# Product hierarchy

A product has the following hierarchy:

[product](#product) -> [product step](#product-step) -> [product revision](#product-revision)

Furthermore the product step order has to be defined in the [product station link table](#product-station-link).

## 1. Product<a name="product"></a>
The product consists of:
- name
- description
- unique ID (product_id)

## 2. Product step<a name="product-step"></a>
A product is split in several steps. These steps can be for instance a programming station or an EOL station.
A product step consists of:
- product_id (link to upstream product)
- unique ID (product_step_id)
- version (a string like "CSample", "BSample", "Series" etc..)
- git_branch
- git_credential_id (link to git table which contains URL, username, password)
- description
- image
- station_id (link to station table)

All product steps of a product have a production order which has to be configured in the **product station link** table.

## 3. Product revision<a name="product-revision"></a>
The product revision is the global explicit key to run a product at a station. The product revision consits of:
- unique ID (revision_id)
- product_step_id (link to upstream product step)
- params (a json string containing all parameters of this revision)
- commit_id (the git SHA1 of the upstream's product step-> git_credential_id repository)
- date (creation date of revision)

A product revision cannot be changed. It can be created and read.
To modify either **params** or **commit_id** you have to create a new entry.
When a product is loaded in the openProduction UI, the git repository with the given commit_id is checked out.
Read the following chapter [Product run](#product-run) for details on what happens when a product is loaded.

## 4. Product station link<a name="product-station-link"></a>

The product station links define the order of product steps of a product. Suppose you have a product which has to 
run in the following order:
1. Programming station
2. EOL (end of line test)

The product will fail on the EOL station if it did not run through the programming station successfully.

The product station link table consists of:
- unique ID (ID of this link entry)
- product_id (link to product table)
- station_id (link to station table)
- order (order of run lower number means run at first)

In the above example, we would than have a product station link table with the following entries
(suppose that the product_id=0, Programming station id=0, EOL station id=1):

| link_id | product_id | station_id  | order |
| ------- | ---------- | ----------- | ----- |
| 0       | 0          | 0           | 0     |
| 1       | 0          | 1           | 1     |


# Product run<a name="product-run"></a>

When a product revision is loaded, openProduction first creates a **test suite**. The test suite consists of five **stages**:
- load (executed once on loading)
- setup (executed on every test run)
- step (regular steps executed on every test run)
- teardown (guaranteed to be executed on every test run)
- unload (executed once on unloading)

Every **stage** (load/setup/step/teardown/unload) can contain an unlimited number of steps, each executed in alphabetical order.
Per default, openPorduction looks for all files (recursively in all subfolders) with the pattern **hook_*.py** inside the git repository (git_credential_id)
@ commit (commit_id) of the loaded product revision.
It then looks inside all found hook_*.py files for classes of type openProduction.product.ProductExecutor for method names with the patterns:
- step_
- setup_
- teardown_
- load_
- unload_

and adds them to the test suite to be executed.
By default, openProduction also adds some steps to the testSuite, e.g. a "transmit results to database" is added as a teardown step.
The [product revision](#product-revision) step can influence the above described behaviour by defining some key/value pairs in the **params**:
- productHookDir -> look only inside this folder for hook_*.py files
- productHookPattern -> define a different pattern than hook_*.py
- productHookRegularPattern -> define a different pattern than step_
- productHookSetupPattern -> define a different pattern than setup_
- productHookTearDownPattern -> define a different pattern than teardown_
- productHookUnloadPattern -> define a different pattern than unload_

# Code snippets



## List product steps

```python
from openProduction.server import ServerInterface
from openProduction.common import misc
from openProduction.connectors.BaseConnector import ConnectorErrors

workspace = misc.getDefaultAppFolder() #can be any workspace available on local PC
s = ServerInterface.ServerInterface.create(workspace)
rv, data = s.listProductSteps()
if rv == ConnectorErrors.NO_ERROR:
    print ("version of 1st product step: ", data[0]["version"])
```

similarly, you can:
- list all products (listProducts())
- list all product revisions (listProductRevisions())

## create a new product

The following snippet creates a new product with a first station link
(when you add product steps, you need to add product station links as well).

```python
data = {"name": "Peco Rear", "description": "Peco Rear"}
stationLink = {"station_id": 1, "order": 0}
rv, productData, linkData = s.createProduct(data, stationLink)
if rv == ConnectorErrors.NO_ERROR:
    print("new product created succesfully")
    print("the product id is ", productData["product_id"])
```

## create a new product step

```python
f = open(r"C:\Users\Win10 Pro x64\Downloads\station_Prog_PECO_REAR-DEVICE_IMAGE.png", "rb")
img = f.read()
f.close()
data = {"product_id": 4, "version": "BSample", "git_credential_id": 1,
        "git_branch": "DTAGD", "description": "DTAGD Programmierplatz", "image": img, "station_id": 1}

params = {}
params["productHookDir"] = "Prog"
params["minRssi"] = -60
params["min3V3"] = 3.2
params["max3V3"] = 3.4
params["DTAGDFile"] = "Prog/firmwareDTAGD/RC_OPTODASH-0.1.21AllIncluded.hex"

revision = {"params": params, "commit_id": "596a708356ed0ed0e1fe5a704e7f084f96b1cb48"}
rv, stepData, revisionData = s.createProductStep(data, revision)
```

## create production station link entry
```python
data = {}
data['product_id']= 1
data['station_id']= 3
data['order']= 3
rv = s.createProductStationLink(data)
```

## create a new product revision

Let's assume you have a product revision with a parameter named "maxVoltage" which shall be changed from 5 to 6.
To achieve this, you have to first load the **latest revision** of the product step and than change the corresponding entry:

```python
stationName = "Programmierplatz"
devName = "DTAGD"
vers = "BSample"
rv, rvData = s.getProductStepByName(stationName, devName, vers)
if rv == ConnectorErrors.NO_ERROR:
    rv, lastRevData = s.getLatestProductRevision(rvData["product_step_id"])
    if rv == ConnectorErrors.NO_ERROR:
        lastRevData.pop("revision_id") #remove revision_id, otherwise updateProductRevisionByName raises an error ("revision_id already exists")
        lastRevData.pop("date")
        
        lastRevData["params"]["maxVoltage"] = 6
        
        #if you also want to change the commit_id, uncomment the following:
        #lastRevData["commit_id"] = "ff5ede0654c8afec6ad45ff9b3c0dc22c8a5fb80"
        
        rv, data = s.updateProductRevisionByName(stationName, devName, vers, lastRevData)
        if rv == ConnectorErrors.NO_ERROR:
          print("the newly created revision has the ID: ", data["revision_id"])
```

## duplicate an existing product

Sometimes you want to duplicate an existing prodcut from a CSample or similar version to a series device at the same station. The following snippet helps you to achieve this.


```python
from openProduction.server import ServerInterface
from openProduction.common import misc
from openProduction.connectors.BaseConnector import ConnectorErrors

workspace = misc.getDefaultAppFolder() #can be any workspace available on local PC
s = ServerInterface.ServerInterface.create(workspace)

stationName = "EOL"
devName = "DTAGD"
vers = "CSample"

newVersion = "Serie"
newDescription = None

rv, rvData = s.getProductStepByName(stationName, devName, vers)
if rv == ConnectorErrors.NO_ERROR:
    rv, lastRevData = s.getLatestProductRevision(rvData["product_step_id"])
    if rv == ConnectorErrors.NO_ERROR:
        if newDescription == None:
            newDescription = rvData["description"]
                        
        data = {"product_id": rvData["product_id"], "version": newVersion, "git_credential_id": rvData["cred.git_credential_id"],
                "git_branch": rvData["git_branch"], "description": newDescription, "image": rvData["image"], "station_id": rvData["station_id"]}

        lastRevData.pop("revision_id") #remove revision_id, otherwise updateProductRevisionByName raises an error ("revision_id already exists")
        lastRevData.pop("date")        
        params = lastRevData["params"]
        params["PNnumber"] = "0501.338.605"
        
        commitID = lastRevData["commit_id"]
        commitID = "4436151e2388a67bac3fb387dfc8b0fe89ecac20"
        
        revision = {"params": params, "commit_id": commitID}
        rv, stepData, revisionData = s.createProductStep(data, revision)
        if rv == ConnectorErrors.NO_ERROR:
            print ("product successfully duplicated to "+newVersion)
```
