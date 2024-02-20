import os
from typing import Dict, List

import yaml


def multiqc_config(self) -> Dict[str, List[str]]:
    """Make sure basic multiQC plugins are installed and plots are exported
    Basic template:

    .. code-block:: yaml

        report_comment: >
            This report has been generated by the <a href="https://github.com/nf-core/quantms" target="_blank">nf-core/quantms</a>
            analysis pipeline. For information about how to interpret these results, please see the
            <a href="https://nf-co.re/quantms" target="_blank">documentation</a>.
        report_section_order:
            software_versions:
                order: -1000
            nf-core-quantms-summary:
                order: -1001
        export_plots: true

    """

    passed: List[str] = []
    failed: List[str] = []

    # Remove field that should be ignored according to the linting config
    ignore_configs = self.lint_config.get("multiqc_config", [])

    fn = os.path.join(self.wf_path, "assets", "multiqc_config.yml")

    # Return a failed status if we can't find the file
    if not os.path.isfile(fn):
        return {"ignored": ["'assets/multiqc_config.yml' not found"]}

    try:
        with open(fn) as fh:
            mqc_yml = yaml.safe_load(fh)
    except Exception as e:
        return {"failed": [f"Could not parse yaml file: {fn}, {e}"]}

    # check if requried sections are present
    required_sections = ["report_section_order", "export_plots", "report_comment"]
    for section in required_sections:
        if section not in mqc_yml and section not in ignore_configs:
            failed.append(f"'assets/multiqc_config.yml' does not contain `{section}`")
            return {"passed": passed, "failed": failed}
        else:
            passed.append(f"'assets/multiqc_config.yml' contains `{section}`")

    try:
        orders = {}
        summary_plugin_name = f"{self.pipeline_prefix}-{self.pipeline_name}-summary"
        min_plugins = ["software_versions", summary_plugin_name]
        for plugin in min_plugins:
            if plugin not in mqc_yml["report_section_order"]:
                raise AssertionError(f"Section {plugin} missing in report_section_order")
            if "order" not in mqc_yml["report_section_order"][plugin]:
                raise AssertionError(f"Section {plugin} 'order' missing. Must be < 0")
            plugin_order = mqc_yml["report_section_order"][plugin]["order"]
            if plugin_order >= 0:
                raise AssertionError(f"Section {plugin} 'order' must be < 0")

        for plugin in mqc_yml["report_section_order"]:
            if "order" in mqc_yml["report_section_order"][plugin]:
                orders[plugin] = mqc_yml["report_section_order"][plugin]["order"]

        if orders[summary_plugin_name] != min(orders.values()):
            raise AssertionError(f"Section {summary_plugin_name} should have the lowest order")
        orders.pop(summary_plugin_name)
        if orders["software_versions"] != min(orders.values()):
            raise AssertionError("Section software_versions should have the second lowest order")
    except (AssertionError, KeyError, TypeError) as e:
        failed.append(f"'assets/multiqc_config.yml' does not meet requirements: {e}")
    else:
        passed.append("'assets/multiqc_config.yml' follows the ordering scheme of the minimally required plugins.")

    if "report_comment" not in ignore_configs:
        # Check that the minimum plugins exist and are coming first in the summary
        version = self.nf_config.get("manifest.version", "").strip(" '\"")
        if "dev" in version:
            version = "dev"
            report_comments = (
                f'This report has been generated by the <a href="https://github.com/nf-core/{self.pipeline_name}/tree/dev" target="_blank">nf-core/{self.pipeline_name}</a>'
                f" analysis pipeline. For information about how to interpret these results, please see the "
                f'<a href="https://nf-co.re/{self.pipeline_name}/dev/docs/output" target="_blank">documentation</a>.'
            )

        else:
            report_comments = (
                f'This report has been generated by the <a href="https://github.com/nf-core/{self.pipeline_name}/releases/tag/{version}" target="_blank">nf-core/{self.pipeline_name}</a>'
                f" analysis pipeline. For information about how to interpret these results, please see the "
                f'<a href="https://nf-co.re/{self.pipeline_name}/{version}/docs/output" target="_blank">documentation</a>.'
            )

        if mqc_yml["report_comment"].strip() != report_comments:
            # find where the report_comment is wrong and give it as a hint
            hint = report_comments
            failed.append(
                f"'assets/multiqc_config.yml' does not contain a matching 'report_comment'.  \n"
                f"The expected comment is:  \n"
                f"```{hint}```  \n"
                f"The current comment is:  \n"
                f"```{ mqc_yml['report_comment'].strip()}```"
            )
        else:
            passed.append("'assets/multiqc_config.yml' contains a matching 'report_comment'.")

    # Check that export_plots is activated
    try:
        if not mqc_yml["export_plots"]:
            raise AssertionError()
    except (AssertionError, KeyError, TypeError):
        failed.append("'assets/multiqc_config.yml' does not contain 'export_plots: true'.")
    else:
        passed.append("'assets/multiqc_config.yml' contains 'export_plots: true'.")

    return {"passed": passed, "failed": failed}
