"""
# jsii-code-samples

> An example jsii package authored in TypeScript that gets published as GitHub packages for Node.js, Python, Java and dotnet.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

__jsii_assembly__ = jsii.JSIIAssembly.load("jsii-code-samples", "1.0.5", __name__, "jsii-code-samples@1.0.5.jsii.tgz")


class HelloWorld(metaclass=jsii.JSIIMeta, jsii_type="jsii-code-samples.HelloWorld"):
    def __init__(self) -> None:
        jsii.create(HelloWorld, self, [])

    @jsii.member(jsii_name="fibonacci")
    def fibonacci(self, num: jsii.Number) -> jsii.Number:
        """
        :param num: -
        """
        return jsii.invoke(self, "fibonacci", [num])

    @jsii.member(jsii_name="sayHello")
    def say_hello(self, name: str) -> str:
        """
        :param name: -
        """
        return jsii.invoke(self, "sayHello", [name])


__all__ = ["HelloWorld", "__jsii_assembly__"]

publication.publish()
