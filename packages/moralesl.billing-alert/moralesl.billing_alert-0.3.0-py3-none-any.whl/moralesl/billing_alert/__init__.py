"""
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
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_cloudwatch_actions
import aws_cdk.aws_sns
import aws_cdk.aws_sns_subscriptions
import aws_cdk.core
import constructs

__jsii_assembly__ = jsii.JSIIAssembly.load("@moralesl/billing-alert", "0.3.0", "moralesl.billing_alert", "billing-alert@0.3.0.jsii.tgz")


class BillingAlert(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@moralesl/billing-alert.BillingAlert"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, amount: jsii.Number, emails: typing.List[str]) -> None:
        """
        :param scope: -
        :param id: -
        :param amount: The amount of USD when the alarm should trigger.
        :param emails: The emails that subscribe to the billing alert.
        """
        props = BillingAlertProps(amount=amount, emails=emails)

        jsii.create(BillingAlert, self, [scope, id, props])


@jsii.data_type(jsii_type="@moralesl/billing-alert.BillingAlertProps", jsii_struct_bases=[], name_mapping={'amount': 'amount', 'emails': 'emails'})
class BillingAlertProps():
    def __init__(self, *, amount: jsii.Number, emails: typing.List[str]):
        """
        :param amount: The amount of USD when the alarm should trigger.
        :param emails: The emails that subscribe to the billing alert.
        """
        self._values = {
            'amount': amount,
            'emails': emails,
        }

    @builtins.property
    def amount(self) -> jsii.Number:
        """The amount of USD when the alarm should trigger."""
        return self._values.get('amount')

    @builtins.property
    def emails(self) -> typing.List[str]:
        """The emails that subscribe to the billing alert."""
        return self._values.get('emails')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BillingAlertProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["BillingAlert", "BillingAlertProps", "__jsii_assembly__"]

publication.publish()
