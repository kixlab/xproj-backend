from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from userprofile.models import UserProfile
from rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(UserDetailsSerializer):
    is_participant = serializers.BooleanField(source = 'userprofile.is_participant')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('is_participant', 'step', )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        is_participant = profile_data.get('is_participant')
        step = profile_data.get('step')
        instance = super(UserSerializer, self).update(instance, validated_data)

        

        if not hasattr(instance, 'userprofile'):
            profile = UserProfile(user = instance, is_participant = is_participant, step=step)
            profile.save()

        profile = instance.userprofile

        if profile_data and is_participant:
            profile.is_participant = is_participant
            profile.step = step
            profile.save()

        return instance

# class NewUserSerializer(RegisterSerializer):
#     is_participant = serializers.BooleanField(source = 'userprofile.is_participant')

#     class Meta(RegisterSerializer.Meta):
#         fields = RegisterSerializer.Meta.fields + ('is_participant', )

#     def save(self, request):
#         is_participant = request.data['is_participant']
        
#         user = super().save(request)


#         return user
        
# from rest_framework import serializers
# from rest_auth.serializers import UserDetailsSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ('url', 'id', 'user', 'is_participant', 'step')