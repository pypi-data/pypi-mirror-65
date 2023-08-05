"""
[![npm version](https://badge.fury.io/js/%40taimos%2Fcdk-construct-alexa-skill.svg)](https://badge.fury.io/js/%40taimos%2Fcdk-construct-alexa-skill)
[![PyPI version](https://badge.fury.io/py/taimos.cdk-construct-alexa-skill.svg)](https://badge.fury.io/py/taimos.cdk-construct-alexa-skill)

# A CDK L3 Construct for an Alexa Skill backend

## Installation

You can install the library into your project using npm or pip.

```bash
npm install @taimos/cdk-construct-alexa-skill

pip3 install taimos.cdk-construct-alexa-skill
```

# Contributing

We welcome community contributions and pull requests.

# License

The CDK construct library is distributed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

See [LICENSE](./LICENSE) for more information.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_dynamodb
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core
import constructs

__jsii_assembly__ = jsii.JSIIAssembly.load("@taimos/cdk-construct-alexa-skill", "1.0.0", __name__, "cdk-construct-alexa-skill@1.0.0.jsii.tgz")


@jsii.data_type(jsii_type="@taimos/cdk-construct-alexa-skill.AlexaSkillConfig", jsii_struct_bases=[], name_mapping={'code_asset': 'codeAsset', 'skill_id': 'skillId', 'skill_name': 'skillName', 'code_handler': 'codeHandler', 'environment': 'environment', 'user_attribute': 'userAttribute'})
class AlexaSkillConfig():
    def __init__(self, *, code_asset: aws_cdk.aws_lambda.Code, skill_id: str, skill_name: str, code_handler: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, user_attribute: typing.Optional[str]=None):
        """
        :param code_asset: The code to use for the backend lambda.
        :param skill_id: The Alexa Skill id.
        :param skill_name: The Alexa Skill name.
        :param code_handler: The handler for the lambda function. Default: dist/index.handler
        :param environment: Environement variables for the Lambda function.
        :param user_attribute: name of the user attribute for DynamoDB. Default: id
        """
        self._values = {
            'code_asset': code_asset,
            'skill_id': skill_id,
            'skill_name': skill_name,
        }
        if code_handler is not None: self._values["code_handler"] = code_handler
        if environment is not None: self._values["environment"] = environment
        if user_attribute is not None: self._values["user_attribute"] = user_attribute

    @builtins.property
    def code_asset(self) -> aws_cdk.aws_lambda.Code:
        """The code to use for the backend lambda."""
        return self._values.get('code_asset')

    @builtins.property
    def skill_id(self) -> str:
        """The Alexa Skill id."""
        return self._values.get('skill_id')

    @builtins.property
    def skill_name(self) -> str:
        """The Alexa Skill name."""
        return self._values.get('skill_name')

    @builtins.property
    def code_handler(self) -> typing.Optional[str]:
        """The handler for the lambda function.

        default
        :default: dist/index.handler
        """
        return self._values.get('code_handler')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Environement variables for the Lambda function."""
        return self._values.get('environment')

    @builtins.property
    def user_attribute(self) -> typing.Optional[str]:
        """name of the user attribute for DynamoDB.

        default
        :default: id
        """
        return self._values.get('user_attribute')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AlexaSkillConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class AlexaSkillStack(aws_cdk.core.Stack, metaclass=jsii.JSIIMeta, jsii_type="@taimos/cdk-construct-alexa-skill.AlexaSkillStack"):
    def __init__(self, parent: aws_cdk.core.App, *, code_asset: aws_cdk.aws_lambda.Code, skill_id: str, skill_name: str, code_handler: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, user_attribute: typing.Optional[str]=None) -> None:
        """
        :param parent: -
        :param code_asset: The code to use for the backend lambda.
        :param skill_id: The Alexa Skill id.
        :param skill_name: The Alexa Skill name.
        :param code_handler: The handler for the lambda function. Default: dist/index.handler
        :param environment: Environement variables for the Lambda function.
        :param user_attribute: name of the user attribute for DynamoDB. Default: id
        """
        config = AlexaSkillConfig(code_asset=code_asset, skill_id=skill_id, skill_name=skill_name, code_handler=code_handler, environment=environment, user_attribute=user_attribute)

        jsii.create(AlexaSkillStack, self, [parent, config])


__all__ = ["AlexaSkillConfig", "AlexaSkillStack", "__jsii_assembly__"]

publication.publish()
