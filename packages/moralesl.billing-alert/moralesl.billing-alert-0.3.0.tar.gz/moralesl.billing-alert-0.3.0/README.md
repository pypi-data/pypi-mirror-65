## CDK Billing Alert utility

---


[![Build Status](https://travis-ci.com/moralesl/cdk-billing-alert.svg?branch=master)](https://travis-ci.com/moralesl/cdk-billing-alert)
[![GitHub release](https://img.shields.io/github/release/moralesl/cdk-billing-alert/all.svg)](https://img.shields.io/github/release/moralesl/cdk-billing-alert/all.svg)

---


Utility CDK construct to setup billing alerts easily

## Example

The following example shows how to set up a billing alert:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from moralesl.billing_alert import BillingAlert

BillingAlert(self, "BillingAlertTenDollars",
    amount=10,
    emails=["test@example.com"
    ]
)
```
