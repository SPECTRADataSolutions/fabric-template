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