from django.db import models

# class Configs(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50, verbose_name='配置名')
#     path = models.CharField(max_length=1024, verbose_name='路径')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = '配置'
#         verbose_name_plural = '配置管理'

# class Url(models.Model):
#     id = models.AutoField(primary_key=True)
#     url = models.CharField(max_length=50, verbose_name='接口地址')
#
#     def __str__(self):
#         return self.url

class Variables(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50, verbose_name='参数')
    value = models.CharField(max_length=1024, verbose_name='值')

    def __str__(self):
        return self.key + ' ： ' + self.value

    class Meta:
        verbose_name = '变量'
        verbose_name_plural = '变量管理'

class Headers(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50, verbose_name='参数')
    value = models.CharField(max_length=1024, verbose_name='值')

    def __str__(self):
        return self.key + ' ： ' + self.value

class Extracts(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50, verbose_name='变量名')
    value = models.CharField(max_length=1024, verbose_name='匹配值')

    def __str__(self):
        return self.key + ' ： ' + self.value

class Validates(models.Model):
    VALIDATE_TYPE_CHOICE = (
        ('eq', 'eq'),
    )
    id = models.AutoField(primary_key=True)
    AssertMode = models.CharField(max_length=50, default='eq', verbose_name='校验方式', choices=VALIDATE_TYPE_CHOICE)
    AssertKey = models.CharField(max_length=50, verbose_name='校验参数')
    AssertValue = models.CharField(max_length=50, verbose_name='预期值')

    def __str__(self):
        return self.AssertKey + ' ： ' + self.AssertValue

# Create your models here.
class Teststep(models.Model):
    REQUEST_TYPE_CHOICE = (
        ('GET', 'GET'),
        ('POST', 'POST'),
    )
    RESULT_CHOICE = (
        (True, '跳转'),
        (False, '不跳转'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='步骤名称')
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    AllowRedirects = models.BooleanField(default=True, verbose_name='允许跳转',choices=RESULT_CHOICE)
    url = models.CharField(max_length=50, verbose_name='接口地址')
    headers = models.ManyToManyField(Headers, verbose_name='头信息', blank=True)
    data = models.TextField(blank=True, null=True, verbose_name='内容')
    extracts = models.ManyToManyField(Extracts, verbose_name='继承变量', blank=True)
    validates = models.ManyToManyField(Validates,verbose_name='校验点',blank=True)
    description = models.TextField(max_length=1024, blank=True, null=True, verbose_name='描述')
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    creater = models.ForeignKey('auth.User', related_name='createapi', on_delete=models.CASCADE, verbose_name='创建人')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口管理'

class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    casename = models.CharField(max_length=50, verbose_name='用例名称')
    teststep = models.ManyToManyField(Teststep, related_name='step_case', verbose_name='关联步骤', blank=True)
    variables = models.ManyToManyField(Variables, verbose_name='参数', blank=True)
    path = models.CharField(max_length=50, verbose_name='路径', null=True, blank=True)
    base_url = models.CharField(max_length=50, verbose_name='base_url', null=True, blank=True)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    creater = models.ForeignKey('auth.User', on_delete=models.CASCADE,  verbose_name="创建人",related_name="createcase")



    def __str__(self):
        return self.casename

    class Meta:
        verbose_name = '用例'
        verbose_name_plural = '测试用例管理'

class TestSuite(models.Model):
    id = models.AutoField(primary_key=True)
    suitename = models.CharField(max_length=50,verbose_name='测试套件名')
    path = models.CharField(max_length=50, verbose_name='路径', null=True, blank=True)
    variables = models.ManyToManyField(Variables, verbose_name='参数', blank=True)
    description = models.TextField(max_length=1024, blank=True, null=True, verbose_name='描述')
    createtime = models.DateField(auto_now_add=True, verbose_name='创建时间')
    runcount = models.IntegerField(verbose_name='运行次数',default=0)
    runtime = models.DateTimeField(auto_now=True,verbose_name='最后运行时间',null=True)
    testcase = models.ManyToManyField(TestCase,related_name='case_suite',verbose_name='关联用例',blank=True)
    creater = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="创建人",related_name="createsuite")

    def __str__(self):
        return self.suitename

    class Meta:
        verbose_name = '测试套件'
        verbose_name_plural = '测试套件管理'


class TestReport(models.Model):
    RESULT_CHOICE =(
    (True, '成功'),
    (False, '失败'),
)


    id = models.AutoField(primary_key=True)
    testsuite = models.ForeignKey(TestSuite,on_delete=models.CASCADE,verbose_name="测试套件", related_name="testsuite_result",null=True,blank=True)
    testcase = models.ForeignKey(TestCase,on_delete=models.CASCADE,verbose_name="测试用例", related_name="testcase_result",null=True,blank=True)
    result = models.BooleanField(verbose_name='测试进度',choices=RESULT_CHOICE)
    reportname = models.CharField(max_length=1024,verbose_name='测试报告名')
    case_count = models.IntegerField(verbose_name='总用例数量',null=True)
    succeescase_count = models.IntegerField(verbose_name='成功用例数量',null=True)
    # succees_case = models.ManyToManyField(TestCase,related_name='succees_case_report',verbose_name='成功用例',blank=True)
    failcase_count = models.IntegerField(verbose_name='失败用例数量',null=True)
    # fail_case = models.ManyToManyField(TestCase, related_name='fail_case_report', verbose_name='失败用例', blank=True)
    step_count = models.IntegerField(verbose_name='总步骤数量',null=True)
    succeesstep_count = models.IntegerField(verbose_name='成功步骤数量',null=True)
    # succees_step = models.ManyToManyField(Teststep,related_name='succees_step_report',verbose_name='成功步骤',blank=True)
    failstep_count = models.IntegerField(verbose_name='失败步骤数量',null=True)
    # fail_step = models.ManyToManyField(Teststep, related_name='fail_step_report', verbose_name='失败步骤', blank=True)
    errorstep_count = models.IntegerField(verbose_name='错误步骤数量', null=True)
    skipstep_count = models.IntegerField(verbose_name='跳过步骤数量', null=True)
    report_data = models.FileField(verbose_name='测试报告文件')
    run_time = models.DateTimeField(auto_now_add=True,verbose_name='测试时间')

    def __str__(self):
        return self.reportname

    class Meta:
        verbose_name = '测试报告'
        verbose_name_plural = '测试报告管理'

