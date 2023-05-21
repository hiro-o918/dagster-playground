from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from . import foo

daily_refresh_schedule = ScheduleDefinition(job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *")

defs = Definitions(
    assets=load_assets_from_package_module(foo),
    jobs=[foo.all_foo_job],
    schedules=[daily_refresh_schedule],
)
