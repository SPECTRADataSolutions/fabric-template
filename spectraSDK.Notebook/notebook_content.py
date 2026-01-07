# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5cb93b81-8923-a984-4c5b-a9ec9325ae26",
# META       "default_lakehouse_name": "zephyrLakehouse",
# META       "default_lakehouse_workspace_id": "16490dde-33b4-446e-8120-c12b0a68ed88",
# META       "known_lakehouses": [
# META         {
# META           "id": "5cb93b81-8923-a984-4c5b-a9ec9325ae26"
# META         }
# META       ]
# META     },
# META     "environment": {
# META       "environmentId": "92a8349b-6a62-b2e9-40bf-1ac52e9ab184",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # SPECTRA Fabric SDK v0.3.0
# # Complete SDK embedded as notebook for fast iteration.
# Use: `%run spectraSDK` at top of notebooks.

# CELL ********************

# ══════════════════════════════════════════════════════════════════════════════
# Zephyr Endpoints Catalog (224 endpoints - ZERO DUPLICATES)
# ══════════════════════════════════════════════════════════════════════════════
# Auto-generated from docs/endpoints.json
# Categories: admin (11), attachments (2), automation (10), cycles (17), defects (3), executions (21), fields (13), groups (2), info (1), license (3), other (26), projects (19), releases (5), requirements (4), roles (2), search (5), system (7), testcases (58), users (15)
# Hierarchical: 56/224 endpoints require parent IDs
# Metadata: full_path, query_parameters, path_parameters, resource (all preserved)

ZEPHYR_ENDPOINTS_CATALOG = [
    {
        "endpoint_path": "/admin/preference/admin",
        "full_path": "/admin/preference/admin",
        "http_method": "GET",
        "category": "admin",
        "description": "Get All Preferences - Admin",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All Preferences - Admin [/admin/preference/admin]",
    },
    {
        "endpoint_path": "/admin/app",
        "full_path": "/admin/app",
        "http_method": "GET",
        "category": "admin",
        "description": "Get All Applications",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All Applications  [/admin/app]",
    },
    {
        "endpoint_path": "/admin/preference/lov/all",
        "full_path": "/admin/preference/lov/all",
        "http_method": "GET",
        "category": "admin",
        "description": "Get list of values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get list of values [/admin/preference/lov/all]",
    },
    {
        "endpoint_path": "/admin/preference/all",
        "full_path": "/admin/preference/all",
        "http_method": "GET",
        "category": "admin",
        "description": "Get All Preferences",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All Preferences  [/admin/preference/all]",
    },
    {
        "endpoint_path": "/admin/preference/anonymous",
        "full_path": "/admin/preference/anonymous",
        "http_method": "GET",
        "category": "admin",
        "description": "Get Anonymous Preferences",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get Anonymous Preferences  [/admin/preference/anonymous]",
    },
    {
        "endpoint_path": "/admin/backup/schedule",
        "full_path": "/admin/backup/schedule",
        "http_method": "GET",
        "category": "admin",
        "description": "Get Daily Back-up Schedule",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get Daily Back-up Schedule [/admin/backup/schedule]",
    },
    {
        "endpoint_path": "/admin/ldap/default/settings",
        "full_path": "/admin/ldap/default/settings",
        "http_method": "GET",
        "category": "admin",
        "description": "Get All user preferences",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All user preferences  [/admin/ldap/default/settings]",
    },
    {
        "endpoint_path": "/admin/preference",
        "full_path": "/admin/preference{?key}",
        "http_method": "GET",
        "category": "admin",
        "description": "Get Preference by key",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["key"],
        "path_parameters": [],
        "resource": "Get Preference by key [/admin/preference{?key}]",
    },
    {
        "endpoint_path": "/admin/preference/item/usage",
        "full_path": "/admin/preference/item/usage{?preferencename}{?value}{?id}",
        "http_method": "GET",
        "category": "admin",
        "description": "Get Preference Item Usage",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["preferencename", "value", "id"],
        "path_parameters": [],
        "resource": "Get Preference Item Usage [/admin/preference/item/usage{?preferencename}{?value}{?id}]",
    },
    {
        "endpoint_path": "/admin/user/preference",
        "full_path": "/admin/user/preference",
        "http_method": "GET",
        "category": "admin",
        "description": "Get All user preferences",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All user preferences  [/admin/user/preference]",
    },
    {
        "endpoint_path": "/admin/preference",
        "full_path": "/admin/preference",
        "http_method": "PUT",
        "category": "admin",
        "description": "Update a given Preference",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Update a given Preference [/admin/preference]",
    },
    {
        "endpoint_path": "/assignmenttree",
        "full_path": "/assignmenttree/{cyclephaseid}/bulk/tree/{treeid}/from/{fromid}/to/{toid}{?cascade}{?easmode}",
        "http_method": "PUT",
        "category": "other",
        "description": "Change multiple assignments",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["cascade", "easmode"],
        "path_parameters": ["cyclephaseid", "treeid", "fromid", "toid"],
        "resource": "Change multiple assignments [/assignmenttree/{cyclephaseid}/bulk/tree/{treeid}/from/{fromid}/to/{toid}{?cascade}{?easmode}]",
    },
    {
        "endpoint_path": "/assignmenttree",
        "full_path": "/assignmenttree/{cyclephaseid}/assign/byschedule{?maxresults}{?scheduleids}{?maintainassignments}{?parenttreeid}{?includehierarchy}{?isCreateWithLatestVersion}",
        "http_method": "POST",
        "category": "other",
        "description": "Create free form release testschedule",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [
            "maxresults",
            "scheduleids",
            "maintainassignments",
            "parenttreeid",
            "includehierarchy",
            "isCreateWithLatestVersion",
        ],
        "path_parameters": ["cyclephaseid"],
        "resource": "Create free form release testschedule [/assignmenttree/{cyclephaseid}/assign/byschedule{?maxresults}{?scheduleids}{?maintainassignments}{?parenttreeid}{?includehierarchy}{?isCreateWithLatestVersion}]",
    },
    {
        "endpoint_path": "/assignmenttree",
        "full_path": "/assignmenttree/{cyclephaseid}/assign/bytree/{parenttreeid}{?includehierarchy}{?dtoResponse}",
        "http_method": "POST",
        "category": "other",
        "description": "Create freeForm testcase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["includehierarchy", "dtoResponse"],
        "path_parameters": ["cyclephaseid", "parenttreeid"],
        "resource": "Create freeForm testcase [/assignmenttree/{cyclephaseid}/assign/bytree/{parenttreeid}{?includehierarchy}{?dtoResponse}]",
    },
    {
        "endpoint_path": "/assignmenttree",
        "full_path": "/assignmenttree/{cyclephaseid}/assign/bysearch/{parenttreeid}{?searchquery}{?maxresults}{?testcaseid}{?zql}{?activeprojectid}{?includehierarchy}",
        "http_method": "POST",
        "category": "other",
        "description": "Create testcase free form using search",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [
            "searchquery",
            "maxresults",
            "testcaseid",
            "zql",
            "activeprojectid",
            "includehierarchy",
        ],
        "path_parameters": ["cyclephaseid", "parenttreeid"],
        "resource": "Create testcase free form using search [/assignmenttree/{cyclephaseid}/assign/bysearch/{parenttreeid}{?searchquery}{?maxresults}{?testcaseid}{?zql}{?activeprojectid}{?includehierarchy}]",
    },
    {
        "endpoint_path": "/attachment",
        "full_path": "/attachment/{id}",
        "http_method": "GET",
        "category": "attachments",
        "description": "Get Attachment Details by id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Get Attachment Details by id [/attachment/{id}]",
    },
    {
        "endpoint_path": "/attachment",
        "full_path": "/attachment{?itemid}{?type}{?isLink}",
        "http_method": "GET",
        "category": "attachments",
        "description": "Get attachment details",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["itemid", "type", "isLink"],
        "path_parameters": [],
        "resource": "Get attachment details [/attachment{?itemid}{?type}{?isLink}]",
    },
    {
        "endpoint_path": "/automation/job/delete",
        "full_path": "/automation/job/delete",
        "http_method": "POST",
        "category": "automation",
        "description": "Delete job using job id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Delete job using job id [/automation/job/delete]",
    },
    {
        "endpoint_path": "/automation/schedule",
        "full_path": "/automation/schedule{?schedulejobid}",
        "http_method": "GET",
        "category": "automation",
        "description": "get Scheduled job via scheduled job id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["schedulejobid"],
        "path_parameters": [],
        "resource": "get Scheduled job via scheduled job id [/automation/schedule{?schedulejobid}]",
    },
    {
        "endpoint_path": "/automation/job/detail",
        "full_path": "/automation/job/detail",
        "http_method": "POST",
        "category": "automation",
        "description": "Configure new Job",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Configure new Job [/automation/job/detail]",
    },
    {
        "endpoint_path": "/upload-file/automation/cancel",
        "full_path": "/upload-file/automation/cancel/{scheduleId}",
        "http_method": "POST",
        "category": "automation",
        "description": "Cancel job by id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["scheduleId"],
        "resource": "Cancel job by id [/upload-file/automation/cancel/{scheduleId}]",
    },
    {
        "endpoint_path": "/upload-file/automation/create-and-execute-job",
        "full_path": "/upload-file/automation/create-and-execute-job",
        "http_method": "POST",
        "category": "automation",
        "description": "Create/execute a job",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create/execute a job [/upload-file/automation/create-and-execute-job]",
    },
    {
        "endpoint_path": "/upload-file/automation/schedule/get-latest-job-progress",
        "full_path": "/upload-file/automation/schedule/get-latest-job-progress{?jobid}",
        "http_method": "GET",
        "category": "automation",
        "description": "Get latest Scheduled Automation Job Progress",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["jobid"],
        "path_parameters": [],
        "resource": "Get latest Scheduled Automation Job Progress  [/upload-file/automation/schedule/get-latest-job-progress{?jobid}]",
    },
    {
        "endpoint_path": "/upload-file/automation/file-upload-job/list",
        "full_path": "/upload-file/automation/file-upload-job/list{?releaseId}{?projectId}",
        "http_method": "GET",
        "category": "automation",
        "description": "All scheduled jobs by project id and release id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["releaseId", "projectId"],
        "path_parameters": [],
        "resource": "All scheduled jobs by project id and release id  [/upload-file/automation/file-upload-job/list{?releaseId}{?projectId}]",
    },
    {
        "endpoint_path": "/upload-file/automation/create-job-detail",
        "full_path": "/upload-file/automation/create-job-detail",
        "http_method": "POST",
        "category": "automation",
        "description": "Create new Job",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create new Job [/upload-file/automation/create-job-detail]",
    },
    {
        "endpoint_path": "/upload-file/automation/execute-job",
        "full_path": "/upload-file/automation/execute-job",
        "http_method": "POST",
        "category": "automation",
        "description": "Schedule/execute job for File Upload",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Schedule/execute job for File Upload [/upload-file/automation/execute-job]",
    },
    {
        "endpoint_path": "/upload-file/automation/update-execute-job",
        "full_path": "/upload-file/automation/update-execute-job",
        "http_method": "POST",
        "category": "automation",
        "description": "Update/execute a job",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Update/execute a job [/upload-file/automation/update-execute-job]",
    },
    {
        "endpoint_path": "/cycle/assignments",
        "full_path": "/cycle/assignments/{releaseid}{?allexecutions}",
        "http_method": "GET",
        "category": "cycles",
        "description": "Calculate assignments for release",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["allexecutions"],
        "path_parameters": ["releaseid"],
        "resource": "Calculate assignments for release [/cycle/assignments/{releaseid}{?allexecutions}]",
    },
    {
        "endpoint_path": "/cycle/clone",
        "full_path": "/cycle/clone/{cycleid}{?deep}{?copyassignments}",
        "http_method": "POST",
        "category": "cycles",
        "description": "Clone a Cycle",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["deep", "copyassignments"],
        "path_parameters": ["cycleid"],
        "resource": "Clone a Cycle  [/cycle/clone/{cycleid}{?deep}{?copyassignments}]",
    },
    {
        "endpoint_path": "/cycle/cyclephase/clone",
        "full_path": "/cycle/cyclephase/clone/{cyclephaseid}",
        "http_method": "POST",
        "category": "cycles",
        "description": "Clone a CyclePhase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["cyclephaseid"],
        "resource": "Clone a CyclePhase [/cycle/cyclephase/clone/{cyclephaseid}]",
    },
    {
        "endpoint_path": "/cycle/copy",
        "full_path": "/cycle/copy/{sourcecyclephaseid}/to/{targetcycleid}",
        "http_method": "POST",
        "category": "cycles",
        "description": "copy a CyclePhase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["sourcecyclephaseid", "targetcycleid"],
        "resource": "copy a CyclePhase [/cycle/copy/{sourcecyclephaseid}/to/{targetcycleid}]",
    },
    {
        "endpoint_path": "/cycle",
        "full_path": "/cycle/",
        "http_method": "POST",
        "category": "cycles",
        "description": "Create a New Cycle",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create a New Cycle [/cycle/]",
    },
    {
        "endpoint_path": "/cycle",
        "full_path": "/cycle/{cycleid}/phase{?scheduleId}",
        "http_method": "POST",
        "category": "cycles",
        "description": "Create Cycle Phase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["scheduleId"],
        "path_parameters": ["cycleid"],
        "resource": "Create Cycle Phase [/cycle/{cycleid}/phase{?scheduleId}]",
    },
    {
        "endpoint_path": "/cycle",
        "full_path": "/cycle/{id}",
        "http_method": "DELETE",
        "category": "cycles",
        "description": "Delete Cycle",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Delete Cycle [/cycle/{id}]",
    },
    {
        "endpoint_path": "/cycle",
        "full_path": "/cycle/{cycleid}/phase/{cyclephaseid}",
        "http_method": "DELETE",
        "category": "cycles",
        "description": "Delete Cycle Phase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["cycleid", "cyclephaseid"],
        "resource": "Delete Cycle Phase [/cycle/{cycleid}/phase/{cyclephaseid}]",
    },
    {
        "endpoint_path": "/cycle",
        "full_path": "/cycle/{cycleid}",
        "http_method": "GET",
        "category": "cycles",
        "description": "Get Cycle by ID",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["cycleid"],
        "resource": "Get Cycle by ID [/cycle/{cycleid}]",
    },
    {
        "endpoint_path": "/cycle/cycleName",
        "full_path": "/cycle/cycleName/{releaseid}{?orderBy}{?cycleName}",
        "http_method": "GET",
        "category": "cycles",
        "description": "Get Cycle names for release",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["orderBy", "cycleName"],
        "path_parameters": ["releaseid"],
        "resource": "Get Cycle names for release [/cycle/cycleName/{releaseid}{?orderBy}{?cycleName}]",
    },
    {
        "endpoint_path": "/cycle/phase/name",
        "full_path": "/cycle/phase/name{?ids}",
        "http_method": "GET",
        "category": "cycles",
        "description": "Get all cyclePhase Names",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["ids"],
        "path_parameters": [],
        "resource": "Get all cyclePhase Names [/cycle/phase/name{?ids}]",
    },
    {
        "endpoint_path": "/cycle/release",
        "full_path": "/cycle/release/{releaseid}",
        "http_method": "GET",
        "category": "cycles",
        "description": "Get Cycle for release",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "Get Cycle for release [/cycle/release/{releaseid}]",
    },
    {
        "endpoint_path": "/cycle/status/count",
        "full_path": "/cycle/status/count/{releaseid}",
        "http_method": "GET",
        "category": "cycles",
        "description": "get status count for releaseid",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "get status count for releaseid [/cycle/status/count/{releaseid}]",
    },
    {
        "endpoint_path": "/cycle/move",
        "full_path": "/cycle/move/{sourcecyclephaseid}/to/{targetcycleid}",
        "http_method": "POST",
        "category": "cycles",
        "description": "Move a CyclePhase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["sourcecyclephaseid", "targetcycleid"],
        "resource": "Move a CyclePhase [/cycle/move/{sourcecyclephaseid}/to/{targetcycleid}]",
    },
    {
        "endpoint_path": "/cycle/toggle",
        "full_path": "/cycle/toggle/{cycleId}/{value}",
        "http_method": "PUT",
        "category": "cycles",
        "description": "get status count for releaseid",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["cycleId", "value"],
        "resource": "get status count for releaseid [/cycle/toggle/{cycleId}/{value}]",
    },
    {
        "endpoint_path": "/cycle",
        "full_path": "/cycle/{cycleId}",
        "http_method": "PUT",
        "category": "cycles",
        "description": "Update a Cycle",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["cycleId"],
        "resource": "Update a Cycle [/cycle/{cycleId}]",
    },
    {
        "endpoint_path": "/cycle",
        "full_path": "/cycle/{cycleid}/phase",
        "http_method": "PUT",
        "category": "cycles",
        "description": "Update Cycle Phase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["cycleid"],
        "resource": "Update Cycle Phase [/cycle/{cycleid}/phase]",
    },
    {
        "endpoint_path": "/defectmapping",
        "full_path": "/defectmapping/",
        "http_method": "POST",
        "category": "defects",
        "description": "Save defect schedule",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Save defect schedule [/defectmapping/]",
    },
    {
        "endpoint_path": "/defect",
        "full_path": "/defect/",
        "http_method": "POST",
        "category": "defects",
        "description": "Create defect in the system.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create defect in the system. [/defect/]",
    },
    {
        "endpoint_path": "/defect",
        "full_path": "/defect/{defectId}?projectId={projectId}",
        "http_method": "GET",
        "category": "defects",
        "description": "Get defect by ID",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["defectId", "projectId"],
        "resource": "Get defect by ID [/defect/{defectId}?projectId={projectId}]",
    },
    {
        "endpoint_path": "//executionchangehistory",
        "full_path": "//executionchangehistory{?releaseTestScheduleId}{?isascorder}{?offset}{?pagesize}",
        "http_method": "GET",
        "category": "other",
        "description": "Get Testcase usage history details",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "releaseTestScheduleId",
            "isascorder",
            "offset",
            "pagesize",
        ],
        "path_parameters": [],
        "resource": "Get Testcase usage history details [//executionchangehistory{?releaseTestScheduleId}{?isascorder}{?offset}{?pagesize}]",
    },
    {
        "endpoint_path": "/execution/assign",
        "full_path": "/execution/assign",
        "http_method": "PUT",
        "category": "executions",
        "description": "Assign/Reassign schedules values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Assign/Reassign schedules values [/execution/assign]",
    },
    {
        "endpoint_path": "/execution/bulk",
        "full_path": "/execution/bulk{?scheduleids}{?status}{?testerid}{?tcrCatalogTreeId}{?allExecutions}{?includeanyoneuser}",
        "http_method": "PUT",
        "category": "executions",
        "description": "Execute testcases",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "scheduleids",
            "status",
            "testerid",
            "tcrCatalogTreeId",
            "allExecutions",
            "includeanyoneuser",
        ],
        "path_parameters": [],
        "resource": "Execute testcases [/execution/bulk{?scheduleids}{?status}{?testerid}{?tcrCatalogTreeId}{?allExecutions}{?includeanyoneuser}]",
    },
    {
        "endpoint_path": "/execution",
        "full_path": "/execution/",
        "http_method": "POST",
        "category": "executions",
        "description": "Create schedules values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create schedules values [/execution/]",
    },
    {
        "endpoint_path": "/execution",
        "full_path": "/execution{?ids}",
        "http_method": "DELETE",
        "category": "executions",
        "description": "Delete / Unassign test schedules",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["ids"],
        "path_parameters": [],
        "resource": "Delete / Unassign test schedules [/execution{?ids}]",
    },
    {
        "endpoint_path": "/execution",
        "full_path": "/execution/{cyclephaseid}/testcase{?testcaseids}{?tcrCatalogTreeId}{?filterTcName}",
        "http_method": "DELETE",
        "category": "executions",
        "description": "Delete / Unassign frozen test cases and schedules",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["testcaseids", "tcrCatalogTreeId", "filterTcName"],
        "path_parameters": ["cyclephaseid"],
        "resource": "Delete / Unassign frozen test cases and schedules [/execution/{cyclephaseid}/testcase{?testcaseids}{?tcrCatalogTreeId}{?filterTcName}]",
    },
    {
        "endpoint_path": "/execution/path",
        "full_path": "/execution/path{?scheduleid}{?assigneeuserid}",
        "http_method": "GET",
        "category": "executions",
        "description": "Get node path",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["scheduleid", "assigneeuserid"],
        "path_parameters": [],
        "resource": "Get node path [/execution/path{?scheduleid}{?assigneeuserid}]",
    },
    {
        "endpoint_path": "/execution",
        "full_path": "/execution/{id}",
        "http_method": "GET",
        "category": "executions",
        "description": "To get Schedule by ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "To get Schedule by ID [/execution/{id}]",
    },
    {
        "endpoint_path": "/execution/ids",
        "full_path": "/execution/ids{?ids}",
        "http_method": "GET",
        "category": "executions",
        "description": "To schedule by schedule IDs",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["ids"],
        "path_parameters": [],
        "resource": "To schedule by schedule IDs [/execution/ids{?ids}]",
    },
    {
        "endpoint_path": "/execution/expanded",
        "full_path": "/execution/expanded{?ids}{?stepresults}{?resulthistory}",
        "http_method": "GET",
        "category": "executions",
        "description": "To schedule by schedule ids",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["ids", "stepresults", "resulthistory"],
        "path_parameters": [],
        "resource": "To schedule by schedule ids [/execution/expanded{?ids}{?stepresults}{?resulthistory}]",
    },
    {
        "endpoint_path": "/execution/user/project",
        "full_path": "/execution/user/project{?projectid}{?createdby}{?testerid}{?parentid}{?cyclephaseid}{?releaseid}{?order}{?orderByAsc}{?offset}{?pagesize}",
        "http_method": "GET",
        "category": "executions",
        "description": "Get Schedules by Criteria",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "projectid",
            "createdby",
            "testerid",
            "parentid",
            "cyclephaseid",
            "releaseid",
            "order",
            "orderByAsc",
            "offset",
            "pagesize",
        ],
        "path_parameters": [],
        "resource": "Get Schedules by Criteria [/execution/user/project{?projectid}{?createdby}{?testerid}{?parentid}{?cyclephaseid}{?releaseid}{?order}{?orderByAsc}{?offset}{?pagesize}]",
    },
    {
        "endpoint_path": "/execution",
        "full_path": "/execution{?testerid}{?parentid}{?cyclephaseid}{?releaseid}{?order}{?isascorder}{?offset}{?includeanyoneuser}{?pagesize}{?is_cfield}",
        "http_method": "GET",
        "category": "executions",
        "description": "Get Schedules by Criteria",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "testerid",
            "parentid",
            "cyclephaseid",
            "releaseid",
            "order",
            "isascorder",
            "offset",
            "includeanyoneuser",
            "pagesize",
            "is_cfield",
        ],
        "path_parameters": [],
        "resource": "Get Schedules by Criteria [/execution{?testerid}{?parentid}{?cyclephaseid}{?releaseid}{?order}{?isascorder}{?offset}{?includeanyoneuser}{?pagesize}{?is_cfield}]",
    },
    {
        "endpoint_path": "/execution/byfilter",
        "full_path": "/execution/byfilter{?testcaseid}{?releaseid}{?rtsid}{?order}{?isascorder}{?offset}{?pagesize}",
        "http_method": "GET",
        "category": "executions",
        "description": "Get Teststep results by IDs",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "testcaseid",
            "releaseid",
            "rtsid",
            "order",
            "isascorder",
            "offset",
            "pagesize",
        ],
        "path_parameters": [],
        "resource": "Get Teststep results by IDs [/execution/byfilter{?testcaseid}{?releaseid}{?rtsid}{?order}{?isascorder}{?offset}{?pagesize}]",
    },
    {
        "endpoint_path": "/execution/modify",
        "full_path": "/execution/modify",
        "http_method": "POST",
        "category": "executions",
        "description": "Modify schedules values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Modify schedules values [/execution/modify]",
    },
    {
        "endpoint_path": "/execution/statusandattachment",
        "full_path": "/execution/statusandattachment/{id}{?status}",
        "http_method": "PUT",
        "category": "executions",
        "description": "To update execution details, attachment and status",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["status"],
        "path_parameters": ["id"],
        "resource": "To update execution details, attachment and status [/execution/statusandattachment/{id}{?status}]",
    },
    {
        "endpoint_path": "/execution",
        "full_path": "/execution/{id}{?status}{?testerid}{?time}{?allExecutions}{?includeanyoneuser}",
        "http_method": "PUT",
        "category": "executions",
        "description": "To update execution details",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "status",
            "testerid",
            "time",
            "allExecutions",
            "includeanyoneuser",
        ],
        "path_parameters": ["id"],
        "resource": "To update execution details [/execution/{id}{?status}{?testerid}{?time}{?allExecutions}{?includeanyoneuser}]",
    },
    {
        "endpoint_path": "/execution",
        "full_path": "/execution",
        "http_method": "PUT",
        "category": "executions",
        "description": "Update Schedules Values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Update Schedules Values [/execution]",
    },
    {
        "endpoint_path": "/execution/updateteststatus",
        "full_path": "/execution/updateteststatus",
        "http_method": "POST",
        "category": "executions",
        "description": "Update Test Execution Status",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Update Test Execution Status [/execution/updateteststatus]",
    },
    {
        "endpoint_path": "/externalrequirement/importall",
        "full_path": "/externalrequirement/importall{?projectId}",
        "http_method": "POST",
        "category": "other",
        "description": "Import External Requirement Based on Filter or JQL",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["projectId"],
        "path_parameters": [],
        "resource": "Import External Requirement Based on Filter or JQL [/externalrequirement/importall{?projectId}]",
    },
    {
        "endpoint_path": "/externalGroup/importGroupsAndUsers",
        "full_path": "/externalGroup/importGroupsAndUsers",
        "http_method": "POST",
        "category": "other",
        "description": "Import groups and users from the list",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Import groups and users from the list [/externalGroup/importGroupsAndUsers]",
    },
    {
        "endpoint_path": "/externalGroup/search",
        "full_path": "/externalGroup/search{?name}{?pagesize}",
        "http_method": "GET",
        "category": "other",
        "description": "Search groups in LDAP or crowd",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["name", "pagesize"],
        "path_parameters": [],
        "resource": "Search groups in LDAP or crowd [/externalGroup/search{?name}{?pagesize}]",
    },
    {
        "endpoint_path": "/externalGroup/sync",
        "full_path": "/externalGroup/sync",
        "http_method": "PUT",
        "category": "other",
        "description": "Sync groups and users from the list",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Sync groups and users from the list [/externalGroup/sync]",
    },
    {
        "endpoint_path": "/field",
        "full_path": "/field/",
        "http_method": "POST",
        "category": "fields",
        "description": "Add Custom Field",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Add Custom Field [/field/]",
    },
    {
        "endpoint_path": "/field/fieldtype",
        "full_path": "/field/fieldtype",
        "http_method": "GET",
        "category": "fields",
        "description": "Get all the field's type metadata.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get all the field's type metadata. [/field/fieldtype]",
    },
    {
        "endpoint_path": "/field/metadata",
        "full_path": "/field/metadata{?visible}",
        "http_method": "GET",
        "category": "fields",
        "description": "Get customfield metadata",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["visible"],
        "path_parameters": [],
        "resource": "Get customfield metadata  [/field/metadata{?visible}]",
    },
    {
        "endpoint_path": "/field",
        "full_path": "/field/{id}",
        "http_method": "GET",
        "category": "fields",
        "description": "Get Field by Id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Get Field by Id [/field/{id}]",
    },
    {
        "endpoint_path": "/field/name",
        "full_path": "/field/name{?name}{?projectid}",
        "http_method": "GET",
        "category": "fields",
        "description": "Get Field by dispaly name",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["name", "projectid"],
        "path_parameters": [],
        "resource": "Get Field by dispaly name [/field/name{?name}{?projectid}]",
    },
    {
        "endpoint_path": "/field",
        "full_path": "/field{?name}",
        "http_method": "GET",
        "category": "fields",
        "description": "Get Field by fieldName",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["name"],
        "path_parameters": [],
        "resource": "Get Field by fieldName [/field{?name}]",
    },
    {
        "endpoint_path": "/field/importfields",
        "full_path": "/field/importfields/{entityName}",
        "http_method": "GET",
        "category": "fields",
        "description": "Get Importable Fields By Entity",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["entityName"],
        "resource": "Get Importable Fields By Entity  [/field/importfields/{entityName}]",
    },
    {
        "endpoint_path": "/field/ids",
        "full_path": "/field/ids{?ids}",
        "http_method": "GET",
        "category": "fields",
        "description": "Get list of CustomFields",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["ids"],
        "path_parameters": [],
        "resource": "Get list of CustomFields [/field/ids{?ids}]",
    },
    {
        "endpoint_path": "/field/project",
        "full_path": "/field/project/{id}",
        "http_method": "GET",
        "category": "fields",
        "description": "Get list of project specific CustomFields",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Get list of project specific CustomFields [/field/project/{id}]",
    },
    {
        "endpoint_path": "/field/entity",
        "full_path": "/field/entity/{entityname}{?includsystemfield}",
        "http_method": "GET",
        "category": "fields",
        "description": "Get fields by entity",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["includsystemfield"],
        "path_parameters": ["entityname"],
        "resource": "Get fields by entity [/field/entity/{entityname}{?includsystemfield}]",
    },
    {
        "endpoint_path": "/field/cascade",
        "full_path": "/field/cascade",
        "http_method": "PUT",
        "category": "fields",
        "description": "Update Cascade",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Update Cascade [/field/cascade]",
    },
    {
        "endpoint_path": "/field/validate",
        "full_path": "/field/validate{?id}{?entityname}{?searchfieldname}",
        "http_method": "GET",
        "category": "fields",
        "description": "Validating field in the system.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["id", "entityname", "searchfieldname"],
        "path_parameters": [],
        "resource": "Validating field in the system. [/field/validate{?id}{?entityname}{?searchfieldname}]",
    },
    {
        "endpoint_path": "/fieldmap",
        "full_path": "/fieldmap/",
        "http_method": "POST",
        "category": "fields",
        "description": "create field map",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "create field map  [/fieldmap/]",
    },
    {
        "endpoint_path": "/fileWatcher/watcher",
        "full_path": "/fileWatcher/watcher{?schedulejobid}",
        "http_method": "GET",
        "category": "other",
        "description": "get Scheduled job via scheduled job id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["schedulejobid"],
        "path_parameters": [],
        "resource": "get Scheduled job via scheduled job id [/fileWatcher/watcher{?schedulejobid}]",
    },
    {
        "endpoint_path": "/fileWatcher/watcher",
        "full_path": "/fileWatcher/watcher",
        "http_method": "POST",
        "category": "other",
        "description": "Schedule job for ZBlast",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Schedule job for ZBlast [/fileWatcher/watcher]",
    },
    {
        "endpoint_path": "/gadget",
        "full_path": "/gadget/{dashboardId}",
        "http_method": "GET",
        "category": "other",
        "description": "Get all requirement node and requirement name by release id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["dashboardId"],
        "resource": "Get all requirement node and requirement name by release id [/gadget/{dashboardId}]",
    },
    {
        "endpoint_path": "/global-repository/project",
        "full_path": "/global-repository/project",
        "http_method": "GET",
        "category": "other",
        "description": "Get All projects that allowed access to current global reporsitory user",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All projects that allowed access to current global reporsitory user [/global-repository/project]",
    },
    {
        "endpoint_path": "/group",
        "full_path": "/group/",
        "http_method": "POST",
        "category": "groups",
        "description": "Create group in the System",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create group in the System [/group/]",
    },
    {
        "endpoint_path": "/group",
        "full_path": "/group",
        "http_method": "PUT",
        "category": "groups",
        "description": "Update group in the System",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Update group in the System [/group]",
    },
    {
        "endpoint_path": "/import",
        "full_path": "/import/",
        "http_method": "POST",
        "category": "other",
        "description": "Add new import job",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Add new import job [/import/]",
    },
    {
        "endpoint_path": "/import/execute",
        "full_path": "/import/execute/{id}/{action}",
        "http_method": "PUT",
        "category": "other",
        "description": "Execute import job by id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id", "action"],
        "resource": "Execute import job by id [/import/execute/{id}/{action}]",
    },
    {
        "endpoint_path": "/info/license",
        "full_path": "/info/license",
        "http_method": "GET",
        "category": "info",
        "description": "Get License Information.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get License Information. [/info/license]",
    },
    {
        "endpoint_path": "/license",
        "full_path": "/license/",
        "http_method": "GET",
        "category": "license",
        "description": "Get License Information",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get License Information [/license/]",
    },
    {
        "endpoint_path": "/parsertemplate",
        "full_path": "/parsertemplate/",
        "http_method": "POST",
        "category": "other",
        "description": "Create Template",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create Template  [/parsertemplate/]",
    },
    {
        "endpoint_path": "/parsertemplate",
        "full_path": "/parsertemplate/{id}",
        "http_method": "DELETE",
        "category": "other",
        "description": "Delete Template",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Delete Template  [/parsertemplate/{id}]",
    },
    {
        "endpoint_path": "/parsertemplate",
        "full_path": "/parsertemplate/{TemplateId}",
        "http_method": "GET",
        "category": "other",
        "description": "Get Template",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["TemplateId"],
        "resource": "Get Template  [/parsertemplate/{TemplateId}]",
    },
    {
        "endpoint_path": "/parsertemplate",
        "full_path": "/parsertemplate",
        "http_method": "GET",
        "category": "other",
        "description": "Get List of Templates",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get List of Templates  [/parsertemplate]",
    },
    {
        "endpoint_path": "/parsertemplate",
        "full_path": "/parsertemplate/{templateId}",
        "http_method": "PUT",
        "category": "other",
        "description": "Update Template",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["templateId"],
        "resource": "Update Template  [/parsertemplate/{templateId}]",
    },
    {
        "endpoint_path": "/project",
        "full_path": "/project/",
        "http_method": "POST",
        "category": "projects",
        "description": "Create Project",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create Project [/project/]",
    },
    {
        "endpoint_path": "/project/details",
        "full_path": "/project/details",
        "http_method": "GET",
        "category": "projects",
        "description": "Get All Normal Project Details",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All Normal Project Details [/project/details]",
    },
    {
        "endpoint_path": "/project/normal",
        "full_path": "/project/normal",
        "http_method": "GET",
        "category": "projects",
        "description": "Get All Normal project",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All Normal project [/project/normal]",
    },
    {
        "endpoint_path": "/project/all/leads",
        "full_path": "/project/all/leads",
        "http_method": "GET",
        "category": "projects",
        "description": "Get lead for all projects",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get lead for all projects [/project/all/leads]",
    },
    {
        "endpoint_path": "/project",
        "full_path": "/project/{id}{?isLite}",
        "http_method": "GET",
        "category": "projects",
        "description": "Get Project by ID",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["isLite"],
        "path_parameters": ["id"],
        "resource": "Get Project by ID [/project/{id}{?isLite}]",
    },
    {
        "endpoint_path": "/project/user",
        "full_path": "/project/user/{UserID}?isLite=False&adminUser=False",
        "http_method": "GET",
        "category": "projects",
        "description": "Get Project by User ID",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["UserID"],
        "resource": "Get Project by User ID [/project/user/{UserID}?isLite=False&adminUser=False]",
    },
    {
        "endpoint_path": "/project/project",
        "full_path": "/project/project/{UserID}",
        "http_method": "GET",
        "category": "projects",
        "description": "Get allocated Projects",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["UserID"],
        "resource": "Get allocated Projects [/project/project/{UserID}]",
    },
    {
        "endpoint_path": "/project/count/allprojects",
        "full_path": "/project/count/allprojects",
        "http_method": "GET",
        "category": "projects",
        "description": "Get Project Team Count for all projects",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get Project Team Count for all projects [/project/count/allprojects]",
    },
    {
        "endpoint_path": "/project/count/allusers",
        "full_path": "/project/count/allusers",
        "http_method": "GET",
        "category": "projects",
        "description": "Get Project Team Count for all users",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get Project Team Count for all users [/project/count/allusers]",
    },
    {
        "endpoint_path": "/project/allocated/projects",
        "full_path": "/project/allocated/projects",
        "http_method": "GET",
        "category": "projects",
        "description": "Get Project Team  for Allocated Projects",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get Project Team  for Allocated Projects [/project/allocated/projects]",
    },
    {
        "endpoint_path": "/project/projectteam",
        "full_path": "/project/projectteam/{pid}",
        "http_method": "GET",
        "category": "projects",
        "description": "Get Project team for project",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["pid"],
        "resource": "Get Project team for project [/project/projectteam/{pid}]",
    },
    {
        "endpoint_path": "/project",
        "full_path": "/project{?userId}{?isLite}",
        "http_method": "GET",
        "category": "projects",
        "description": "Get All projects by UserId",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["userId", "isLite"],
        "path_parameters": [],
        "resource": "Get All projects by UserId [/project{?userId}{?isLite}]",
    },
    {
        "endpoint_path": "/project/lite",
        "full_path": "/project/lite",
        "http_method": "GET",
        "category": "projects",
        "description": "Get All projects",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All projects  [/project/lite]",
    },
    {
        "endpoint_path": "/project/shared",
        "full_path": "/project/shared",
        "http_method": "GET",
        "category": "projects",
        "description": "Get All Shared projects",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All Shared projects  [/project/shared]",
    },
    {
        "endpoint_path": "/project/sharedprojects",
        "full_path": "/project/sharedprojects/{projectid}",
        "http_method": "GET",
        "category": "projects",
        "description": "Get Shared projects",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["projectid"],
        "resource": "Get Shared projects  [/project/sharedprojects/{projectid}]",
    },
    {
        "endpoint_path": "/project/sharedtoprojects",
        "full_path": "/project/sharedtoprojects/{projectid}",
        "http_method": "GET",
        "category": "projects",
        "description": "Get Shared projects shared to given project",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["projectid"],
        "resource": "Get Shared projects shared to given project [/project/sharedtoprojects/{projectid}]",
    },
    {
        "endpoint_path": "/project",
        "full_path": "/project",
        "http_method": "PUT",
        "category": "projects",
        "description": "Assign User to the Project",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Assign User to the Project [/project]",
    },
    {
        "endpoint_path": "/project",
        "full_path": "/project/{projectId}/migrate{?externalStorageId}",
        "http_method": "POST",
        "category": "projects",
        "description": "Project storage migration",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["externalStorageId"],
        "path_parameters": ["projectId"],
        "resource": "Project storage migration [/project/{projectId}/migrate{?externalStorageId}]",
    },
    {
        "endpoint_path": "/project",
        "full_path": "/project/{projectId}/migration/retry",
        "http_method": "PUT",
        "category": "projects",
        "description": "Retry failed attachment migration",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["projectId"],
        "resource": "Retry failed attachment migration [/project/{projectId}/migration/retry]",
    },
    {
        "endpoint_path": "/release",
        "full_path": "/release/",
        "http_method": "POST",
        "category": "releases",
        "description": "Create New Release",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create New Release [/release/]",
    },
    {
        "endpoint_path": "/release/paged/project",
        "full_path": "/release/paged/project/{projectid}{?pagesize}{?offset}{?order}{?isascorder}{?isVisible}",
        "http_method": "GET",
        "category": "releases",
        "description": "Get releases for a project through page and offset",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["pagesize", "offset", "order", "isascorder", "isVisible"],
        "path_parameters": ["projectid"],
        "resource": "Get releases for a project through page and offset [/release/paged/project/{projectid}{?pagesize}{?offset}{?order}{?isascorder}{?isVisible}]",
    },
    {
        "endpoint_path": "/release",
        "full_path": "/release/{releaseid}",
        "http_method": "GET",
        "category": "releases",
        "description": "Get Release by Release ID",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "Get Release by Release ID [/release/{releaseid}]",
    },
    {
        "endpoint_path": "/release",
        "full_path": "/release",
        "http_method": "GET",
        "category": "releases",
        "description": "Get all releases for all projects with Access",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get all releases for all projects with Access [/release]",
    },
    {
        "endpoint_path": "/release/project",
        "full_path": "/release/project/{projectid}",
        "http_method": "GET",
        "category": "releases",
        "description": "Get releases for a project",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["projectid"],
        "resource": "Get releases for a project [/release/project/{projectid}]",
    },
    {
        "endpoint_path": "/requirement",
        "full_path": "/requirement/",
        "http_method": "POST",
        "category": "requirements",
        "description": "Create new requirement",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create new requirement [/requirement/]",
    },
    {
        "endpoint_path": "/requirement",
        "full_path": "/requirement/{id}",
        "http_method": "PUT",
        "category": "requirements",
        "description": "Update Requirement",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Update Requirement [/requirement/{id}]",
    },
    {
        "endpoint_path": "/requirement/bulk",
        "full_path": "/requirement/bulk",
        "http_method": "POST",
        "category": "requirements",
        "description": "Bulk Update Requirement",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Bulk Update Requirement [/requirement/bulk]",
    },
    {
        "endpoint_path": "/requirementtree/add",
        "full_path": "/requirementtree/add/",
        "http_method": "POST",
        "category": "requirements",
        "description": "Create new requirement tree",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create new requirement tree [/requirementtree/add/]",
    },
    {
        "endpoint_path": "/role",
        "full_path": "/role/",
        "http_method": "POST",
        "category": "roles",
        "description": "Add role",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Add role [/role/]",
    },
    {
        "endpoint_path": "/role/permission",
        "full_path": "/role/permission{?roleid}",
        "http_method": "PUT",
        "category": "roles",
        "description": "Save or assign role permissions",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["roleid"],
        "path_parameters": [],
        "resource": "Save or assign role permissions [/role/permission{?roleid}]",
    },
    {
        "endpoint_path": "/advancesearch/reindex",
        "full_path": "/advancesearch/reindex/{pid}",
        "http_method": "PUT",
        "category": "search",
        "description": "Reindex specific project by id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["pid"],
        "resource": "Reindex specific project by id [/advancesearch/reindex/{pid}]",
    },
    {
        "endpoint_path": "/advancesearch",
        "full_path": "/advancesearch/",
        "http_method": "POST",
        "category": "search",
        "description": "Search via filters",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Search via filters [/advancesearch/]",
    },
    {
        "endpoint_path": "/advancesearch/zql",
        "full_path": "/advancesearch/zql",
        "http_method": "POST",
        "category": "search",
        "description": "Search via filters",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Search via filters [/advancesearch/zql]",
    },
    {
        "endpoint_path": "/advancesearch/testexecutions",
        "full_path": "/advancesearch/testexecutions/{altid}{?maxresults}",
        "http_method": "GET",
        "category": "search",
        "description": "Search test executions for given altId",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["maxresults"],
        "path_parameters": ["altid"],
        "resource": "Search test executions for given altId [/advancesearch/testexecutions/{altid}{?maxresults}]",
    },
    {
        "endpoint_path": "/testcase/search/update/bulk",
        "full_path": "/testcase/search/update/bulk?releaseId={releaseid}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Search and Edit the Testcase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "Search and Edit the Testcase [/testcase/search/update/bulk?releaseId={releaseid}]",
    },
    {
        "endpoint_path": "/testcase/search/update/bulk",
        "full_path": "/testcase/search/update/bulk?releaseId={releaseid}",
        "http_method": "/TESTCASE/SEARCH/ALLOCATE/BULK/REQUIREMENT",
        "category": "testcases",
        "description": "Search and Edit the Testcase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "Search and Edit the Testcase [/testcase/search/update/bulk?releaseId={releaseid}]",
    },
    {
        "endpoint_path": "POST",
        "full_path": "POST",
        "http_method": "/TESTCASE/SEARCH/DELETE/BULK?RELEASEID={RELEASEID}",
        "category": "other",
        "description": "Search and Map the Testcase",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Search and Map the Testcase [POST]",
    },
    {
        "endpoint_path": "/advancesearch/reindex/health",
        "full_path": "/advancesearch/reindex/health",
        "http_method": "GET",
        "category": "search",
        "description": "Check Indexing Health",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Check Indexing Health [/advancesearch/reindex/health]",
    },
    {
        "endpoint_path": "/system/info/cache/clear",
        "full_path": "/system/info/cache/clear{?clearall}{?cachename}",
        "http_method": "POST",
        "category": "system",
        "description": "Clear the Specified Cache",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["clearall", "cachename"],
        "path_parameters": [],
        "resource": "Clear the Specified Cache [/system/info/cache/clear{?clearall}{?cachename}]",
    },
    {
        "endpoint_path": "/system/info/downloadzbot",
        "full_path": "/system/info/downloadzbot",
        "http_method": "PUT",
        "category": "system",
        "description": "Download Zbot",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Download Zbot [/system/info/downloadzbot]",
    },
    {
        "endpoint_path": "/system/info/cache/info",
        "full_path": "/system/info/cache/info",
        "http_method": "GET",
        "category": "system",
        "description": "Get All list of Caches",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get All list of Caches [/system/info/cache/info]",
    },
    {
        "endpoint_path": "/system/info/channelinfo",
        "full_path": "/system/info/channelinfo",
        "http_method": "GET",
        "category": "system",
        "description": "Get Channel Information",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get Channel Information [/system/info/channelinfo]",
    },
    {
        "endpoint_path": "/system/info/license",
        "full_path": "/system/info/license",
        "http_method": "GET",
        "category": "system",
        "description": "Get License Information",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get License Information [/system/info/license]",
    },
    {
        "endpoint_path": "/system/info/servertime",
        "full_path": "/system/info/servertime",
        "http_method": "GET",
        "category": "system",
        "description": "Get License Information",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get License Information [/system/info/servertime]",
    },
    {
        "endpoint_path": "/system/info/stats",
        "full_path": "/system/info/stats",
        "http_method": "GET",
        "category": "system",
        "description": "Get License Information",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get License Information [/system/info/stats]",
    },
    {
        "endpoint_path": "/license/detail",
        "full_path": "/license/detail",
        "http_method": "GET",
        "category": "license",
        "description": "Get License Detail Information",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get License Detail Information [/license/detail]",
    },
    {
        "endpoint_path": "/license/peak/detail",
        "full_path": "/license/peak/detail?licensetype={licensetype}",
        "http_method": "GET",
        "category": "license",
        "description": "License Peak Usage Detail",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["licensetype"],
        "resource": "License Peak Usage Detail [/license/peak/detail?licensetype={licensetype}]",
    },
    {
        "endpoint_path": "/execution/teststepresult/bytctid",
        "full_path": "/execution/teststepresult/bytctid{?tctid}",
        "http_method": "GET",
        "category": "executions",
        "description": "Get teststep results by ID's",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["tctid"],
        "path_parameters": [],
        "resource": "Get teststep results by ID's [/execution/teststepresult/bytctid{?tctid}]",
    },
    {
        "endpoint_path": "/execution/teststepresult",
        "full_path": "/execution/teststepresult/{id}",
        "http_method": "GET",
        "category": "executions",
        "description": "Get Test Step Result",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Get Test Step Result [/execution/teststepresult/{id}]",
    },
    {
        "endpoint_path": "/execution/teststepresult",
        "full_path": "/execution/teststepresult{?sids}{?cyclephaseid}",
        "http_method": "GET",
        "category": "executions",
        "description": "Get test step results by criteria",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["sids", "cyclephaseid"],
        "path_parameters": [],
        "resource": "Get test step results by criteria [/execution/teststepresult{?sids}{?cyclephaseid}]",
    },
    {
        "endpoint_path": "/execution/teststepresult/saveorupdate",
        "full_path": "/execution/teststepresult/saveorupdate",
        "http_method": "POST",
        "category": "executions",
        "description": "Save or Update Test step result",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Save or Update Test step result [/execution/teststepresult/saveorupdate]",
    },
    {
        "endpoint_path": "/testcase/allocate/requirement",
        "full_path": "/testcase/allocate/requirement/{testcaseid}{?releaseid}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Allocate Requirements to testcase Id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["releaseid"],
        "path_parameters": ["testcaseid"],
        "resource": "Allocate Requirements to testcase Id  [/testcase/allocate/requirement/{testcaseid}{?releaseid}]",
    },
    {
        "endpoint_path": "/testcase/allocate/requirement",
        "full_path": "/testcase/allocate/requirement{?releaseid}{?tcrCatalogTreeId}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Allocate Requirements to testcase Ids",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["releaseid", "tcrCatalogTreeId"],
        "path_parameters": [],
        "resource": "Allocate Requirements to testcase Ids  [/testcase/allocate/requirement{?releaseid}{?tcrCatalogTreeId}]",
    },
    {
        "endpoint_path": "/testcase/bulk",
        "full_path": "/testcase/bulk{?externalid}{?priority}{?tag}{?comments}{?scriptpath}{?scriptid}{?scriptname}{?automated}{?estimatedtime}{?testcaseid}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Bulk Update Testcase values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "externalid",
            "priority",
            "tag",
            "comments",
            "scriptpath",
            "scriptid",
            "scriptname",
            "automated",
            "estimatedtime",
            "testcaseid",
        ],
        "path_parameters": [],
        "resource": "Bulk Update Testcase values [/testcase/bulk{?externalid}{?priority}{?tag}{?comments}{?scriptpath}{?scriptid}{?scriptname}{?automated}{?estimatedtime}{?testcaseid}]",
    },
    {
        "endpoint_path": "/testcase/update/bulk",
        "full_path": "/testcase/update/bulk{?tcrCatalogTreeId}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Bulk Update Testcase values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["tcrCatalogTreeId"],
        "path_parameters": [],
        "resource": "Bulk Update Testcase values [/testcase/update/bulk{?tcrCatalogTreeId}]",
    },
    {
        "endpoint_path": "/testcase/clone/on",
        "full_path": "/testcase/clone/on/{releaseid}/to/{targettreeid}{?sourceitemids}{?link}{?cloneAllDetails}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Clone Testcase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["sourceitemids", "link", "cloneAllDetails"],
        "path_parameters": ["releaseid", "targettreeid"],
        "resource": "Clone Testcase [/testcase/clone/on/{releaseid}/to/{targettreeid}{?sourceitemids}{?link}{?cloneAllDetails}]",
    },
    {
        "endpoint_path": "/testcase/bulk",
        "full_path": "/testcase/bulk{?scheduleId}{?nobulkcommit}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Create bulk Testcase",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["scheduleId", "nobulkcommit"],
        "path_parameters": [],
        "resource": "Create bulk Testcase [/testcase/bulk{?scheduleId}{?nobulkcommit}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/",
        "http_method": "POST",
        "category": "testcases",
        "description": "Create Testcase",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create Testcase [/testcase/]",
    },
    {
        "endpoint_path": "/testcase/createnewversion",
        "full_path": "/testcase/createnewversion/{id}",
        "http_method": "POST",
        "category": "testcases",
        "description": "create new version of testcase",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "create new version of testcase [/testcase/createnewversion/{id}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/{id}",
        "http_method": "DELETE",
        "category": "testcases",
        "description": "Delete Testcase",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Delete Testcase  [/testcase/{id}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase{?tcrCatalogTreeId}",
        "http_method": "DELETE",
        "category": "testcases",
        "description": "Delete Multiple Testcase Tree Linkage",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["tcrCatalogTreeId"],
        "path_parameters": [],
        "resource": "Delete Multiple Testcase Tree Linkage [/testcase{?tcrCatalogTreeId}]",
    },
    {
        "endpoint_path": "/testcase/requirement",
        "full_path": "/testcase/requirement/{testcaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Requirement Summary by Testcase ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["testcaseid"],
        "resource": "Get Requirement Summary by Testcase ID [/testcase/requirement/{testcaseid}]",
    },
    {
        "endpoint_path": "/testcase/tags",
        "full_path": "/testcase/tags",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get all tags",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get all tags [/testcase/tags]",
    },
    {
        "endpoint_path": "/testcase/tags",
        "full_path": "/testcase/tags/{releaseid}{?fetchall}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get all tags",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["fetchall"],
        "path_parameters": ["releaseid"],
        "resource": "Get all tags [/testcase/tags/{releaseid}{?fetchall}]",
    },
    {
        "endpoint_path": "/testcase/name",
        "full_path": "/testcase/name{?tcid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get all Testcase Names by Testcase IDs",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["tcid"],
        "path_parameters": [],
        "resource": "Get all Testcase Names by Testcase IDs [/testcase/name{?tcid}]",
    },
    {
        "endpoint_path": "/testcase/count",
        "full_path": "/testcase/count{?tcrcatalogtreeid}{?releaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Count Of Testcases By Phase",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["tcrcatalogtreeid", "releaseid"],
        "path_parameters": [],
        "resource": "Get Count Of Testcases By Phase [/testcase/count{?tcrcatalogtreeid}{?releaseid}]",
    },
    {
        "endpoint_path": "/testcase/count/ids",
        "full_path": "/testcase/count/ids{?treeids}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Count Of Testcases By Phase ids.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["treeids"],
        "path_parameters": [],
        "resource": "Get Count Of Testcases By Phase ids. [/testcase/count/ids{?treeids}]",
    },
    {
        "endpoint_path": "/testcase/count",
        "full_path": "/testcase/count/{releaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Count Of Testcases By Phase ids.",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "Get Count Of Testcases By Phase ids. [/testcase/count/{releaseid}]",
    },
    {
        "endpoint_path": "/testcase/cumulative",
        "full_path": "/testcase/cumulative{?releaseid}{?requirementid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Cumulative Testcase by Release ID and Requirement ID.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["releaseid", "requirementid"],
        "path_parameters": [],
        "resource": "Cumulative Testcase by Release ID and Requirement ID. [/testcase/cumulative{?releaseid}{?requirementid}]",
    },
    {
        "endpoint_path": "/testcase/cumulative/data",
        "full_path": "/testcase/cumulative/data{?releaseid}{?requirementid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Cumulative Testcase by Release ID and Requirement ID.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["releaseid", "requirementid"],
        "path_parameters": [],
        "resource": "Get Cumulative Testcase by Release ID and Requirement ID. [/testcase/cumulative/data{?releaseid}{?requirementid}]",
    },
    {
        "endpoint_path": "/testcase/count/discrete",
        "full_path": "/testcase/count/discrete/{releaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Testcase count per node",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "Testcase count per node [/testcase/count/discrete/{releaseid}]",
    },
    {
        "endpoint_path": "/testcase/path",
        "full_path": "/testcase/path{?testcaseid}{?tctid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Traceable Path from Root",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["testcaseid", "tctid"],
        "path_parameters": [],
        "resource": "Get Traceable Path from Root [/testcase/path{?testcaseid}{?tctid}]",
    },
    {
        "endpoint_path": "/testcase/pathbyrelease",
        "full_path": "/testcase/pathbyrelease{?testcaseid}{?releaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Traceable Path from Root",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["testcaseid", "releaseid"],
        "path_parameters": [],
        "resource": "Get Traceable Path from Root [/testcase/pathbyrelease{?testcaseid}{?releaseid}]",
    },
    {
        "endpoint_path": "/testcase/planning",
        "full_path": "/testcase/planning/{treeId}{?offset}{?pagesize}{?order}{?isascorder}{?tcname}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase by Criteria",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["offset", "pagesize", "order", "isascorder", "tcname"],
        "path_parameters": ["treeId"],
        "resource": "Get Testcase by Criteria [/testcase/planning/{treeId}{?offset}{?pagesize}{?order}{?isascorder}{?tcname}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/{testcaseId}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase by ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["testcaseId"],
        "resource": "Get Testcase by ID [/testcase/{testcaseId}]",
    },
    {
        "endpoint_path": "/testcase/nodes",
        "full_path": "/testcase/nodes{?treeids}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcases by Tree IDs",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["treeids"],
        "path_parameters": [],
        "resource": "Get Testcases by Tree IDs [/testcase/nodes{?treeids}]",
    },
    {
        "endpoint_path": "/testcase/detail",
        "full_path": "/testcase/detail/{id}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase details by ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Get Testcase details by ID [/testcase/detail/{id}]",
    },
    {
        "endpoint_path": "/testcase/altid",
        "full_path": "/testcase/altid{?altids}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase by ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["altids"],
        "path_parameters": [],
        "resource": "Get Testcase by ID [/testcase/altid{?altids}]",
    },
    {
        "endpoint_path": "/testcase/byrequirement",
        "full_path": "/testcase/byrequirement{?requirementid}{?breadcrumb}{?releaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase Summary by Requirement ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["requirementid", "breadcrumb", "releaseid"],
        "path_parameters": [],
        "resource": "Get Testcase Summary by Requirement ID [/testcase/byrequirement{?requirementid}{?breadcrumb}{?releaseid}]",
    },
    {
        "endpoint_path": "/testcase/versions",
        "full_path": "/testcase/versions{?testcaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get all testcase version by testcase id",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["testcaseid"],
        "path_parameters": [],
        "resource": "Get all testcase version by testcase id  [/testcase/versions{?testcaseid}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase{?offset}{?pagesize}{?releaseid}{?keyword}{?zqlquery}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase by Criteria",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["offset", "pagesize", "releaseid", "keyword", "zqlquery"],
        "path_parameters": [],
        "resource": "Get Testcase by Criteria [/testcase{?offset}{?pagesize}{?releaseid}{?keyword}{?zqlquery}]",
    },
    {
        "endpoint_path": "/testcase/tree",
        "full_path": "/testcase/tree/{treeid}{?offset}{?pagesize}{?order}{?isascorder}{?dbsearch}{?frozen}{?is_cfield}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase by Tree ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "offset",
            "pagesize",
            "order",
            "isascorder",
            "dbsearch",
            "frozen",
            "is_cfield",
        ],
        "path_parameters": ["treeid"],
        "resource": "Get Testcase by Tree ID [/testcase/tree/{treeid}{?offset}{?pagesize}{?order}{?isascorder}{?dbsearch}{?frozen}{?is_cfield}]",
    },
    {
        "endpoint_path": "/testcase/mapby/altid",
        "full_path": "/testcase/mapby/altid",
        "http_method": "POST",
        "category": "testcases",
        "description": "Map Testcase to Requirement",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Map Testcase to Requirement [/testcase/mapby/altid]",
    },
    {
        "endpoint_path": "/testcase/move/from",
        "full_path": "/testcase/move/from/{sourceentryid}/to/{targetentryid}{?sourceitemids}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Move Testcases",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["sourceitemids"],
        "path_parameters": ["sourceentryid", "targetentryid"],
        "resource": "Move Testcases [/testcase/move/from/{sourceentryid}/to/{targetentryid}{?sourceitemids}]",
    },
    {
        "endpoint_path": "/testcase/share/on",
        "full_path": "/testcase/share/on/{releaseid}/to/{targettreeid}{?sourceitemids}{?showinfomessage}{?link}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Share Testcase",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["sourceitemids", "showinfomessage", "link"],
        "path_parameters": ["releaseid", "targettreeid"],
        "resource": "Share Testcase [/testcase/share/on/{releaseid}/to/{targettreeid}{?sourceitemids}{?showinfomessage}{?link}]",
    },
    {
        "endpoint_path": "/testcase/flag",
        "full_path": "/testcase/flag/{flag}{?testcaseids}{?tcrCatalogTreeId}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Update Flag status by Tree Testcase ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["testcaseids", "tcrCatalogTreeId"],
        "path_parameters": ["flag"],
        "resource": "Update Flag status by Tree Testcase ID  [/testcase/flag/{flag}{?testcaseids}{?tcrCatalogTreeId}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/{id}{?forceCreateNewVersion}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Update Testcase values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["forceCreateNewVersion"],
        "path_parameters": ["id"],
        "resource": "Update Testcase values [/testcase/{id}{?forceCreateNewVersion}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/{tctId}/replacewithversion/{testcaseVersionId}{?releaseid}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Update Testcase With Version",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["releaseid"],
        "path_parameters": ["tctId", "testcaseVersionId"],
        "resource": "Update Testcase With Version  [/testcase/{tctId}/replacewithversion/{testcaseVersionId}{?releaseid}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase{?forceCreateNewVersion}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Update Testcase values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["forceCreateNewVersion"],
        "path_parameters": [],
        "resource": "Update Testcase values [/testcase{?forceCreateNewVersion}]",
    },
    {
        "endpoint_path": "/testcasetree/copy",
        "full_path": "/testcasetree/copy/{nodeid}/{sourcereleaseid}/to/{targetparentid}/{targetreleaseid}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Copy Testcase tree node to another target node",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [
            "nodeid",
            "sourcereleaseid",
            "targetparentid",
            "targetreleaseid",
        ],
        "resource": "Copy Testcase tree node to another target node [/testcasetree/copy/{nodeid}/{sourcereleaseid}/to/{targetparentid}/{targetreleaseid}]",
    },
    {
        "endpoint_path": "/testcasetree",
        "full_path": "/testcasetree{?parentid}{?assignedusers}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Create Tree node",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["parentid", "assignedusers"],
        "path_parameters": [],
        "resource": "Create Tree node [/testcasetree{?parentid}{?assignedusers}]",
    },
    {
        "endpoint_path": "/testcasetree",
        "full_path": "/testcasetree/{id}",
        "http_method": "DELETE",
        "category": "testcases",
        "description": "Delete Testcase Tree",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Delete Testcase Tree [/testcasetree/{id}]",
    },
    {
        "endpoint_path": "/testcasetree/phases/execution",
        "full_path": "/testcasetree/phases/execution/{releaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Execution Tree by releaseid",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "Get Execution Tree by releaseid [/testcasetree/phases/execution/{releaseid}]",
    },
    {
        "endpoint_path": "/testcasetree/hierarchy",
        "full_path": "/testcasetree/hierarchy/{treeid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get TCR hierarchy",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["treeid"],
        "resource": "Get TCR hierarchy [/testcasetree/hierarchy/{treeid}]",
    },
    {
        "endpoint_path": "/testcasetree",
        "full_path": "/testcasetree/{tctId}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase Tree",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["tctId"],
        "resource": "Get Testcase Tree [/testcasetree/{tctId}]",
    },
    {
        "endpoint_path": "/testcasetree/phases",
        "full_path": "/testcasetree/phases/{releaseid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Testcase Tree by releaseid",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["releaseid"],
        "resource": "Get Testcase Tree by releaseid [/testcasetree/phases/{releaseid}]",
    },
    {
        "endpoint_path": "/testcasetree/projectrepository",
        "full_path": "/testcasetree/projectrepository/{projectid}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get Project Repository Testcase Tree by projectid",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": [],
        "path_parameters": ["projectid"],
        "resource": "Get Project Repository Testcase Tree by projectid [/testcasetree/projectrepository/{projectid}]",
    },
    {
        "endpoint_path": "/testcasetree/lite",
        "full_path": "/testcasetree/lite{?type}{?releaseid}{?revisionid}{?parentid}{?isShared}{?limit}{?offset}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get tree by criteria",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "type",
            "releaseid",
            "revisionid",
            "parentid",
            "isShared",
            "limit",
            "offset",
        ],
        "path_parameters": [],
        "resource": "Get tree by criteria [/testcasetree/lite{?type}{?releaseid}{?revisionid}{?parentid}{?isShared}{?limit}{?offset}]",
    },
    {
        "endpoint_path": "/testcasetree/move",
        "full_path": "/testcasetree/move/{nodeid}/to/{targetid}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Move Testcase tree",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["nodeid", "targetid"],
        "resource": "Move Testcase tree  [/testcasetree/move/{nodeid}/to/{targetid}]",
    },
    {
        "endpoint_path": "/testcasetree/move",
        "full_path": "/testcasetree/move/{nodeid}/{sourcereleaseid}/to/{targetid}/{targetreleaseid}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Move Testcase tree to other Release",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["nodeid", "sourcereleaseid", "targetid", "targetreleaseid"],
        "resource": "Move Testcase tree to other Release [/testcasetree/move/{nodeid}/{sourcereleaseid}/to/{targetid}/{targetreleaseid}]",
    },
    {
        "endpoint_path": "/testcasetree/share",
        "full_path": "/testcasetree/share/{nodeid}/{sourcereleaseid}/to/{targetparentid}/{targetreleaseid}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Share Testcase tree node to another target node",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [
            "nodeid",
            "sourcereleaseid",
            "targetparentid",
            "targetreleaseid",
        ],
        "resource": "Share Testcase tree node to another target node [/testcasetree/share/{nodeid}/{sourcereleaseid}/to/{targetparentid}/{targetreleaseid}]",
    },
    {
        "endpoint_path": "/testcasetree/assignuser",
        "full_path": "/testcasetree/assignuser/{id}{?name}{?description}{?assignedusers}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Update tree node values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["name", "description", "assignedusers"],
        "path_parameters": ["id"],
        "resource": "Update tree node values [/testcasetree/assignuser/{id}{?name}{?description}{?assignedusers}]",
    },
    {
        "endpoint_path": "/testcasetree",
        "full_path": "/testcasetree/{treeId}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Update tree node values",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["treeId"],
        "resource": "Update tree node values [/testcasetree/{treeId}]",
    },
    {
        "endpoint_path": "/tcuh/testcase",
        "full_path": "/tcuh/testcase/{id}{?isascorder}{?order}{?offset}{?pagesize}",
        "http_method": "GET",
        "category": "other",
        "description": "Get Testcase usage history details",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["isascorder", "order", "offset", "pagesize"],
        "path_parameters": ["id"],
        "resource": "Get Testcase usage history details [/tcuh/testcase/{id}{?isascorder}{?order}{?offset}{?pagesize}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/{testcaseVersionId}/teststep/detail/{tctId}",
        "http_method": "POST",
        "category": "testcases",
        "description": "Create teststep",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["testcaseVersionId", "tctId"],
        "resource": "Create teststep [/testcase/{testcaseVersionId}/teststep/detail/{tctId}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/{testcaseVersionId}/teststep/{tctId}",
        "http_method": "DELETE",
        "category": "testcases",
        "description": "Delete teststep",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["testcaseVersionId", "tctId"],
        "resource": "Delete teststep [/testcase/{testcaseVersionId}/teststep/{tctId}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/{testcaseVersionId}/teststep{?isfetchstepversion}{?versionId}",
        "http_method": "GET",
        "category": "testcases",
        "description": "Get teststep",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["isfetchstepversion", "versionId"],
        "path_parameters": ["testcaseVersionId"],
        "resource": "Get teststep [/testcase/{testcaseVersionId}/teststep{?isfetchstepversion}{?versionId}]",
    },
    {
        "endpoint_path": "/testcase",
        "full_path": "/testcase/{testcaseVersionId}/teststep/detail/{testcaseTreeId}",
        "http_method": "PUT",
        "category": "testcases",
        "description": "Update teststep",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["testcaseVersionId", "testcaseTreeId"],
        "resource": "Update teststep [/testcase/{testcaseVersionId}/teststep/detail/{testcaseTreeId}]",
    },
    {
        "endpoint_path": "/ui/auditLogs",
        "full_path": "/ui/auditLogs{?offset}{?pagesize}{?order}{?isascorder}",
        "http_method": "POST",
        "category": "other",
        "description": "Get audit logs Grid view",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["offset", "pagesize", "order", "isascorder"],
        "path_parameters": [],
        "resource": "Get audit logs Grid view [/ui/auditLogs{?offset}{?pagesize}{?order}{?isascorder}]",
    },
    {
        "endpoint_path": "/ui/users",
        "full_path": "/ui/users{?offset}{?pagesize}{?hidedisabledusers}{?order}{?isascorder}{?isLoggedIn}",
        "http_method": "GET",
        "category": "other",
        "description": "Get user Grid view",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "offset",
            "pagesize",
            "hidedisabledusers",
            "order",
            "isascorder",
            "isLoggedIn",
        ],
        "path_parameters": [],
        "resource": "Get user Grid view [/ui/users{?offset}{?pagesize}{?hidedisabledusers}{?order}{?isascorder}{?isLoggedIn}]",
    },
    {
        "endpoint_path": "/ui/searchGroups",
        "full_path": "/ui/searchGroups{?text}{?offset}{?pagesize}{?order}{?isascorder}{?hidedisabledgroups}",
        "http_method": "GET",
        "category": "other",
        "description": "Get group Grid view",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "text",
            "offset",
            "pagesize",
            "order",
            "isascorder",
            "hidedisabledgroups",
        ],
        "path_parameters": [],
        "resource": "Get group Grid view [/ui/searchGroups{?text}{?offset}{?pagesize}{?order}{?isascorder}{?hidedisabledgroups}]",
    },
    {
        "endpoint_path": "/ui/searchProjects",
        "full_path": "/ui/searchProjects{?text}{?offset}{?pagesize}{?order}{?isascorder}{?includeglobalproject}{?isProjectAdmin}",
        "http_method": "GET",
        "category": "other",
        "description": "Get project Grid view",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [
            "text",
            "offset",
            "pagesize",
            "order",
            "isascorder",
            "includeglobalproject",
            "isProjectAdmin",
        ],
        "path_parameters": [],
        "resource": "Get project Grid view [/ui/searchProjects{?text}{?offset}{?pagesize}{?order}{?isascorder}{?includeglobalproject}{?isProjectAdmin}]",
    },
    {
        "endpoint_path": "/user",
        "full_path": "/user/",
        "http_method": "POST",
        "category": "users",
        "description": "Create User in the System",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Create User in the System [/user/]",
    },
    {
        "endpoint_path": "/user/current",
        "full_path": "/user/current{?auditLog}",
        "http_method": "GET",
        "category": "users",
        "description": "Get Current Logged-In Users",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["auditLog"],
        "path_parameters": [],
        "resource": "Get Current Logged-In Users [/user/current{?auditLog}]",
    },
    {
        "endpoint_path": "/user/defect",
        "full_path": "/user/defect",
        "http_method": "GET",
        "category": "users",
        "description": "Get Defect Users present in System.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get Defect Users present in System. [/user/defect]",
    },
    {
        "endpoint_path": "/user/filter",
        "full_path": "/user/filter{?includeDashboardUser}",
        "http_method": "GET",
        "category": "users",
        "description": "Get All Users Present in the System.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["includeDashboardUser"],
        "path_parameters": [],
        "resource": "Get All Users Present in the System. [/user/filter{?includeDashboardUser}]",
    },
    {
        "endpoint_path": "/user/loggedin/count",
        "full_path": "/user/loggedin/count{?skipdefectuser}",
        "http_method": "GET",
        "category": "users",
        "description": "Getting all the Logged-In in User count",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["skipdefectuser"],
        "path_parameters": [],
        "resource": "Getting all the Logged-In in User count [/user/loggedin/count{?skipdefectuser}]",
    },
    {
        "endpoint_path": "/user",
        "full_path": "/user/{id}{?isLite}",
        "http_method": "GET",
        "category": "users",
        "description": "Get User by ID",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["isLite"],
        "path_parameters": ["id"],
        "resource": "Get User by ID [/user/{id}{?isLite}]",
    },
    {
        "endpoint_path": "/user",
        "full_path": "/user{?hidedisabledusers}",
        "http_method": "GET",
        "category": "users",
        "description": "Get All Users Present in the System.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["hidedisabledusers"],
        "path_parameters": [],
        "resource": "Get All Users Present in the System. [/user{?hidedisabledusers}]",
    },
    {
        "endpoint_path": "/user/project",
        "full_path": "/user/project/{projectid}{?isLite}{?adminUser}",
        "http_method": "GET",
        "category": "users",
        "description": "Get User by Project ID",
        "requires_auth": True,
        "hierarchical": True,
        "query_parameters": ["isLite", "adminUser"],
        "path_parameters": ["projectid"],
        "resource": "Get User by Project ID [/user/project/{projectid}{?isLite}{?adminUser}]",
    },
    {
        "endpoint_path": "/user/validZbotUsers",
        "full_path": "/user/validZbotUsers{?projectId}",
        "http_method": "GET",
        "category": "users",
        "description": "Get valid users for Zbot.",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": ["projectId"],
        "path_parameters": [],
        "resource": "Get valid users for Zbot. [/user/validZbotUsers{?projectId}]",
    },
    {
        "endpoint_path": "/user/logout",
        "full_path": "/user/logout",
        "http_method": "DELETE",
        "category": "users",
        "description": "Logout User from System",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Logout User from System [/user/logout]",
    },
    {
        "endpoint_path": "/user",
        "full_path": "/user/{id}",
        "http_method": "PUT",
        "category": "users",
        "description": "Update User",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "Update User [/user/{id}]",
    },
    {
        "endpoint_path": "/usertoken/all",
        "full_path": "/usertoken/all",
        "http_method": "DELETE",
        "category": "users",
        "description": "delete all token",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "delete all token  [/usertoken/all]",
    },
    {
        "endpoint_path": "/usertoken",
        "full_path": "/usertoken/{id}",
        "http_method": "DELETE",
        "category": "users",
        "description": "delete token",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": ["id"],
        "resource": "delete token  [/usertoken/{id}]",
    },
    {
        "endpoint_path": "/usertoken",
        "full_path": "/usertoken/",
        "http_method": "POST",
        "category": "users",
        "description": "generate token",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "generate token  [/usertoken/]",
    },
    {
        "endpoint_path": "/usertoken",
        "full_path": "/usertoken",
        "http_method": "GET",
        "category": "users",
        "description": "Get all token",
        "requires_auth": True,
        "hierarchical": False,
        "query_parameters": [],
        "path_parameters": [],
        "resource": "Get all token  [/usertoken]",
    },
]


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ══════════════════════════════════════════════════════════════════════════════
# Error Handling Components (SPECTRA-Grade)
# ══════════════════════════════════════════════════════════════════════════════

import json
import random
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

import requests
from pyspark.sql import Row, SparkSession
from pyspark.sql.types import (
    BooleanType,
    DateType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

# Import error classes (assumes spectra_core package is available in Fabric environment)
try:
    from spectra_core.errors import (
        AuthenticationError,
        AuthorizationError,
        ConfigurationError,
        ExternalServiceError,
        NotFoundError,
        ValidationError,
    )
except ImportError:
    # Fallback for local testing or if package not available
    class ValidationError(Exception):
        def __init__(self, message: str, **kwargs):
            self.message = message  # Store message as attribute
            self.category = kwargs.get("category", "validation")
            self.context = kwargs.get("context", {})
            self.retryable = False
            self.stage = kwargs.get("stage")
            self.source_system = kwargs.get("source_system")
            super().__init__(message)
    
    class AuthenticationError(Exception):
        def __init__(self, message: str = "Authentication failed", **kwargs):
            self.message = message  # Store message as attribute
            self.category = kwargs.get("category", "auth")
            self.context = kwargs.get("context", {})
            self.retryable = False
            self.stage = kwargs.get("stage")
            self.source_system = kwargs.get("source_system")
            super().__init__(message)
    
    class AuthorizationError(Exception):
        def __init__(self, message: str = "Insufficient permissions", **kwargs):
            self.message = message  # Store message as attribute
            self.category = kwargs.get("category", "auth")
            self.context = kwargs.get("context", {})
            self.retryable = False
            self.stage = kwargs.get("stage")
            self.source_system = kwargs.get("source_system")
            super().__init__(message)
    
    class NotFoundError(Exception):
        def __init__(self, resource: str, identifier: str, **kwargs):
            message = f"{resource} not found: {identifier}"
            self.message = message  # Store message as attribute
            self.resource = resource
            self.identifier = identifier
            self.category = kwargs.get("category", "api")
            self.context = kwargs.get("context", {})
            self.context.update({"resource": resource, "identifier": identifier})
            self.retryable = kwargs.get("retryable", False)
            self.stage = kwargs.get("stage")
            self.source_system = kwargs.get("source_system")
            super().__init__(message)
    
    class ConfigurationError(Exception):
        def __init__(self, message: str, **kwargs):
            self.message = message  # Store message as attribute
            self.category = kwargs.get("category", "config")
            self.context = kwargs.get("context", {})
            self.retryable = False
            self.stage = kwargs.get("stage")
            self.source_system = kwargs.get("source_system")
            super().__init__(message)
    
    class ExternalServiceError(Exception):
        def __init__(self, service: str, message: str, **kwargs):
            self.service = service
            self.message = message  # Store message as attribute
            self.category = kwargs.get("category", "api")
            self.context = kwargs.get("context", {})
            self.context.update({"service": service})
            self.retryable = kwargs.get("retryable", True)
            self.stage = kwargs.get("stage")
            self.source_system = kwargs.get("source_system")
            super().__init__(f"{service}: {message}")


class ErrorClassification:
    """Classify errors and return appropriate specific error class instances.
    
    Returns specific error classes (ValidationError, AuthenticationError, etc.)
    based on error type, HTTP status code, or exception type.
    """
    
    RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
    NON_RETRYABLE_STATUS_CODES = {400, 401, 403, 404}
    
    @staticmethod
    def classify_http_error(status_code: int, error: Exception, **kwargs):
        """Classify HTTP error, return appropriate specific error class."""
        context = kwargs.get("context", {})
        context["status_code"] = status_code
        
        # Return specific class based on status code
        if status_code == 401:
            return AuthenticationError(
                message=str(error),
                category="auth",
                context=context,
                **{k: v for k, v in kwargs.items() if k != "context"}
            )
        elif status_code == 403:
            return AuthorizationError(
                message=str(error),
                category="auth",
                context=context,
                **{k: v for k, v in kwargs.items() if k != "context"}
            )
        elif status_code == 404:
            return NotFoundError(
                resource=kwargs.get("resource", "Resource"),
                identifier=kwargs.get("identifier", "unknown"),
                category="api",
                context=context,
                **{k: v for k, v in kwargs.items() if k not in ("context", "resource", "identifier")}
            )
        else:
            # 429, 500, 502, 503, 504 → ExternalServiceError
            retryable = status_code in ErrorClassification.RETRYABLE_STATUS_CODES
            return ExternalServiceError(
                service=kwargs.get("service", "API"),
                message=str(error),
                category="api",
                context=context,
                retryable=retryable,
                **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
            )
    
    @staticmethod
    def classify_exception(error: Exception, **kwargs):
        """Classify any exception, return appropriate specific error class."""
        if isinstance(error, requests.exceptions.Timeout):
            return ExternalServiceError(
                service=kwargs.get("service", "API"),
                message=str(error),
                category="network",
                context=kwargs.get("context", {}),
                retryable=True,
                **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
            )
        elif isinstance(error, requests.exceptions.ConnectionError):
            return ExternalServiceError(
                service=kwargs.get("service", "API"),
                message=str(error),
                category="network",
                context=kwargs.get("context", {}),
                retryable=True,
                **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
            )
        elif isinstance(error, requests.exceptions.HTTPError):
            status_code = error.response.status_code if error.response else 0
            return ErrorClassification.classify_http_error(status_code, error, **kwargs)
        else:
            # Unknown exception - wrap in ValidationError (generic failure)
            return ValidationError(
                message=f"Unknown error: {str(error)}",
                category="unknown",
                context={**kwargs.get("context", {}), "exception_type": type(error).__name__},
                **{k: v for k, v in kwargs.items() if k != "context"}
            )


class APIRequestHandler:
    """Handle API requests with retry logic, exponential backoff, and error classification.
    
    Wraps API calls with retry logic, classifies errors into specific error classes,
    and handles transient failures gracefully.
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        logger: Optional[Any] = None,
    ):
        """Initialize API request handler.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds for exponential backoff
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff (2.0 = doubles each retry)
            jitter: Add random jitter to delay (prevents thundering herd)
            logger: Optional logger instance
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.logger = logger
    
    def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Tuple[Any, Optional[Exception]]:
        """Execute function with retry logic, return result and optional error (specific class).
        
        Args:
            func: Function to execute (e.g., requests.get, requests.post)
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func and error context
        
        Returns:
            Tuple of (result, error) where error is None on success,
            or a specific error class instance on failure.
        
        Error context kwargs:
            service: Service name for ExternalServiceError
            stage: Pipeline stage for error tracking
            source_system: Source system identifier
            resource: Resource name for NotFoundError
            identifier: Resource identifier for NotFoundError
        """
        last_error = None
        
        # Extract error context kwargs (these are NOT passed to func)
        error_context_kwargs = {
            "context": kwargs.pop("context", {}),
            "service": kwargs.pop("service", "API"),
            "stage": kwargs.pop("stage", None),
            "source_system": kwargs.pop("source_system", None),
            "resource": kwargs.pop("resource", None),
            "identifier": kwargs.pop("identifier", None),
        }
        
        context = error_context_kwargs["context"]
        service = error_context_kwargs["service"]
        stage = error_context_kwargs["stage"]
        source_system = error_context_kwargs["source_system"]
        
        for attempt in range(self.max_retries + 1):
            try:
                # Only pass valid function kwargs (error context already filtered out)
                result = func(*args, **kwargs)
                # Check for HTTP errors if result has status_code
                if hasattr(result, "status_code"):
                    result.raise_for_status()
                return result, None
            
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response else 0
                error = ErrorClassification.classify_http_error(
                    status_code,
                    e,
                    service=service,
                    context={**context, "attempt": attempt + 1, "max_retries": self.max_retries},
                    stage=stage,
                    source_system=source_system,
                    resource=error_context_kwargs.get("resource"),
                    identifier=error_context_kwargs.get("identifier"),
                )
                last_error = error
                
                # Don't retry non-retryable errors
                if not error.retryable or attempt >= self.max_retries:
                    if self.logger:
                        self.logger.warning(f"⚠️ API request failed (non-retryable or max retries): {error}")
                    return None, error
                
                # Retry with backoff
                delay = min(
                    self.base_delay * (self.exponential_base ** attempt),
                    self.max_delay
                )
                if self.jitter:
                    delay = delay * (0.5 + random.random() * 0.5)  # 50-100% of delay
                
                if self.logger:
                    self.logger.debug(f"🔄 Retrying after {delay:.2f}s (attempt {attempt + 1}/{self.max_retries})")
                time.sleep(delay)
            
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                error = ErrorClassification.classify_exception(
                    e,
                    service=service,
                    context={**context, "attempt": attempt + 1, "max_retries": self.max_retries},
                    stage=stage,
                    source_system=source_system,
                    resource=error_context_kwargs.get("resource"),
                    identifier=error_context_kwargs.get("identifier"),
                )
                last_error = error
                
                # Network errors are retryable
                if attempt >= self.max_retries:
                    if self.logger:
                        self.logger.warning(f"⚠️ API request failed (max retries): {error}")
                    return None, error
                
                # Retry with backoff
                delay = min(
                    self.base_delay * (self.exponential_base ** attempt),
                    self.max_delay
                )
                if self.jitter:
                    delay = delay * (0.5 + random.random() * 0.5)
                
                if self.logger:
                    self.logger.debug(f"🔄 Retrying after {delay:.2f}s (attempt {attempt + 1}/{self.max_retries})")
                time.sleep(delay)
            
            except Exception as e:
                # Unknown exception - wrap in ValidationError
                error = ValidationError(
                    message=f"Unknown error: {str(e)}",
                    category="unknown",
                    context={**context, "attempt": attempt + 1, "max_retries": self.max_retries, "exception_type": type(e).__name__},
                    stage=stage,
                    source_system=source_system,
                )
                last_error = error
                if self.logger:
                    self.logger.warning(f"⚠️ API request failed (unknown error): {error}")
                return None, error
        
        return None, last_error


class ErrorCollector:
    """Collect errors without failing stage - enables graceful degradation.
    
    Collects errors during pipeline execution, allowing the stage to continue
    even when some operations fail. Provides summary and categorization.
    """
    
    def __init__(self):
        """Initialize error collector."""
        # Collect any SpectraError subclass (polymorphic)
        self.errors: List[Exception] = []
        self.critical_errors: List[Exception] = []
    
    def add(self, error: Exception, critical: bool = False):
        """Add error to collector (accepts any SpectraError subclass).
        
        Args:
            error: Error instance (ValidationError, AuthenticationError, etc.)
            critical: If True, add to critical_errors (fails stage)
        """
        if critical:
            self.critical_errors.append(error)
        else:
            self.errors.append(error)
    
    def has_errors(self) -> bool:
        """Check if any errors collected."""
        return len(self.errors) > 0 or len(self.critical_errors) > 0
    
    def has_critical_errors(self) -> bool:
        """Check if any critical errors collected."""
        return len(self.critical_errors) > 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get error summary for logging.
        
        Returns:
            Dictionary with error counts, categories, codes, and types.
        """
        from collections import Counter
        
        # Handle both SpectraError subclasses (with structured fields) and generic exceptions
        all_errors = self.errors + self.critical_errors
        categories = Counter(
            getattr(e, "category", "unknown") for e in all_errors
        )
        codes = Counter(
            getattr(e, "code", type(e).__name__) for e in all_errors
        )
        error_types = Counter(type(e).__name__ for e in all_errors)
        
        return {
            "total_errors": len(self.errors),
            "critical_errors": len(self.critical_errors),
            "errors_by_category": dict(categories),
            "errors_by_code": dict(codes),
            "errors_by_type": dict(error_types),
            "has_retryable_errors": any(
                getattr(e, "retryable", False) for e in all_errors
            ),
        }
    
    def get_all_errors(self) -> List[Exception]:
        """Get all errors (non-critical and critical)."""
        return self.errors + self.critical_errors


# ══════════════════════════════════════════════════════════════════════════════
# Data Quality Helpers (Quarantining)
# ══════════════════════════════════════════════════════════════════════════════


class DataQualityHelpers:
    """SPECTRA-grade data quality and quarantine helpers.
    
    Metadata-driven validation and quarantining following SPECTRA standards.
    """
    
    @staticmethod
    def validate_and_quarantine(
        spark: SparkSession,
        delta: "DeltaTable",
        df: Any,  # DataFrame
        entity_name: str,
        stage: str,
        validation_rules: List[Dict[str, Any]],
        logger: Optional["SPECTRALogger"] = None,
        quarantine_enabled: bool = True,
        source_system: Optional[str] = None,
    ) -> Tuple[Any, Any, List[Any], Dict[str, Any]]:  # Returns (DataFrame, DataFrame, List[SpectraError], Dict)
        """Validate DataFrame against rules, quarantine invalid records.
        
        SPECTRA-Grade Pattern:
        - Metadata-driven validation (rules are data, not code)
        - Preserves all records (never drops)
        - Returns structured errors (SpectraError instances)
        - Integrates with error handling system
        
        Args:
            spark: Spark session
            delta: DeltaTable helper
            df: Input DataFrame to validate
            entity_name: Entity name (e.g., "projects", "releases")
            stage: Pipeline stage (e.g., "source", "clean")
            validation_rules: List of validation rule dicts with keys:
                - name: Rule name
                - condition: PySpark column expression or lambda
                - message: Error message
                - severity: "error" or "warning"
            logger: Logger instance
            quarantine_enabled: Whether to write quarantine table (default: True)
            source_system: Source system identifier (e.g., "zephyr")
            
        Returns:
            Tuple of:
            - df_valid: Valid records (pass all error rules)
            - df_invalid: Invalid records (fail at least one error rule)
            - errors: List of SpectraError instances for quarantined records
            - summary: Validation summary dict
        """
        from pyspark.sql import functions as F
        
        # Handle empty DataFrame
        if df.count() == 0:
            return df, spark.createDataFrame([], df.schema), [], {
                "entity": entity_name,
                "stage": stage,
                "total_records": 0,
                "valid_records": 0,
                "quarantined_records": 0,
                "quarantine_rate": 0.0,
                "errors": 0,
                "warnings": 0,
            }
        
        # Build error condition expression
        error_condition = F.lit(False)
        warning_condition = F.lit(False)
        error_reason = F.lit(None).cast("string")
        warning_reason = F.lit(None).cast("string")
        
        error_rules = [r for r in validation_rules if r.get("severity") == "error"]
        warning_rules = [r for r in validation_rules if r.get("severity") == "warning"]
        
        # Build error conditions
        for rule in error_rules:
            condition = rule["condition"](df) if callable(rule["condition"]) else rule["condition"]
            error_condition = error_condition | condition
            error_reason = F.when(
                condition & error_reason.isNull(),
                F.lit(rule["message"])
            ).otherwise(error_reason)
        
        # Build warning conditions (warnings also quarantined but less critical)
        for rule in warning_rules:
            condition = rule["condition"](df) if callable(rule["condition"]) else rule["condition"]
            warning_condition = warning_condition | condition
            warning_reason = F.when(
                condition & warning_reason.isNull(),
                F.lit(rule["message"])
            ).otherwise(warning_reason)
        
        # Combine error and warning conditions (both result in quarantine)
        quarantine_condition = error_condition | warning_condition
        quarantine_reason = F.coalesce(error_reason, warning_reason)
        
        # Add reason columns
        df_with_reasons = df.withColumn("errorReason", error_reason) \
                           .withColumn("warningReason", warning_reason) \
                           .withColumn("quarantineReason", quarantine_reason) \
                           .withColumn("quarantineAt", F.current_timestamp())
        
        # Split valid/invalid
        df_invalid = df_with_reasons.filter(quarantine_condition)
        df_valid = df_with_reasons.filter(~quarantine_condition)
        
        # Remove DQ tracking columns from valid DataFrame (keep clean)
        dq_columns = ["errorReason", "warningReason", "quarantineReason", "quarantineAt"]
        df_valid = df_valid.drop(*[col for col in dq_columns if col in df_valid.columns])
        
        # Create SpectraError instances for quarantined records
        errors = []
        invalid_count = df_invalid.count()
        
        if invalid_count > 0:
            # Group by error reason for summary
            error_summary = df_invalid.groupBy("quarantineReason").count().collect()
            
            for row in error_summary:
                reason = row["quarantineReason"]
                count = row["count"]
                
                error = ValidationError(
                    message=f"{count} {entity_name} records failed validation: {reason}",
                    category="data",
                    context={
                        "entity": entity_name,
                        "stage": stage,
                        "reason": reason,
                        "count": count,
                        "quarantine_table": f"quarantine.{stage}{entity_name.capitalize()}"
                    },
                    retryable=False,
                    stage=stage,
                    source_system=source_system
                )
                errors.append(error)
            
            # Quarantine invalid records
            if quarantine_enabled:
                DataQualityHelpers._write_quarantine_table(
                    spark=spark,
                    delta=delta,
                    df_invalid=df_invalid,
                    entity_name=entity_name,
                    stage=stage,
                    logger=logger
                )
        
        # Validation summary
        valid_count = df_valid.count()
        total_count = valid_count + invalid_count
        summary = {
            "entity": entity_name,
            "stage": stage,
            "total_records": total_count,
            "valid_records": valid_count,
            "quarantined_records": invalid_count,
            "quarantine_rate": invalid_count / total_count if total_count > 0 else 0.0,
            "errors": len([e for e in errors if "error" in str(getattr(e, "context", {})).get("reason", "").lower()]),
            "warnings": len([e for e in errors if "warning" in str(getattr(e, "context", {})).get("reason", "").lower()]),
        }
        
        if logger:
            if invalid_count > 0:
                logger.warning(f"⚠️ Validation: {valid_count} valid, {invalid_count} quarantined {entity_name} records")
            else:
                logger.info(f"✅ Validation: {valid_count} valid {entity_name} records (0 quarantined)")
        
        return df_valid, df_invalid, errors, summary
    
    @staticmethod
    def _write_quarantine_table(
        spark: SparkSession,
        delta: "DeltaTable",
        df_invalid: Any,  # DataFrame
        entity_name: str,
        stage: str,
        logger: Optional["SPECTRALogger"] = None,
    ) -> str:
        """Write invalid records to quarantine table following SPECTRA standard.
        
        SPECTRA Standard:
        - Path: Tables/quarantine/{stage}/{entityName}
        - Table: quarantine.{stage}{EntityName} (camelCase)
        - Mode: append (preserve history)
        - Schema: mergeSchema=true (handle evolution)
        
        Args:
            spark: Spark session
            delta: DeltaTable helper
            df_invalid: Invalid records DataFrame
            entity_name: Entity name (e.g., "projects")
            stage: Pipeline stage (e.g., "source")
            logger: Logger instance
            
        Returns:
            Quarantine table name
        """
        quarantine_path = f"Tables/quarantine/{stage}/{entity_name}"
        table_name = f"quarantine.{stage}{entity_name.capitalize()}"  # camelCase
        
        delta.write(
            df_invalid,
            table_name,
            quarantine_path,
            mode="append",
            merge_schema=True
        )
        delta.register(table_name, quarantine_path)
        
        if logger:
            logger.warning(f"⚠️ Quarantined {df_invalid.count()} {entity_name} records to {table_name}")
        
        return table_name


# ══════════════════════════════════════════════════════════════════════════════
# Source Stage Helper Functions (Standardized, Shareable)
# ══════════════════════════════════════════════════════════════════════════════


class SourceStageHelpers:
    """Standardized helper functions for Source stage operations.

    All functions are static and reusable across different source systems.
    Naming convention: verb_noun (e.g., create_portfolio_table, validate_api_auth)
    """

    @staticmethod
    def create_source_portfolio_table(
        spark: SparkSession,
        delta: "DeltaTable",
        logger: "SPECTRALogger",
        session: "NotebookSession",
        contract_version: str,
        auth_method: str,
        auth_status: str,
        endpoint_catalog: Optional[List[Dict]] = None,
        endpoint_success_rate: float = 0.0,
        supports_incremental: bool = False,
    ) -> None:
        """Create source.portfolio table with comprehensive metadata for dashboard.

        Args:
            spark: Spark session
            delta: DeltaTable instance for writing
            logger: Logger instance
            session: NotebookSession with capabilities and context
            contract_version: Contract version from contract.yaml
            auth_method: Auth method type (apiToken|oauth2|basic|pat)
            auth_status: Last auth status (valid|invalid|unknown)
            endpoint_catalog: List of endpoint dictionaries (optional)
            endpoint_success_rate: Success rate (0.0-1.0)
            supports_incremental: Does API support incremental extraction?
        """
        logger.info("📊 Creating portfolio table...")

        # Aggregate endpoint metrics if catalog provided
        total_endpoints = 0
        hierarchical_endpoints = 0
        endpoint_categories = {}

        if endpoint_catalog:
            total_endpoints = len(endpoint_catalog)
            hierarchical_endpoints = sum(
                1 for ep in endpoint_catalog if ep.get("hierarchical", False)
            )
            # Count by category
            category_counts = {}
            for ep in endpoint_catalog:
                category = ep.get("category", "other")
                category_counts[category] = category_counts.get(category, 0) + 1
            endpoint_categories = json.dumps(category_counts)

        # Get discovery date (first run or existing record)
        discovery_date = datetime.utcnow().date()
        try:
            source_system = session.ctx["source_system"]
            existing = spark.sql(
                f"SELECT discovery_date FROM source.portfolio WHERE source_system = '{source_system}'"
            ).first()
            if existing:
                discovery_date = existing["discovery_date"]
        except:
            pass  # Table doesn't exist yet

        # Get capabilities from session
        capability_meta = session.result.get("projectAccessVerified", {})
        hierarchical_access_validated = (
            capability_meta.get("status") == "Success" if capability_meta else False
        )
        # Set auth check time if auth was successful (case-insensitive)
        auth_check_time = (
            datetime.utcnow()
            if auth_status and auth_status.lower() in ("success", "valid")
            else None
        )

        # Define schema explicitly to handle nullable datetime
        schema = StructType(
            [
                StructField("source_system", StringType(), False),
                StructField("contract_version", StringType(), False),
                StructField("discovery_date", DateType(), False),
                StructField("total_endpoints", IntegerType(), False),
                StructField("endpoint_categories", StringType(), False),
                StructField("hierarchical_endpoints", IntegerType(), False),
                StructField("auth_method", StringType(), False),
                StructField("auth_status", StringType(), False),
                StructField("last_auth_check", TimestampType(), True),  # Nullable
                StructField("hierarchical_access_validated", BooleanType(), False),
                StructField("endpoint_success_rate", DoubleType(), False),
                StructField("supports_incremental", BooleanType(), False),
                StructField("status", StringType(), False),
                StructField("is_enabled", BooleanType(), False),
                StructField("last_updated", TimestampType(), False),
            ]
        )

        # Build portfolio record
        df_portfolio = spark.createDataFrame(
            [
                Row(
                    source_system=session.ctx["source_system"],
                    contract_version=contract_version,
                    discovery_date=discovery_date,
                    total_endpoints=total_endpoints,
                    endpoint_categories=endpoint_categories or "{}",
                    hierarchical_endpoints=hierarchical_endpoints,
                    auth_method=auth_method,
                    auth_status=auth_status,
                    last_auth_check=auth_check_time,
                    hierarchical_access_validated=hierarchical_access_validated,
                    endpoint_success_rate=float(endpoint_success_rate),
                    supports_incremental=supports_incremental,
                    status="active",
                    is_enabled=True,
                    last_updated=datetime.utcnow(),
                )
            ],
            schema=schema,
        )

        delta.write(
            df_portfolio,
            "source.portfolio",
            "Tables/source/portfolio",
            mode="overwrite",
        )
        delta.register("source.portfolio", "Tables/source/portfolio")
        logger.info("✅ Portfolio table created")

    @staticmethod
    def create_source_config_table(
        spark: SparkSession,
        delta: "DeltaTable",
        logger: "SPECTRALogger",
        session: "NotebookSession",
        sdk_version: str = "0.3.0",
    ) -> None:
        """Create source.config table with runtime execution context."""
        logger.info("⚙️ Creating config table...")

        df_config = spark.createDataFrame(
            [
                Row(
                    config_key="execution_mode",
                    config_value="pipeline"
                    if session.pipeline.is_active
                    else "interactive",
                    last_updated=datetime.utcnow(),
                ),
                Row(
                    config_key="operation_type",
                    config_value=session.pipeline.operation_type,
                    last_updated=datetime.utcnow(),
                ),
                Row(
                    config_key="notebook_name",
                    config_value=session.ctx["notebook_name"],
                    last_updated=datetime.utcnow(),
                ),
                Row(
                    config_key="stage",
                    config_value=session.ctx["stage"],
                    last_updated=datetime.utcnow(),
                ),
                Row(
                    config_key="sdk_version",
                    config_value=sdk_version,
                    last_updated=datetime.utcnow(),
                ),
                Row(
                    config_key="bootstrap_enabled",
                    config_value=str(session.params.get("bootstrap", False)),
                    last_updated=datetime.utcnow(),
                ),
            ]
        )

        delta.write(
            df_config, "source.config", "Tables/source/config", mode="overwrite"
        )
        delta.register("source.config", "Tables/source/config")
        logger.info("✅ Config table created")

    @staticmethod
    def create_source_credentials_table(
        spark: SparkSession,
        delta: "DeltaTable",
        logger: "SPECTRALogger",
        api_token: str,
        validation_status: str = "Success",
    ) -> None:
        """Create source.credentials table with masked token."""
        logger.info("🔐 Creating credentials table...")

        masked_token = f"***{api_token[-3:]}" if len(api_token) >= 3 else "***"
        df_credentials = spark.createDataFrame(
            [
                Row(
                    credential_type="api_token",
                    credential_value=masked_token,
                    last_validated=datetime.utcnow(),
                    validation_status=validation_status,
                )
            ]
        )

        delta.write(
            df_credentials,
            "source.credentials",
            "Tables/source/credentials",
            mode="overwrite",
        )
        delta.register("source.credentials", "Tables/source/credentials")
        logger.info("✅ Credentials table created")

    @staticmethod
    def validate_api_authentication(
        base_url: str,
        api_token: str,
        test_endpoint: str,
        logger: "SPECTRALogger",
        timeout: int = 10,
        auth_header: str = "Authorization",
        auth_prefix: str = "Bearer",
        service: str = "API",
        stage: Optional[str] = None,
        source_system: Optional[str] = None,
    ) -> Tuple[Dict, Optional[List]]:
        """Generic API authentication validation with retry logic and error handling.

        Returns:
            Tuple of (result_dict, response_data)
        """
        logger.info("🔍 Validating authentication...")
        
        # Use APIRequestHandler for retry logic
        handler = APIRequestHandler(
            max_retries=3,
            base_delay=1.0,
            max_delay=30.0,
            logger=logger,
        )
        
        url = f"{base_url}{test_endpoint}"
        headers = {auth_header: f"{auth_prefix} {api_token}"}
        
        response, error = handler.execute_with_retry(
            requests.get,
            url,
            headers=headers,
            timeout=timeout,
            service=service,
            stage=stage or "source",
            source_system=source_system,
            context={"endpoint": test_endpoint, "operation": "authentication_validation"},
        )
        
        if error:
            # Authentication errors are critical - fail immediately
            error_message = getattr(error, "message", str(error))
            if isinstance(error, AuthenticationError):
                logger.error(f"❌ Authentication failed: {error_message}")
            else:
                logger.error(f"❌ Authentication validation failed: {error_message}")
            return {"status": "Failed", "error": error_message, "error_type": type(error).__name__}, None
        
        # Parse response
        try:
            data = response.json()
        except Exception as e:
            logger.error(f"❌ Failed to parse authentication response: {str(e)}")
            return {"status": "Failed", "error": f"Invalid response format: {str(e)}"}, None

        # Try to infer count from response
        if isinstance(data, list):
            count = len(data)
        elif isinstance(data, dict):
            for key in ["projects", "items", "results", "data", "values"]:
                if key in data and isinstance(data[key], list):
                    count = len(data[key])
                    logger.info(f"✅ Authentication successful ({count} items)")
                    return {"status": "Success", "count": count}, data
            count = 1
        else:
            count = 1

        logger.info(f"✅ Authentication successful ({count} items)")
        return {"status": "Success", "count": count}, data

    @staticmethod
    def validate_api_resource_access(
        base_url: str,
        api_token: str,
        resource_endpoint: str,
        resource_id: Optional[str] = None,
        logger: Optional["SPECTRALogger"] = None,
        timeout: int = 10,
        auth_header: str = "Authorization",
        auth_prefix: str = "Bearer",
        service: str = "API",
        stage: Optional[str] = None,
        source_system: Optional[str] = None,
    ) -> Dict:
        """Validate access to a specific API resource with retry logic and error handling."""
        if resource_id:
            endpoint = resource_endpoint.replace(
                "{projectId}", str(resource_id)
            ).replace("{releaseId}", str(resource_id))
        else:
            endpoint = resource_endpoint

        if logger:
            logger.debug(f"Testing resource access: {endpoint}...")

        # Use APIRequestHandler for retry logic
        handler = APIRequestHandler(
            max_retries=2,  # Fewer retries for resource validation (less critical)
            base_delay=1.0,
            max_delay=10.0,
            logger=logger,
        )
        
        url = f"{base_url}{endpoint}"
        headers = {auth_header: f"{auth_prefix} {api_token}"}
        
        # Extract resource name for error context
        resource_name = endpoint.split("/")[-1] if endpoint else "resource"
        
        response, error = handler.execute_with_retry(
            requests.get,
            url,
            headers=headers,
            timeout=timeout,
            service=service,
            stage=stage or "source",
            source_system=source_system,
            resource=resource_name,
            identifier=str(resource_id) if resource_id else "unknown",
            context={"endpoint": endpoint, "operation": "resource_access_validation", "resource_id": resource_id},
        )
        
        if error:
            error_message = getattr(error, "message", str(error))
            if logger:
                if isinstance(error, NotFoundError):
                    logger.warning(f"⚠️ Resource not found: {endpoint} (this may be expected)")
                elif isinstance(error, AuthorizationError):
                    logger.warning(f"⚠️ Resource access denied: {endpoint}")
                else:
                    logger.warning(f"⚠️ Resource access validation failed: {error_message}")
            return {"status": "Failed", "error": error_message, "error_type": type(error).__name__}
        
        # Parse response
        try:
            data = response.json()
            count = len(data) if isinstance(data, list) else 1
            if logger:
                logger.info(f"✅ Resource access validated ({count} items)")
            return {"status": "Success", "count": count}
        except Exception as e:
            if logger:
                logger.error(f"❌ Failed to parse resource response: {str(e)}")
            return {"status": "Failed", "error": f"Invalid response format: {str(e)}"}

    @staticmethod
    def bootstrap_endpoints_catalog(
        spark: SparkSession,
        delta: "DeltaTable",
        logger: "SPECTRALogger",
        endpoints_catalog: List[Dict],
        catalog_name: str = "ZEPHYR_ENDPOINTS_CATALOG",
    ) -> int:
        """Bootstrap endpoints catalog to Delta table."""
        logger.info("📚 Bootstrapping endpoints catalog...")

        if not endpoints_catalog:
            raise RuntimeError(f"{catalog_name} is empty. Ensure catalog is loaded.")

        df_endpoints = spark.createDataFrame([Row(**ep) for ep in endpoints_catalog])
        delta.write(
            df_endpoints,
            "source.endpoints",
            "Tables/source/endpoints",
            mode="overwrite",
        )
        delta.register("source.endpoints", "Tables/source/endpoints")

        logger.info(f"✅ Endpoints bootstrapped ({len(endpoints_catalog)} endpoints)")
        return len(endpoints_catalog)


    @staticmethod
    def display_portfolio_summary(
        spark: SparkSession,
        logger: "SPECTRALogger",
        source_system: str = "zephyr",
    ) -> None:
        """Display formatted portfolio summary from source.portfolio table.

        Args:
            spark: Spark session
            logger: Logger instance
            source_system: Source system identifier (default: "zephyr")
        """
        logger.info("📊 Portfolio Summary:")

        try:
            portfolio_df = spark.sql(f"""
                SELECT 
                    source_system,
                    contract_version,
                    total_endpoints,
                    endpoint_categories,
                    hierarchical_endpoints,
                    auth_method,
                    auth_status,
                    hierarchical_access_validated,
                    endpoint_success_rate,
                    supports_incremental,
                    status,
                    is_enabled,
                    last_updated
                FROM source.portfolio
                WHERE source_system = '{source_system}'
            """)

            portfolio = portfolio_df.first()
            if portfolio:
                categories = (
                    json.loads(portfolio["endpoint_categories"])
                    if portfolio["endpoint_categories"]
                    else {}
                )

                print("=" * 80)
                print(f"# 🎯 {portfolio['source_system'].upper()} SOURCE PORTFOLIO")
                print("=" * 80)
                print(f"\n**Source System:** {portfolio['source_system'].upper()}")
                print(f"**Contract Version:** {portfolio['contract_version']}")
                print(
                    f"**Status:** {portfolio['status'].upper()} ({'✅ Enabled' if portfolio['is_enabled'] else '❌ Disabled'})"
                )
                print("\n---")
                print("\n## 📊 Endpoint Portfolio")
                print(f"- **Total Endpoints:** {portfolio['total_endpoints']}")
                print(
                    f"- **Hierarchical Endpoints:** {portfolio['hierarchical_endpoints']}"
                )
                print("- **Endpoint Categories:**")
                for category, count in sorted(
                    categories.items(), key=lambda x: x[1], reverse=True
                )[:10]:
                    print(f"  - {category}: {count}")
                if len(categories) > 10:
                    print(f"  - ... and {len(categories) - 10} more categories")

                print("\n---")
                print("\n## 🔐 Authentication")
                print(f"- **Method:** {portfolio['auth_method']}")
                print(f"- **Status:** {portfolio['auth_status'].upper()}")
                print(
                    f"- **Hierarchical Access:** {'✅ Validated' if portfolio['hierarchical_access_validated'] else '❌ Not Validated'}"
                )

                print("\n---")
                print("\n## 📈 Capabilities")
                print(
                    f"- **Endpoint Success Rate:** {portfolio['endpoint_success_rate']:.1%}"
                )
                print(
                    f"- **Incremental Support:** {'✅ Yes' if portfolio['supports_incremental'] else '❌ No'}"
                )

                print("\n---")
                print("\n## 📅 Metadata")
                print(f"- **Last Updated:** {portfolio['last_updated']}")

                print("\n" + "=" * 80)
                print(
                    "\n💡 **View full portfolio:** Query `source.portfolio` table in Lakehouse"
                )
                print(
                    "📊 **Dashboard ready:** All metrics available for SPECTRA Source Portfolio Dashboard"
                )
                print("=" * 80)
            else:
                logger.warning("⚠️ Portfolio table exists but no record found")
        except Exception as e:
            logger.warning(f"⚠️ Could not display portfolio summary: {str(e)}")

    @staticmethod
    def execute_source_stage(
        spark: SparkSession,
        session: "NotebookSession",
        endpoints_catalog_global_name: Optional[str] = None,
        contract_version: Optional[str] = None,
        auth_method: Optional[str] = None,
        endpoint_success_rate: float = 0.70,
        supports_incremental: Optional[bool] = None,
        test_endpoint: Optional[str] = None,
        resource_endpoint_template: Optional[str] = None,
        timeout: int = 10,
        auth_header: str = "Authorization",
        auth_prefix: str = "Bearer",
        run_validation: Optional[bool] = None,
    ) -> None:
        """Orchestrate complete source stage execution - reusable for any source system.

        Automatically infers configuration from session context and variables when not provided.

        Args:
            spark: Spark session
            session: NotebookSession instance (must have load_context() and initialize() called)
            endpoints_catalog_global_name: Global variable name for endpoints catalog (inferred if None)
            contract_version: Contract version string (inferred from variables or defaults)
            auth_method: Authentication method type (inferred from variables or defaults)
            endpoint_success_rate: Expected endpoint success rate (0.0-1.0)
            supports_incremental: Whether API supports incremental extraction
            test_endpoint: Endpoint to test authentication (source-system specific default)
            resource_endpoint_template: Template for resource access validation (source-system specific)
            timeout: Request timeout
            auth_header: HTTP header name for auth
            auth_prefix: Auth prefix (e.g., "Bearer")
            run_validation: Whether to run validation tests (defaults to session.params["test"])
        """
        # Wrap execution in try/except to ensure Discord notification on failure
        try:
            SourceStageHelpers._execute_source_stage_internal(
                spark=spark,
                session=session,
                endpoints_catalog_global_name=endpoints_catalog_global_name,
                contract_version=contract_version,
                auth_method=auth_method,
                endpoint_success_rate=endpoint_success_rate,
                supports_incremental=supports_incremental,
                test_endpoint=test_endpoint,
                resource_endpoint_template=resource_endpoint_template,
                timeout=timeout,
                auth_header=auth_header,
                auth_prefix=auth_prefix,
                run_validation=run_validation,
            )
        except Exception as e:
            # Mark session as failed
            session.mark_failed(str(e))
            
            # Send Discord notification about failure
            SourceStageHelpers.send_exception_notification(session=session, exception=e)
            
            # Re-raise the original exception to fail the stage
            raise
    
    @staticmethod
    def _execute_source_stage_internal(
        spark: SparkSession,
        session: "NotebookSession",
        endpoints_catalog_global_name: Optional[str] = None,
        contract_version: Optional[str] = None,
        auth_method: Optional[str] = None,
        endpoint_success_rate: float = 0.70,
        supports_incremental: Optional[bool] = None,
        test_endpoint: Optional[str] = None,
        resource_endpoint_template: Optional[str] = None,
        timeout: int = 10,
        auth_header: str = "Authorization",
        auth_prefix: str = "Bearer",
        run_validation: Optional[bool] = None,
    ) -> None:
        """Internal implementation of source stage execution.
        
        This method contains the actual execution logic. The public
        execute_source_stage() method wraps this with exception handling
        to ensure Discord notifications are sent on failure.
        """
        # Infer configuration from session context and variables
        source_system = session.ctx["source_system"]

        # Infer endpoints catalog name: {SOURCE_SYSTEM}_ENDPOINTS_CATALOG
        if endpoints_catalog_global_name is None:
            endpoints_catalog_global_name = f"{source_system.upper()}_ENDPOINTS_CATALOG"

        # Infer contract version from variables or default
        if contract_version is None:
            contract_version = (
                session.variables.get("CONTRACT_VERSION", required=False) or "3.0.0"
            )

        # Infer auth method from variables or default
        if auth_method is None:
            auth_method = (
                session.variables.get("AUTH_METHOD", required=False) or "apiToken"
            )

        # Source-system specific defaults
        source_configs = {
            "zephyr": {
                "test_endpoint": "/project/details",
                "resource_endpoint_template": "/release/project/{projectId}",
                "supports_incremental": True,  # Zephyr has lastModifiedOn, lastTestedOn fields
            },
            "jira": {
                "test_endpoint": "/myself",
                "resource_endpoint_template": "/project/{projectId}",
                "supports_incremental": True,  # Jira has updated field for incremental
            },
        }

        source_config = source_configs.get(source_system.lower(), {})

        if test_endpoint is None:
            test_endpoint = source_config.get("test_endpoint", "/")

        if resource_endpoint_template is None:
            resource_endpoint_template = source_config.get("resource_endpoint_template")

        # Infer incremental support from source system config (defaults to False if not specified)
        if supports_incremental is None:
            supports_incremental = source_config.get("supports_incremental", False)
        log = session.log
        api_token = session.variables.get_secret("API_TOKEN")
        base_url = session.ctx["full_url"]
        
        # Initialize error collector for graceful degradation
        error_collector = ErrorCollector()

        # 1. Create config table
        SourceStageHelpers.create_source_config_table(
            spark=spark,
            delta=session.delta,
            logger=log,
            session=session,
            sdk_version="0.3.0",
        )
        session.add_capability("configTablesCreated")

        # 2. Validate authentication (CRITICAL - fails stage if failed)
        auth_result, all_projects = SourceStageHelpers.validate_api_authentication(
            base_url=base_url,
            api_token=api_token,
            test_endpoint=test_endpoint,
            logger=log,
            timeout=timeout,
            auth_header=auth_header,
            auth_prefix=auth_prefix,
            service=f"{source_system.upper()} API",
            stage="source",
            source_system=source_system,
        )

        if auth_result["status"] == "Failed":
            # Authentication is critical - fail immediately
            error = AuthenticationError(
                message=auth_result.get("error", "Unknown error"),
                category="auth",
                context={"endpoint": test_endpoint, "operation": "authentication"},
                stage="source",
                source_system=source_system,
            )
            error_collector.add(error, critical=True)
            error_message = getattr(error, "message", str(error))
            session.mark_failed(f"Authentication failed: {error_message}")
            
            # Log error summary before failing
            summary = error_collector.get_summary()
            log.error(f"❌ Source stage failed - Error summary: {summary}")
            raise error  # Raise the error to fail the stage

        session.add_capability("authVerified", **auth_result)

        # 3. Extract first project ID and validate resource access (NON-CRITICAL)
        first_project_id = None
        if all_projects and isinstance(all_projects, list) and len(all_projects) > 0:
            first_project_id = (
                all_projects[0].get("id") if isinstance(all_projects[0], dict) else None
            )

        if first_project_id and resource_endpoint_template:
            project_result = SourceStageHelpers.validate_api_resource_access(
                base_url=base_url,
                api_token=api_token,
                resource_endpoint=resource_endpoint_template,
                resource_id=first_project_id,
                logger=log,
                timeout=timeout,
                auth_header=auth_header,
                auth_prefix=auth_prefix,
                service=f"{source_system.upper()} API",
                stage="source",
                source_system=source_system,
            )
            
            # Resource access validation is non-critical - collect errors but continue
            if project_result["status"] == "Failed":
                error = ErrorClassification.classify_exception(
                    Exception(project_result.get("error", "Resource access failed")),
                    service=f"{source_system.upper()} API",
                    stage="source",
                    source_system=source_system,
                    context={"endpoint": resource_endpoint_template, "resource_id": first_project_id},
                )
                error_collector.add(error, critical=False)  # Non-critical - continue
                error_message = getattr(error, "message", str(error))
                log.warning(f"⚠️ Resource access validation failed (non-critical): {error_message}")
            
            session.add_capability("projectAccessVerified", **project_result)

        # 4. Create credentials table
        SourceStageHelpers.create_source_credentials_table(
            spark=spark,
            delta=session.delta,
            logger=log,
            api_token=api_token,
            validation_status=auth_result["status"],
        )

        # 5. Bootstrap endpoints catalog if needed
        ENDPOINTS_CATALOG = None
        try:
            import sys

            frame = sys._getframe(1)
            while frame:
                if endpoints_catalog_global_name in frame.f_globals:
                    ENDPOINTS_CATALOG = frame.f_globals[endpoints_catalog_global_name]
                    break
                frame = frame.f_back
        except:
            pass

        if session.params["bootstrap"]:
            if ENDPOINTS_CATALOG is None:
                raise RuntimeError(
                    f"{endpoints_catalog_global_name} not found. Ensure %run spectraSDK is executed before this block."
                )
            endpoint_count = SourceStageHelpers.bootstrap_endpoints_catalog(
                spark=spark,
                delta=session.delta,
                logger=log,
                endpoints_catalog=ENDPOINTS_CATALOG,
                catalog_name=endpoints_catalog_global_name,
            )
            session.add_capability("bootstrapped", endpoint_count=endpoint_count)

        # 6. Create portfolio table
        SourceStageHelpers.create_source_portfolio_table(
            spark=spark,
            delta=session.delta,
            logger=log,
            session=session,
            contract_version=contract_version,
            auth_method=auth_method,
            auth_status=auth_result["status"],
            endpoint_catalog=ENDPOINTS_CATALOG,
            endpoint_success_rate=endpoint_success_rate,
            supports_incremental=supports_incremental,
        )
        session.add_capability("tablesRegistered")

        # 7. Check for critical errors before proceeding
        if error_collector.has_critical_errors():
            summary = error_collector.get_summary()
            log.error(f"❌ Source stage failed - Critical errors detected: {summary}")
            # Raise first critical error to fail the stage
            raise error_collector.critical_errors[0]
        
        # 9. Run validation tests (always run for SPECTRA-grade, optional via test param)
        if run_validation is None:
            # Always run validations for production-grade pipeline
            run_validation = True

        if run_validation:
            validation_result = SourceStageValidation.validate_all_source_tables(
                spark=spark, session=session, logger=log
            )
            if not validation_result["valid"]:
                log.warning(
                    f"⚠️ Validation completed with {len(validation_result['errors'])} error(s)"
                )
                # Collect validation errors (non-critical)
                for error_msg in validation_result["errors"]:
                    error = ValidationError(
                        message=str(error_msg),
                        category="validation",
                        context={"operation": "table_validation"},
                        stage="source",
                        source_system=source_system,
                    )
                    error_collector.add(error, critical=False)
                
                for error in validation_result["errors"][:5]:
                    log.warning(f"  ❌ {error}")
                if len(validation_result["errors"]) > 5:
                    log.warning(
                        f"  ... and {len(validation_result['errors']) - 5} more errors"
                    )
            else:
                log.info("✅ All validation tests passed")
            session.result["validation"] = validation_result
        
        # Store error summary in session for activity logging
        if error_collector.has_errors():
            error_summary = error_collector.get_summary()
            session.result["errors"] = error_summary
            log.info(f"ℹ️ Source stage completed with {error_summary['total_errors']} non-critical error(s)")

        # 10. Send Discord notification with activity log details
        try:
            from datetime import datetime

            # Auto-detect source-specific webhook (e.g., DISCORD_WEBHOOK_URL_ZEPHYR)
            source_system_upper = source_system.upper()
            webhook_var = f"DISCORD_WEBHOOK_URL_{source_system_upper}"
            webhook_url = session.variables.get(webhook_var, required=False)
            # Fallback to generic DISCORD_WEBHOOK_URL if source-specific not found
            if not webhook_url:
                webhook_url = session.variables.get(
                    "DISCORD_WEBHOOK_URL", required=False
                )
            
            # Send notification regardless of status (include errors if present)
            if webhook_url:
                duration = (datetime.utcnow() - session.start_time).total_seconds() if session.start_time else 0.0
                status_emoji = "✅" if session.result["status"] == "Success" else "❌"
                
                # Build comprehensive notification with activity log details
                message_parts = []
                
                # Header with status
                message_parts.append(f"{status_emoji} **{session.ctx['source_name']} Source Stage Finalised**")
                message_parts.append(f"**Status:** {session.result['status']} | **Duration:** {duration:.1f}s")
                message_parts.append("")
                
                # Capabilities
                if session.result.get("capabilities"):
                    capabilities_str = ", ".join(session.result["capabilities"][:5])  # First 5
                    if len(session.result["capabilities"]) > 5:
                        capabilities_str += f" +{len(session.result['capabilities']) - 5} more"
                    message_parts.append(f"**Capabilities:** {capabilities_str}")
                    message_parts.append("")
                
                # Error summary (if errors occurred)
                error_summary = session.result.get("errors", {})
                if error_summary:
                    total_errors = error_summary.get("total_errors", 0)
                    critical_errors = error_summary.get("critical_errors", 0)
                    errors_by_category = error_summary.get("errors_by_category", {})
                    
                    if critical_errors > 0:
                        message_parts.append(f"⚠️ **Critical Errors:** {critical_errors}")
                    if total_errors > 0:
                        message_parts.append(f"**Non-Critical Errors:** {total_errors}")
                        if errors_by_category:
                            category_str = ", ".join([f"{cat}: {count}" for cat, count in list(errors_by_category.items())[:3]])
                            if len(errors_by_category) > 3:
                                category_str += " +more"
                            message_parts.append(f"  _By category: {category_str}_")
                    message_parts.append("")
                
                # Validation status
                if "validation" in session.result:
                    validation_result = session.result["validation"]
                    if validation_result.get("valid"):
                        message_parts.append("✅ **Validation:** All tests passed")
                    else:
                        error_count = len(validation_result.get("errors", []))
                        message_parts.append(f"⚠️ **Validation:** {error_count} error(s) found")
                    message_parts.append("")
                
                # Execution context
                execution_mode = "Interactive" if session.ctx.get("in_interactive") else "Pipeline"
                message_parts.append(f"**Execution:** {execution_mode} | **Lakehouse:** `{session.ctx.get('lakehouse_name', 'unknown')}`")
                message_parts.append("")
                
                # Outputs
                message_parts.append("**Outputs:**")
                message_parts.append("• `source.portfolio` | `source.config`")
                message_parts.append("• `source.credentials` | `source.endpoints`")
                message_parts.append("")
                
                # Activity log reference
                message_parts.append(f"📝 **Activity Log:** `log.{session.ctx['stage']}`")
                message_parts.append("")
                
                # Next steps
                message_parts.append("**Next:** Prepare Stage (Schema Introspection)")

                message = "\n".join(message_parts)

                SourceStageHelpers.send_discord_notification(
                    webhook_url=webhook_url,
                    message=message,
                    logger=log,
                    priority="high" if error_summary.get("critical_errors", 0) > 0 else "normal",
                )
        except Exception as e:
            if log:
                log.debug(f"Discord notification skipped: {str(e)}")

    @staticmethod
    def send_discord_notification(
        webhook_url: str,
        message: str,
        logger: Optional["SPECTRALogger"] = None,
        priority: str = "normal",
        timeout: float = 10.0,
    ) -> bool:
        """Send Discord notification via webhook (non-blocking).

        Args:
            webhook_url: Discord webhook URL
            message: Message content (supports markdown)
            logger: Optional logger instance
            priority: Priority level (normal, high, critical)
            timeout: Request timeout in seconds

        Returns:
            True if notification sent successfully, False otherwise
        """
        try:
            import requests

            payload = {"content": message}

            # Try to send (non-blocking - don't fail notebook if Discord is down)
            response = requests.post(webhook_url, json=payload, timeout=timeout)
            response.raise_for_status()

            if logger:
                logger.debug("📢 Discord notification sent")

            return True

        except Exception as e:
            # Don't fail notebook execution if notification fails
            if logger:
                logger.debug(f"Discord notification failed: {str(e)}")
            return False
    
    @staticmethod
    def send_exception_notification(
        session: "NotebookSession",
        exception: Exception,
        webhook_url: Optional[str] = None,
    ) -> None:
        """Send Discord notification for stage failure due to exception.
        
        Args:
            session: NotebookSession instance
            exception: Exception that caused the failure
            webhook_url: Optional webhook URL (will be auto-detected if None)
        """
        try:
            from datetime import datetime
            
            # Auto-detect webhook URL if not provided
            if not webhook_url:
                source_system = session.ctx.get("source_system", "unknown")
                source_system_upper = source_system.upper()
                webhook_var = f"DISCORD_WEBHOOK_URL_{source_system_upper}"
                webhook_url = session.variables.get(webhook_var, required=False)
                if not webhook_url:
                    webhook_url = session.variables.get("DISCORD_WEBHOOK_URL", required=False)
            
            if not webhook_url:
                return  # No webhook configured
            
            duration = (
                (datetime.utcnow() - session.start_time).total_seconds()
                if session.start_time else 0.0
            )
            
            # Get error type and message
            error_type = type(exception).__name__
            error_message = str(exception)
            
            # Build failure notification
            message_parts = []
            message_parts.append(f"❌ **{session.ctx.get('source_name', 'Source')} Stage Failed**")
            message_parts.append(f"**Status:** Failed | **Duration:** {duration:.1f}s")
            message_parts.append("")
            message_parts.append(f"**Error Type:** `{error_type}`")
            
            # Truncate long error messages
            if len(error_message) > 500:
                error_message = error_message[:500] + "..."
            message_parts.append(f"**Error Message:** ```{error_message}```")
            message_parts.append("")
            
            # Add error context if available (from structured errors)
            if hasattr(exception, "context") and isinstance(exception.context, dict):
                context_items = list(exception.context.items())[:3]  # First 3 context items
                if context_items:
                    context_str = ", ".join([f"`{k}`: {v}" for k, v in context_items])
                    message_parts.append(f"**Context:** {context_str}")
                    message_parts.append("")
            
            # Add error category if available
            if hasattr(exception, "category"):
                message_parts.append(f"**Category:** `{exception.category}`")
                if hasattr(exception, "retryable"):
                    message_parts.append(f"**Retryable:** {'Yes' if exception.retryable else 'No'}")
                message_parts.append("")
            
            # Execution context
            execution_mode = "Interactive" if session.ctx.get("in_interactive") else "Pipeline"
            message_parts.append(f"**Execution:** {execution_mode} | **Lakehouse:** `{session.ctx.get('lakehouse_name', 'unknown')}`")
            message_parts.append("")
            
            # Activity log reference
            message_parts.append(f"📝 **Activity Log:** `log.{session.ctx.get('stage', 'unknown')}`")
            message_parts.append("")
            message_parts.append("⚠️ **Action Required:** Check activity log for full error details and stack trace")
            
            message = "\n".join(message_parts)
            
            SourceStageHelpers.send_discord_notification(
                webhook_url=webhook_url,
                message=message,
                logger=session.log,
                priority="critical",  # Critical priority for failures
            )
        except Exception as notify_error:
            # Don't fail if Discord notification fails
            if session.log:
                session.log.debug(f"Exception notification failed: {str(notify_error)}")


class DataValidation:
    """Data validation helper for API responses, schemas, and data quality.

    Provides comprehensive validation capabilities for the Source stage,
    including API response validation, schema validation, row counts, and
    data quality checks.
    """

    @staticmethod
    def validate_api_response(
        response_data: Any,
        required_fields: Optional[List[str]] = None,
        field_types: Optional[Dict[str, type]] = None,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate API response structure and content.

        Args:
            response_data: API response data (dict or list)
            required_fields: List of required field names
            field_types: Dict of field_name -> expected_type
            logger: Logger instance

        Returns:
            Dict with validation results: {"valid": bool, "errors": List[str]}
        """
        errors = []

        # Validate JSON structure
        if not isinstance(response_data, (dict, list)):
            errors.append(f"Expected dict or list, got {type(response_data).__name__}")
            return {"valid": False, "errors": errors}

        # If it's a list, validate the first item
        if isinstance(response_data, list):
            if not response_data:
                errors.append("Empty response list")
                return {"valid": False, "errors": errors}
            response_data = response_data[0]

        # Validate required fields
        if required_fields:
            for field in required_fields:
                if field not in response_data:
                    errors.append(f"Missing required field: {field}")

        # Validate field types
        if field_types:
            for field, expected_type in field_types.items():
                if field in response_data:
                    if not isinstance(response_data[field], expected_type):
                        actual_type = type(response_data[field]).__name__
                        expected_type_name = expected_type.__name__
                        errors.append(
                            f"Field '{field}' has type {actual_type}, expected {expected_type_name}"
                        )

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info("✅ API response validation passed")
            else:
                logger.warning(f"⚠️ API response validation failed: {', '.join(errors)}")

        return {"valid": is_valid, "errors": errors}

    @staticmethod
    def validate_dataframe_schema(
        df,
        expected_schema: Optional[Any] = None,
        required_columns: Optional[List[str]] = None,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate DataFrame schema against expected structure.

        Args:
            df: Spark DataFrame
            expected_schema: Expected StructType schema (optional)
            required_columns: List of required column names (optional)
            logger: Logger instance

        Returns:
            Dict with validation results: {"valid": bool, "errors": List[str]}
        """
        errors = []

        # Validate required columns
        if required_columns:
            df_columns = set(df.columns)
            for col in required_columns:
                if col not in df_columns:
                    errors.append(f"Missing required column: {col}")

        # Validate full schema if provided
        if expected_schema:
            if df.schema != expected_schema:
                errors.append("Schema mismatch")
                # Provide detailed mismatch info
                expected_fields = {f.name: f.dataType for f in expected_schema.fields}
                actual_fields = {f.name: f.dataType for f in df.schema.fields}

                for col, expected_type in expected_fields.items():
                    if col not in actual_fields:
                        errors.append(f"  Missing column: {col}")
                    elif actual_fields[col] != expected_type:
                        errors.append(
                            f"  Column '{col}': expected {expected_type}, got {actual_fields[col]}"
                        )

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info("✅ DataFrame schema validation passed")
            else:
                logger.warning(f"  ⚠️ Schema validation failed: {', '.join(errors)}")

        return {"valid": is_valid, "errors": errors}

    @staticmethod
    def validate_row_count(
        df,
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None,
        expected_rows: Optional[int] = None,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate DataFrame row count.

        Args:
            df: Spark DataFrame
            min_rows: Minimum expected rows
            max_rows: Maximum expected rows
            expected_rows: Exact expected row count
            logger: Logger instance

        Returns:
            Dict with validation results: {"valid": bool, "row_count": int, "errors": List[str]}
        """
        row_count = df.count()
        errors = []

        if min_rows is not None and row_count < min_rows:
            errors.append(f"Row count {row_count} below minimum {min_rows}")

        if max_rows is not None and row_count > max_rows:
            errors.append(f"Row count {row_count} exceeds maximum {max_rows}")

        if expected_rows is not None and row_count != expected_rows:
            errors.append(
                f"Row count {row_count} does not match expected {expected_rows}"
            )

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info(f"✅ Row count validation passed: {row_count} rows")
            else:
                logger.warning(f"  ⚠️ Row count validation failed: {', '.join(errors)}")

        return {"valid": is_valid, "row_count": row_count, "errors": errors}

    @staticmethod
    def validate_no_nulls(
        df,
        columns: List[str],
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate that specified columns have no null values.

        Args:
            df: Spark DataFrame
            columns: List of column names to check
            logger: Logger instance

        Returns:
            Dict with validation results: {"valid": bool, "null_counts": Dict[str, int], "errors": List[str]}
        """
        from pyspark.sql.functions import col

        errors = []
        null_counts = {}

        for column in columns:
            if column not in df.columns:
                errors.append(f"Column '{column}' not found in DataFrame")
                continue

            null_count = df.filter(col(column).isNull()).count()
            null_counts[column] = null_count

            if null_count > 0:
                errors.append(f"Column '{column}' has {null_count} null values")

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info(f"✅ Null validation passed for {len(columns)} columns")
            else:
                logger.warning(f"  ⚠️ Null validation failed: {', '.join(errors)}")

        return {"valid": is_valid, "null_counts": null_counts, "errors": errors}

    @staticmethod
    def validate_unique_ids(
        df,
        id_column: str,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate that an ID column contains unique values.

        Args:
            df: Spark DataFrame
            id_column: Name of the ID column
            logger: Logger instance

        Returns:
            Dict with validation results: {"valid": bool, "total_count": int, "unique_count": int, "duplicate_count": int, "errors": List[str]}
        """
        errors = []

        if id_column not in df.columns:
            errors.append(f"Column '{id_column}' not found in DataFrame")
            return {"valid": False, "errors": errors}

        total_count = df.count()
        unique_count = df.select(id_column).distinct().count()
        duplicate_count = total_count - unique_count

        if duplicate_count > 0:
            errors.append(
                f"Column '{id_column}' has {duplicate_count} duplicate values"
            )

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info(
                    f"✅ Uniqueness validation passed: {total_count} unique IDs"
                )
            else:
                logger.warning(
                    f"  ⚠️ Uniqueness validation failed: {duplicate_count} duplicates found"
                )

        return {
            "valid": is_valid,
            "total_count": total_count,
            "unique_count": unique_count,
            "duplicate_count": duplicate_count,
            "errors": errors,
        }

    @staticmethod
    def validate_data_quality(
        df,
        validations: List[Dict[str, Any]],
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Run multiple data quality validations.

        Args:
            df: Spark DataFrame
            validations: List of validation configs, each with:
                - type: "no_nulls" | "unique_ids" | "row_count" | "schema"
                - **kwargs: specific args for each validation type
            logger: Logger instance

        Returns:
            Dict with aggregated validation results

        Example:
            validations = [
                {"type": "no_nulls", "columns": ["id", "name"]},
                {"type": "unique_ids", "id_column": "id"},
                {"type": "row_count", "min_rows": 1},
            ]
        """
        all_errors = []
        results = {}

        for validation in validations:
            val_type = validation.pop("type")

            if val_type == "no_nulls":
                result = DataValidation.validate_no_nulls(
                    df, logger=logger, **validation
                )
            elif val_type == "unique_ids":
                result = DataValidation.validate_unique_ids(
                    df, logger=logger, **validation
                )
            elif val_type == "row_count":
                result = DataValidation.validate_row_count(
                    df, logger=logger, **validation
                )
            elif val_type == "schema":
                result = DataValidation.validate_dataframe_schema(
                    df, logger=logger, **validation
                )
            else:
                result = {
                    "valid": False,
                    "errors": [f"Unknown validation type: {val_type}"],
                }

            results[val_type] = result
            if not result["valid"]:
                all_errors.extend(result["errors"])

        is_valid = len(all_errors) == 0
        if logger:
            if is_valid:
                logger.info(f"✅ All {len(validations)} data quality checks passed")
            else:
                logger.warning(
                    f"  ⚠️ Data quality validation failed: {len(all_errors)} errors"
                )

        return {
            "valid": is_valid,
            "validation_results": results,
            "errors": all_errors,
        }


class SourceStageValidation:
    """Comprehensive validation helpers for Source stage outputs.

    Provides contract validation, schema validation, and data quality checks
    for all source stage tables. Designed to be called from Stage 5 (VALIDATE)
    when test=True parameter is set.
    """

    @staticmethod
    def validate_portfolio_table(
        spark: SparkSession,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate source.portfolio table.

        Checks:
        - Table exists
        - Single row per source system
        - Required fields present
        - Data types correct
        - JSON fields valid
        - Numeric ranges valid
        - Discovery date preserved on updates
        """
        errors = []
        results = {}

        try:
            df = spark.table("source.portfolio")
            row_count = df.count()

            # Validate row count
            if row_count != 1:
                errors.append(f"Expected 1 portfolio row, found {row_count}")

            # Validate required fields
            required_fields = [
                "source_system",
                "contract_version",
                "total_endpoints",
                "hierarchical_endpoints",
                "endpoint_categories",
                "auth_method",
                "auth_status",
                "hierarchical_access_validated",
                "endpoint_success_rate",
                "supports_incremental",
                "status",
                "is_enabled",
                "discovery_date",
                "last_updated",
            ]

            for field in required_fields:
                if field not in df.columns:
                    errors.append(f"Missing required field: {field}")

            if row_count > 0:
                row = df.first().asDict()

                # Validate endpoint success rate (0.0-1.0)
                success_rate = row.get("endpoint_success_rate")
                if success_rate is not None:
                    if not (0.0 <= float(success_rate) <= 1.0):
                        errors.append(
                            f"endpoint_success_rate out of range: {success_rate}"
                        )

                # Validate endpoint_categories JSON
                categories_json = row.get("endpoint_categories", "{}")
                try:
                    import json

                    json.loads(categories_json)
                except:
                    errors.append(
                        f"endpoint_categories is not valid JSON: {categories_json[:50]}"
                    )

                # Validate discovery_date <= last_updated
                discovery_date = row.get("discovery_date")
                last_updated = row.get("last_updated")
                if discovery_date and last_updated:
                    if (
                        discovery_date > last_updated.date()
                        if hasattr(last_updated, "date")
                        else last_updated
                    ):
                        errors.append("discovery_date must be <= last_updated")

            results["row_count"] = row_count
            results["required_fields_check"] = len(
                [f for f in required_fields if f in df.columns]
            ) == len(required_fields)

        except Exception as e:
            errors.append(f"Error validating portfolio table: {str(e)}")
            results["table_exists"] = False
        else:
            results["table_exists"] = True

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info("✅ Portfolio table validation passed")
            else:
                logger.warning(f"  ⚠️ Portfolio validation failed: {len(errors)} errors")
                for error in errors:
                    logger.warning(f"    - {error}")

        return {"valid": is_valid, "errors": errors, "results": results}

    @staticmethod
    def validate_endpoints_catalog(
        spark: SparkSession,
        expected_count: Optional[int] = None,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate source.endpoints table.

        Checks:
        - Table exists
        - Row count (validated if expected_count provided)
        - No duplicate endpoints (path + method + category)
        - Required fields populated
        - Hierarchical flag accuracy
        """
        errors = []
        results = {}

        try:
            df = spark.table("source.endpoints")
            row_count = df.count()

            # Validate row count (only if expected_count provided)
            if expected_count is not None and row_count != expected_count:
                errors.append(f"Expected {expected_count} endpoints, found {row_count}")

            # Check for duplicates (using full_path + http_method - the actual unique endpoint identifier)
            duplicate_check = (
                df.groupBy("full_path", "http_method").count().filter("count > 1")
            )
            duplicate_count = duplicate_check.count()
            if duplicate_count > 0:
                errors.append(
                    f"Found {duplicate_count} duplicate endpoint(s) (same full_path + method)"
                )

            # Validate required fields
            required_fields = ["endpoint_path", "http_method", "category"]
            for field in required_fields:
                null_count = df.filter(df[field].isNull() | (df[field] == "")).count()
                if null_count > 0:
                    errors.append(f"Field '{field}' has {null_count} null/empty values")

            # Validate hierarchical count matches portfolio
            hierarchical_count = df.filter(df.hierarchical == True).count()
            results["hierarchical_count"] = hierarchical_count

            # Category distribution (optimized - collect only when necessary for small datasets)
            category_counts_df = df.groupBy("category").count()
            category_counts = category_counts_df.collect()
            results["categories"] = {
                row["category"]: row["count"] for row in category_counts
            }

            results["row_count"] = row_count
            results["duplicate_count"] = duplicate_count

        except Exception as e:
            errors.append(f"Error validating endpoints catalog: {str(e)}")
            results["table_exists"] = False
        else:
            results["table_exists"] = True

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info(
                    f"✅ Endpoints catalog validation passed ({row_count} endpoints)"
                )
            else:
                logger.warning(f"  ⚠️ Endpoints validation failed: {len(errors)} errors")
                for error in errors:
                    logger.warning(f"    - {error}")

        return {"valid": is_valid, "errors": errors, "results": results}

    @staticmethod
    def validate_config_table(
        spark: SparkSession,
        expected_keys: List[str] = None,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate source.config table.

        Checks:
        - Table exists
        - Expected config keys present
        - Values match execution context
        """
        errors = []
        results = {}

        if expected_keys is None:
            expected_keys = [
                "execution_mode",
                "operation_type",
                "notebook_name",
                "stage",
                "sdk_version",
                "bootstrap_enabled",
            ]

        try:
            df = spark.table("source.config")
            row_count = df.count()

            # Get all config keys (optimized - use DataFrame operations)
            config_keys_df = df.select("config_key").distinct()
            config_keys = [row["config_key"] for row in config_keys_df.collect()]
            results["config_keys"] = config_keys

            # Check expected keys present
            missing_keys = [key for key in expected_keys if key not in config_keys]
            if missing_keys:
                errors.append(f"Missing config keys: {', '.join(missing_keys)}")

            # Validate SDK version
            sdk_version_row = df.filter(df.config_key == "sdk_version").first()
            if sdk_version_row:
                sdk_version = sdk_version_row.config_value
                results["sdk_version"] = sdk_version
                if sdk_version != "0.3.0":
                    errors.append(f"Unexpected SDK version: {sdk_version}")

            results["row_count"] = row_count

        except Exception as e:
            errors.append(f"Error validating config table: {str(e)}")
            results["table_exists"] = False
        else:
            results["table_exists"] = True

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info(f"✅ Config table validation passed ({row_count} rows)")
            else:
                logger.warning(f"  ⚠️ Config validation failed: {len(errors)} errors")
                for error in errors:
                    logger.warning(f"    - {error}")

        return {"valid": is_valid, "errors": errors, "results": results}

    @staticmethod
    def validate_credentials_table(
        spark: SparkSession,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Validate source.credentials table.

        Checks:
        - Table exists
        - Token properly masked (***_XXX format)
        - No plaintext tokens
        """
        errors = []
        results = {}

        try:
            df = spark.table("source.credentials")
            row_count = df.count()

            if row_count > 0:
                credential_value = df.select("credential_value").first()[0]

                # Check masking format (should be ***_XXX or ***XXX)
                if not credential_value.startswith("***"):
                    errors.append(
                        f"Token not properly masked: {credential_value[:10]}..."
                    )

                # Check length (masked should be short)
                if len(credential_value) > 10:
                    errors.append(
                        f"Suspicious token length: {len(credential_value)} chars"
                    )

                results["masking_format"] = credential_value[:10]

            results["row_count"] = row_count

        except Exception as e:
            errors.append(f"Error validating credentials table: {str(e)}")
            results["table_exists"] = False
        else:
            results["table_exists"] = True

        is_valid = len(errors) == 0
        if logger:
            if is_valid:
                logger.info("✅ Credentials table validation passed (token masked)")
            else:
                logger.warning(
                    f"  ⚠️ Credentials validation failed: {len(errors)} errors"
                )
                for error in errors:
                    logger.warning(f"    - {error}")

        return {"valid": is_valid, "errors": errors, "results": results}


    @staticmethod
    def validate_all_source_tables(
        spark: SparkSession,
        session: "NotebookSession",
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Run comprehensive validation on all source stage tables.

        Returns aggregated validation results for all tables.
        """
        all_errors = []
        validation_results = {}

        # Validate each table
        validation_results["portfolio"] = (
            SourceStageValidation.validate_portfolio_table(spark, logger)
        )
        validation_results["endpoints"] = (
            SourceStageValidation.validate_endpoints_catalog(spark, logger=logger)
        )
        validation_results["config"] = SourceStageValidation.validate_config_table(
            spark, logger=logger
        )
        validation_results["credentials"] = (
            SourceStageValidation.validate_credentials_table(spark, logger)
        )

        # Aggregate errors
        for table_name, result in validation_results.items():
            if not result["valid"]:
                all_errors.extend([f"{table_name}: {e}" for e in result["errors"]])

        # Cross-table validations
        cross_errors = []

        # Validate endpoint counts match between portfolio and endpoints
        try:
            portfolio_df = spark.table("source.portfolio")
            endpoints_df = spark.table("source.endpoints")

            portfolio_endpoints = portfolio_df.first()["total_endpoints"]
            actual_endpoints = endpoints_df.count()

            if portfolio_endpoints != actual_endpoints:
                cross_errors.append(
                    f"Endpoint count mismatch: portfolio={portfolio_endpoints}, actual={actual_endpoints}"
                )

            portfolio_hierarchical = portfolio_df.first()["hierarchical_endpoints"]
            actual_hierarchical = endpoints_df.filter(
                endpoints_df.hierarchical == True
            ).count()

            if portfolio_hierarchical != actual_hierarchical:
                cross_errors.append(
                    f"Hierarchical endpoint count mismatch: portfolio={portfolio_hierarchical}, actual={actual_hierarchical}"
                )
        except Exception as e:
            cross_errors.append(f"Cross-table validation error: {str(e)}")

        all_errors.extend(cross_errors)
        validation_results["cross_table_validation"] = {
            "valid": len(cross_errors) == 0,
            "errors": cross_errors,
        }

        is_valid = len(all_errors) == 0
        if logger:
            if is_valid:
                logger.info("=" * 80)
                logger.info("✅ All source stage validations passed")
            else:
                logger.warning("=" * 80)
                logger.warning(
                    f"  ⚠️ Validation completed with {len(all_errors)} error(s)"
                )
                logger.warning("=" * 80)

        return {
            "valid": is_valid,
            "validation_results": validation_results,
            "errors": all_errors,
            "summary": {
                "tables_validated": len(validation_results),
                "total_errors": len(all_errors),
                "all_passed": is_valid,
            },
        }


class SchemaDiscoveryHelpers:
    """Generic schema discovery helpers for comprehensive test data creation.

    Provides reusable methods for discovering API schemas, data structures,
    and validation rules by creating comprehensive test data. Works for ANY
    REST API - not specific to Zephyr.

    SPECTRA-Grade: Generic logic in SDK, source-specific logic in templates.
    """

    @staticmethod
    def create_entity_comprehensively(
        base_url: str,
        endpoint: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        logger: Optional["SPECTRALogger"] = None,
        timeout: int = 30,
        save_response_path: Optional[str] = None,
    ) -> tuple[Optional[Dict[str, Any]], Optional[int], Optional[str]]:
        """Create entity via POST and capture full response - generic for any REST API.

        Args:
            base_url: Full API base URL (e.g., "https://api.example.com/v1")
            endpoint: API endpoint path (e.g., "/release" or "/issue")
            payload: Entity payload (dict)
            headers: HTTP headers dict (must include auth)
            logger: Optional logger instance
            timeout: Request timeout in seconds
            save_response_path: Optional path to save response JSON file

        Returns:
            Tuple of (entity_data, entity_id, error_message)
            - entity_data: Extracted entity dict (handles wrapped responses)
            - entity_id: Entity ID if created successfully
            - error_message: Error message if creation failed
        """
        import requests

        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        if logger:
            logger.info(f"Creating entity: POST {endpoint}")

        try:
            response = requests.post(
                url, headers=headers, json=payload, timeout=timeout
            )
            response.raise_for_status()

            created_entity = response.json()

            # Extract entity data (handle wrapped responses)
            entity_data = created_entity
            entity_id = None

            if isinstance(created_entity, dict):
                # Check for common wrapper keys (source-agnostic)
                wrapper_keys = ["dto", "data", "result", "entity", "item", "object"]
                # Also check for source-specific wrappers
                for key in list(created_entity.keys()):
                    if key.endswith("Dto") or key.endswith("DTO"):
                        wrapper_keys.insert(0, key)

                for key in wrapper_keys:
                    if key in created_entity:
                        entity_data = created_entity[key]
                        break

                entity_id = (
                    entity_data.get("id") if isinstance(entity_data, dict) else None
                )

            # Save response if path provided
            if save_response_path:
                import json
                from pathlib import Path

                Path(save_response_path).parent.mkdir(parents=True, exist_ok=True)
                with open(save_response_path, "w") as f:
                    json.dump(created_entity, f, indent=2)
                if logger:
                    logger.info(f"  💾 Saved response to: {save_response_path}")

            if logger:
                logger.info(f"  ✅ Created successfully! ID: {entity_id}")

            return entity_data, entity_id, None

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text[:500]}"

            # Save error response if path provided
            if save_response_path:
                import json
                from pathlib import Path

                error_path = str(save_response_path).replace(
                    "_response.json", f"_error_{e.response.status_code}.json"
                )
                Path(error_path).parent.mkdir(parents=True, exist_ok=True)
                try:
                    error_data = {
                        "status_code": e.response.status_code,
                        "payload": payload,
                        "error": e.response.text,
                    }
                    with open(error_path, "w") as f:
                        json.dump(error_data, f, indent=2)
                except:
                    pass

            if logger:
                logger.warning(f"  ❌ Creation failed: {error_msg}")

            return None, None, error_msg

        except Exception as e:
            error_msg = str(e)
            if logger:
                logger.warning(f"  ❌ Error: {error_msg}")
            return None, None, error_msg

    @staticmethod
    def analyze_field_structure(
        field_name: str, field_value: Any, path: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze a field's structure and return schema definition - generic for any JSON.

        Args:
            field_name: Field name
            field_value: Field value (any type)
            path: Optional JSON path segments (for nested fields)

        Returns:
            Schema definition dict with structureType, dataType, nullability, etc.
        """
        if path is None:
            path = [field_name]

        schema_def = {
            "fieldId": ".".join(path),
            "rawField": path,
            "targetField": path,
        }

        # Determine structure type and data type
        if field_value is None:
            schema_def["structureType"] = "scalar"
            schema_def["dataType"] = ["null"]
            schema_def["isNullable"] = True
        elif isinstance(field_value, bool):
            schema_def["structureType"] = "scalar"
            schema_def["dataType"] = ["bool"]
            schema_def["isNullable"] = False
        elif isinstance(field_value, int):
            schema_def["structureType"] = "scalar"
            schema_def["dataType"] = ["int64"]
            schema_def["isNullable"] = False
        elif isinstance(field_value, float):
            schema_def["structureType"] = "scalar"
            schema_def["dataType"] = ["float64"]
            schema_def["isNullable"] = False
        elif isinstance(field_value, str):
            schema_def["structureType"] = "scalar"
            schema_def["dataType"] = ["text"]
            schema_def["isNullable"] = False
        elif isinstance(field_value, list):
            schema_def["structureType"] = "array"
            if field_value:
                # Analyze first item to determine array element type
                first_item = field_value[0]
                item_schema = SchemaDiscoveryHelpers.analyze_field_structure(
                    f"{field_name}_item", first_item, path + ["item"]
                )
                schema_def["dataType"] = item_schema["dataType"]
                schema_def["itemStructureType"] = item_schema["structureType"]
            else:
                schema_def["dataType"] = ["json"]  # Empty array - unknown type
                schema_def["itemStructureType"] = "unknown"
            schema_def["isNullable"] = True
        elif isinstance(field_value, dict):
            schema_def["structureType"] = "record"
            schema_def["dataType"] = ["json"]
            schema_def["isNullable"] = False
            # Recursively analyze nested fields
            schema_def["fields"] = []
            for nested_key, nested_value in field_value.items():
                nested_path = path + [nested_key]
                nested_schema = SchemaDiscoveryHelpers.analyze_field_structure(
                    nested_key, nested_value, nested_path
                )
                schema_def["fields"].append(nested_schema)
        else:
            schema_def["structureType"] = "unknown"
            schema_def["dataType"] = ["json"]
            schema_def["isNullable"] = True

        return schema_def

    @staticmethod
    def compare_payload_response(
        payload: Dict[str, Any],
        response: Dict[str, Any],
        logger: Optional["SPECTRALogger"] = None,
    ) -> Dict[str, Any]:
        """Compare sent payload vs received response to infer API transformations.

        Args:
            payload: Original payload sent to API
            response: Response received from API
            logger: Optional logger instance

        Returns:
            Dict with comparison results:
            - fields_sent: Fields in payload
            - fields_received: Fields in response
            - fields_added: Fields API added
            - fields_removed: Fields API ignored
            - fields_transformed: Fields with different values/types
        """
        payload_fields = set(payload.keys()) if isinstance(payload, dict) else set()
        response_fields = set(response.keys()) if isinstance(response, dict) else set()

        fields_added = response_fields - payload_fields
        fields_removed = payload_fields - response_fields
        fields_common = payload_fields & response_fields

        # Check for transformations
        fields_transformed = []
        for field in fields_common:
            payload_val = payload.get(field)
            response_val = response.get(field)
            if payload_val != response_val:
                fields_transformed.append(
                    {
                        "field": field,
                        "payload_value": payload_val,
                        "response_value": response_val,
                        "type_changed": type(payload_val) != type(response_val),
                    }
                )

        result = {
            "fields_sent": list(payload_fields),
            "fields_received": list(response_fields),
            "fields_added": list(fields_added),
            "fields_removed": list(fields_removed),
            "fields_transformed": fields_transformed,
            "api_adds_fields": len(fields_added) > 0,
            "api_ignores_fields": len(fields_removed) > 0,
            "api_transforms_fields": len(fields_transformed) > 0,
        }

        if logger:
            if fields_added:
                logger.info(
                    f"  📥 API adds {len(fields_added)} fields: {list(fields_added)[:5]}"
                )
            if fields_removed:
                logger.info(
                    f"  📤 API ignores {len(fields_removed)} fields: {list(fields_removed)[:5]}"
                )
            if fields_transformed:
                logger.info(f"  🔄 API transforms {len(fields_transformed)} fields")

        return result

    @staticmethod
    def discover_schema_from_responses(
        responses: List[Dict[str, Any]],
        entity_type: str,
        logger: Optional["SPECTRALogger"] = None,
    ) -> List[Dict[str, Any]]:
        """Discover schema from multiple API responses - generic for any entity type.

        Args:
            responses: List of API response dicts (all same entity type)
            entity_type: Entity type name (for logging)
            logger: Optional logger instance

        Returns:
            List of schema field definitions
        """
        from collections import defaultdict

        if logger:
            logger.info(
                f"Discovering schema for {entity_type} from {len(responses)} response(s)"
            )

        # Collect all fields across all responses
        all_fields = defaultdict(list)  # field_name -> [values from all responses]

        for response in responses:
            # Handle wrapped responses
            entity_data = response
            if isinstance(response, dict):
                for key in ["dto", "data", "result", "entity"]:
                    if key in response:
                        entity_data = response[key]
                        break

            if isinstance(entity_data, dict):
                for field_name, field_value in entity_data.items():
                    all_fields[field_name].append(field_value)

        # Analyze each field
        schema_definitions = []
        for field_name, values in all_fields.items():
            # Use most common non-null value for analysis
            non_null_values = [v for v in values if v is not None]
            sample_value = non_null_values[0] if non_null_values else values[0]

            field_schema = SchemaDiscoveryHelpers.analyze_field_structure(
                field_name, sample_value, [field_name]
            )

            # Infer nullability from values
            has_null = any(v is None for v in values)
            field_schema["isNullable"] = has_null
            field_schema["isRequired"] = not has_null and len(non_null_values) == len(
                values
            )

            schema_definitions.append(field_schema)

        if logger:
            logger.info(f"  ✅ Discovered {len(schema_definitions)} fields")

        return schema_definitions

    @staticmethod
    def test_validation_rules(
        base_url: str,
        endpoint: str,
        valid_payload: Dict[str, Any],
        invalid_variations: List[Dict[str, Any]],
        headers: Dict[str, str],
        logger: Optional["SPECTRALogger"] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """Test validation rules by trying invalid data - generic for any API.

        Args:
            base_url: Full API base URL
            endpoint: API endpoint path
            valid_payload: Known valid payload (baseline)
            invalid_variations: List of invalid payload variations to test
            headers: HTTP headers dict
            logger: Optional logger instance
            timeout: Request timeout

        Returns:
            Dict with validation test results:
            - valid_payload_result: Result from valid payload
            - invalid_variations_results: List of results from invalid payloads
            - validation_rules_inferred: Inferred validation rules
        """
        if logger:
            logger.info(f"Testing validation rules for {endpoint}")

        # Test valid payload first
        valid_data, valid_id, valid_error = (
            SchemaDiscoveryHelpers.create_entity_comprehensively(
                base_url=base_url,
                endpoint=endpoint,
                payload=valid_payload,
                headers=headers,
                logger=logger,
                timeout=timeout,
            )
        )

        # Test invalid variations
        invalid_results = []
        for i, invalid_payload in enumerate(invalid_variations):
            if logger:
                logger.info(
                    f"  Testing invalid variation {i + 1}/{len(invalid_variations)}"
                )

            invalid_data, invalid_id, invalid_error = (
                SchemaDiscoveryHelpers.create_entity_comprehensively(
                    base_url=base_url,
                    endpoint=endpoint,
                    payload=invalid_payload,
                    headers=headers,
                    logger=logger,
                    timeout=timeout,
                )
            )

            invalid_results.append(
                {
                    "payload": invalid_payload,
                    "success": invalid_id is not None,
                    "error": invalid_error,
                }
            )

        # Infer validation rules from results
        validation_rules = []
        for result in invalid_results:
            if result["error"]:
                # Try to extract validation rule from error message
                error_msg = result["error"]
                validation_rules.append(
                    {
                        "invalid_payload": result["payload"],
                        "error_message": error_msg,
                        "rule_inferred": "Unknown",  # Could parse error message
                    }
                )

        return {
            "valid_payload_result": {
                "success": valid_id is not None,
                "entity_id": valid_id,
                "error": valid_error,
            },
            "invalid_variations_results": invalid_results,
            "validation_rules_inferred": validation_rules,
            "total_tests": len(invalid_variations) + 1,
            "validation_errors_found": len(validation_rules),
        }


class Pipeline:
    """Fabric pipeline execution context."""

    def __init__(self, spark):
        self._spark = spark

    @property
    def is_active(self) -> bool:
        """Is this notebook running in a pipeline?"""
        return self.operation_type != "SessionCreation"

    @property
    def is_interactive(self) -> bool:
        """Is this notebook running interactively in Fabric?"""
        return self.operation_type == "SessionCreation"

    @property
    def is_local(self) -> bool:
        """Is this notebook running locally? (Future)"""
        workspace_id = self._spark.conf.get("trident.workspace.id", "")
        return workspace_id == ""

    @property
    def operation_type(self) -> str:
        """Fabric operation type (SessionCreation, PipelineRun, etc.)"""
        return self._spark.conf.get("trident.operation.type", "Unknown")

    @property
    def activity_id(self) -> str:
        """Unique ID for this pipeline activity."""
        return self._spark.conf.get("trident.activity.id", "")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ══════════════════════════════════════════════════════════════════════════════
# Environment Class - Infrastructure Context
# ══════════════════════════════════════════════════════════════════════════════


class Environment:
    """Fabric workspace and lakehouse environment context."""

    def __init__(self, spark):
        self._spark = spark

    @property
    def workspace_id(self) -> str:
        """Fabric workspace UUID."""
        return self._spark.conf.get("trident.workspace.id", "")

    @property
    def lakehouse_id(self) -> str:
        """Attached lakehouse UUID."""
        return self._spark.conf.get("trident.lakehouse.id", "")

    @property
    def lakehouse_name(self) -> str:
        """Attached lakehouse display name."""
        return self._spark.conf.get("trident.lakehouse.name", "")

    @property
    def tenant_id(self) -> str:
        """Azure tenant UUID."""
        return self._spark.conf.get("trident.tenant.id", "")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ══════════════════════════════════════════════════════════════════════════════
# VariableLibrary Class - Configuration Accessor
# ══════════════════════════════════════════════════════════════════════════════


class VariableLibrary:
    """Fabric Variable Library accessor."""

    def __init__(self, library_name: str):
        self.library_name = library_name
        self._library_obj = None

    def get(self, key: str, default=None, required: bool = False):
        """Get variable from library."""
        value = None

        # Try Fabric Variable Library
        if self.library_name:
            try:
                if self._library_obj is None:
                    from notebookutils import variableLibrary

                    self._library_obj = variableLibrary.getLibrary(self.library_name)

                value = getattr(self._library_obj, key, None)
            except Exception:
                pass  # Variable Library not available, fall back to environment

        # Fallback to environment
        if value is None:
            import os

            value = os.environ.get(key)

        # Handle not found
        if value is None:
            if required:
                raise ValueError(
                    f"Required variable '{key}' not found in Variable Library '{self.library_name}'"
                )
            return default

        return value

    def get_secret(self, key: str, required: bool = True):
        """Get secret variable (never logged)."""
        return self.get(key, required=required)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean variable."""
        value = self.get(key)
        if value is None:
            return default
        return str(value).lower() in ("true", "1", "yes", "on")

    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer variable."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ══════════════════════════════════════════════════════════════════════════════
# DeltaTable Class - Delta Operations
# ══════════════════════════════════════════════════════════════════════════════

import logging


class DeltaTable:
    """Delta table operations helper."""

    def __init__(self, spark, log=None):
        self._spark = spark
        self._log = log or logging.getLogger(__name__)

    def write(
        self, df, table_name: str, path: str, mode: str = "overwrite", partition_by=None
    ):
        """Write DataFrame to Delta."""

        writer = df.write.format("delta").mode(mode)

        # Schema handling
        if mode == "overwrite":
            writer = writer.option("overwriteSchema", "true")
        if mode == "append":
            writer = writer.option("mergeSchema", "true")

        if partition_by:
            writer = writer.partitionBy(*partition_by)

        writer.save(path)

        row_count = df.count()
        if self._log:
            self._log.debug(f"✅ Wrote {row_count} rows to {path}")

    def register(self, table_name: str, path: str) -> None:
        """Register Delta table in Spark metastore (Jira's _ensure_table pattern).

        Args:
            table_name: Full table name with schema (e.g., "source.config")
            path: Delta table path (e.g., "Tables/source/config")
        """
        # Normalize path - ensure forward slashes and proper format
        normalized_path = str(path).replace('\\', '/').strip()
        
        # Debug logging for path issues
        if self._log:
            self._log.debug(f"🔍 Registering {table_name} with path: '{normalized_path}' (type: {type(path)}, length: {len(normalized_path)})")
        
        # Validate path starts with Tables/ or Files/
        if not normalized_path.startswith(('Tables/', 'Files/')):
            if self._log:
                self._log.warning(
                    f"⚠️ Invalid path format for {table_name}: '{normalized_path}' (first 10 chars: '{normalized_path[:10]}')"
                )
            return
        
        # Extract schema name (e.g., "source" from "source.config")
        schema_name = table_name.split(".")[0]

        # Create schema first (idempotent)
        try:
            self._spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        except Exception:
            pass  # Schema may already exist or not supported

        # Register table (idempotent - Jira pattern)
        try:
            self._spark.sql(
                f"CREATE TABLE IF NOT EXISTS {table_name} USING DELTA LOCATION '{normalized_path}'"
            )
            if self._log:
                self._log.debug(f"✅ Table registered: {table_name}")
        except Exception as e:
            error_msg = str(e)
            # Suppress known Fabric quirk: activity log registration warning (data still written successfully)
            is_activity_log = table_name.startswith("log.")
            is_known_quirk = "Invalid root directory" in error_msg and "got: Tab" in error_msg
            
            if is_activity_log and is_known_quirk:
                # Suppress warning - known Fabric quirk, data written successfully and queryable by path
                if self._log:
                    self._log.debug(
                        f"📝 Activity log written to {normalized_path} (registration skipped due to known Fabric quirk)"
                    )
            elif self._log:
                self._log.warning(
                    f"⚠️ Registration failed: {table_name} - {error_msg[:100]}"
                )


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ══════════════════════════════════════════════════════════════════════════════
# SPECTRALogger Class - Logging
# ══════════════════════════════════════════════════════════════════════════════

import sys


class SPECTRALogger:
    """SPECTRA-grade logger."""

    @staticmethod
    def create(
        name: str,
        level: str = "INFO",
        notebook_name=None,
        workspace_id=None,
        stage=None,
    ):
        """Create SPECTRA logger."""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.handlers.clear()

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper()))

        # Simplified format: timestamp - level - message (no redundant notebook/stage)
        format_parts = ["%(asctime)s", "%(levelname)-8s", "%(message)s"]
        formatter = logging.Formatter(
            " - ".join(format_parts), datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

        return logger

    @staticmethod
    def get_default_level(is_interactive: bool = False) -> str:
        """
        Determine log level based on execution mode.

        Interactive (Fabric UI) → DEBUG (verbose diagnostics)
        Pipeline (production) → INFO (clean logs)
        """
        return "DEBUG" if is_interactive else "INFO"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ══════════════════════════════════════════════════════════════════════════════
# NotebookSession Class - Main Orchestrator
# ══════════════════════════════════════════════════════════════════════════════


class NotebookSession:
    """Manages complete notebook lifecycle with 7-stage pattern."""

    def __init__(self, variable_library_name: str):
        self.variable_library_name = variable_library_name
        self.ctx = {}
        self.params = {}
        self.log = None
        self.debug = False
        self.start_time = None
        self.result = {"status": "Success", "capabilities": []}

        # Specialized components
        self.pipeline = None
        self.environment = None
        self.variables = None
        self.delta = None

    def load_context(self, bootstrap=False, backfill=False, spark: Optional[SparkSession] = None, **kwargs):
        """Stage 2: Load Fabric context + Variable Library.
        
        Args:
            bootstrap: Bootstrap flag
            backfill: Backfill flag
            spark: Optional SparkSession (defaults to getOrCreate() if not provided)
            **kwargs: Additional parameters
        """
        # Use provided spark or get/create one (lazy fallback for backward compatibility)
        spark = spark or SparkSession.builder.getOrCreate()

        # Initialize components
        self.pipeline = Pipeline(spark)
        self.environment = Environment(spark)
        self.variables = VariableLibrary(self.variable_library_name)
        self.delta = DeltaTable(spark, self.log)

        # Load config
        source_system = self.variables.get("SOURCE_SYSTEM", required=True)
        source_name = self.variables.get("SOURCE_NAME", required=True)
        stage = self.variables.get("STAGE", required=True)
        notebook_name = self.variables.get("NOTEBOOK_NAME", required=True)
        base_url = self.variables.get("BASE_URL")
        base_path = self.variables.get("BASE_PATH")
        full_url = f"{base_url}{base_path}" if base_url and base_path else base_url

        # Store context
        self.ctx = {
            "workspace_id": self.environment.workspace_id,
            "lakehouse_id": self.environment.lakehouse_id,
            "lakehouse_name": self.environment.lakehouse_name,
            "tenant_id": self.environment.tenant_id,
            "source_system": source_system,
            "source_name": source_name,
            "stage": stage,
            "notebook_name": notebook_name,
            "base_url": base_url,
            "base_path": base_path,
            "full_url": full_url,
            "in_pipeline": self.pipeline.is_active,
            "in_interactive": self.pipeline.is_interactive,
        }

        # Validate parameters
        self.params = {
            "bootstrap": bootstrap,
            "backfill": backfill,
            **kwargs,
        }
        
        return self  # Enable method chaining

    def initialize(self):
        """Stage 3: Initialize logger and start timer."""
        # Debug mode: ON in interactive (Fabric UI), OFF in pipeline (production)
        self.debug = self.ctx["in_interactive"]
        level = SPECTRALogger.get_default_level(self.ctx["in_interactive"])

        log = SPECTRALogger.create(
            name=self.ctx["notebook_name"],
            level=level,
            notebook_name=self.ctx["notebook_name"],
            workspace_id=self.ctx["workspace_id"],
            stage=self.ctx["stage"],
        )

        # Update DeltaTable logger
        if self.delta:
            self.delta._log = log

        self.start_time = datetime.utcnow()

        # Startup banner (clean, production-ready)
        log.info(
            f"🚀 {self.ctx['notebook_name']} | {self.ctx['stage']} | {self.ctx['source_name']}"
        )
        log.info(
            f"📍 {self.ctx['lakehouse_name']} | {'Interactive' if self.ctx['in_interactive'] else 'Pipeline'}"
        )

        self.log = log
        return log

    def add_capability(self, capability: str, **metadata):
        """Add capability to result."""
        self.result["capabilities"].append(capability)
        if metadata:
            self.result[capability] = metadata

    def mark_failed(self, error_msg: str):
        """Mark execution as failed."""
        self.result["status"] = "Failed"
        self.result["error"] = error_msg
        self.log.error(f"❌ {error_msg}")

    def register_tables(self, tables: list):
        """Register multiple tables at once with backtick escaping for dots.

        Args:
            tables: List of (table_name, path) tuples
                e.g., [("source.source", "Tables/source/source")]
        """
        self.log.info(f"📋 Registering {len(tables)} tables in metastore...")

        for table_name, path in tables:
            # Use backticks to escape dots in table names
            escaped_name = f"`{table_name}`"
            try:
                self.delta._spark.sql(
                    f"CREATE TABLE IF NOT EXISTS {escaped_name} USING DELTA LOCATION '{path}'"
                )
                self.log.info(f"  ✅ {table_name}")
            except Exception as e:
                self.log.warning(
                    f"   ⚠️ Registration failed: {table_name} - {str(e)[:100]}"
                )

    def validate(self):
        """Stage 5: Validate execution."""
        if self.result["status"] == "Success":
            self.log.info("✅ Validation passed")
        else:
            self.log.error("❌ Validation failed")
            raise RuntimeError(
                f"Execution failed: {self.result.get('error', 'Unknown error')}"
            )

    def record(self, spark: Optional[SparkSession] = None):
        """Stage 6: Record activity to Delta log table for audit trail.
        
        Logs execution metadata, capabilities, status, errors, and duration
        to `Tables/log/{stage}log` Delta table for observability.
        
        Args:
            spark: Optional SparkSession (defaults to getOrCreate() if not provided)
        """
        # Use provided spark or get/create one (lazy fallback for backward compatibility)
        spark = spark or SparkSession.builder.getOrCreate()
        
        # Calculate duration
        duration_seconds = (
            (datetime.utcnow() - self.start_time).total_seconds()
            if self.start_time
            else 0.0
        )
        
        # Prepare error summary
        error_summary = self.result.get("errors", {})
        error_summary_json = json.dumps(error_summary) if error_summary else None
        
        # Prepare capabilities (comma-separated string)
        capabilities_str = ", ".join(self.result.get("capabilities", [])) if self.result.get("capabilities") else None
        
        # Prepare parameters (JSON string)
        params_json = json.dumps(self.params) if self.params else None
        
        # Build activity log record
        schema = StructType(
            [
                StructField("execution_id", StringType(), False),  # Unique execution ID
                StructField("notebook_name", StringType(), False),
                StructField("stage", StringType(), False),
                StructField("source_system", StringType(), False),
                StructField("source_name", StringType(), False),
                StructField("workspace_id", StringType(), False),
                StructField("lakehouse_id", StringType(), False),
                StructField("lakehouse_name", StringType(), False),
                StructField("execution_mode", StringType(), False),  # "interactive" or "pipeline"
                StructField("status", StringType(), False),  # "Success" or "Failed"
                StructField("error_message", StringType(), True),  # Nullable
                StructField("capabilities", StringType(), True),  # Nullable - comma-separated
                StructField("duration_seconds", DoubleType(), False),
                StructField("error_summary", StringType(), True),  # Nullable - JSON string
                StructField("parameters", StringType(), True),  # Nullable - JSON string
                StructField("start_time", TimestampType(), False),
                StructField("end_time", TimestampType(), False),
                StructField("recorded_at", TimestampType(), False),
            ]
        )
        
        # Generate execution ID (timestamp-based, unique per execution)
        execution_id = f"{self.ctx['notebook_name']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"
        
        df_log = spark.createDataFrame(
            [
                Row(
                    execution_id=execution_id,
                    notebook_name=self.ctx["notebook_name"],
                    stage=self.ctx["stage"],
                    source_system=self.ctx["source_system"],
                    source_name=self.ctx["source_name"],
                    workspace_id=self.ctx["workspace_id"],
                    lakehouse_id=self.ctx["lakehouse_id"],
                    lakehouse_name=self.ctx["lakehouse_name"],
                    execution_mode="interactive" if self.ctx["in_interactive"] else "pipeline",
                    status=self.result.get("status", "Unknown"),
                    error_message=self.result.get("error"),
                    capabilities=capabilities_str,
                    duration_seconds=duration_seconds,
                    error_summary=error_summary_json,
                    parameters=params_json,
                    start_time=self.start_time if self.start_time else datetime.utcnow(),
                    end_time=datetime.utcnow(),
                    recorded_at=datetime.utcnow(),
                )
            ],
            schema=schema,
        )
        
        # Write to Delta table (append mode for historical log)
        # Use log.{stage} format to match Tables/log/ path structure
        log_table_name = f"log.{self.ctx['stage']}"
        # Ensure path uses forward slashes and starts with Tables/
        # Use same pattern as other tables: Tables/{schema}/{table}
        log_table_path = f"Tables/log/{self.ctx['stage']}log"
        
        # Debug: log the exact path being used
        if self.log:
            self.log.debug(f"🔍 Activity log path: '{log_table_path}' (length: {len(log_table_path)})")
        
        try:
            self.delta.write(
                df_log,
                log_table_name,
                log_table_path,
                mode="append",  # Append for historical log
            )
            # Pass path as string directly (already normalized in register method)
            self.delta.register(log_table_name, log_table_path)
            self.log.info(f"📝 Activity logged to {log_table_name} ({duration_seconds:.1f}s, {self.result['status']})")
        except Exception as e:
            # Activity logging failures should not fail the stage, but log as warning
            # Data is still written to path, can be queried by path if registration fails
            error_msg = str(e)
            if "DoesNotExist" in error_msg:
                # Schema might not exist - try creating it explicitly
                try:
                    schema_name = log_table_name.split(".")[0]
                    self.delta._spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
                    # Retry registration
                    self.delta.register(log_table_name, log_table_path)
                    self.log.info(f"📝 Activity logged to {log_table_name} ({duration_seconds:.1f}s, {self.result['status']})")
                except Exception as retry_error:
                    self.log.warning(
                        f"⚠️ Activity log registration failed (data written to {log_table_path}): {str(retry_error)[:150]}"
                    )
            else:
                self.log.warning(
                    f"⚠️ Activity logging failed (data written to {log_table_path}): {error_msg[:150]}"
                )

    def finalise(self):
        """Stage 7: Finalise execution and send notifications.
        
        Note: Discord notifications are sent from execute_source_stage() 
        to include activity log details. This method just logs finalisation.
        """
        duration = (datetime.utcnow() - self.start_time).total_seconds() if self.start_time else 0.0

        self.log.info(
            f"✅ {self.ctx['notebook_name']} Finalised | {duration:.1f}s | {self.result['status']}"
        )
        if self.result.get("capabilities"):
            self.log.info(f"💪 Capabilities: {', '.join(self.result['capabilities'])}")
        
        # Log error summary if present
        error_summary = self.result.get("errors", {})
        if error_summary:
            total = error_summary.get("total_errors", 0)
            critical = error_summary.get("critical_errors", 0)
            if critical > 0:
                self.log.warning(f"⚠️ Completed with {critical} critical error(s) and {total} total error(s)")
            elif total > 0:
                self.log.info(f"ℹ️ Completed with {total} non-critical error(s)")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ==============================================================================
# ZEPHYR API INTELLIGENCE
# Auto-generated from intelligence/ folder
# Source: API Intelligence Framework (7-phase discovery)
# ==============================================================================


# CELL **CELL**

# MARKDOWN **MARKDOWN**
# == ZEPHYR API INTELLIGENCE (COMPLETE) ================================= SPECTRA
# 
# **Complete Intelligence**: Schemas with full Jira-style metadata:
# - `entity`: Target dimension name (singular)
# - `fieldId`: Raw API field name
# - `structureType`: scalar | array
# - `rawField`: Properties to extract from source
# - `targetField`: Flattened target column names
# - `dataType`: Target data types
# - `dimensionName`: Dimension table name (for arrays)
# - `bridgeName`: Bridge table name (for many-to-many)
# 
# **Source**: API Intelligence Framework + Manual Overrides
# **Maturity**: L6 (Jira-proven pattern)

# CODE **CODE**

# ==============================================================================
# ZEPHYR API INTELLIGENCE (COMPLETE)
# Auto-generated from intelligence/complete-intelligence.yaml
# Source: API Intelligence Framework + Manual Overrides
# Maturity: L6 (Jira-proven pattern)
# ==============================================================================


# CELL **CELL**

# MARKDOWN **MARKDOWN**
# == ZEPHYR API INTELLIGENCE (COMPLETE) ================================= SPECTRA
# 
# **Complete Intelligence**: Schemas with full Jira-style metadata:
# - `entity`: Target dimension name (singular)
# - `fieldId`: Raw API field name
# - `structureType`: scalar | array
# - `rawField`: Properties to extract from source
# - `targetField`: Flattened target column names
# - `dataType`: Target data types
# - `dimensionName`: Dimension table name (for arrays)
# - `bridgeName`: Bridge table name (for many-to-many)
# 
# **Source**: API Intelligence Framework + Manual Overrides
# **Maturity**: L6 (Jira-proven pattern)

# CODE **CODE**

# ==============================================================================
# ZEPHYR API INTELLIGENCE (COMPLETE)
# Auto-generated from intelligence/complete-intelligence.yaml
# Source: API Intelligence Framework + Manual Overrides
# Maturity: L6 (Jira-proven pattern)
# ==============================================================================

class ZephyrIntelligence:
    """Zephyr API intelligence - complete schema with dimensional modeling."""

    # Complete entity schemas (fields include: entity, fieldId, structureType,
    # rawField, targetField, dataType, dimensionName, bridgeName, etc.)
    ENTITIES = {
        "cycle": {
            "endpoint": "/cycle",
            "field_count": 14,
            "fields": [
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "cycle.id",
                                            "entity": "cycleId",
                                            "fieldId": "id",
                                            "group": "identity",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "id"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "cycleId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "cycle.environment",
                                            "entity": "environment",
                                            "fieldId": "environment",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "environment"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "environment"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "cycle.build",
                                            "entity": "build",
                                            "fieldId": "build",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "build"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "build"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "cycle.name",
                                            "entity": "cycleName",
                                            "fieldId": "name",
                                            "group": "identity",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "name"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "cycleName"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "cycle.startDate",
                                            "entity": "startDate",
                                            "fieldId": "startDate",
                                            "group": "timestamps",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "startDate"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "startDate"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "cycle.endDate",
                                            "entity": "endDate",
                                            "fieldId": "endDate",
                                            "group": "timestamps",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "endDate"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "endDate"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "cycle.cycleStartDate",
                                            "entity": "cycleStartDate",
                                            "fieldId": "cycleStartDate",
                                            "group": "timestamps",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "cycleStartDate"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "cycleStartDate"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "cycle.cycleEndDate",
                                            "entity": "cycleEndDate",
                                            "fieldId": "cycleEndDate",
                                            "group": "timestamps",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "cycleEndDate"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "cycleEndDate"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "cycle.status",
                                            "entity": "status",
                                            "fieldId": "status",
                                            "group": "status",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "status"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "status"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "cycle.revision",
                                            "entity": "revision",
                                            "fieldId": "revision",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "revision"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "revision"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "cycle.releaseId",
                                            "entity": "releaseId",
                                            "fieldId": "releaseId",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "releaseId"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "releaseId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "array<int64>",
                                                            "array<text>",
                                                            "array<date>",
                                                            "array<date>",
                                                            "array<bool>"
                                            ],
                                            "description": "cycle.cyclePhases array of text",
                                            "entity": "cyclePhase",
                                            "fieldId": "cyclePhases",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Phases within a test cycle. Can be empty for cycles without phases.",
                                            "rawField": [
                                                            "id",
                                                            "name",
                                                            "startDate",
                                                            "endDate",
                                                            "isActive"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "array",
                                            "targetField": [
                                                            "cyclePhaseId",
                                                            "cyclePhaseName",
                                                            "cyclePhaseStartDate",
                                                            "cyclePhaseEndDate",
                                                            "cyclePhaseIsActive"
                                            ],
                                            "dimensionName": "dimCyclePhase",
                                            "bridgeName": "bridgeCyclePhase"
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "cycle.createdOn",
                                            "entity": "createdOn",
                                            "fieldId": "createdOn",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "createdOn"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "createdOn"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "bool"
                                            ],
                                            "description": "cycle.hasChild",
                                            "entity": "hasChild",
                                            "fieldId": "hasChild",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requires unlocked release. Use existing releases.",
                                            "rawField": [
                                                            "hasChild"
                                            ],
                                            "sourceEndpoint": "/cycle",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "hasChild"
                                            ]
                            }
            ]
        },
        "release": {
            "endpoint": "/release",
            "field_count": 12,
            "fields": [
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "release.id",
                                            "entity": "releaseId",
                                            "fieldId": "id",
                                            "group": "identity",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "id"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "releaseId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "release.name",
                                            "entity": "releaseName",
                                            "fieldId": "name",
                                            "group": "identity",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "name"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "releaseName"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "release.description",
                                            "entity": "description",
                                            "fieldId": "description",
                                            "group": "metadata",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "description"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "description"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "release.startDate",
                                            "entity": "startDate",
                                            "fieldId": "startDate",
                                            "group": "timestamps",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "startDate"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "startDate"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "release.releaseStartDate",
                                            "entity": "releaseStartDate",
                                            "fieldId": "releaseStartDate",
                                            "group": "timestamps",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "releaseStartDate"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "releaseStartDate"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "release.createdDate",
                                            "entity": "createdDate",
                                            "fieldId": "createdDate",
                                            "group": "timestamps",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "createdDate"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "createdDate"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "release.projectId",
                                            "entity": "projectId",
                                            "fieldId": "projectId",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "projectId"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "projectId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "release.orderId",
                                            "entity": "orderId",
                                            "fieldId": "orderId",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "orderId"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "orderId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "bool"
                                            ],
                                            "description": "release.globalRelease",
                                            "entity": "globalRelease",
                                            "fieldId": "globalRelease",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "globalRelease"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "globalRelease"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "bool"
                                            ],
                                            "description": "release.projectRelease",
                                            "entity": "projectRelease",
                                            "fieldId": "projectRelease",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "projectRelease"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "projectRelease"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "bool"
                                            ],
                                            "description": "release.hasChild",
                                            "entity": "hasChild",
                                            "fieldId": "hasChild",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "hasChild"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "hasChild"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "bool"
                                            ],
                                            "description": "release.syncEnabled",
                                            "entity": "syncEnabled",
                                            "fieldId": "syncEnabled",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-003: Locks for >60s after creation",
                                            "rawField": [
                                                            "syncEnabled"
                                            ],
                                            "sourceEndpoint": "/release",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "syncEnabled"
                                            ]
                            }
            ]
        },
        "requirement": {
            "endpoint": "/requirementtree/add",
            "field_count": 10,
            "fields": [
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "requirement.id",
                                            "entity": "requirementId",
                                            "fieldId": "id",
                                            "group": "identity",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.",
                                            "rawField": [
                                                            "id"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "requirementId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "requirement.name",
                                            "entity": "requirementName",
                                            "fieldId": "name",
                                            "group": "identity",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.",
                                            "rawField": [
                                                            "name"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "requirementName"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "requirement.description",
                                            "entity": "description",
                                            "fieldId": "description",
                                            "group": "metadata",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.",
                                            "rawField": [
                                                            "description"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "description"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "requirement.projectId",
                                            "entity": "projectId",
                                            "fieldId": "projectId",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.",
                                            "rawField": [
                                                            "projectId"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "projectId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "requirement.parentId",
                                            "entity": "parentId",
                                            "fieldId": "parentId",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.",
                                            "rawField": [
                                                            "parentId"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "parentId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "array<int64>",
                                                            "array<text>"
                                            ],
                                            "description": "requirement.categories array of text",
                                            "entity": "category",
                                            "fieldId": "categories",
                                            "group": "relationships",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requirement categorization. Empty in test data - needs validation.",
                                            "rawField": [
                                                            "id",
                                                            "name"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "array",
                                            "targetField": [
                                                            "categoryId",
                                                            "categoryName"
                                            ],
                                            "dimensionName": "dimCategory",
                                            "bridgeName": "bridgeRequirementCategory",
                                            "confidence": "low"
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "array<int64>",
                                                            "array<text>",
                                                            "array<text>",
                                                            "array<array<int64>>"
                                            ],
                                            "description": "requirement.requirements array of text",
                                            "entity": "requirement",
                                            "fieldId": "requirements",
                                            "group": "relationships",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Hierarchical requirement tree. requirements[] contains child requirements.",
                                            "rawField": [
                                                            "id",
                                                            "name",
                                                            "description",
                                                            "releaseIds"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "array",
                                            "targetField": [
                                                            "requirementId",
                                                            "requirementName",
                                                            "requirementDescription",
                                                            "requirementReleaseIds"
                                            ],
                                            "dimensionName": "dimRequirement",
                                            "bridgeName": "bridgeRequirementTree"
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "requirement.lastModifiedOn",
                                            "entity": "lastModifiedOn",
                                            "fieldId": "lastModifiedOn",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.",
                                            "rawField": [
                                                            "lastModifiedOn"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "lastModifiedOn"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "array<int64>"
                                            ],
                                            "description": "requirement.releaseIds array of text",
                                            "entity": "releaseId",
                                            "fieldId": "releaseIds",
                                            "group": "relationships",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Releases associated with this requirement.",
                                            "rawField": [
                                                            "releaseIds"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "array",
                                            "targetField": [
                                                            "releaseId"
                                            ],
                                            "dimensionName": "dimRelease",
                                            "bridgeName": "bridgeRequirementRelease"
                            },
                            {
                                            "apiStatus": "\u2705 Working (workaround)",
                                            "dataType": [
                                                            "bool"
                                            ],
                                            "description": "requirement.hasChild",
                                            "entity": "hasChild",
                                            "fieldId": "hasChild",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.",
                                            "rawField": [
                                                            "hasChild"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "hasChild"
                                            ]
                            }
            ]
        },
        "requirement_folder": {
            "endpoint": "/requirementtree/add",
            "field_count": 9,
            "fields": [
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "requirement_folder.id",
                                            "entity": "requirement_folderId",
                                            "fieldId": "id",
                                            "group": "identity",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Works perfectly",
                                            "rawField": [
                                                            "id"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "requirement_folderId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "requirement_folder.name",
                                            "entity": "requirement_folderName",
                                            "fieldId": "name",
                                            "group": "identity",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Works perfectly",
                                            "rawField": [
                                                            "name"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "requirement_folderName"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "text"
                                            ],
                                            "description": "requirement_folder.description",
                                            "entity": "description",
                                            "fieldId": "description",
                                            "group": "metadata",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Works perfectly",
                                            "rawField": [
                                                            "description"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "description"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "requirement_folder.projectId",
                                            "entity": "projectId",
                                            "fieldId": "projectId",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Works perfectly",
                                            "rawField": [
                                                            "projectId"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "projectId"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "array<int64>",
                                                            "array<text>"
                                            ],
                                            "description": "requirement_folder.categories array of text",
                                            "entity": "category",
                                            "fieldId": "categories",
                                            "group": "relationships",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Requirement categorization. Empty in test data - needs validation.",
                                            "rawField": [
                                                            "id",
                                                            "name"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "array",
                                            "targetField": [
                                                            "categoryId",
                                                            "categoryName"
                                            ],
                                            "dimensionName": "dimCategory",
                                            "bridgeName": "bridgeRequirementCategory",
                                            "confidence": "low"
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "array<int64>",
                                                            "array<text>",
                                                            "array<text>",
                                                            "array<array<int64>>"
                                            ],
                                            "description": "requirement_folder.requirements array of text",
                                            "entity": "requirement",
                                            "fieldId": "requirements",
                                            "group": "relationships",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Hierarchical requirement tree. requirements[] contains child requirements.",
                                            "rawField": [
                                                            "id",
                                                            "name",
                                                            "description",
                                                            "releaseIds"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "array",
                                            "targetField": [
                                                            "requirementId",
                                                            "requirementName",
                                                            "requirementDescription",
                                                            "requirementReleaseIds"
                                            ],
                                            "dimensionName": "dimRequirement",
                                            "bridgeName": "bridgeRequirementTree"
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "int64"
                                            ],
                                            "description": "requirement_folder.lastModifiedOn",
                                            "entity": "lastModifiedOn",
                                            "fieldId": "lastModifiedOn",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Works perfectly",
                                            "rawField": [
                                                            "lastModifiedOn"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "lastModifiedOn"
                                            ]
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "array<int64>"
                                            ],
                                            "description": "requirement_folder.releaseIds array of text",
                                            "entity": "releaseId",
                                            "fieldId": "releaseIds",
                                            "group": "relationships",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Releases associated with this requirement.",
                                            "rawField": [
                                                            "releaseIds"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "array",
                                            "targetField": [
                                                            "releaseId"
                                            ],
                                            "dimensionName": "dimRelease",
                                            "bridgeName": "bridgeRequirementRelease"
                            },
                            {
                                            "apiStatus": "\u2705 Working",
                                            "dataType": [
                                                            "bool"
                                            ],
                                            "description": "requirement_folder.hasChild",
                                            "entity": "hasChild",
                                            "fieldId": "hasChild",
                                            "group": "attributes",
                                            "isNullable": True,
                                            "isRequired": False,
                                            "notes": "Works perfectly",
                                            "rawField": [
                                                            "hasChild"
                                            ],
                                            "sourceEndpoint": "/requirementtree/add",
                                            "structureType": "scalar",
                                            "targetField": [
                                                            "hasChild"
                                            ]
                            }
            ]
        },
        "testcase_folder": {
            "endpoint": "/testcasetree",
            "field_count": 0,
            "fields": []
        },
    }

    # Dependencies (creation order)
    DEPENDENCIES = {
            "allocation": {
                    "dependency_count": 1,
                    "dependent_count": 0,
                    "depends_on": [
                            "testcase"
                    ],
                    "required_by": []
            },
            "cycle": {
                    "dependency_count": 1,
                    "dependent_count": 1,
                    "depends_on": [
                            "release"
                    ],
                    "required_by": [
                            "execution"
                    ]
            },
            "execution": {
                    "dependency_count": 2,
                    "dependent_count": 0,
                    "depends_on": [
                            "testcase",
                            "cycle"
                    ],
                    "required_by": []
            },
            "project": {
                    "dependency_count": 0,
                    "dependent_count": 1,
                    "depends_on": [],
                    "required_by": [
                            "testcase_folder"
                    ]
            },
            "release": {
                    "dependency_count": 0,
                    "dependent_count": 1,
                    "depends_on": [],
                    "required_by": [
                            "cycle"
                    ]
            },
            "requirement": {
                    "dependency_count": 1,
                    "dependent_count": 0,
                    "depends_on": [
                            "requirement_folder"
                    ],
                    "required_by": []
            },
            "requirement_folder": {
                    "dependency_count": 0,
                    "dependent_count": 1,
                    "depends_on": [],
                    "required_by": [
                            "requirement"
                    ]
            },
            "testcase": {
                    "dependency_count": 1,
                    "dependent_count": 2,
                    "depends_on": [
                            "testcase_folder"
                    ],
                    "required_by": [
                            "allocation",
                            "execution"
                    ]
            },
            "testcase_folder": {
                    "dependency_count": 1,
                    "dependent_count": 1,
                    "depends_on": [
                            "project"
                    ],
                    "required_by": [
                            "testcase"
                    ]
            }
    }
    HIERARCHY = {
            "level_0": [
                    "project",
                    "release",
                    "requirement_folder"
            ],
            "level_1": [
                    "testcase_folder",
                    "cycle",
                    "requirement"
            ],
            "level_2": [
                    "testcase"
            ],
            "level_3": [
                    "allocation",
                    "execution"
            ]
    }
    INDEPENDENT_ENTITIES = [
            "project",
            "release",
            "requirement_folder"
    ]
    LEAF_ENTITIES = [
            "requirement",
            "execution",
            "allocation"
    ]

    # Constraints (blockers, bugs, API quirks)
    CONSTRAINTS = {
        "api_inconsistencies": [
                    {
                                "entity": "requirement",
                                "id": "INCONSISTENCY-001",
                                "issue": "POST /requirement is broken, must use POST /requirementtree/add",
                                "notes": "Folder and requirement creation use same endpoint, differentiated by parentId presence",
                                "title": "Requirement Creation Uses Folder Endpoint"
                    },
                    {
                                "entity": "multiple",
                                "examples": {
                                            "cycle": "Requires epoch milliseconds (int)",
                                            "release": "Accepts 'YYYY-MM-DD' string"
                                },
                                "id": "INCONSISTENCY-002",
                                "issue": "Some endpoints accept 'YYYY-MM-DD', others require epoch milliseconds",
                                "notes": "No consistent date format across API",
                                "title": "Date Format Inconsistency"
                    }
        ],
        "blockers": [
                    {
                                "date_discovered": "2025-12-08",
                                "endpoint": "POST /requirement",
                                "entity": "requirement",
                                "id": "BLOCKER-001",
                                "impact": "Cannot create requirements via documented API",
                                "issue": "Returns HTTP 500: 'Cannot invoke java.lang.Long.longValue() because id is null'",
                                "reported_to_vendor": False,
                                "severity": "critical",
                                "title": "Requirement Creation API Broken",
                                "workaround": {
                                            "method": "Use POST /requirementtree/add with parentId",
                                            "notes": "Must create requirement_folder first, then use parentId",
                                            "status": "\u2705 Working"
                                }
                    },
                    {
                                "blocks": [
                                            "testcase",
                                            "execution",
                                            "allocation"
                                ],
                                "date_discovered": "2025-12-08",
                                "endpoint": "POST /testcasetree",
                                "entity": "testcase_folder",
                                "id": "BLOCKER-002",
                                "impact": "Cannot create testcase folders, blocks all testcase/execution/allocation creation",
                                "issue": "Returns HTTP 400: 'For input string: None'",
                                "reported_to_vendor": False,
                                "severity": "critical",
                                "title": "Testcase Folder API Broken",
                                "workaround": {
                                            "method": "Manual creation in UI required",
                                            "notes": "Tried 4 variations (omit parentId, parentId: None, parentId: 0, no parentId field) - all failed",
                                            "status": "\u26a0\ufe0f Manual only"
                                }
                    },
                    {
                                "date_discovered": "2025-12-08",
                                "endpoint": "POST /release",
                                "entity": "release",
                                "id": "BLOCKER-003",
                                "impact": "Cannot create cycles immediately after release creation",
                                "issue": "Newly created releases are locked for >60 seconds, preventing cycle creation",
                                "reported_to_vendor": False,
                                "severity": "high",
                                "title": "Release Lock Duration >60 Seconds",
                                "workaround": {
                                            "method": "Use existing (old) releases for cycle creation",
                                            "notes": "Tested 15s, 30s, 60s delays - all failed. Old releases work immediately.",
                                            "status": "\u2705 Working"
                                }
                    }
        ],
        "bugs": [
                    {
                                "date_discovered": "2025-12-08",
                                "endpoint": "GET /release/{id}",
                                "entity": "release",
                                "id": "BUG-007",
                                "impact": "Cannot validate release creation via GET",
                                "issue": "Returns HTTP 403 Forbidden even with valid API token",
                                "reported_to_vendor": False,
                                "severity": "medium",
                                "title": "Release GET by ID Returns HTTP 403",
                                "workaround": {
                                            "method": "Skip GET validation for releases",
                                            "notes": "Assume creation succeeded if POST returns 200/201",
                                            "status": "\u2705 Working"
                                }
                    }
        ],
        "quirks": [
                    {
                                "date_discovered": "2025-12-08",
                                "entity": "requirement",
                                "id": "QUIRK-001",
                                "impact": "Must use timestamps or UUIDs in requirement names",
                                "issue": "API rejects duplicate requirement names even across different test runs",
                                "severity": "low",
                                "title": "Requirement Names Must Be Unique Across All Runs",
                                "workaround": {
                                            "method": "Include timestamp in requirement name",
                                            "notes": "Use datetime.now().strftime('%Y%m%d%H%M%S') in name",
                                            "status": "\u2705 Working"
                                }
                    },
                    {
                                "date_discovered": "2025-12-08",
                                "entity": "cycle",
                                "id": "QUIRK-002",
                                "impact": "Must use existing releases or wait >60s",
                                "issue": "Cannot create cycle with newly created release (locked)",
                                "severity": "medium",
                                "title": "Cycle Creation Requires Unlocked Release",
                                "workaround": {
                                            "method": "Query for existing releases and use oldest one",
                                            "notes": "Oldest releases are most likely unlocked",
                                            "status": "\u2705 Working"
                                }
                    },
                    {
                                "date_discovered": "2025-12-08",
                                "entity": "testcase",
                                "id": "QUIRK-003",
                                "impact": "Blocked by BLOCKER-002 (folder creation broken)",
                                "issue": "Cannot create testcase without tcrCatalogTreeId",
                                "severity": "medium",
                                "title": "Testcase Requires tcrCatalogTreeId (Folder ID)",
                                "workaround": {
                                            "method": "None - depends on folder API fix",
                                            "notes": "Must fix folder API first",
                                            "status": "\u274c Blocked"
                                }
                    }
        ],
        "undocumented_behavior": [
                    {
                                "behavior": "Releases are locked after creation for >60 seconds",
                                "entity": "release",
                                "id": "UNDOCUMENTED-001",
                                "notes": "Not mentioned in API documentation",
                                "title": "Release Lock Mechanism"
                    },
                    {
                                "behavior": "API rejects parentId: None despite documentation suggesting it's valid for root folders",
                                "entity": "testcase_folder",
                                "id": "UNDOCUMENTED-002",
                                "notes": "Documentation doesn't clarify how to create root folders",
                                "title": "Folder API parentId Rejection"
                    }
        ],
    }

    @classmethod
    def get_entity_fields(cls, entity: str):
        """Get all fields for an entity (with complete schema)."""
        return cls.ENTITIES.get(entity, {}).get('fields', [])

    @classmethod
    def get_entity_schema(cls, entity: str):
        """Get complete entity schema."""
        return cls.ENTITIES.get(entity, {})

    @classmethod
    def get_dependencies(cls, entity: str):
        """Get dependencies for an entity."""
        for dep in getattr(cls, 'INDEPENDENT_ENTITIES', []):
            if dep == entity:
                return {'depends_on': [], 'required_by': []}
        return {}

    @classmethod
    def get_creation_order(cls):
        """Get entities in dependency order."""
        return []

    @classmethod
    def get_all_constraints(cls):
        """Get all constraints (blockers, bugs, quirks)."""
        return cls.CONSTRAINTS

    @classmethod
    def get_array_fields(cls, entity: str):
        """Get all array-type fields for an entity."""
        fields = cls.get_entity_fields(entity)
        return [f for f in fields if f.get("structureType") == "array"]

    @classmethod
    def get_dimensional_fields(cls, entity: str):
        """Get fields with dimensional modeling metadata."""
        fields = cls.get_entity_fields(entity)
        return [f for f in fields if "dimensionName" in f or "bridgeName" in f]


# CELL ********************

# ==============================================================================
# ZEPHYR API INTELLIGENCE
# Auto-generated from intelligence/ folder
# Source: API Intelligence Framework (7-phase discovery)
# ==============================================================================

class ZephyrIntelligence:
    """Zephyr API intelligence - schemas, dependencies, constraints."""

    # Schemas from intelligence/schemas/*.json
    SCHEMAS = {
        "cycle": {
            "entity": "cycle",
            "endpoint": "/cycle",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "environment": {
                                                            "type": "string"
                                            },
                                            "build": {
                                                            "type": "string"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "startDate": {
                                                            "type": "integer"
                                            },
                                            "endDate": {
                                                            "type": "integer"
                                            },
                                            "cycleStartDate": {
                                                            "type": "string"
                                            },
                                            "cycleEndDate": {
                                                            "type": "string"
                                            },
                                            "status": {
                                                            "type": "integer"
                                            },
                                            "revision": {
                                                            "type": "integer"
                                            },
                                            "releaseId": {
                                                            "type": "integer"
                                            },
                                            "cyclePhases": {
                                                            "type": "array"
                                            },
                                            "createdOn": {
                                                            "type": "integer"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "build",
                                            "createdOn",
                                            "cycleEndDate",
                                            "cyclePhases",
                                            "cycleStartDate",
                                            "endDate",
                                            "environment",
                                            "hasChild",
                                            "id",
                                            "name",
                                            "releaseId",
                                            "revision",
                                            "startDate",
                                            "status"
                            ]
            },
            "notes": 'Requires unlocked release. Use existing releases.'
        },
        "release": {
            "entity": "release",
            "endpoint": "/release",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "startDate": {
                                                            "type": "integer"
                                            },
                                            "releaseStartDate": {
                                                            "type": "string"
                                            },
                                            "createdDate": {
                                                            "type": "integer"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "orderId": {
                                                            "type": "integer"
                                            },
                                            "globalRelease": {
                                                            "type": "boolean"
                                            },
                                            "projectRelease": {
                                                            "type": "boolean"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            },
                                            "syncEnabled": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "createdDate",
                                            "description",
                                            "globalRelease",
                                            "hasChild",
                                            "id",
                                            "name",
                                            "orderId",
                                            "projectId",
                                            "projectRelease",
                                            "releaseStartDate",
                                            "startDate",
                                            "syncEnabled"
                            ]
            },
            "notes": 'BLOCKER-003: Locks for >60s after creation'
        },
        "requirement": {
            "entity": "requirement",
            "endpoint": "/requirementtree/add",
            "method": "POST",
            "status": '✅ Working (workaround)',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "parentId": {
                                                            "type": "integer"
                                            },
                                            "categories": {
                                                            "type": "array"
                                            },
                                            "requirements": {
                                                            "type": "array"
                                            },
                                            "lastModifiedOn": {
                                                            "type": "integer"
                                            },
                                            "releaseIds": {
                                                            "type": "array"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "categories",
                                            "description",
                                            "hasChild",
                                            "id",
                                            "lastModifiedOn",
                                            "name",
                                            "parentId",
                                            "projectId",
                                            "releaseIds",
                                            "requirements"
                            ]
            },
            "notes": 'BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.'
        },
        "requirement_folder": {
            "entity": "requirement_folder",
            "endpoint": "/requirementtree/add",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "categories": {
                                                            "type": "array"
                                            },
                                            "requirements": {
                                                            "type": "array"
                                            },
                                            "lastModifiedOn": {
                                                            "type": "integer"
                                            },
                                            "releaseIds": {
                                                            "type": "array"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "categories",
                                            "description",
                                            "hasChild",
                                            "id",
                                            "lastModifiedOn",
                                            "name",
                                            "projectId",
                                            "releaseIds",
                                            "requirements"
                            ]
            },
            "notes": 'Works perfectly'
        },
        "testcase_folder": {
            "entity": "testcase_folder",
            "endpoint": "/testcasetree",
            "method": "POST",
            "status": '❌ Broken',
            "schema": None,
            "notes": 'BLOCKER-002: API rejects valid payloads (HTTP 400)'
        },
    }

    # READ endpoints for production mode (GET endpoints for reading from project 44)
    # These are used by Prepare stage to build schema from production data
    READ_ENDPOINTS = {
        "project": {
            "endpoint": "/project",
            "method": "GET",
            "description": "Get all projects",
            "read_only": True,
            "project": 44  # Production project
        },
        "release": {
            "endpoint": "/release",
            "method": "GET",
            "description": "Get releases for a project",
            "read_only": True,
            "project": 44,  # Production project
            "query_params": ["projectId"],
            "example": "/release?projectId=44"
        },
        "cycle": {
            "endpoint": "/cycle/release/{releaseid}",
            "method": "GET",
            "description": "Get cycles for a release",
            "read_only": True,
            "project": 44,  # Production project
            "path_params": ["releaseid"],
            "depends_on": "release",  # Must fetch release first
            "example": "/cycle/release/123"
        },
        "execution": {
            "endpoint": "/execution",
            "method": "GET",
            "description": "Get executions (may require cycle/testcase filters)",
            "read_only": True,
            "project": 44,  # Production project
            "depends_on": ["cycle", "testcase"]
        },
        "requirement": {
            "endpoint": "/requirement",
            "method": "GET",
            "description": "Get requirements",
            "read_only": True,
            "project": 44  # Production project
        },
        "testcase": {
            "endpoint": "/testcase",
            "method": "GET",
            "description": "Get test cases",
            "read_only": True,
            "project": 44  # Production project
        }
    }

    # Dependencies from intelligence/dependencies.yaml
    DEPENDENCIES = {'project': {'depends_on': [], 'required_by': ['testcase_folder'], 'dependency_count': 0, 'dependent_count': 1}, 'release': {'depends_on': [], 'required_by': ['cycle'], 'dependency_count': 0, 'dependent_count': 1}, 'requirement_folder': {'depends_on': [], 'required_by': ['requirement'], 'dependency_count': 0, 'dependent_count': 1}, 'requirement': {'depends_on': ['requirement_folder'], 'required_by': [], 'dependency_count': 1, 'dependent_count': 0}, 'cycle': {'depends_on': ['release'], 'required_by': ['execution'], 'dependency_count': 1, 'dependent_count': 1}, 'testcase_folder': {'depends_on': ['project'], 'required_by': ['testcase'], 'dependency_count': 1, 'dependent_count': 1}, 'testcase': {'depends_on': ['testcase_folder'], 'required_by': ['allocation', 'execution'], 'dependency_count': 1, 'dependent_count': 2}, 'execution': {'depends_on': ['testcase', 'cycle'], 'required_by': [], 'dependency_count': 2, 'dependent_count': 0}, 'allocation': {'depends_on': ['testcase'], 'required_by': [], 'dependency_count': 1, 'dependent_count': 0}}

    # Constraints from intelligence/quirks.yaml
    CONSTRAINTS = {'blockers': [{'id': 'BLOCKER-001', 'title': 'Requirement Creation API Broken', 'severity': 'critical', 'entity': 'requirement', 'endpoint': 'POST /requirement', 'issue': "Returns HTTP 500: 'Cannot invoke java.lang.Long.longValue() because id is null'", 'impact': 'Cannot create requirements via documented API', 'workaround': {'method': 'Use POST /requirementtree/add with parentId', 'status': '✅ Working', 'notes': 'Must create requirement_folder first, then use parentId'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}, {'id': 'BLOCKER-002', 'title': 'Testcase Folder API Broken', 'severity': 'critical', 'entity': 'testcase_folder', 'endpoint': 'POST /testcasetree', 'issue': "Returns HTTP 400: 'For input string: null'", 'impact': 'Cannot create testcase folders, blocks all testcase/execution/allocation creation', 'workaround': {'method': 'Manual creation in UI required', 'status': '⚠️ Manual only', 'notes': 'Tried 4 variations (omit parentId, parentId: null, parentId: 0, no parentId field) - all failed'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08', 'blocks': ['testcase', 'execution', 'allocation']}, {'id': 'BLOCKER-003', 'title': 'Release Lock Duration >60 Seconds', 'severity': 'high', 'entity': 'release', 'endpoint': 'POST /release', 'issue': 'Newly created releases are locked for >60 seconds, preventing cycle creation', 'impact': 'Cannot create cycles immediately after release creation', 'workaround': {'method': 'Use existing (old) releases for cycle creation', 'status': '✅ Working', 'notes': 'Tested 15s, 30s, 60s delays - all failed. Old releases work immediately.'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}], 'bugs': [{'id': 'BUG-007', 'title': 'Release GET by ID Returns HTTP 403', 'severity': 'medium', 'entity': 'release', 'endpoint': 'GET /release/{id}', 'issue': 'Returns HTTP 403 Forbidden even with valid API token', 'impact': 'Cannot validate release creation via GET', 'workaround': {'method': 'Skip GET validation for releases', 'status': '✅ Working', 'notes': 'Assume creation succeeded if POST returns 200/201'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}], 'quirks': [{'id': 'QUIRK-001', 'title': 'Requirement Names Must Be Unique Across All Runs', 'severity': 'low', 'entity': 'requirement', 'issue': 'API rejects duplicate requirement names even across different test runs', 'impact': 'Must use timestamps or UUIDs in requirement names', 'workaround': {'method': 'Include timestamp in requirement name', 'status': '✅ Working', 'notes': "Use datetime.now().strftime('%Y%m%d%H%M%S') in name"}, 'date_discovered': '2025-12-08'}, {'id': 'QUIRK-002', 'title': 'Cycle Creation Requires Unlocked Release', 'severity': 'medium', 'entity': 'cycle', 'issue': 'Cannot create cycle with newly created release (locked)', 'impact': 'Must use existing releases or wait >60s', 'workaround': {'method': 'Query for existing releases and use oldest one', 'status': '✅ Working', 'notes': 'Oldest releases are most likely unlocked'}, 'date_discovered': '2025-12-08'}, {'id': 'QUIRK-003', 'title': 'Testcase Requires tcrCatalogTreeId (Folder ID)', 'severity': 'medium', 'entity': 'testcase', 'issue': 'Cannot create testcase without tcrCatalogTreeId', 'impact': 'Blocked by BLOCKER-002 (folder creation broken)', 'workaround': {'method': 'None - depends on folder API fix', 'status': '❌ Blocked', 'notes': 'Must fix folder API first'}, 'date_discovered': '2025-12-08'}], 'api_inconsistencies': [{'id': 'INCONSISTENCY-001', 'title': 'Requirement Creation Uses Folder Endpoint', 'entity': 'requirement', 'issue': 'POST /requirement is broken, must use POST /requirementtree/add', 'notes': 'Folder and requirement creation use same endpoint, differentiated by parentId presence'}, {'id': 'INCONSISTENCY-002', 'title': 'Date Format Inconsistency', 'entity': 'multiple', 'issue': "Some endpoints accept 'YYYY-MM-DD', others require epoch milliseconds", 'examples': {'release': "Accepts 'YYYY-MM-DD' string", 'cycle': 'Requires epoch milliseconds (int)'}, 'notes': 'No consistent date format across API'}], 'undocumented_behavior': [{'id': 'UNDOCUMENTED-001', 'title': 'Release Lock Mechanism', 'entity': 'release', 'behavior': 'Releases are locked after creation for >60 seconds', 'notes': 'Not mentioned in API documentation'}, {'id': 'UNDOCUMENTED-002', 'title': 'Folder API parentId Rejection', 'entity': 'testcase_folder', 'behavior': "API rejects parentId: null despite documentation suggesting it's valid for root folders", 'notes': "Documentation doesn't clarify how to create root folders"}]}

    @classmethod
    def get_schema(cls, entity: str):
        """Get schema for an entity."""
        return cls.SCHEMAS.get(entity)

    @classmethod
    def get_dependencies(cls, entity: str):
        """Get dependencies for an entity."""
        return cls.DEPENDENCIES.get(entity, {})

    @classmethod
    def get_creation_order(cls):
        """Get entities in dependency order."""
        # Based on topological sort from intelligence/creation-order.yaml
        return ['project', 'release', 'requirement_folder', 'testcase_folder', 'cycle', 'requirement', 'testcase', 'allocation', 'execution']

    @classmethod
    def get_all_constraints(cls):
        """Get all constraints (blockers, bugs, quirks)."""
        return cls.CONSTRAINTS
    
    @classmethod
    def get_read_endpoint(cls, entity: str):
        """Get READ endpoint for an entity (production mode - GET endpoints)."""
        return cls.READ_ENDPOINTS.get(entity)
    
    @classmethod
    def get_read_endpoint_path(cls, entity: str, **params):
        """Get READ endpoint path with parameters filled in."""
        endpoint_info = cls.READ_ENDPOINTS.get(entity)
        if not endpoint_info:
            return None
        
        path = endpoint_info["endpoint"]
        
        # Fill path parameters (e.g., {releaseid} → actual release ID)
        if "path_params" in endpoint_info:
            for param in endpoint_info["path_params"]:
                if param in params:
                    path = path.replace(f"{{{param}}}", str(params[param]))
        
        # Add query parameters
        if "query_params" in endpoint_info and params:
            query_parts = []
            for param in endpoint_info["query_params"]:
                if param in params:
                    query_parts.append(f"{param}={params[param]}")
            if query_parts:
                path += "?" + "&".join(query_parts)
        
        return path

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }


# CELL ********************

# ==============================================================================
# ZEPHYR API INTELLIGENCE
# Auto-generated from intelligence/ folder
# Source: API Intelligence Framework (7-phase discovery)
# ==============================================================================

class ZephyrIntelligence:
    """Zephyr API intelligence - schemas, dependencies, constraints."""

    # Schemas from intelligence/schemas/*.json
    SCHEMAS = {
        "cycle": {
            "entity": "cycle",
            "endpoint": "/cycle",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "environment": {
                                                            "type": "string"
                                            },
                                            "build": {
                                                            "type": "string"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "startDate": {
                                                            "type": "integer"
                                            },
                                            "endDate": {
                                                            "type": "integer"
                                            },
                                            "cycleStartDate": {
                                                            "type": "string"
                                            },
                                            "cycleEndDate": {
                                                            "type": "string"
                                            },
                                            "status": {
                                                            "type": "integer"
                                            },
                                            "revision": {
                                                            "type": "integer"
                                            },
                                            "releaseId": {
                                                            "type": "integer"
                                            },
                                            "cyclePhases": {
                                                            "type": "array"
                                            },
                                            "createdOn": {
                                                            "type": "integer"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "build",
                                            "createdOn",
                                            "cycleEndDate",
                                            "cyclePhases",
                                            "cycleStartDate",
                                            "endDate",
                                            "environment",
                                            "hasChild",
                                            "id",
                                            "name",
                                            "releaseId",
                                            "revision",
                                            "startDate",
                                            "status"
                            ]
            },
            "notes": 'Requires unlocked release. Use existing releases.'
        },
        "release": {
            "entity": "release",
            "endpoint": "/release",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "startDate": {
                                                            "type": "integer"
                                            },
                                            "releaseStartDate": {
                                                            "type": "string"
                                            },
                                            "createdDate": {
                                                            "type": "integer"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "orderId": {
                                                            "type": "integer"
                                            },
                                            "globalRelease": {
                                                            "type": "boolean"
                                            },
                                            "projectRelease": {
                                                            "type": "boolean"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            },
                                            "syncEnabled": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "createdDate",
                                            "description",
                                            "globalRelease",
                                            "hasChild",
                                            "id",
                                            "name",
                                            "orderId",
                                            "projectId",
                                            "projectRelease",
                                            "releaseStartDate",
                                            "startDate",
                                            "syncEnabled"
                            ]
            },
            "notes": 'BLOCKER-003: Locks for >60s after creation'
        },
        "requirement": {
            "entity": "requirement",
            "endpoint": "/requirementtree/add",
            "method": "POST",
            "status": '✅ Working (workaround)',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "parentId": {
                                                            "type": "integer"
                                            },
                                            "categories": {
                                                            "type": "array"
                                            },
                                            "requirements": {
                                                            "type": "array"
                                            },
                                            "lastModifiedOn": {
                                                            "type": "integer"
                                            },
                                            "releaseIds": {
                                                            "type": "array"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "categories",
                                            "description",
                                            "hasChild",
                                            "id",
                                            "lastModifiedOn",
                                            "name",
                                            "parentId",
                                            "projectId",
                                            "releaseIds",
                                            "requirements"
                            ]
            },
            "notes": 'BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.'
        },
        "requirement_folder": {
            "entity": "requirement_folder",
            "endpoint": "/requirementtree/add",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "categories": {
                                                            "type": "array"
                                            },
                                            "requirements": {
                                                            "type": "array"
                                            },
                                            "lastModifiedOn": {
                                                            "type": "integer"
                                            },
                                            "releaseIds": {
                                                            "type": "array"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "categories",
                                            "description",
                                            "hasChild",
                                            "id",
                                            "lastModifiedOn",
                                            "name",
                                            "projectId",
                                            "releaseIds",
                                            "requirements"
                            ]
            },
            "notes": 'Works perfectly'
        },
        "testcase_folder": {
            "entity": "testcase_folder",
            "endpoint": "/testcasetree",
            "method": "POST",
            "status": '❌ Broken',
            "schema": None,
            "notes": 'BLOCKER-002: API rejects valid payloads (HTTP 400)'
        },
    }

    # READ endpoints for production mode (GET endpoints for reading from project 44)
    # These are used by Prepare stage to build schema from production data
    READ_ENDPOINTS = {
        "project": {
            "endpoint": "/project",
            "method": "GET",
            "description": "Get all projects",
            "read_only": True,
            "project": 44  # Production project
        },
        "release": {
            "endpoint": "/release",
            "method": "GET",
            "description": "Get releases for a project",
            "read_only": True,
            "project": 44,  # Production project
            "query_params": ["projectId"],
            "example": "/release?projectId=44"
        },
        "cycle": {
            "endpoint": "/cycle/release/{releaseid}",
            "method": "GET",
            "description": "Get cycles for a release",
            "read_only": True,
            "project": 44,  # Production project
            "path_params": ["releaseid"],
            "depends_on": "release",  # Must fetch release first
            "example": "/cycle/release/123"
        },
        "execution": {
            "endpoint": "/execution",
            "method": "GET",
            "description": "Get executions (may require cycle/testcase filters)",
            "read_only": True,
            "project": 44,  # Production project
            "depends_on": ["cycle", "testcase"]
        },
        "requirement": {
            "endpoint": "/requirement",
            "method": "GET",
            "description": "Get requirements",
            "read_only": True,
            "project": 44  # Production project
        },
        "testcase": {
            "endpoint": "/testcase",
            "method": "GET",
            "description": "Get test cases",
            "read_only": True,
            "project": 44  # Production project
        }
    }

    # Dependencies from intelligence/dependencies.yaml
    DEPENDENCIES = {'project': {'depends_on': [], 'required_by': ['testcase_folder'], 'dependency_count': 0, 'dependent_count': 1}, 'release': {'depends_on': [], 'required_by': ['cycle'], 'dependency_count': 0, 'dependent_count': 1}, 'requirement_folder': {'depends_on': [], 'required_by': ['requirement'], 'dependency_count': 0, 'dependent_count': 1}, 'requirement': {'depends_on': ['requirement_folder'], 'required_by': [], 'dependency_count': 1, 'dependent_count': 0}, 'cycle': {'depends_on': ['release'], 'required_by': ['execution'], 'dependency_count': 1, 'dependent_count': 1}, 'testcase_folder': {'depends_on': ['project'], 'required_by': ['testcase'], 'dependency_count': 1, 'dependent_count': 1}, 'testcase': {'depends_on': ['testcase_folder'], 'required_by': ['allocation', 'execution'], 'dependency_count': 1, 'dependent_count': 2}, 'execution': {'depends_on': ['testcase', 'cycle'], 'required_by': [], 'dependency_count': 2, 'dependent_count': 0}, 'allocation': {'depends_on': ['testcase'], 'required_by': [], 'dependency_count': 1, 'dependent_count': 0}}

    # Constraints from intelligence/quirks.yaml
    CONSTRAINTS = {'blockers': [{'id': 'BLOCKER-001', 'title': 'Requirement Creation API Broken', 'severity': 'critical', 'entity': 'requirement', 'endpoint': 'POST /requirement', 'issue': "Returns HTTP 500: 'Cannot invoke java.lang.Long.longValue() because id is null'", 'impact': 'Cannot create requirements via documented API', 'workaround': {'method': 'Use POST /requirementtree/add with parentId', 'status': '✅ Working', 'notes': 'Must create requirement_folder first, then use parentId'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}, {'id': 'BLOCKER-002', 'title': 'Testcase Folder API Broken', 'severity': 'critical', 'entity': 'testcase_folder', 'endpoint': 'POST /testcasetree', 'issue': "Returns HTTP 400: 'For input string: null'", 'impact': 'Cannot create testcase folders, blocks all testcase/execution/allocation creation', 'workaround': {'method': 'Manual creation in UI required', 'status': '⚠️ Manual only', 'notes': 'Tried 4 variations (omit parentId, parentId: null, parentId: 0, no parentId field) - all failed'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08', 'blocks': ['testcase', 'execution', 'allocation']}, {'id': 'BLOCKER-003', 'title': 'Release Lock Duration >60 Seconds', 'severity': 'high', 'entity': 'release', 'endpoint': 'POST /release', 'issue': 'Newly created releases are locked for >60 seconds, preventing cycle creation', 'impact': 'Cannot create cycles immediately after release creation', 'workaround': {'method': 'Use existing (old) releases for cycle creation', 'status': '✅ Working', 'notes': 'Tested 15s, 30s, 60s delays - all failed. Old releases work immediately.'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}], 'bugs': [{'id': 'BUG-007', 'title': 'Release GET by ID Returns HTTP 403', 'severity': 'medium', 'entity': 'release', 'endpoint': 'GET /release/{id}', 'issue': 'Returns HTTP 403 Forbidden even with valid API token', 'impact': 'Cannot validate release creation via GET', 'workaround': {'method': 'Skip GET validation for releases', 'status': '✅ Working', 'notes': 'Assume creation succeeded if POST returns 200/201'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}], 'quirks': [{'id': 'QUIRK-001', 'title': 'Requirement Names Must Be Unique Across All Runs', 'severity': 'low', 'entity': 'requirement', 'issue': 'API rejects duplicate requirement names even across different test runs', 'impact': 'Must use timestamps or UUIDs in requirement names', 'workaround': {'method': 'Include timestamp in requirement name', 'status': '✅ Working', 'notes': "Use datetime.now().strftime('%Y%m%d%H%M%S') in name"}, 'date_discovered': '2025-12-08'}, {'id': 'QUIRK-002', 'title': 'Cycle Creation Requires Unlocked Release', 'severity': 'medium', 'entity': 'cycle', 'issue': 'Cannot create cycle with newly created release (locked)', 'impact': 'Must use existing releases or wait >60s', 'workaround': {'method': 'Query for existing releases and use oldest one', 'status': '✅ Working', 'notes': 'Oldest releases are most likely unlocked'}, 'date_discovered': '2025-12-08'}, {'id': 'QUIRK-003', 'title': 'Testcase Requires tcrCatalogTreeId (Folder ID)', 'severity': 'medium', 'entity': 'testcase', 'issue': 'Cannot create testcase without tcrCatalogTreeId', 'impact': 'Blocked by BLOCKER-002 (folder creation broken)', 'workaround': {'method': 'None - depends on folder API fix', 'status': '❌ Blocked', 'notes': 'Must fix folder API first'}, 'date_discovered': '2025-12-08'}], 'api_inconsistencies': [{'id': 'INCONSISTENCY-001', 'title': 'Requirement Creation Uses Folder Endpoint', 'entity': 'requirement', 'issue': 'POST /requirement is broken, must use POST /requirementtree/add', 'notes': 'Folder and requirement creation use same endpoint, differentiated by parentId presence'}, {'id': 'INCONSISTENCY-002', 'title': 'Date Format Inconsistency', 'entity': 'multiple', 'issue': "Some endpoints accept 'YYYY-MM-DD', others require epoch milliseconds", 'examples': {'release': "Accepts 'YYYY-MM-DD' string", 'cycle': 'Requires epoch milliseconds (int)'}, 'notes': 'No consistent date format across API'}], 'undocumented_behavior': [{'id': 'UNDOCUMENTED-001', 'title': 'Release Lock Mechanism', 'entity': 'release', 'behavior': 'Releases are locked after creation for >60 seconds', 'notes': 'Not mentioned in API documentation'}, {'id': 'UNDOCUMENTED-002', 'title': 'Folder API parentId Rejection', 'entity': 'testcase_folder', 'behavior': "API rejects parentId: null despite documentation suggesting it's valid for root folders", 'notes': "Documentation doesn't clarify how to create root folders"}]}

    @classmethod
    def get_schema(cls, entity: str):
        """Get schema for an entity."""
        return cls.SCHEMAS.get(entity)

    @classmethod
    def get_dependencies(cls, entity: str):
        """Get dependencies for an entity."""
        return cls.DEPENDENCIES.get(entity, {})

    @classmethod
    def get_creation_order(cls):
        """Get entities in dependency order."""
        # Based on topological sort from intelligence/creation-order.yaml
        return ['project', 'release', 'requirement_folder', 'testcase_folder', 'cycle', 'requirement', 'testcase', 'allocation', 'execution']

    @classmethod
    def get_all_constraints(cls):
        """Get all constraints (blockers, bugs, quirks)."""
        return cls.CONSTRAINTS
    
    @classmethod
    def get_read_endpoint(cls, entity: str):
        """Get READ endpoint for an entity (production mode - GET endpoints)."""
        return cls.READ_ENDPOINTS.get(entity)
    
    @classmethod
    def get_read_endpoint_path(cls, entity: str, **params):
        """Get READ endpoint path with parameters filled in."""
        endpoint_info = cls.READ_ENDPOINTS.get(entity)
        if not endpoint_info:
            return None
        
        path = endpoint_info["endpoint"]
        
        # Fill path parameters (e.g., {releaseid} → actual release ID)
        if "path_params" in endpoint_info:
            for param in endpoint_info["path_params"]:
                if param in params:
                    path = path.replace(f"{{{param}}}", str(params[param]))
        
        # Add query parameters
        if "query_params" in endpoint_info and params:
            query_parts = []
            for param in endpoint_info["query_params"]:
                if param in params:
                    query_parts.append(f"{param}={params[param]}")
            if query_parts:
                path += "?" + "&".join(query_parts)
        
        return path

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
