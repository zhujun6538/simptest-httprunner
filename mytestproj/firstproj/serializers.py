from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

# class ConfigSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.ConfigInfo
#         fields = []
#         for field in model._meta.fields:
#             fields.append(field.name)


class TeststepSerializer(serializers.ModelSerializer):
    creater = serializers.ReadOnlyField(source='creater.username')

    class Meta:
        model = models.Teststep
        fields = []
        for field in model._meta.fields:
            fields.append(field.name)
        fields.append('headers')
        fields.append('extracts')
        fields.append('validates')
        # fields = ('id', 'name', 'requestType', 'AllowRedirects', 'apiAddress', 'data', 'description', 'createtime', 'headers','extracts','validates','creater')

class TestCaseSerializer(serializers.ModelSerializer):
    creater = serializers.ReadOnlyField(source='creater.username')


    class Meta:
        model = models.TestCase
        fields = []
        for field in model._meta.fields:
            fields.append(field.name)
        fields.append('teststep')
        fields.append('variables')
        # fields = ('id', 'casename', 'relateapi', 'examineType', 'expecthttpCode', 'expectdata', 'createtime', 'creater')

class TestSuiteSerializer(serializers.ModelSerializer):
    creater = serializers.ReadOnlyField(source='creater.username')

    class Meta:
        model = models.TestSuite
        fields = []
        fields.append('variables')
        fields.append('testcase')
        for field in model._meta.fields:
            fields.append(field.name)
        # fields = ('id', 'suitename', 'description','createtime', 'runcount', 'runtime','suitecase','creater')

class TestReportSerializer(serializers.ModelSerializer):
    testsuite = serializers.StringRelatedField(read_only=True)
    testcase = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.TestReport
        fields = []
        for field in model._meta.fields:
            fields.append(field.name)
        # fields = ('id', 'testsuite', 'result', 'reportname', 'error', 'msg', 'report_data', 'run_time')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    createapi = serializers.StringRelatedField(many=True, read_only=True)
    createcase = serializers.StringRelatedField(many=True, read_only=True)
    createsuite = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url','id', 'username', 'createapi','createcase','createsuite')