from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import renderers,pagination
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.forms import modelform_factory
from rest_framework.reverse import reverse
from django.shortcuts import redirect
from rest_framework.routers import APIRootView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.widgets import SelectDateWidget
from rest_framework.decorators import action
from . import runner
from .generator import Generator
import os
import json


class RootView(APIRootView):
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return Response(status=200,template_name='test_framework/index.html')

# Create your views here.
# class ConfigInfoViewSet(viewsets.ModelViewSet):
#     queryset = models.ConfigInfo.objects.all()
#     serializer_class = serializers.ConfigSerializer
#     renderer_classes = (renderers.TemplateHTMLRenderer,)
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
#
#     def list(self,request, *args, **kwargs):
#         ConfigForm = modelform_factory(models.ConfigInfo,fields = ('__all__'))
#         createform = ConfigForm()
#         return Response({'createform':createform},status=200,template_name='test_framework/addconfig.html')

    # 重写视图集create方法
    # def create(self, request, *args, **kwargs):
    #     super().create(request=request)

class TeststepViewSet(viewsets.ModelViewSet):
    queryset = models.Teststep.objects.all()
    serializer_class = serializers.TeststepSerializer
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name','requestType')

    def list(self, request, *args, **kwargs):
        page_data = super().list(request=request).data
        api_list = super().list(request=request).data['results']
        apititle = {}
        #获取字段名在前台表格列示
        for field in models.Teststep._meta.fields:
            apititle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        ApiForm = modelform_factory(models.Teststep,exclude = ('creater',))
        createform = ApiForm()
        #将api的表单对象放入data便于模板使用
        for slz in api_list:
            api = models.Teststep.objects.get(id=slz['id'])
            apiform = ApiForm(instance = api)
            slz['apiform']=apiform
        rdata = self.paginator.get_html_context()
        rdata['apilist'] = api_list
        rdata['apititle'] = apititle
        rdata['createform'] = createform
        return Response(rdata,status=200,template_name='test_framework/teststep.html')
        # return Response({'apilist':api_list,'apititle':apititle,'createform':createform},status=200,template_name='test_framework/Teststep.html')

    # 重写视图集create方法
    def create(self, request, *args, **kwargs):
        request.data.url = reverse('Teststep-list')
        super().create(request=request)
        return redirect('Teststep-list')

    def perform_create(self, serializer):
        serializer.save(creater=self.request.user)

    # 重写视图集destroy方法
    def destroy(self, request, *args, **kwargs):
        request.data.url = reverse('Teststep-list')
        super().destroy(request=request)
        return Response(status=200)

    # 重写视图集retrieve方法
    def retrieve(self, request, *args, **kwargs):
        return redirect('Teststep-list')


    # 重写视图集update方法
    def update(self, request, *args, **kwargs):
        request.data.url = reverse('Teststep-list')
        super().update(request=request)
        return Response(status=200)

class TestCaseViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。

    另外我们还提供了一个额外的`highlight`操作。
    """
    queryset = models.TestCase.objects.all()
    serializer_class = serializers.TestCaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('casename','teststep')

    def list(self, request, *args, **kwargs):
        page_data = super().list(request=request).data
        case_list = super().list(request=request).data['results']
        casetitle = {}
        #获取字段名在前台表格列示
        for field in models.TestCase._meta.fields:
            casetitle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        CaseForm = modelform_factory(models.TestCase,exclude = ('creater',))
        createform = CaseForm()
        #将api的表单对象放入data便于模板使用
        for slz in case_list:
            case = models.TestCase.objects.get(id=slz['id'])
            caseform = CaseForm(instance = case)
            slz['caseform']=caseform
        rdata = self.paginator.get_html_context()
        rdata['caselist'] = case_list
        rdata['casetitle'] = casetitle
        rdata['createform'] = createform
        return Response(rdata,status=200,template_name='test_framework/caseinfo.html')
        # return Response({'caselist':case_list,'casetitle':casetitle,'createform':createform},status=200,template_name='test_framework/caseinfo.html')

    # # 重写get_queryset方法
    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     # queryset = models.TestCase.objects.all()
    #     queryset = self.queryset
    #     suitename = self.request.query_params.get('case_suite', None)
    #     if suitename is not None:
    #         suite = models.TestSuite.objects.filter(suitename__contains = suitename)[0]
    #         queryset = queryset.filter(case_suite = suite)
    #     return queryset

    # 重写视图集create方法
    def create(self, request, *args, **kwargs):
        request.data.url = reverse('testcase-list')
        super().create(request=request)
        return redirect('testcase-list')

    def perform_create(self, serializer):
        # relateapi = models.Teststep.objects.get(pk=self.request.data['relateapi'])
        serializer.save(creater=self.request.user)

    # 重写视图集destroy方法
    def destroy(self, request, *args, **kwargs):
        request.data.url = reverse('testcase-list')
        super().destroy(request=request)
        return Response(status=200)

    # 重写视图集retrieve方法
    def retrieve(self, request, *args, **kwargs):
        return redirect('testcase-list')

    # 重写视图集update方法
    def update(self, request, *args, **kwargs):
        request.data.url = reverse('testcase-list')
        super().update(request=request)
        return Response(status=200)

    # 运行套件
    @action(methods=['post'],detail='testcase-detail',url_path='runcase',url_name='testcase-runcase')
    def runcase(self,request, *args, **kwargs):
        thiscase = models.TestCase.objects.get(pk=kwargs['pk'])
        generator = Generator()
        testcasedict = generator.gen_case(thiscase)
        try:
            testrunner = runner.TestRunner()
            testrunner.run(json.dumps(testcasedict))
            testrunner.gen_case_report(thiscase)
        except Exception as e:
            pass
        return redirect('testsuite-list')



class TestSuiteViewSet(viewsets.ModelViewSet):
    queryset = models.TestSuite.objects.all()
    serializer_class = serializers.TestSuiteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('suitename','testcase')


    def list(self, request, *args, **kwargs):
        suite_list = super().list(request=request).data['results']
        suitetitle = {}
        #获取字段名在前台表格列示
        for field in models.TestSuite._meta.fields:
            suitetitle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        SuiteForm = modelform_factory(models.TestSuite,exclude = ('creater',),widgets={"createtime": SelectDateWidget()})
        createform = SuiteForm()
        #将api的表单对象放入data便于模板使用
        for slz in suite_list:
            suite = models.TestSuite.objects.get(id=slz['id'])
            suiteform = SuiteForm(instance = suite)
            slz['suiteform']=suiteform
        rdata = self.paginator.get_html_context()
        rdata['suitelist'] = suite_list
        rdata['suitetitle'] = suitetitle
        rdata['createform'] = createform
        return Response(rdata,status=200,template_name='test_framework/suiteinfo.html')
        # return Response({'suitelist':suite_list,'suitetitle':suitetitle,'createform':createform},status=200,template_name='test_framework/suiteinfo.html')

    # 重写视图集create方法
    def create(self, request, *args, **kwargs):
        request.data.url = reverse('testsuite-list')
        super().create(request=request)
        return redirect('testsuite-list')

    def perform_create(self, serializer):
        serializer.save(creater=self.request.user)

    # 重写视图集destroy方法
    def destroy(self, request, *args, **kwargs):
        request.data.url = reverse('testsuite-list')
        super().destroy(request=request)
        return Response(status=200)

    # 重写视图集retrieve方法
    def retrieve(self, request, *args, **kwargs):
        return redirect('testsuite-list')

    # 重写视图集update方法
    def update(self, request, *args, **kwargs):
        request.data.url = reverse('testsuite-list')
        super().update(request=request)
        return Response(status=200)

    # 运行套件
    @action(methods=['post'],detail='testsuite-detail',url_path='runsuite',url_name='testcase-runsuite')
    def runsuite(self,request, *args, **kwargs):
        thissuite = models.TestSuite.objects.get(pk=kwargs['pk'])
        generator = Generator()
        testcasedict = generator.gen_suite(thissuite)
        try:
            testrunner = runner.TestRunner()
            testrunner.run(json.dumps(testcasedict))
            testrunner.gen_suite_report(thissuite)
        except Exception as e:
            pass

        return redirect('testsuite-list')

class TestReportViewSet(viewsets.ModelViewSet):
    queryset = models.TestReport.objects.all()
    serializer_class = serializers.TestReportSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('testsuite','testcase','result')

    def list(self, request, *args, **kwargs):
        report_list = super().list(request=request).data['results']
        reporttitle = {}
        #获取字段名在前台表格列示
        for field in models.TestReport._meta.fields:
            reporttitle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        ReportForm = modelform_factory(models.TestReport,fields = ('__all__'),widgets={"run_time": SelectDateWidget()})
        createform = ReportForm()
        #将api的表单对象放入data便于模板使用
        for slz in report_list:
            report = models.TestReport.objects.get(id=slz['id'])
            reportform = ReportForm(instance = report)
            slz['reportform']=reportform
        rdata = self.paginator.get_html_context()
        rdata['reportlist'] = report_list
        rdata['reporttitle'] = reporttitle
        rdata['createform'] = createform
        return Response(rdata,status=200,template_name='test_framework/reportinfo.html')
        # return Response({'reportlist':report_list,'reporttitle':reporttitle,'createform':createform},status=200,template_name='test_framework/reportinfo.html')

    # 重写视图集destroy方法
    def destroy(self, request, *args, **kwargs):
        request.data.url = reverse('testreport-list')
        super().destroy(request=request)
        return Response(status=200)

    # 重写视图集retrieve方法
    def retrieve(self, request, *args, **kwargs):
        return redirect('testreport-list')

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    此视图自动提供`list`和`detail`操作。
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('')

    def list(self, request, *args, **kwargs):
        user_list = super().list(request=request).data['results']
        usertitle = {}
        #获取字段名在前台表格列示
        for field in User._meta.fields:
            usertitle[field.name] = field.verbose_name
        # 创建表单，自定义样式
        UserForm = modelform_factory(User,fields=('id', 'username'))
        createform = UserForm()
        #将api的表单对象放入data便于模板使用
        for slz in user_list:
            user = User.objects.get(id=slz['id'])
            userform = UserForm(instance = user)
            slz['userform']=userform
        rdata = self.paginator.get_html_context()
        rdata['userlist'] = user_list
        rdata['usertitle'] = usertitle
        rdata['createform'] = createform
        return Response(rdata,status=200,template_name='test_framework/userinfo.html')
        # return Response({'userlist':user_list,'usertitle':usertitle,'createform':createform},status=200,template_name='test_framework/userinfo.html')
