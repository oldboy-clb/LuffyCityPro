from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import CategorySerializer,CourseSerializer,CourseDetailSerializer,CourseChapterSerializer
# Create your views here.
class CategoryView(APIView):
    def get(self,request):
        # 通过ORM操作获取所有分类数据
        querset = models.Category.objects.all()
        # 利用序列化器去序列化我们的数据
        ser_obj = CategorySerializer(querset,many=True)
        # 返回
        return Response(ser_obj.data)

class CourseView(APIView):
    #获取过滤条件中的分类ID
    def get(self,request):
        category_id = request.query_params.get('category_id',0)
        # 根据过滤分类获取课程
        if category_id == 0:
            queryset = models.Course.objects.all().order_by("order")
            print(models.Course.objects.all().order_by('order'))
        else:
            queryset = models.Course.objects.filter(category_id=category_id).all().order_by('order')
            print(queryset)
        # 序列化课程数据
        ser_obj = CourseSerializer(queryset,many=True)
        return Response(ser_obj.data)


class CourseDetailView(APIView):
    def get(self,request,pk):
        print(pk)
        # 根据PK 获取课程详情
        course_detail_obj = models.CourseDetail.objects.filter(course__id=pk).first()
        if not course_detail_obj:
            return Response({"code":1001,"error":"查询的课程不存在"})
        # 序列化课程详情
        # 只有一个对象不需要many=True
        ser_obj = CourseDetailSerializer(course_detail_obj)
        # print(course_detail_obj)
        return Response(ser_obj.data)

class CourseChapterView(APIView):
    def get(self,request,pk):
        queryset = models.CourseChapter.objects.filter(course_id=pk)
        ser_obj = CourseChapterSerializer(queryset,many=True)
        return Response(ser_obj.data)