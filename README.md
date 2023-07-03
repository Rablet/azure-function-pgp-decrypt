# Introduction

This is a simple PoC for creating an Azure Function which will trigger when a blob is created in an Azure Storage Account.
It will assume the blob is a GPG encrypted file and decrypt it.

Instructions for the steps in Azure to create an Azure Function with an event subscription here: https://learn.microsoft.com/en-us/azure/azure-functions/functions-event-grid-blob-trigger?pivots=programming-language-python
