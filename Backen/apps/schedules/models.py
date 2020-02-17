from django.db import models
from apps.users.models import UserProfile,OrgProfile


class CopyMixin():
    """
    复制功能Mixin，用于自动替换外键，但不保存
    """
    #COPY_KEY_LIST = []#可以自行添加

    def replace_foreign_key(self,use_copy_key_list=False,**kwargs):
        if not use_copy_key_list and not hasattr(self,"COPY_KEY_LIST"):
            raise
        else:
            if not hasattr(self,"COPY_KEY_LIST"):
                self.COPY_KEY_LIST = []
                for f in self._meta.fields:
                    if f.__class__.__name__ == 'ForeignField':
                        self.COPY_KEY_LIST.append(f.name)
        for iter in self.COPY_KEY_LIST:
            if iter in kwargs:
                if kwargs[iter] is not None:
                    setattr(self,iter,kwargs[iter])
                    #设置为None则默认不更改
            else:
                raise Exception("缺少定义在COPY_KEY_LIST中的外键")
        #不保存
        return self

class ScheduleTable(models.Model,CopyMixin):
    title = models.CharField(verbose_name="标题", max_length=32)
    description = models.TextField(verbose_name="描述", blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    SCHEDULE_TABLE_PERMISSION_CHOICES = (('0',"public"),('1',"protected"),('2',"private"))
    #public所有人可见，protected仅好友可见，private仅操作者可见
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,verbose_name="所属用户",
                             default="",null=True,related_name="user_table")
    permission = models.CharField(max_length=10,choices=SCHEDULE_TABLE_PERMISSION_CHOICES,
                                  default='2')
    COPY_KEY_LIST = ["user"]
    class Meta:
        unique_together = ("user","title")
    def __str__(self):
        return f"user:{self.user},title:{self.title}"
    @classmethod
    def get_permission_choice(cls):
        """
        返回table权限对应的元组
        :return:
        """
        return cls.SCHEDULE_TABLE_PERMISSION_CHOICES
    def copy(self,new_title=None,**kwargs):
        """
        复制并产生一个日程表,新表名称在旧表后加上[的副本]
        :param new_title:
        :param kwargs:包括user的一个字典
        :return:
        """
        st = self
        st.pk = None
        st.replace_foreign_key(use_copy_key_list=True,**kwargs)
        if new_title is None:
            st.title = f"{self.title}的副本"
        st.save()
        #创建新表
        if "user" not in kwargs:
            raise Exception("缺少定义在COPY_KEY_LIST中的外键")
        tmp = {"user":kwargs["user"],"table":st}
        for iter in self.table_schedule.all():
            iter.copy(tmp).save()
        return st
    def insert(self,schedule,ignore = False):
        pass
    def insert_many(self,ignore=False,*args):
        pass
    def copy_from(self,st,delete=False):
        """
        从st中复制,并，如果delete为真
        :param st:
        :param delete:
        :return:
        """

    def check_diff(self,st,time_range=None):
        """
        判断两个日程表在time_range的区间里是否有冲突
        :param st:另一个日程表
        :param time_range:一个由两个datetime组成的元组
        :return: 返回(status_code,intersection_list),其中intersection_list形如[(1)]
        """
        if time_range is not None:
            if time_range[0] > time_range[1]:
                return (-1,[])
            # 如果时间颠倒了判为冲突
            else:
                group_self = list(self.table_schedule.all())
                group_st = list(st.table_schedule.all())

        else:
            group_self = list(self.table_schedule.filter(start_time__gt=time_range[0]).filter(end_time__lt=time_range[1]))
            group_st = list(st.table_schedule.filter(start_time__gt=time_range[0]).filter(end_time__lt=time_range[1]))
        intersection_list = []
        for count,iter in enumerate(group_self):
            for compare in range(count+1,len(group_st)+1):
                tmp = group_st[compare]
                if iter.intersection(tmp):
                    intersection_list.append((iter.pk,tmp.pk))
        if intersection_list:
            return (1,intersection_list)
        else:
            return (0,intersection_list)

    def merge(self,st,time_range=None,ignore=False,delete_st=False):
        if ignore:
            return (self.copy_from(st,delete_st),None)
        else:
            diff = self.check_diff(st,time_range)
            if (diff[0] != 1):
                return (None,diff)
            else:
                return (self.copy_from(st,delete_st),diff)
"""
公共编辑，团队编辑
"""
# class GroupScheduleTable(BaseScheduleTable):
#     group =
class BaseMessage(models.Model,CopyMixin):
    add_time = models.DateField(auto_now_add=True, verbose_name="添加时间")
    title = models.CharField(verbose_name="标题", max_length=32)
    description = models.TextField(verbose_name="描述", blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"title:{self.title},add_time:{self.add_time}"

    def copy(self, **kwargs):
        """
        提供一个副本，注意此处没有保存，需要手动保存
        :param: kwargs
        :return: 一个schedule副本
        """
        sch = self
        sch.pk = None
        sch.replace_foreign_key(use_copy_key_list=True,**kwargs)
        return sch

class Todo(BaseMessage):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Todo",
                             default="",related_name="user_todo")
    is_finished=models.BooleanField(default=False,verbose_name="是否完成")
    class Meta:
        unique_together = ("user", "title")

class BaseSchedule(BaseMessage):
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户",
                             default="", null=True, related_name="user_schedule")

    COPY_KEY_LIST = ["user"]

    class Meta:
        get_latest_by = "start_time"
        ordering = ["start_time","end_time"]
        abstract = True

    def __str__(self):
        return f"title:{self.title},user:{self.user},add_time:{self.add_time}"

    def is_cover(self,sch):
        """
        判断当前时间段是否覆盖sch的时间段
        :param sch:
        :return:如果是返回True，否则返回False
        """
        return (self.start_time<=sch.start_time and self.end_time>=sch.end_time)

    def intersection(self,sch):
        """
        判断是否有交集
        :param sch:
        :return:如果是返回True，否则返回False

        设当前Schedule为A，另一个为B。
        一共有四种情况：
        A覆盖B，返回
        B覆盖A；
        A在B左边并且相交；
        A在B右边并且相交；
        """
        return (self.is_cover(sch) or sch.is_cover(self) or
                self.end_time>sch.start_time or
                sch.end_time>self.start_time)


class Schedule(BaseSchedule):
    weight = models.IntegerField(default=9,verbose_name="权重")
    table = models.ForeignKey(ScheduleTable, on_delete=models.CASCADE, verbose_name="日程表",
                              default="", null=True, related_name="table_schedule")
    COPY_KEY_LIST = ["user","table"]

    class Meta:
        get_latest_by = "start_time"
        ordering = ["start_time","end_time",'weight']
    def __str__(self):
        return f"title:{self.title},user:{self.user},table:{self.table}" \
            f",add_time:{self.add_time}"
    #为0~9，后面会自动处理超出范围的数




def update(user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    update_fields = []
    for key, value in kwargs:
        if hasattr(user, key) and (key != "pk"):
            setattr(user, key, value)
            update_fields.append(key)
    user.save(update_fields=update_fields)

def copy_schedules_by_id(user_id,group_id,schedules):
    pass