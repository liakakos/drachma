import { DamlLfValue } from '@da/ui-core';

export const version = {
  schema: 'navigator-config',
  major: 2,
  minor: 0,
};

export const customViews = (userId, party, role) => ({
  operator: {
    type: "table-view",
    title: "Operator",
    source: {
      type: "contracts",
      filter: [
        {
          field: "argument.operator",
          value: party,
        },
        {
          field: "template.id",
          value: "Dwolla.Onboarding:Operator"
        }
      ],
      search: "",
      sort: [
        {
          field: "id",
          direction: "ASCENDING"
        }
      ]
    },
    columns: [
      {
        key: "argument.operator",
        title: "Operator",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).operator
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      }
    ]
  },
  user: {
    type: "table-view",
    title: "User",
    source: {
      type: "contracts",
      filter: [
        {
          field: "template.id",
          value: "Dwolla.Onboarding:User"
        }
      ],
      search: "",
      sort: [
        {
          field: "id",
          direction: "ASCENDING"
        }
      ]
    },
    columns: [
      {
        key: "argument.user",
        title: "User",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).user
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.operator",
        title: "Operator",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).operator
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      }
    ]
  },
  customers: {
    type: "table-view",
    title: "Customers",
    source: {
      type: "contracts",
      filter: [
        {
          field: "template.id",
          value: "Dwolla.Customers:Customer"
        }
      ],
      search: "",
      sort: [
        {
          field: "id",
          direction: "ASCENDING"
        }
      ]
    },
    columns: [
      {
        key: "argument.customerId",
        title: "Id",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).customerId
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.firstName",
        title: "First",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).firstName
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.lastName",
        title: "Last",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).lastName
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.email",
        title: "Email",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).email
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.customerType",
        title: "Type",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).customerType
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.status",
        title: "Status",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).status
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.created",
        title: "Created",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).created
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.user",
        title: "User",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).user
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.operator",
        title: "Operator",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).operator
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      }
    ]
  },
  funding_sources: {
    type: "table-view",
    title: "Funding Sources",
    source: {
      type: "contracts",
      filter: [
        {
          field: "template.id",
          value: "Dwolla.FundingSources:FundingSource@"
        }
      ],
      search: "",
      sort: [
        {
          field: "id",
          direction: "ASCENDING"
        }
      ]
    },
    columns: [
      {
        key: "argument.fundingSourceId",
        title: "Id",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).fundingSourceId
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.status",
        title: "Status",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).status
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.fundingSourceType",
        title: "Type",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).fundingSourceType
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.bankAccountType",
        title: "Account",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).bankAccountType
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.name",
        title: "Name",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).name
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.created",
        title: "Created",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).created
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.optBalance",
        title: "Balance",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).optBalance
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.removed",
        title: "Removed",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).removed ? "True" : "False"
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.channels",
        title: "Channels",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).channels
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.bankName",
        title: "Bank Name",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).bankName
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.user",
        title: "User",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).user
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.operator",
        title: "Operator",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).operator
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      }
    ]
  },
  micro_deposits: {
    type: "table-view",
    title: "Micro Deposits",
    source: {
      type: "contracts",
      filter: [
        {
          field: "template.id",
          value: "Dwolla.FundingSources:MicroDeposits"
        }
      ],
      search: "",
      sort: [
        {
          field: "id",
          direction: "ASCENDING"
        }
      ]
    },
    columns: [
      {
        key: "argument.fundingSourceId",
        title: "Funding Source Id",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).fundingSourceId
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.bankAccountType",
        title: "Account",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).bankAccountType
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.name",
        title: "Name",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).name
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.created",
        title: "Created",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).created
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.status",
        title: "Status",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).status
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.user",
        title: "User",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).user
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.operator",
        title: "Operator",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).operator
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      }
    ]
  },
  transfer_requests: {
    type: "table-view",
    title: "Transfer Requests",
    source: {
      type: "contracts",
      filter: [
        {
          field: "template.id",
          value: "Dwolla.Transfers:ReceiveFundsRequest"
        }
      ],
      search: "",
      sort: [
        {
          field: "id",
          direction: "ASCENDING"
        }
      ]
    },
    columns: [
      {
        key: "argument.sender",
        title: "Sender",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).sender
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.receiver",
        title: "Receiver",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).receiver
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.senderSourceId",
        title: "Sender Funding Source Id",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).senderSourceId
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.amount",
        title: "Amount",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).amount["currency"] + " " + DamlLfValue.toJSON(rowData.argument).amount["value"]
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.operator",
        title: "Operator",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).operator
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      }
    ]
  },
  transfers: {
    type: "table-view",
    title: "Transfers",
    source: {
      type: "contracts",
      filter: [
        {
          field: "template.id",
          value: "Dwolla.Transfers:Transfer@"
        }
      ],
      search: "",
      sort: [
        {
          field: "id",
          direction: "ASCENDING"
        }
      ]
    },
    columns: [
      {
        key: "argument.sender",
        title: "Sender",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).sender
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.receiver",
        title: "Receiver",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).receiver
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.transferId",
        title: "Id",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).transferId
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.status",
        title: "Status",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).status
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.amount",
        title: "Amount",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).amount["currency"] + " " + DamlLfValue.toJSON(rowData.argument).amount["value"]
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.created",
        title: "Created",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).created
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.metadata",
        title: "Metadata",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).metadata
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.clearing",
        title: "Clearing",
        createCell: ({rowData}) => ({
          type: "text",
          value: JSON.stringify(DamlLfValue.toJSON(rowData.argument).clearing)
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.achDetails",
        title: "ACH Details",
        createCell: ({rowData}) => ({
          type: "text",
          value: JSON.stringify(DamlLfValue.toJSON(rowData.argument).achDetails)
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.correlationId",
        title: "Correlation Id",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).correlationId
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.individualAchId",
        title: "Individual ACH Id",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).individualAchId
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      },
      {
        key: "argument.operator",
        title: "Operator",
        createCell: ({rowData}) => ({
          type: "text",
          value: DamlLfValue.toJSON(rowData.argument).operator
        }),
        sortable: true,
        width: 80,
        weight: 0,
        alignment: "left"
      }
    ]
  },
})
