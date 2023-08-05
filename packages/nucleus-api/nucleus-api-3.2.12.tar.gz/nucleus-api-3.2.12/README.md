# nucleus-api
Nucleus text analytics APIs from SumUp Analytics. Example and documentation: https://www.sumup.ai/apis/#nucleus-documentation

- Package version: v3.2.12

For more information, please visit [https://www.sumup.ai](https://www.sumup.ai)

## Requirements.

Python 3.5 or 3.6 is set up in a virtual environment. More details: https://docs.python.org/3/tutorial/venv.html. 
All commands in this documents assume running python from the virtual environment.

## Installation & Usage
### pip install
Run pip from Python virtual environment
```sh
pip install nucleus_api --upgrade
```

Then import the package:
```python
import nucleus_api 
```

## Getting Started

1. Go to the examples directory `cd examples`
1. An example using all APIs is provided in a Jupyter Notebook (all-api-examples-py.ipynb) and a Python script all-api-examples-py.py
1. Open the example in Jupyter Notebook or a text editor and update the lines below with provided host name and API key
    ```
    configuration.host = 'API_HOST_HERE'
    configuration.api_key['x-api-key'] = 'API_KEY_HERE'
    ```
1. Execute the example in Jupyter Notebook or use the command line: 'python3 all-api-examples-py.py'

## Guideline for Calibration
[Guideline for Calibration](examples / Guidelines % 20 for % 20Calibrating % 20Nucleus % 20APIs.pdf) is available
in examples / (examples) directory.

##  Documentation for Helper Functions
[**upload_files**](HelperFunc.md#upload_files)
[**upload_jsons**](HelperFunc.md#upload_jsons)
[**upload_urls**](HelperFunc.md#upload_urls)
[**summarize_file_url**](HelperFunc.md#summarize_file_url)  

## Documentation for API Endpoints

All URIs are relative to *https://localhost:5000*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*NucleusApi* | [**get_job**](docs/NucleusApi.md#get_job) | **GET** /jobs | 
*NucleusApi* | [**get_list_datasets**](docs/NucleusApi.md#get_list_datasets) | **GET** /datasets | 
*NucleusApi* | [**get_list_filters**](docs/NucleusApi.md#get_list_filters) | **GET** /filters | 
*NucleusApi* | [**get_user**](docs/NucleusApi.md#get_user) | **GET** /users | 
*NucleusApi* | [**post_admin_add_user**](docs/NucleusApi.md#post_admin_add_user) | **POST** /admin/add_user | 
*NucleusApi* | [**post_admin_delete_user**](docs/NucleusApi.md#post_admin_delete_user) | **POST** /admin/delete_user | 
*NucleusApi* | [**post_admin_list**](docs/NucleusApi.md#post_admin_list) | **POST** /admin/list | 
*NucleusApi* | [**post_admin_manage_dataset**](docs/NucleusApi.md#post_admin_manage_dataset) | **POST** /admin/manage_dataset | 
*NucleusApi* | [**post_admin_update_user**](docs/NucleusApi.md#post_admin_update_user) | **POST** /admin/update_user | 
*NucleusApi* | [**post_append_json_to_dataset**](docs/NucleusApi.md#post_append_json_to_dataset) | **POST** /datasets/append_json_to_dataset | 
*NucleusApi* | [**post_author_connectivity_api**](docs/NucleusApi.md#post_author_connectivity_api) | **POST** /topics/author_connectivity | 
*NucleusApi* | [**post_available_sec_filings**](docs/NucleusApi.md#post_available_sec_filings) | **POST** /feeds/available_sec_filings | 
*NucleusApi* | [**post_bulk_insert_json**](docs/NucleusApi.md#post_bulk_insert_json) | **POST** /datasets/bulk_insert_json | 
*NucleusApi* | [**post_create_dataset_from_sec_filings**](docs/NucleusApi.md#post_create_dataset_from_sec_filings) | **POST** /feeds/create_dataset_from_sec_filings | 
*NucleusApi* | [**post_custom_tracker_api**](docs/NucleusApi.md#post_custom_tracker_api) | **POST** /dashboard/custom_tracker | 
*NucleusApi* | [**post_dataset_info**](docs/NucleusApi.md#post_dataset_info) | **POST** /datasets/dataset_info | 
*NucleusApi* | [**post_dataset_tagging**](docs/NucleusApi.md#post_dataset_tagging) | **POST** /datasets/dataset_tagging | 
*NucleusApi* | [**post_delete_dataset**](docs/NucleusApi.md#post_delete_dataset) | **POST** /datasets/delete_dataset | 
*NucleusApi* | [**post_delete_document**](docs/NucleusApi.md#post_delete_document) | **POST** /datasets/delete_document | 
*NucleusApi* | [**post_delete_filter**](docs/NucleusApi.md#post_delete_filter) | **POST** /filters/delete_filter | 
*NucleusApi* | [**post_doc_classify_api**](docs/NucleusApi.md#post_doc_classify_api) | **POST** /documents/document_classify | 
*NucleusApi* | [**post_doc_display**](docs/NucleusApi.md#post_doc_display) | **POST** /documents/document_display | 
*NucleusApi* | [**post_doc_info**](docs/NucleusApi.md#post_doc_info) | **POST** /documents/document_info | 
*NucleusApi* | [**post_doc_new_words_api**](docs/NucleusApi.md#post_doc_new_words_api) | **POST** /documents/document_new_words | 
*NucleusApi* | [**post_doc_novelty_api**](docs/NucleusApi.md#post_doc_novelty_api) | **POST** /documents/document_novelty | 
*NucleusApi* | [**post_doc_recommend_api**](docs/NucleusApi.md#post_doc_recommend_api) | **POST** /documents/document_recommend | 
*NucleusApi* | [**post_doc_sentiment_api**](docs/NucleusApi.md#post_doc_sentiment_api) | **POST** /documents/document_sentiment | 
*NucleusApi* | [**post_doc_summary_api**](docs/NucleusApi.md#post_doc_summary_api) | **POST** /documents/document_summary | 
*NucleusApi* | [**post_document_contrast_summary_api**](docs/NucleusApi.md#post_document_contrast_summary_api) | **POST** /documents/document_contrasted_summary | 
*NucleusApi* | [**post_example_job**](docs/NucleusApi.md#post_example_job) | **POST** /jobs/start_example_job | 
*NucleusApi* | [**post_key_authors_api**](docs/NucleusApi.md#post_key_authors_api) | **POST** /dashboard/key_authors | 
*NucleusApi* | [**post_legacy**](docs/NucleusApi.md#post_legacy) | **POST** /legacy | 
*NucleusApi* | [**post_metadata_autocomplete**](docs/NucleusApi.md#post_metadata_autocomplete) | **POST** /datasets/metadata_autocomplete | 
*NucleusApi* | [**post_metadata_histogram**](docs/NucleusApi.md#post_metadata_histogram) | **POST** /datasets/metadata_histogram | 
*NucleusApi* | [**post_rename_dataset**](docs/NucleusApi.md#post_rename_dataset) | **POST** /datasets/rename_dataset | 
*NucleusApi* | [**post_save_filter**](docs/NucleusApi.md#post_save_filter) | **POST** /filters/save_filter | 
*NucleusApi* | [**post_setup_connector**](docs/NucleusApi.md#post_setup_connector) | **POST** /connectors/setup_connector | 
*NucleusApi* | [**post_smart_alerts_api**](docs/NucleusApi.md#post_smart_alerts_api) | **POST** /dashboard/smart_alerts | 
*NucleusApi* | [**post_topic_api**](docs/NucleusApi.md#post_topic_api) | **POST** /topics/topics | 
*NucleusApi* | [**post_topic_consensus_api**](docs/NucleusApi.md#post_topic_consensus_api) | **POST** /topics/topic_consensus | 
*NucleusApi* | [**post_topic_consensus_transfer_api**](docs/NucleusApi.md#post_topic_consensus_transfer_api) | **POST** /topics/topic_consensus_transfer | 
*NucleusApi* | [**post_topic_contrast_api**](docs/NucleusApi.md#post_topic_contrast_api) | **POST** /topics/topic_contrast | 
*NucleusApi* | [**post_topic_delta_api**](docs/NucleusApi.md#post_topic_delta_api) | **POST** /topics/topic_delta | 
*NucleusApi* | [**post_topic_historical_analysis_api**](docs/NucleusApi.md#post_topic_historical_analysis_api) | **POST** /topics/topic_historical | 
*NucleusApi* | [**post_topic_sentiment_api**](docs/NucleusApi.md#post_topic_sentiment_api) | **POST** /topics/topic_sentiment | 
*NucleusApi* | [**post_topic_sentiment_transfer_api**](docs/NucleusApi.md#post_topic_sentiment_transfer_api) | **POST** /topics/topic_sentiment_transfer | 
*NucleusApi* | [**post_topic_summary_api**](docs/NucleusApi.md#post_topic_summary_api) | **POST** /topics/topic_summary | 
*NucleusApi* | [**post_topic_transfer_api**](docs/NucleusApi.md#post_topic_transfer_api) | **POST** /topics/topic_transfer | 
*NucleusApi* | [**post_update_dataset_metadata**](docs/NucleusApi.md#post_update_dataset_metadata) | **POST** /datasets/update_dataset_metadata | 
*NucleusApi* | [**post_upload_file**](docs/NucleusApi.md#post_upload_file) | **POST** /datasets/upload_file | 
*NucleusApi* | [**post_upload_url**](docs/NucleusApi.md#post_upload_url) | **POST** /datasets/import_file_from_url | 
*NucleusApi* | [**post_user**](docs/NucleusApi.md#post_user) | **POST** /users | 


## Documentation For Models

 - [AdminAddUserModel](docs/AdminAddUserModel.md)
 - [AdminAddUserRespModel](docs/AdminAddUserRespModel.md)
 - [AdminDeleteUserModel](docs/AdminDeleteUserModel.md)
 - [AdminDeleteUserRespModel](docs/AdminDeleteUserRespModel.md)
 - [AdminListModel](docs/AdminListModel.md)
 - [AdminListRespModel](docs/AdminListRespModel.md)
 - [AdminManageDatasetModel](docs/AdminManageDatasetModel.md)
 - [AdminManageDatasetRespModel](docs/AdminManageDatasetRespModel.md)
 - [AdminUpdateUserModel](docs/AdminUpdateUserModel.md)
 - [AdminUpdateUserRespModel](docs/AdminUpdateUserRespModel.md)
 - [ApiCall](docs/ApiCall.md)
 - [AppendJsonRespModel](docs/AppendJsonRespModel.md)
 - [Appendjsonparams](docs/Appendjsonparams.md)
 - [AuthorConnectL1RespModel](docs/AuthorConnectL1RespModel.md)
 - [AuthorConnectL2RespModel](docs/AuthorConnectL2RespModel.md)
 - [AuthorConnectRespModel](docs/AuthorConnectRespModel.md)
 - [AuthorConnection](docs/AuthorConnection.md)
 - [AvailableFilingsResponseModel](docs/AvailableFilingsResponseModel.md)
 - [BulkInsertParams](docs/BulkInsertParams.md)
 - [BulkInsertRespModel](docs/BulkInsertRespModel.md)
 - [CreateSecDatasetResponseModel](docs/CreateSecDatasetResponseModel.md)
 - [CustomTrackerL1RespModel](docs/CustomTrackerL1RespModel.md)
 - [CustomTrackerModel](docs/CustomTrackerModel.md)
 - [CustomTrackerRespModel](docs/CustomTrackerRespModel.md)
 - [DatasetInfo](docs/DatasetInfo.md)
 - [DatasetInfoModel](docs/DatasetInfoModel.md)
 - [DatasetInfoRespModel](docs/DatasetInfoRespModel.md)
 - [DatasetRespModel](docs/DatasetRespModel.md)
 - [DatasetTagging](docs/DatasetTagging.md)
 - [DatasetTaggingL1RespModel](docs/DatasetTaggingL1RespModel.md)
 - [DatasetTaggingRespModel](docs/DatasetTaggingRespModel.md)
 - [DeleteDatasetModel](docs/DeleteDatasetModel.md)
 - [DeleteDatasetRespModel](docs/DeleteDatasetRespModel.md)
 - [DeleteDocumentModel](docs/DeleteDocumentModel.md)
 - [DeleteDocumentRespModel](docs/DeleteDocumentRespModel.md)
 - [DeleteFilterModel](docs/DeleteFilterModel.md)
 - [DeleteFilterRespModel](docs/DeleteFilterRespModel.md)
 - [DocClassifyL1RespModel](docs/DocClassifyL1RespModel.md)
 - [DocClassifyL2DRRespModel](docs/DocClassifyL2DRRespModel.md)
 - [DocClassifyL2PMRespModel](docs/DocClassifyL2PMRespModel.md)
 - [DocClassifyModel](docs/DocClassifyModel.md)
 - [DocClassifyRespModel](docs/DocClassifyRespModel.md)
 - [DocDisplay](docs/DocDisplay.md)
 - [DocDisplayL1RespModel](docs/DocDisplayL1RespModel.md)
 - [DocDisplayRespModel](docs/DocDisplayRespModel.md)
 - [DocInfo](docs/DocInfo.md)
 - [DocInfoRespModel](docs/DocInfoRespModel.md)
 - [Document](docs/Document.md)
 - [DocumentContrastSummaryL1Model](docs/DocumentContrastSummaryL1Model.md)
 - [DocumentContrastSummaryL2Model](docs/DocumentContrastSummaryL2Model.md)
 - [DocumentContrastSummaryModel](docs/DocumentContrastSummaryModel.md)
 - [DocumentContrastSummaryRespModel](docs/DocumentContrastSummaryRespModel.md)
 - [DocumentNewWordsL1Model](docs/DocumentNewWordsL1Model.md)
 - [DocumentNewWordsModel](docs/DocumentNewWordsModel.md)
 - [DocumentNewWordsRespModel](docs/DocumentNewWordsRespModel.md)
 - [DocumentNoveltyL1Model](docs/DocumentNoveltyL1Model.md)
 - [DocumentNoveltyModel](docs/DocumentNoveltyModel.md)
 - [DocumentNoveltyRespModel](docs/DocumentNoveltyRespModel.md)
 - [DocumentRecommendL1RespModel](docs/DocumentRecommendL1RespModel.md)
 - [DocumentRecommendL2RespModel](docs/DocumentRecommendL2RespModel.md)
 - [DocumentRecommendModel](docs/DocumentRecommendModel.md)
 - [DocumentRecommendRespModel](docs/DocumentRecommendRespModel.md)
 - [DocumentSentimentL1Model](docs/DocumentSentimentL1Model.md)
 - [DocumentSentimentModel](docs/DocumentSentimentModel.md)
 - [DocumentSentimentRespModel](docs/DocumentSentimentRespModel.md)
 - [DocumentSummaryL1Model](docs/DocumentSummaryL1Model.md)
 - [DocumentSummaryL2Model](docs/DocumentSummaryL2Model.md)
 - [DocumentSummaryModel](docs/DocumentSummaryModel.md)
 - [DocumentSummaryRespModel](docs/DocumentSummaryRespModel.md)
 - [EdgarAvailableFields](docs/EdgarAvailableFields.md)
 - [EdgarFields](docs/EdgarFields.md)
 - [EdgarQuery](docs/EdgarQuery.md)
 - [ExampleJobInnerResponse](docs/ExampleJobInnerResponse.md)
 - [ExampleJobResponse](docs/ExampleJobResponse.md)
 - [FilePropertyModel](docs/FilePropertyModel.md)
 - [FilterModel](docs/FilterModel.md)
 - [JobRespModel](docs/JobRespModel.md)
 - [JobStatusRespModel](docs/JobStatusRespModel.md)
 - [JsonPropertyModel](docs/JsonPropertyModel.md)
 - [KeyAuthorsL1RespModel](docs/KeyAuthorsL1RespModel.md)
 - [KeyAuthorsL2RespModel](docs/KeyAuthorsL2RespModel.md)
 - [KeyAuthorsModel](docs/KeyAuthorsModel.md)
 - [KeyAuthorsRespModel](docs/KeyAuthorsRespModel.md)
 - [LegacyResponseModel](docs/LegacyResponseModel.md)
 - [ListDatasetsRespModel](docs/ListDatasetsRespModel.md)
 - [ListFiltersModel](docs/ListFiltersModel.md)
 - [MetadataAutocomplete](docs/MetadataAutocomplete.md)
 - [MetadataAutocompleteRespModel](docs/MetadataAutocompleteRespModel.md)
 - [MetadataHistogram](docs/MetadataHistogram.md)
 - [NestedDocInfoModel](docs/NestedDocInfoModel.md)
 - [NestedTopicConsensusModel](docs/NestedTopicConsensusModel.md)
 - [NestedTopicConsensusTransferModel](docs/NestedTopicConsensusTransferModel.md)
 - [NestedTopicSentimentTransferModel](docs/NestedTopicSentimentTransferModel.md)
 - [PostUserRespModel](docs/PostUserRespModel.md)
 - [RenameDatasetModel](docs/RenameDatasetModel.md)
 - [RenameDatasetRespModel](docs/RenameDatasetRespModel.md)
 - [SaveFilterModel](docs/SaveFilterModel.md)
 - [SaveFilterRespModel](docs/SaveFilterRespModel.md)
 - [SetupConnectorModel](docs/SetupConnectorModel.md)
 - [SmartAlertsL1RespModel](docs/SmartAlertsL1RespModel.md)
 - [SmartAlertsL2RespModel](docs/SmartAlertsL2RespModel.md)
 - [SmartAlertsModel](docs/SmartAlertsModel.md)
 - [SmartAlertsRespModel](docs/SmartAlertsRespModel.md)
 - [TopicConsensusModel](docs/TopicConsensusModel.md)
 - [TopicConsensusRespModel](docs/TopicConsensusRespModel.md)
 - [TopicConsensusTransferModel](docs/TopicConsensusTransferModel.md)
 - [TopicConsensusTransferRespModel](docs/TopicConsensusTransferRespModel.md)
 - [TopicContrastL1RespModel](docs/TopicContrastL1RespModel.md)
 - [TopicContrastL21RespModel](docs/TopicContrastL21RespModel.md)
 - [TopicContrastL22RespModel](docs/TopicContrastL22RespModel.md)
 - [TopicContrastModel](docs/TopicContrastModel.md)
 - [TopicContrastRespModel](docs/TopicContrastRespModel.md)
 - [TopicDeltaL1RespModel](docs/TopicDeltaL1RespModel.md)
 - [TopicDeltaL2RespModel](docs/TopicDeltaL2RespModel.md)
 - [TopicDeltaModel](docs/TopicDeltaModel.md)
 - [TopicDeltaRespModel](docs/TopicDeltaRespModel.md)
 - [TopicHistoryL1RespModel](docs/TopicHistoryL1RespModel.md)
 - [TopicHistoryModel](docs/TopicHistoryModel.md)
 - [TopicHistoryRespModel](docs/TopicHistoryRespModel.md)
 - [TopicL1RespModel](docs/TopicL1RespModel.md)
 - [TopicL2RespModel](docs/TopicL2RespModel.md)
 - [TopicRespModel](docs/TopicRespModel.md)
 - [TopicSentimentL1RespModel](docs/TopicSentimentL1RespModel.md)
 - [TopicSentimentModel](docs/TopicSentimentModel.md)
 - [TopicSentimentRespModel](docs/TopicSentimentRespModel.md)
 - [TopicSentimentTransferModel](docs/TopicSentimentTransferModel.md)
 - [TopicSentimentTransferRespModel](docs/TopicSentimentTransferRespModel.md)
 - [TopicSummaryL1RespModel](docs/TopicSummaryL1RespModel.md)
 - [TopicSummaryL2RespModel](docs/TopicSummaryL2RespModel.md)
 - [TopicSummaryModel](docs/TopicSummaryModel.md)
 - [TopicSummaryRespModel](docs/TopicSummaryRespModel.md)
 - [TopicTransferL1RespModel](docs/TopicTransferL1RespModel.md)
 - [TopicTransferL2RespModel](docs/TopicTransferL2RespModel.md)
 - [TopicTransferModel](docs/TopicTransferModel.md)
 - [TopicTransferRespModel](docs/TopicTransferRespModel.md)
 - [Topics](docs/Topics.md)
 - [UpdateDatasetMetadataModel](docs/UpdateDatasetMetadataModel.md)
 - [UpdateDatasetMetadataRespModel](docs/UpdateDatasetMetadataRespModel.md)
 - [UploadFileRespModel](docs/UploadFileRespModel.md)
 - [UploadURLModel](docs/UploadURLModel.md)
 - [UploadUrlRespModel](docs/UploadUrlRespModel.md)
 - [UrlPropertyModel](docs/UrlPropertyModel.md)
 - [User](docs/User.md)
 - [UserModel](docs/UserModel.md)



Copyright 2019 SumUp Analytics, Inc

