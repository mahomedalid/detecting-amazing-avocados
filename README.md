# Detecting Amazing Avocados.

Detecting Amazing Avocados aim to create a low-cost grading and sorting fruit machine. We will start with avocados, because they have the nice characteristic that if they seem good by the outside when harvested it is usually good by the inside.

# Getting Started

## Creating your ML model (optional)

1. Install [Lobe.ai](https://www.lobe.ai/)
2. Download the [raw data set](storageexplorer://v=1&accountid=%2Fsubscriptions%2F9e4be01c-985e-4886-bca8-990d4b722050%2FresourceGroups%2Favocado%2Fproviders%2FMicrosoft.Storage%2FstorageAccounts%2Favocadosphotos&subscriptionid=9e4be01c-985e-4886-bca8-990d4b722050&resourcetype=Azure.BlobContainer&resourcename=rawphotos) you can use [AzCopy](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10) or the [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)
3. Create your ML model by labeling the photos and using [the lobe.ai help](https://www.lobe.ai/docs/welcome/welcome).
4. Export your ML model as a **Tensor-flow lite** model.

## Installing and testing your ML model into the Adafruit Kit

1. [Setup your Pi](https://learn.adafruit.com/lobe-rock-paper-scissors/setting-up-your-pi-2)
2. [Download the Lobe.ai code](https://learn.adafruit.com/lobe-rock-paper-scissors/play-rock-paper-scissors)
3. [Transfer and test the model](https://learn.adafruit.com/lobe-rock-paper-scissors/testing-your-model-on-the-pi), there is an example of [how to transfer files using an ftp connection](https://learn.adafruit.com/lobe-rock-paper-scissors/setup-an-ftp-connection) but you can also use scp, or any other method to transfer files.

# Contributing

