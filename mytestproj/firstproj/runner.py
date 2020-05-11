from httprunner.api import HttpRunner
from httprunner.report import gen_html_report
import yaml
import json
import os
from . import models
from . import urls
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class TestRunner():
    def __init__(self):
        self.summary = {}
        self.reportpath = ''

    def run(self,testdata):
        data = json.loads(testdata)
        runner = HttpRunner(failfast=False)
        runner.run_tests(data)
        self.summary = runner._summary
        report_dir = os.path.join(urls.get_media_root(), "reports")
        self.reportpath = gen_html_report(self.summary,report_dir=report_dir)

    def gen_suite_report(self,suite):
        models.TestReport.objects.create(testsuite=suite,
                                                      result=self.summary['success'],
                                                      reportname=suite.suitename+'测试报告',
                                         case_count=self.summary['stat']['testcases']['total'],
                                                      succeescase_count=self.summary['stat']['testcases']['success'],
                                                      failcase_count=self.summary['stat']['testcases']['fail'],
                                         step_count=self.summary['stat']['teststeps']['total'],
                                         succeesstep_count=self.summary['stat']['teststeps']['successes'],
                                         failstep_count=self.summary['stat']['teststeps']['failures'],
                                         errorstep_count=self.summary['stat']['teststeps']['errors'],
                                         skipstep_count=self.summary['stat']['teststeps']['skipped'],
                                                      report_data=self.reportpath
                                                      )

    def gen_case_report(self,case):
        models.TestReport.objects.create(testcase=case,
                                                      result=self.summary['success'],
                                                      reportname=case.casename+'测试报告',
                                         case_count=self.summary['stat']['testcases']['total'],
                                         succeescase_count=self.summary['stat']['testcases']['success'],
                                         failcase_count=self.summary['stat']['testcases']['fail'],
                                         step_count=self.summary['stat']['teststeps']['total'],
                                         succeesstep_count=self.summary['stat']['teststeps']['successes'],
                                         failstep_count=self.summary['stat']['teststeps']['failures'],
                                         errorstep_count=self.summary['stat']['teststeps']['errors'],
                                         skipstep_count=self.summary['stat']['teststeps']['skipped'],
                                                      report_data=self.reportpath
                                                      )

