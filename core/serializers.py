from djoser.serializers import UserCreateSerializer as BaseUserCreateClass
class UserCreateSerializer(BaseUserCreateClass):
    class Meta(BaseUserCreateClass.Meta):
        fields = ['id','username','password','email','first_name','last_name']