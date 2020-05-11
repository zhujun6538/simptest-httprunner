import json

class Generator():
    def __init__(self):
        pass

    def gen_case(self,testcase_model=None):
        thiscase = testcase_model
        testcasedict = {}
        testcaselist = []
        jsondata = {}
        config = {}
        teststeps = []
        thisteststeps = thiscase.teststep.all()
        config['name'] = thiscase.casename
        config['path'] = ""
        config['variables'] = {}
        for var in thiscase.variables.all():
            config['variables'][var.key] = var.value
        for teststep in thisteststeps:
            dict = {}
            dict['name'] = teststep.name
            dict['request'] = {}
            dict['request']['allow_redirects'] = teststep.AllowRedirects
            dict['request']['url'] = teststep.url
            dict['request']['method'] = teststep.requestType
            if teststep.data != "":
                dict['request']['data'] = json.loads(teststep.data)
            dict['request']['headers'] = {}
            for header in teststep.headers.all():
                dict['request']['headers'][header.key] = header.value
            dict['validate'] = []
            for val in teststep.validates.all():
                if val.AssertKey == 'status_code':
                    dict['validate'].append({val.AssertMode:[val.AssertKey,int(val.AssertValue)]})
                else:
                    dict['validate'].append({val.AssertMode: [val.AssertKey, val.AssertValue]})
            dict['extract'] = {}
            for ext in teststep.extracts.all():
                dict['extract'][ext.key] = ext.value
            teststeps.append(dict)
        jsondata['config'] = config
        jsondata['teststeps'] = teststeps
        testcaselist.append(jsondata)
        testcasedict['testcases'] = testcaselist
        # testcasedict = json.dumps(testcasedict)
        return testcasedict

    def gen_suite(self,testsuite_model=None):
        testsuitedict = {}
        thissuite = testsuite_model
        suitelist = []
        suitedict = {}
        config = {}
        config['name'] = thissuite.suitename
        config['path'] = ""
        config['variables'] = {}
        suitedict['config'] = config
        suitedict['testcases'] = {}
        casedict = {}
        for case in thissuite.testcase.all():
            for obj in self.gen_case(case)['testcases']:
                suite = {}
                suite['variables'] = {}
                # for var in thissuite.variables.all():
                #     casedict[case.casename]['variables'][var.key] = var.value
                suite['parameters'] = {}
                suite['testcase'] = []
                suite['testcase_def'] = obj
            casedict[case.casename] = suite
        suitedict['testcases'] = casedict
        suitelist.append(suitedict)
        testsuitedict['testsuites'] = suitelist
        return testsuitedict











