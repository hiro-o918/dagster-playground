import time
from dagster import AssetMaterialization, In, Output, asset, job, op


@asset(group_name="foo")
def foo1() -> str:
    return "foo1"


@asset(group_name="foo")
def foo2() -> str:
    return "foo2"


@op(tags={"concurrency_limit": "foo_computation"})
def foo3() -> Output[str]:  # type: ignore
    time.sleep(1)
    yield AssetMaterialization(asset_key="foo3", description="foo3")
    yield Output("foo3")


@op(tags={"concurrency_limit": "foo_computation"})
def foo4() -> Output[str]:  # type: ignore
    time.sleep(3)
    yield AssetMaterialization(asset_key="foo4", description="foo4")
    yield Output("foo4")


@op(
    ins={
        "foo1": In(
            dagster_type=str,
        ),
        "foo3": In(
            dagster_type=str,
        ),
    },
)
def foo5(foo1: str, foo3: str) -> Output[str]:
    return Output(foo1 + foo3)


@job(
    config={
        "execution": {
            "config": {
                "multiprocess": {
                    "tag_concurrency_limits": [
                        {
                            "key": "concurrency_limit",
                            "value": "foo_computation",
                            "limit": 1,
                        }
                    ]
                }
            }
        }
    }
)
def all_foo_job() -> None:
    foo5(foo1=foo1(), foo3=foo3())
