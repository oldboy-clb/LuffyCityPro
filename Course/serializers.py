from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    # source 后面会执行一些orm操作
    level = serializers.CharField(source = "get_level_display")
    # source = "get_level_display"
    # 需要重写SerializerMethodField 钩子函数
    price = serializers.SerializerMethodField()
    def get_price(self,obj):
        # 这里没有价格策略 所以开始会报错
        # print('price',obj.price_policy.all().order_by("price").first().price)
        return obj.price_policy.all().order_by("price").first().price
    class Meta:
        model = models.Course
        fields = ["id", "title", "course_img", "brief", "level", "study_num", "price"]
        # fields ="__all__"

class CourseDetailSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source="course.get_level_display")
    study_num = serializers.IntegerField(source= "course.study_num")
    recommend_courses = serializers.SerializerMethodField()
    price_policy = serializers.SerializerMethodField()
    teachers = serializers.SerializerMethodField()
    course_outline = serializers.SerializerMethodField()

    def get_course_outline(self,obj):
        # print([ {"id":outline.id,"title":outline.title} for outline in obj.course_outline.all().order_by('order')])
        return [{"id": outline.id, "title": outline.title, "content": outline.content} for outline in
                obj.course_outline.all().order_by("order")]

    def get_teachers(self, obj):
        return [{"id": teacher.id, "name": teacher.name} for teacher in obj.teachers.all()]

    def get_price_policy(self,obj):
        # print(obj.course.price_policy.all()[1].get_valid_period_display())
        return [{"id": price.id, "valid_price_display": price.get_valid_period_display(), "price": price.price} for price in obj.course.price_policy.all()]

    def get_recommend_courses(self,obj):
        # data = [{"id":recommend.id,"title":recommend.title} for recommend in obj.recommend_courses.all()]
        data = []

        for recommend in obj.recommend_courses.all():
            dict = {}
            dict["id"] = recommend.id
            dict["title"] = recommend.title

            data.append(dict)
        # return [{"id":recommend.id,"title":recommend.title} for recommend in obj.recommend_courses.all()]
        return data
    print("cd",level,study_num)
    class Meta:
        model = models.CourseDetail
        fields = ["id", "hours", "summary", "level", "study_num", "recommend_courses", "teachers",
                  "price_policy", "course_outline"]

class CourseChapterSerializer(serializers.ModelSerializer):
    CourseSection = serializers.SerializerMethodField()
    def get_CourseSection(self,obj):
        # print(obj.course_sections.all().order_by('section_order'))
        # for sections in obj.course_sections.all().order_by('section_order'):
        #     print(sections.id)
        #     print(sections.title)
        #     print(sections.free_trail)
        return [{"id":sections.id,"title":sections.title,"free_trail":sections.free_trail} for sections in obj.course_sections.all().order_by('section_order')]
    class Meta:
        model = models.CourseChapter
        fields = ["id",'title','chapter','CourseSection']

