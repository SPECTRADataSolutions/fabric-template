"""
Zephyr Endpoint Catalog - Auto-generated from endpoints.json

Total: 224 endpoints
Generated: 2025-12-08T14:22:12.704080
"""

ENDPOINTS_CATALOG = [
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
    "resource": "Get All Preferences - Admin [/admin/preference/admin]"
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
    "resource": "Get All Applications  [/admin/app]"
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
    "resource": "Get list of values [/admin/preference/lov/all]"
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
    "resource": "Get All Preferences  [/admin/preference/all]"
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
    "resource": "Get Anonymous Preferences  [/admin/preference/anonymous]"
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
    "resource": "Get Daily Back-up Schedule [/admin/backup/schedule]"
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
    "resource": "Get All user preferences  [/admin/ldap/default/settings]"
  },
  {
    "endpoint_path": "/admin/preference",
    "full_path": "/admin/preference{?key}",
    "http_method": "GET",
    "category": "admin",
    "description": "Get Preference by key",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "key"
    ],
    "path_parameters": [],
    "resource": "Get Preference by key [/admin/preference{?key}]"
  },
  {
    "endpoint_path": "/admin/preference/item/usage",
    "full_path": "/admin/preference/item/usage{?preferencename}{?value}{?id}",
    "http_method": "GET",
    "category": "admin",
    "description": "Get Preference Item Usage",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "preferencename",
      "value",
      "id"
    ],
    "path_parameters": [],
    "resource": "Get Preference Item Usage [/admin/preference/item/usage{?preferencename}{?value}{?id}]"
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
    "resource": "Get All user preferences  [/admin/user/preference]"
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
    "resource": "Update a given Preference [/admin/preference]"
  },
  {
    "endpoint_path": "/assignmenttree",
    "full_path": "/assignmenttree/{cyclephaseid}/bulk/tree/{treeid}/from/{fromid}/to/{toid}{?cascade}{?easmode}",
    "http_method": "PUT",
    "category": "other",
    "description": "Change multiple assignments",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "cascade",
      "easmode"
    ],
    "path_parameters": [
      "cyclephaseid",
      "treeid",
      "fromid",
      "toid"
    ],
    "resource": "Change multiple assignments [/assignmenttree/{cyclephaseid}/bulk/tree/{treeid}/from/{fromid}/to/{toid}{?cascade}{?easmode}]"
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
      "isCreateWithLatestVersion"
    ],
    "path_parameters": [
      "cyclephaseid"
    ],
    "resource": "Create free form release testschedule [/assignmenttree/{cyclephaseid}/assign/byschedule{?maxresults}{?scheduleids}{?maintainassignments}{?parenttreeid}{?includehierarchy}{?isCreateWithLatestVersion}]"
  },
  {
    "endpoint_path": "/assignmenttree",
    "full_path": "/assignmenttree/{cyclephaseid}/assign/bytree/{parenttreeid}{?includehierarchy}{?dtoResponse}",
    "http_method": "POST",
    "category": "other",
    "description": "Create freeForm testcase",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "includehierarchy",
      "dtoResponse"
    ],
    "path_parameters": [
      "cyclephaseid",
      "parenttreeid"
    ],
    "resource": "Create freeForm testcase [/assignmenttree/{cyclephaseid}/assign/bytree/{parenttreeid}{?includehierarchy}{?dtoResponse}]"
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
      "includehierarchy"
    ],
    "path_parameters": [
      "cyclephaseid",
      "parenttreeid"
    ],
    "resource": "Create testcase free form using search [/assignmenttree/{cyclephaseid}/assign/bysearch/{parenttreeid}{?searchquery}{?maxresults}{?testcaseid}{?zql}{?activeprojectid}{?includehierarchy}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Get Attachment Details by id [/attachment/{id}]"
  },
  {
    "endpoint_path": "/attachment",
    "full_path": "/attachment{?itemid}{?type}{?isLink}",
    "http_method": "GET",
    "category": "attachments",
    "description": "Get attachment details",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "itemid",
      "type",
      "isLink"
    ],
    "path_parameters": [],
    "resource": "Get attachment details [/attachment{?itemid}{?type}{?isLink}]"
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
    "resource": "Delete job using job id [/automation/job/delete]"
  },
  {
    "endpoint_path": "/automation/schedule",
    "full_path": "/automation/schedule{?schedulejobid}",
    "http_method": "GET",
    "category": "automation",
    "description": "get Scheduled job via scheduled job id",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "schedulejobid"
    ],
    "path_parameters": [],
    "resource": "get Scheduled job via scheduled job id [/automation/schedule{?schedulejobid}]"
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
    "resource": "Configure new Job [/automation/job/detail]"
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
    "path_parameters": [
      "scheduleId"
    ],
    "resource": "Cancel job by id [/upload-file/automation/cancel/{scheduleId}]"
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
    "resource": "Create/execute a job [/upload-file/automation/create-and-execute-job]"
  },
  {
    "endpoint_path": "/upload-file/automation/schedule/get-latest-job-progress",
    "full_path": "/upload-file/automation/schedule/get-latest-job-progress{?jobid}",
    "http_method": "GET",
    "category": "automation",
    "description": "Get latest Scheduled Automation Job Progress",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "jobid"
    ],
    "path_parameters": [],
    "resource": "Get latest Scheduled Automation Job Progress  [/upload-file/automation/schedule/get-latest-job-progress{?jobid}]"
  },
  {
    "endpoint_path": "/upload-file/automation/file-upload-job/list",
    "full_path": "/upload-file/automation/file-upload-job/list{?releaseId}{?projectId}",
    "http_method": "GET",
    "category": "automation",
    "description": "All scheduled jobs by project id and release id",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "releaseId",
      "projectId"
    ],
    "path_parameters": [],
    "resource": "All scheduled jobs by project id and release id  [/upload-file/automation/file-upload-job/list{?releaseId}{?projectId}]"
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
    "resource": "Create new Job [/upload-file/automation/create-job-detail]"
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
    "resource": "Schedule/execute job for File Upload [/upload-file/automation/execute-job]"
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
    "resource": "Update/execute a job [/upload-file/automation/update-execute-job]"
  },
  {
    "endpoint_path": "/cycle/assignments",
    "full_path": "/cycle/assignments/{releaseid}{?allexecutions}",
    "http_method": "GET",
    "category": "cycles",
    "description": "Calculate assignments for release",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "allexecutions"
    ],
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Calculate assignments for release [/cycle/assignments/{releaseid}{?allexecutions}]"
  },
  {
    "endpoint_path": "/cycle/clone",
    "full_path": "/cycle/clone/{cycleid}{?deep}{?copyassignments}",
    "http_method": "POST",
    "category": "cycles",
    "description": "Clone a Cycle",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "deep",
      "copyassignments"
    ],
    "path_parameters": [
      "cycleid"
    ],
    "resource": "Clone a Cycle  [/cycle/clone/{cycleid}{?deep}{?copyassignments}]"
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
    "path_parameters": [
      "cyclephaseid"
    ],
    "resource": "Clone a CyclePhase [/cycle/cyclephase/clone/{cyclephaseid}]"
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
    "path_parameters": [
      "sourcecyclephaseid",
      "targetcycleid"
    ],
    "resource": "copy a CyclePhase [/cycle/copy/{sourcecyclephaseid}/to/{targetcycleid}]"
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
    "resource": "Create a New Cycle [/cycle/]"
  },
  {
    "endpoint_path": "/cycle",
    "full_path": "/cycle/{cycleid}/phase{?scheduleId}",
    "http_method": "POST",
    "category": "cycles",
    "description": "Create Cycle Phase",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "scheduleId"
    ],
    "path_parameters": [
      "cycleid"
    ],
    "resource": "Create Cycle Phase [/cycle/{cycleid}/phase{?scheduleId}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Delete Cycle [/cycle/{id}]"
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
    "path_parameters": [
      "cycleid",
      "cyclephaseid"
    ],
    "resource": "Delete Cycle Phase [/cycle/{cycleid}/phase/{cyclephaseid}]"
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
    "path_parameters": [
      "cycleid"
    ],
    "resource": "Get Cycle by ID [/cycle/{cycleid}]"
  },
  {
    "endpoint_path": "/cycle/cycleName",
    "full_path": "/cycle/cycleName/{releaseid}{?orderBy}{?cycleName}",
    "http_method": "GET",
    "category": "cycles",
    "description": "Get Cycle names for release",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "orderBy",
      "cycleName"
    ],
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Get Cycle names for release [/cycle/cycleName/{releaseid}{?orderBy}{?cycleName}]"
  },
  {
    "endpoint_path": "/cycle/phase/name",
    "full_path": "/cycle/phase/name{?ids}",
    "http_method": "GET",
    "category": "cycles",
    "description": "Get all cyclePhase Names",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "ids"
    ],
    "path_parameters": [],
    "resource": "Get all cyclePhase Names [/cycle/phase/name{?ids}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Get Cycle for release [/cycle/release/{releaseid}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "get status count for releaseid [/cycle/status/count/{releaseid}]"
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
    "path_parameters": [
      "sourcecyclephaseid",
      "targetcycleid"
    ],
    "resource": "Move a CyclePhase [/cycle/move/{sourcecyclephaseid}/to/{targetcycleid}]"
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
    "path_parameters": [
      "cycleId",
      "value"
    ],
    "resource": "get status count for releaseid [/cycle/toggle/{cycleId}/{value}]"
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
    "path_parameters": [
      "cycleId"
    ],
    "resource": "Update a Cycle [/cycle/{cycleId}]"
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
    "path_parameters": [
      "cycleid"
    ],
    "resource": "Update Cycle Phase [/cycle/{cycleid}/phase]"
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
    "resource": "Save defect schedule [/defectmapping/]"
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
    "resource": "Create defect in the system. [/defect/]"
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
    "path_parameters": [
      "defectId",
      "projectId"
    ],
    "resource": "Get defect by ID [/defect/{defectId}?projectId={projectId}]"
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
      "pagesize"
    ],
    "path_parameters": [],
    "resource": "Get Testcase usage history details [//executionchangehistory{?releaseTestScheduleId}{?isascorder}{?offset}{?pagesize}]"
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
    "resource": "Assign/Reassign schedules values [/execution/assign]"
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
      "includeanyoneuser"
    ],
    "path_parameters": [],
    "resource": "Execute testcases [/execution/bulk{?scheduleids}{?status}{?testerid}{?tcrCatalogTreeId}{?allExecutions}{?includeanyoneuser}]"
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
    "resource": "Create schedules values [/execution/]"
  },
  {
    "endpoint_path": "/execution",
    "full_path": "/execution{?ids}",
    "http_method": "DELETE",
    "category": "executions",
    "description": "Delete / Unassign test schedules",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "ids"
    ],
    "path_parameters": [],
    "resource": "Delete / Unassign test schedules [/execution{?ids}]"
  },
  {
    "endpoint_path": "/execution",
    "full_path": "/execution/{cyclephaseid}/testcase{?testcaseids}{?tcrCatalogTreeId}{?filterTcName}",
    "http_method": "DELETE",
    "category": "executions",
    "description": "Delete / Unassign frozen test cases and schedules",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "testcaseids",
      "tcrCatalogTreeId",
      "filterTcName"
    ],
    "path_parameters": [
      "cyclephaseid"
    ],
    "resource": "Delete / Unassign frozen test cases and schedules [/execution/{cyclephaseid}/testcase{?testcaseids}{?tcrCatalogTreeId}{?filterTcName}]"
  },
  {
    "endpoint_path": "/execution/path",
    "full_path": "/execution/path{?scheduleid}{?assigneeuserid}",
    "http_method": "GET",
    "category": "executions",
    "description": "Get node path",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "scheduleid",
      "assigneeuserid"
    ],
    "path_parameters": [],
    "resource": "Get node path [/execution/path{?scheduleid}{?assigneeuserid}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "To get Schedule by ID [/execution/{id}]"
  },
  {
    "endpoint_path": "/execution/ids",
    "full_path": "/execution/ids{?ids}",
    "http_method": "GET",
    "category": "executions",
    "description": "To schedule by schedule IDs",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "ids"
    ],
    "path_parameters": [],
    "resource": "To schedule by schedule IDs [/execution/ids{?ids}]"
  },
  {
    "endpoint_path": "/execution/expanded",
    "full_path": "/execution/expanded{?ids}{?stepresults}{?resulthistory}",
    "http_method": "GET",
    "category": "executions",
    "description": "To schedule by schedule ids",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "ids",
      "stepresults",
      "resulthistory"
    ],
    "path_parameters": [],
    "resource": "To schedule by schedule ids [/execution/expanded{?ids}{?stepresults}{?resulthistory}]"
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
      "pagesize"
    ],
    "path_parameters": [],
    "resource": "Get Schedules by Criteria [/execution/user/project{?projectid}{?createdby}{?testerid}{?parentid}{?cyclephaseid}{?releaseid}{?order}{?orderByAsc}{?offset}{?pagesize}]"
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
      "is_cfield"
    ],
    "path_parameters": [],
    "resource": "Get Schedules by Criteria [/execution{?testerid}{?parentid}{?cyclephaseid}{?releaseid}{?order}{?isascorder}{?offset}{?includeanyoneuser}{?pagesize}{?is_cfield}]"
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
      "pagesize"
    ],
    "path_parameters": [],
    "resource": "Get Teststep results by IDs [/execution/byfilter{?testcaseid}{?releaseid}{?rtsid}{?order}{?isascorder}{?offset}{?pagesize}]"
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
    "resource": "Modify schedules values [/execution/modify]"
  },
  {
    "endpoint_path": "/execution/statusandattachment",
    "full_path": "/execution/statusandattachment/{id}{?status}",
    "http_method": "PUT",
    "category": "executions",
    "description": "To update execution details, attachment and status",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "status"
    ],
    "path_parameters": [
      "id"
    ],
    "resource": "To update execution details, attachment and status [/execution/statusandattachment/{id}{?status}]"
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
      "includeanyoneuser"
    ],
    "path_parameters": [
      "id"
    ],
    "resource": "To update execution details [/execution/{id}{?status}{?testerid}{?time}{?allExecutions}{?includeanyoneuser}]"
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
    "resource": "Update Schedules Values [/execution]"
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
    "resource": "Update Test Execution Status [/execution/updateteststatus]"
  },
  {
    "endpoint_path": "/externalrequirement/importall",
    "full_path": "/externalrequirement/importall{?projectId}",
    "http_method": "POST",
    "category": "other",
    "description": "Import External Requirement Based on Filter or JQL",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "projectId"
    ],
    "path_parameters": [],
    "resource": "Import External Requirement Based on Filter or JQL [/externalrequirement/importall{?projectId}]"
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
    "resource": "Import groups and users from the list [/externalGroup/importGroupsAndUsers]"
  },
  {
    "endpoint_path": "/externalGroup/search",
    "full_path": "/externalGroup/search{?name}{?pagesize}",
    "http_method": "GET",
    "category": "other",
    "description": "Search groups in LDAP or crowd",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "name",
      "pagesize"
    ],
    "path_parameters": [],
    "resource": "Search groups in LDAP or crowd [/externalGroup/search{?name}{?pagesize}]"
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
    "resource": "Sync groups and users from the list [/externalGroup/sync]"
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
    "resource": "Add Custom Field [/field/]"
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
    "resource": "Get all the field's type metadata. [/field/fieldtype]"
  },
  {
    "endpoint_path": "/field/metadata",
    "full_path": "/field/metadata{?visible}",
    "http_method": "GET",
    "category": "fields",
    "description": "Get customfield metadata",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "visible"
    ],
    "path_parameters": [],
    "resource": "Get customfield metadata  [/field/metadata{?visible}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Get Field by Id [/field/{id}]"
  },
  {
    "endpoint_path": "/field/name",
    "full_path": "/field/name{?name}{?projectid}",
    "http_method": "GET",
    "category": "fields",
    "description": "Get Field by dispaly name",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "name",
      "projectid"
    ],
    "path_parameters": [],
    "resource": "Get Field by dispaly name [/field/name{?name}{?projectid}]"
  },
  {
    "endpoint_path": "/field",
    "full_path": "/field{?name}",
    "http_method": "GET",
    "category": "fields",
    "description": "Get Field by fieldName",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "name"
    ],
    "path_parameters": [],
    "resource": "Get Field by fieldName [/field{?name}]"
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
    "path_parameters": [
      "entityName"
    ],
    "resource": "Get Importable Fields By Entity  [/field/importfields/{entityName}]"
  },
  {
    "endpoint_path": "/field/ids",
    "full_path": "/field/ids{?ids}",
    "http_method": "GET",
    "category": "fields",
    "description": "Get list of CustomFields",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "ids"
    ],
    "path_parameters": [],
    "resource": "Get list of CustomFields [/field/ids{?ids}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Get list of project specific CustomFields [/field/project/{id}]"
  },
  {
    "endpoint_path": "/field/entity",
    "full_path": "/field/entity/{entityname}{?includsystemfield}",
    "http_method": "GET",
    "category": "fields",
    "description": "Get fields by entity",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "includsystemfield"
    ],
    "path_parameters": [
      "entityname"
    ],
    "resource": "Get fields by entity [/field/entity/{entityname}{?includsystemfield}]"
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
    "resource": "Update Cascade [/field/cascade]"
  },
  {
    "endpoint_path": "/field/validate",
    "full_path": "/field/validate{?id}{?entityname}{?searchfieldname}",
    "http_method": "GET",
    "category": "fields",
    "description": "Validating field in the system.",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "id",
      "entityname",
      "searchfieldname"
    ],
    "path_parameters": [],
    "resource": "Validating field in the system. [/field/validate{?id}{?entityname}{?searchfieldname}]"
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
    "resource": "create field map  [/fieldmap/]"
  },
  {
    "endpoint_path": "/fileWatcher/watcher",
    "full_path": "/fileWatcher/watcher{?schedulejobid}",
    "http_method": "GET",
    "category": "other",
    "description": "get Scheduled job via scheduled job id",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "schedulejobid"
    ],
    "path_parameters": [],
    "resource": "get Scheduled job via scheduled job id [/fileWatcher/watcher{?schedulejobid}]"
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
    "resource": "Schedule job for ZBlast [/fileWatcher/watcher]"
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
    "path_parameters": [
      "dashboardId"
    ],
    "resource": "Get all requirement node and requirement name by release id [/gadget/{dashboardId}]"
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
    "resource": "Get All projects that allowed access to current global reporsitory user [/global-repository/project]"
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
    "resource": "Create group in the System [/group/]"
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
    "resource": "Update group in the System [/group]"
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
    "resource": "Add new import job [/import/]"
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
    "path_parameters": [
      "id",
      "action"
    ],
    "resource": "Execute import job by id [/import/execute/{id}/{action}]"
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
    "resource": "Get License Information. [/info/license]"
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
    "resource": "Get License Information [/license/]"
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
    "resource": "Create Template  [/parsertemplate/]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Delete Template  [/parsertemplate/{id}]"
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
    "path_parameters": [
      "TemplateId"
    ],
    "resource": "Get Template  [/parsertemplate/{TemplateId}]"
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
    "resource": "Get List of Templates  [/parsertemplate]"
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
    "path_parameters": [
      "templateId"
    ],
    "resource": "Update Template  [/parsertemplate/{templateId}]"
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
    "resource": "Create Project [/project/]"
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
    "resource": "Get All Normal Project Details [/project/details]"
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
    "resource": "Get All Normal project [/project/normal]"
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
    "resource": "Get lead for all projects [/project/all/leads]"
  },
  {
    "endpoint_path": "/project",
    "full_path": "/project/{id}{?isLite}",
    "http_method": "GET",
    "category": "projects",
    "description": "Get Project by ID",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "isLite"
    ],
    "path_parameters": [
      "id"
    ],
    "resource": "Get Project by ID [/project/{id}{?isLite}]"
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
    "path_parameters": [
      "UserID"
    ],
    "resource": "Get Project by User ID [/project/user/{UserID}?isLite=False&adminUser=False]"
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
    "path_parameters": [
      "UserID"
    ],
    "resource": "Get allocated Projects [/project/project/{UserID}]"
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
    "resource": "Get Project Team Count for all projects [/project/count/allprojects]"
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
    "resource": "Get Project Team Count for all users [/project/count/allusers]"
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
    "resource": "Get Project Team  for Allocated Projects [/project/allocated/projects]"
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
    "path_parameters": [
      "pid"
    ],
    "resource": "Get Project team for project [/project/projectteam/{pid}]"
  },
  {
    "endpoint_path": "/project",
    "full_path": "/project{?userId}{?isLite}",
    "http_method": "GET",
    "category": "projects",
    "description": "Get All projects by UserId",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "userId",
      "isLite"
    ],
    "path_parameters": [],
    "resource": "Get All projects by UserId [/project{?userId}{?isLite}]"
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
    "resource": "Get All projects  [/project/lite]"
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
    "resource": "Get All Shared projects  [/project/shared]"
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
    "path_parameters": [
      "projectid"
    ],
    "resource": "Get Shared projects  [/project/sharedprojects/{projectid}]"
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
    "path_parameters": [
      "projectid"
    ],
    "resource": "Get Shared projects shared to given project [/project/sharedtoprojects/{projectid}]"
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
    "resource": "Assign User to the Project [/project]"
  },
  {
    "endpoint_path": "/project",
    "full_path": "/project/{projectId}/migrate{?externalStorageId}",
    "http_method": "POST",
    "category": "projects",
    "description": "Project storage migration",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "externalStorageId"
    ],
    "path_parameters": [
      "projectId"
    ],
    "resource": "Project storage migration [/project/{projectId}/migrate{?externalStorageId}]"
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
    "path_parameters": [
      "projectId"
    ],
    "resource": "Retry failed attachment migration [/project/{projectId}/migration/retry]"
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
    "resource": "Create New Release [/release/]"
  },
  {
    "endpoint_path": "/release/paged/project",
    "full_path": "/release/paged/project/{projectid}{?pagesize}{?offset}{?order}{?isascorder}{?isVisible}",
    "http_method": "GET",
    "category": "releases",
    "description": "Get releases for a project through page and offset",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "pagesize",
      "offset",
      "order",
      "isascorder",
      "isVisible"
    ],
    "path_parameters": [
      "projectid"
    ],
    "resource": "Get releases for a project through page and offset [/release/paged/project/{projectid}{?pagesize}{?offset}{?order}{?isascorder}{?isVisible}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Get Release by Release ID [/release/{releaseid}]"
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
    "resource": "Get all releases for all projects with Access [/release]"
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
    "path_parameters": [
      "projectid"
    ],
    "resource": "Get releases for a project [/release/project/{projectid}]"
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
    "resource": "Create new requirement [/requirement/]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Update Requirement [/requirement/{id}]"
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
    "resource": "Bulk Update Requirement [/requirement/bulk]"
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
    "resource": "Create new requirement tree [/requirementtree/add/]"
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
    "resource": "Add role [/role/]"
  },
  {
    "endpoint_path": "/role/permission",
    "full_path": "/role/permission{?roleid}",
    "http_method": "PUT",
    "category": "roles",
    "description": "Save or assign role permissions",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "roleid"
    ],
    "path_parameters": [],
    "resource": "Save or assign role permissions [/role/permission{?roleid}]"
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
    "path_parameters": [
      "pid"
    ],
    "resource": "Reindex specific project by id [/advancesearch/reindex/{pid}]"
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
    "resource": "Search via filters [/advancesearch/]"
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
    "resource": "Search via filters [/advancesearch/zql]"
  },
  {
    "endpoint_path": "/advancesearch/testexecutions",
    "full_path": "/advancesearch/testexecutions/{altid}{?maxresults}",
    "http_method": "GET",
    "category": "search",
    "description": "Search test executions for given altId",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "maxresults"
    ],
    "path_parameters": [
      "altid"
    ],
    "resource": "Search test executions for given altId [/advancesearch/testexecutions/{altid}{?maxresults}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Search and Edit the Testcase [/testcase/search/update/bulk?releaseId={releaseid}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Search and Edit the Testcase [/testcase/search/update/bulk?releaseId={releaseid}]"
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
    "resource": "Search and Map the Testcase [POST]"
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
    "resource": "Check Indexing Health [/advancesearch/reindex/health]"
  },
  {
    "endpoint_path": "/system/info/cache/clear",
    "full_path": "/system/info/cache/clear{?clearall}{?cachename}",
    "http_method": "POST",
    "category": "system",
    "description": "Clear the Specified Cache",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "clearall",
      "cachename"
    ],
    "path_parameters": [],
    "resource": "Clear the Specified Cache [/system/info/cache/clear{?clearall}{?cachename}]"
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
    "resource": "Download Zbot [/system/info/downloadzbot]"
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
    "resource": "Get All list of Caches [/system/info/cache/info]"
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
    "resource": "Get Channel Information [/system/info/channelinfo]"
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
    "resource": "Get License Information [/system/info/license]"
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
    "resource": "Get License Information [/system/info/servertime]"
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
    "resource": "Get License Information [/system/info/stats]"
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
    "resource": "Get License Detail Information [/license/detail]"
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
    "path_parameters": [
      "licensetype"
    ],
    "resource": "License Peak Usage Detail [/license/peak/detail?licensetype={licensetype}]"
  },
  {
    "endpoint_path": "/execution/teststepresult/bytctid",
    "full_path": "/execution/teststepresult/bytctid{?tctid}",
    "http_method": "GET",
    "category": "executions",
    "description": "Get teststep results by ID's",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "tctid"
    ],
    "path_parameters": [],
    "resource": "Get teststep results by ID's [/execution/teststepresult/bytctid{?tctid}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Get Test Step Result [/execution/teststepresult/{id}]"
  },
  {
    "endpoint_path": "/execution/teststepresult",
    "full_path": "/execution/teststepresult{?sids}{?cyclephaseid}",
    "http_method": "GET",
    "category": "executions",
    "description": "Get test step results by criteria",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "sids",
      "cyclephaseid"
    ],
    "path_parameters": [],
    "resource": "Get test step results by criteria [/execution/teststepresult{?sids}{?cyclephaseid}]"
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
    "resource": "Save or Update Test step result [/execution/teststepresult/saveorupdate]"
  },
  {
    "endpoint_path": "/testcase/allocate/requirement",
    "full_path": "/testcase/allocate/requirement/{testcaseid}{?releaseid}",
    "http_method": "POST",
    "category": "testcases",
    "description": "Allocate Requirements to testcase Id",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "releaseid"
    ],
    "path_parameters": [
      "testcaseid"
    ],
    "resource": "Allocate Requirements to testcase Id  [/testcase/allocate/requirement/{testcaseid}{?releaseid}]"
  },
  {
    "endpoint_path": "/testcase/allocate/requirement",
    "full_path": "/testcase/allocate/requirement{?releaseid}{?tcrCatalogTreeId}",
    "http_method": "POST",
    "category": "testcases",
    "description": "Allocate Requirements to testcase Ids",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "releaseid",
      "tcrCatalogTreeId"
    ],
    "path_parameters": [],
    "resource": "Allocate Requirements to testcase Ids  [/testcase/allocate/requirement{?releaseid}{?tcrCatalogTreeId}]"
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
      "testcaseid"
    ],
    "path_parameters": [],
    "resource": "Bulk Update Testcase values [/testcase/bulk{?externalid}{?priority}{?tag}{?comments}{?scriptpath}{?scriptid}{?scriptname}{?automated}{?estimatedtime}{?testcaseid}]"
  },
  {
    "endpoint_path": "/testcase/update/bulk",
    "full_path": "/testcase/update/bulk{?tcrCatalogTreeId}",
    "http_method": "PUT",
    "category": "testcases",
    "description": "Bulk Update Testcase values",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "tcrCatalogTreeId"
    ],
    "path_parameters": [],
    "resource": "Bulk Update Testcase values [/testcase/update/bulk{?tcrCatalogTreeId}]"
  },
  {
    "endpoint_path": "/testcase/clone/on",
    "full_path": "/testcase/clone/on/{releaseid}/to/{targettreeid}{?sourceitemids}{?link}{?cloneAllDetails}",
    "http_method": "POST",
    "category": "testcases",
    "description": "Clone Testcase",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "sourceitemids",
      "link",
      "cloneAllDetails"
    ],
    "path_parameters": [
      "releaseid",
      "targettreeid"
    ],
    "resource": "Clone Testcase [/testcase/clone/on/{releaseid}/to/{targettreeid}{?sourceitemids}{?link}{?cloneAllDetails}]"
  },
  {
    "endpoint_path": "/testcase/bulk",
    "full_path": "/testcase/bulk{?scheduleId}{?nobulkcommit}",
    "http_method": "POST",
    "category": "testcases",
    "description": "Create bulk Testcase",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "scheduleId",
      "nobulkcommit"
    ],
    "path_parameters": [],
    "resource": "Create bulk Testcase [/testcase/bulk{?scheduleId}{?nobulkcommit}]"
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
    "resource": "Create Testcase [/testcase/]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "create new version of testcase [/testcase/createnewversion/{id}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Delete Testcase  [/testcase/{id}]"
  },
  {
    "endpoint_path": "/testcase",
    "full_path": "/testcase{?tcrCatalogTreeId}",
    "http_method": "DELETE",
    "category": "testcases",
    "description": "Delete Multiple Testcase Tree Linkage",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "tcrCatalogTreeId"
    ],
    "path_parameters": [],
    "resource": "Delete Multiple Testcase Tree Linkage [/testcase{?tcrCatalogTreeId}]"
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
    "path_parameters": [
      "testcaseid"
    ],
    "resource": "Get Requirement Summary by Testcase ID [/testcase/requirement/{testcaseid}]"
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
    "resource": "Get all tags [/testcase/tags]"
  },
  {
    "endpoint_path": "/testcase/tags",
    "full_path": "/testcase/tags/{releaseid}{?fetchall}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get all tags",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "fetchall"
    ],
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Get all tags [/testcase/tags/{releaseid}{?fetchall}]"
  },
  {
    "endpoint_path": "/testcase/name",
    "full_path": "/testcase/name{?tcid}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get all Testcase Names by Testcase IDs",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "tcid"
    ],
    "path_parameters": [],
    "resource": "Get all Testcase Names by Testcase IDs [/testcase/name{?tcid}]"
  },
  {
    "endpoint_path": "/testcase/count",
    "full_path": "/testcase/count{?tcrcatalogtreeid}{?releaseid}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Count Of Testcases By Phase",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "tcrcatalogtreeid",
      "releaseid"
    ],
    "path_parameters": [],
    "resource": "Get Count Of Testcases By Phase [/testcase/count{?tcrcatalogtreeid}{?releaseid}]"
  },
  {
    "endpoint_path": "/testcase/count/ids",
    "full_path": "/testcase/count/ids{?treeids}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Count Of Testcases By Phase ids.",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "treeids"
    ],
    "path_parameters": [],
    "resource": "Get Count Of Testcases By Phase ids. [/testcase/count/ids{?treeids}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Get Count Of Testcases By Phase ids. [/testcase/count/{releaseid}]"
  },
  {
    "endpoint_path": "/testcase/cumulative",
    "full_path": "/testcase/cumulative{?releaseid}{?requirementid}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Cumulative Testcase by Release ID and Requirement ID.",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "releaseid",
      "requirementid"
    ],
    "path_parameters": [],
    "resource": "Cumulative Testcase by Release ID and Requirement ID. [/testcase/cumulative{?releaseid}{?requirementid}]"
  },
  {
    "endpoint_path": "/testcase/cumulative/data",
    "full_path": "/testcase/cumulative/data{?releaseid}{?requirementid}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Cumulative Testcase by Release ID and Requirement ID.",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "releaseid",
      "requirementid"
    ],
    "path_parameters": [],
    "resource": "Get Cumulative Testcase by Release ID and Requirement ID. [/testcase/cumulative/data{?releaseid}{?requirementid}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Testcase count per node [/testcase/count/discrete/{releaseid}]"
  },
  {
    "endpoint_path": "/testcase/path",
    "full_path": "/testcase/path{?testcaseid}{?tctid}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Traceable Path from Root",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "testcaseid",
      "tctid"
    ],
    "path_parameters": [],
    "resource": "Get Traceable Path from Root [/testcase/path{?testcaseid}{?tctid}]"
  },
  {
    "endpoint_path": "/testcase/pathbyrelease",
    "full_path": "/testcase/pathbyrelease{?testcaseid}{?releaseid}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Traceable Path from Root",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "testcaseid",
      "releaseid"
    ],
    "path_parameters": [],
    "resource": "Get Traceable Path from Root [/testcase/pathbyrelease{?testcaseid}{?releaseid}]"
  },
  {
    "endpoint_path": "/testcase/planning",
    "full_path": "/testcase/planning/{treeId}{?offset}{?pagesize}{?order}{?isascorder}{?tcname}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Testcase by Criteria",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "offset",
      "pagesize",
      "order",
      "isascorder",
      "tcname"
    ],
    "path_parameters": [
      "treeId"
    ],
    "resource": "Get Testcase by Criteria [/testcase/planning/{treeId}{?offset}{?pagesize}{?order}{?isascorder}{?tcname}]"
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
    "path_parameters": [
      "testcaseId"
    ],
    "resource": "Get Testcase by ID [/testcase/{testcaseId}]"
  },
  {
    "endpoint_path": "/testcase/nodes",
    "full_path": "/testcase/nodes{?treeids}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Testcases by Tree IDs",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "treeids"
    ],
    "path_parameters": [],
    "resource": "Get Testcases by Tree IDs [/testcase/nodes{?treeids}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Get Testcase details by ID [/testcase/detail/{id}]"
  },
  {
    "endpoint_path": "/testcase/altid",
    "full_path": "/testcase/altid{?altids}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Testcase by ID",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "altids"
    ],
    "path_parameters": [],
    "resource": "Get Testcase by ID [/testcase/altid{?altids}]"
  },
  {
    "endpoint_path": "/testcase/byrequirement",
    "full_path": "/testcase/byrequirement{?requirementid}{?breadcrumb}{?releaseid}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Testcase Summary by Requirement ID",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "requirementid",
      "breadcrumb",
      "releaseid"
    ],
    "path_parameters": [],
    "resource": "Get Testcase Summary by Requirement ID [/testcase/byrequirement{?requirementid}{?breadcrumb}{?releaseid}]"
  },
  {
    "endpoint_path": "/testcase/versions",
    "full_path": "/testcase/versions{?testcaseid}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get all testcase version by testcase id",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "testcaseid"
    ],
    "path_parameters": [],
    "resource": "Get all testcase version by testcase id  [/testcase/versions{?testcaseid}]"
  },
  {
    "endpoint_path": "/testcase",
    "full_path": "/testcase{?offset}{?pagesize}{?releaseid}{?keyword}{?zqlquery}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get Testcase by Criteria",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "offset",
      "pagesize",
      "releaseid",
      "keyword",
      "zqlquery"
    ],
    "path_parameters": [],
    "resource": "Get Testcase by Criteria [/testcase{?offset}{?pagesize}{?releaseid}{?keyword}{?zqlquery}]"
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
      "is_cfield"
    ],
    "path_parameters": [
      "treeid"
    ],
    "resource": "Get Testcase by Tree ID [/testcase/tree/{treeid}{?offset}{?pagesize}{?order}{?isascorder}{?dbsearch}{?frozen}{?is_cfield}]"
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
    "resource": "Map Testcase to Requirement [/testcase/mapby/altid]"
  },
  {
    "endpoint_path": "/testcase/move/from",
    "full_path": "/testcase/move/from/{sourceentryid}/to/{targetentryid}{?sourceitemids}",
    "http_method": "POST",
    "category": "testcases",
    "description": "Move Testcases",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "sourceitemids"
    ],
    "path_parameters": [
      "sourceentryid",
      "targetentryid"
    ],
    "resource": "Move Testcases [/testcase/move/from/{sourceentryid}/to/{targetentryid}{?sourceitemids}]"
  },
  {
    "endpoint_path": "/testcase/share/on",
    "full_path": "/testcase/share/on/{releaseid}/to/{targettreeid}{?sourceitemids}{?showinfomessage}{?link}",
    "http_method": "POST",
    "category": "testcases",
    "description": "Share Testcase",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "sourceitemids",
      "showinfomessage",
      "link"
    ],
    "path_parameters": [
      "releaseid",
      "targettreeid"
    ],
    "resource": "Share Testcase [/testcase/share/on/{releaseid}/to/{targettreeid}{?sourceitemids}{?showinfomessage}{?link}]"
  },
  {
    "endpoint_path": "/testcase/flag",
    "full_path": "/testcase/flag/{flag}{?testcaseids}{?tcrCatalogTreeId}",
    "http_method": "PUT",
    "category": "testcases",
    "description": "Update Flag status by Tree Testcase ID",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "testcaseids",
      "tcrCatalogTreeId"
    ],
    "path_parameters": [
      "flag"
    ],
    "resource": "Update Flag status by Tree Testcase ID  [/testcase/flag/{flag}{?testcaseids}{?tcrCatalogTreeId}]"
  },
  {
    "endpoint_path": "/testcase",
    "full_path": "/testcase/{id}{?forceCreateNewVersion}",
    "http_method": "PUT",
    "category": "testcases",
    "description": "Update Testcase values",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "forceCreateNewVersion"
    ],
    "path_parameters": [
      "id"
    ],
    "resource": "Update Testcase values [/testcase/{id}{?forceCreateNewVersion}]"
  },
  {
    "endpoint_path": "/testcase",
    "full_path": "/testcase/{tctId}/replacewithversion/{testcaseVersionId}{?releaseid}",
    "http_method": "PUT",
    "category": "testcases",
    "description": "Update Testcase With Version",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "releaseid"
    ],
    "path_parameters": [
      "tctId",
      "testcaseVersionId"
    ],
    "resource": "Update Testcase With Version  [/testcase/{tctId}/replacewithversion/{testcaseVersionId}{?releaseid}]"
  },
  {
    "endpoint_path": "/testcase",
    "full_path": "/testcase{?forceCreateNewVersion}",
    "http_method": "PUT",
    "category": "testcases",
    "description": "Update Testcase values",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "forceCreateNewVersion"
    ],
    "path_parameters": [],
    "resource": "Update Testcase values [/testcase{?forceCreateNewVersion}]"
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
      "targetreleaseid"
    ],
    "resource": "Copy Testcase tree node to another target node [/testcasetree/copy/{nodeid}/{sourcereleaseid}/to/{targetparentid}/{targetreleaseid}]"
  },
  {
    "endpoint_path": "/testcasetree",
    "full_path": "/testcasetree{?parentid}{?assignedusers}",
    "http_method": "POST",
    "category": "testcases",
    "description": "Create Tree node",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "parentid",
      "assignedusers"
    ],
    "path_parameters": [],
    "resource": "Create Tree node [/testcasetree{?parentid}{?assignedusers}]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Delete Testcase Tree [/testcasetree/{id}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Get Execution Tree by releaseid [/testcasetree/phases/execution/{releaseid}]"
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
    "path_parameters": [
      "treeid"
    ],
    "resource": "Get TCR hierarchy [/testcasetree/hierarchy/{treeid}]"
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
    "path_parameters": [
      "tctId"
    ],
    "resource": "Get Testcase Tree [/testcasetree/{tctId}]"
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
    "path_parameters": [
      "releaseid"
    ],
    "resource": "Get Testcase Tree by releaseid [/testcasetree/phases/{releaseid}]"
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
    "path_parameters": [
      "projectid"
    ],
    "resource": "Get Project Repository Testcase Tree by projectid [/testcasetree/projectrepository/{projectid}]"
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
      "offset"
    ],
    "path_parameters": [],
    "resource": "Get tree by criteria [/testcasetree/lite{?type}{?releaseid}{?revisionid}{?parentid}{?isShared}{?limit}{?offset}]"
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
    "path_parameters": [
      "nodeid",
      "targetid"
    ],
    "resource": "Move Testcase tree  [/testcasetree/move/{nodeid}/to/{targetid}]"
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
    "path_parameters": [
      "nodeid",
      "sourcereleaseid",
      "targetid",
      "targetreleaseid"
    ],
    "resource": "Move Testcase tree to other Release [/testcasetree/move/{nodeid}/{sourcereleaseid}/to/{targetid}/{targetreleaseid}]"
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
      "targetreleaseid"
    ],
    "resource": "Share Testcase tree node to another target node [/testcasetree/share/{nodeid}/{sourcereleaseid}/to/{targetparentid}/{targetreleaseid}]"
  },
  {
    "endpoint_path": "/testcasetree/assignuser",
    "full_path": "/testcasetree/assignuser/{id}{?name}{?description}{?assignedusers}",
    "http_method": "PUT",
    "category": "testcases",
    "description": "Update tree node values",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "name",
      "description",
      "assignedusers"
    ],
    "path_parameters": [
      "id"
    ],
    "resource": "Update tree node values [/testcasetree/assignuser/{id}{?name}{?description}{?assignedusers}]"
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
    "path_parameters": [
      "treeId"
    ],
    "resource": "Update tree node values [/testcasetree/{treeId}]"
  },
  {
    "endpoint_path": "/tcuh/testcase",
    "full_path": "/tcuh/testcase/{id}{?isascorder}{?order}{?offset}{?pagesize}",
    "http_method": "GET",
    "category": "other",
    "description": "Get Testcase usage history details",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "isascorder",
      "order",
      "offset",
      "pagesize"
    ],
    "path_parameters": [
      "id"
    ],
    "resource": "Get Testcase usage history details [/tcuh/testcase/{id}{?isascorder}{?order}{?offset}{?pagesize}]"
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
    "path_parameters": [
      "testcaseVersionId",
      "tctId"
    ],
    "resource": "Create teststep [/testcase/{testcaseVersionId}/teststep/detail/{tctId}]"
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
    "path_parameters": [
      "testcaseVersionId",
      "tctId"
    ],
    "resource": "Delete teststep [/testcase/{testcaseVersionId}/teststep/{tctId}]"
  },
  {
    "endpoint_path": "/testcase",
    "full_path": "/testcase/{testcaseVersionId}/teststep{?isfetchstepversion}{?versionId}",
    "http_method": "GET",
    "category": "testcases",
    "description": "Get teststep",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "isfetchstepversion",
      "versionId"
    ],
    "path_parameters": [
      "testcaseVersionId"
    ],
    "resource": "Get teststep [/testcase/{testcaseVersionId}/teststep{?isfetchstepversion}{?versionId}]"
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
    "path_parameters": [
      "testcaseVersionId",
      "testcaseTreeId"
    ],
    "resource": "Update teststep [/testcase/{testcaseVersionId}/teststep/detail/{testcaseTreeId}]"
  },
  {
    "endpoint_path": "/ui/auditLogs",
    "full_path": "/ui/auditLogs{?offset}{?pagesize}{?order}{?isascorder}",
    "http_method": "POST",
    "category": "other",
    "description": "Get audit logs Grid view",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "offset",
      "pagesize",
      "order",
      "isascorder"
    ],
    "path_parameters": [],
    "resource": "Get audit logs Grid view [/ui/auditLogs{?offset}{?pagesize}{?order}{?isascorder}]"
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
      "isLoggedIn"
    ],
    "path_parameters": [],
    "resource": "Get user Grid view [/ui/users{?offset}{?pagesize}{?hidedisabledusers}{?order}{?isascorder}{?isLoggedIn}]"
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
      "hidedisabledgroups"
    ],
    "path_parameters": [],
    "resource": "Get group Grid view [/ui/searchGroups{?text}{?offset}{?pagesize}{?order}{?isascorder}{?hidedisabledgroups}]"
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
      "isProjectAdmin"
    ],
    "path_parameters": [],
    "resource": "Get project Grid view [/ui/searchProjects{?text}{?offset}{?pagesize}{?order}{?isascorder}{?includeglobalproject}{?isProjectAdmin}]"
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
    "resource": "Create User in the System [/user/]"
  },
  {
    "endpoint_path": "/user/current",
    "full_path": "/user/current{?auditLog}",
    "http_method": "GET",
    "category": "users",
    "description": "Get Current Logged-In Users",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "auditLog"
    ],
    "path_parameters": [],
    "resource": "Get Current Logged-In Users [/user/current{?auditLog}]"
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
    "resource": "Get Defect Users present in System. [/user/defect]"
  },
  {
    "endpoint_path": "/user/filter",
    "full_path": "/user/filter{?includeDashboardUser}",
    "http_method": "GET",
    "category": "users",
    "description": "Get All Users Present in the System.",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "includeDashboardUser"
    ],
    "path_parameters": [],
    "resource": "Get All Users Present in the System. [/user/filter{?includeDashboardUser}]"
  },
  {
    "endpoint_path": "/user/loggedin/count",
    "full_path": "/user/loggedin/count{?skipdefectuser}",
    "http_method": "GET",
    "category": "users",
    "description": "Getting all the Logged-In in User count",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "skipdefectuser"
    ],
    "path_parameters": [],
    "resource": "Getting all the Logged-In in User count [/user/loggedin/count{?skipdefectuser}]"
  },
  {
    "endpoint_path": "/user",
    "full_path": "/user/{id}{?isLite}",
    "http_method": "GET",
    "category": "users",
    "description": "Get User by ID",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "isLite"
    ],
    "path_parameters": [
      "id"
    ],
    "resource": "Get User by ID [/user/{id}{?isLite}]"
  },
  {
    "endpoint_path": "/user",
    "full_path": "/user{?hidedisabledusers}",
    "http_method": "GET",
    "category": "users",
    "description": "Get All Users Present in the System.",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "hidedisabledusers"
    ],
    "path_parameters": [],
    "resource": "Get All Users Present in the System. [/user{?hidedisabledusers}]"
  },
  {
    "endpoint_path": "/user/project",
    "full_path": "/user/project/{projectid}{?isLite}{?adminUser}",
    "http_method": "GET",
    "category": "users",
    "description": "Get User by Project ID",
    "requires_auth": True,
    "hierarchical": True,
    "query_parameters": [
      "isLite",
      "adminUser"
    ],
    "path_parameters": [
      "projectid"
    ],
    "resource": "Get User by Project ID [/user/project/{projectid}{?isLite}{?adminUser}]"
  },
  {
    "endpoint_path": "/user/validZbotUsers",
    "full_path": "/user/validZbotUsers{?projectId}",
    "http_method": "GET",
    "category": "users",
    "description": "Get valid users for Zbot.",
    "requires_auth": True,
    "hierarchical": False,
    "query_parameters": [
      "projectId"
    ],
    "path_parameters": [],
    "resource": "Get valid users for Zbot. [/user/validZbotUsers{?projectId}]"
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
    "resource": "Logout User from System [/user/logout]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "Update User [/user/{id}]"
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
    "resource": "delete all token  [/usertoken/all]"
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
    "path_parameters": [
      "id"
    ],
    "resource": "delete token  [/usertoken/{id}]"
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
    "resource": "generate token  [/usertoken/]"
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
    "resource": "Get all token  [/usertoken]"
  }
]

# Category summary
CATEGORY_COUNTS = {
    category: len([e for e in ENDPOINTS_CATALOG if e["category"] == category])
    for category in set(e["category"] for e in ENDPOINTS_CATALOG)
}

# Hierarchical endpoints
HIERARCHICAL_ENDPOINTS = [
    e for e in ENDPOINTS_CATALOG if e["hierarchical"]
]
