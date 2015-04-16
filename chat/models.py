from django.db import models

# Create your models here.
from django.db import models

MEMBER_GENDER = (
    (0, '-'),
    (1, 'Male'),
    (2, 'Female'),
)

MEMBER_PROFILEDATA_TYPE = (
    (0, 'String'),
)

FRIENDREQUEST_TYPE =(
    (0, '-'),
    (1, 'Sent request'),
    (2, 'Reject'),
    (3, 'Cancle'),
    (4, 'Accept')
)

from django.utils import timezone

class Member(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    user = models.ForeignKey('auth.User', related_name='member_user_set')
    data = models.TextField(default='null')

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_member')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def get_data_json(self):
        try:
            type(self.data_json)
        except:
            import json
            try:
                self.data_json = json.loads(self.data)
            except:
                self.data_json = {}
        return self.data_json

    def update_data(self, data_dict):
        import json
        data = self.get_data_json()
        if type(data) == type(None):
            data = {}
        data.update(data_dict)
        self.data = json.dumps(data)
        self.data_json = data
        return self.data_json

    @staticmethod
    def pull(user):
        member_list = Member.objects.filter(user=user)
        if member_list.count() == 0:
            member = Member(user=user)
            member.save()
        else:
            member = member_list[0]
            for member_delete in member_list[1:]:
                member_delete.delete()
        return member

class Profile(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)
    user = models.ForeignKey('auth.User')
    display = models.CharField(max_length=60, blank=True)
    gender = models.IntegerField(choices=MEMBER_GENDER, default=0)
    birthday = models.DateField(null=True, blank=True, default=None)
    data = models.TextField(default='null')
    code = models.CharField(max_length=32, blank=True,db_index=True)
    login_apppro = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.app is None:
            return 'None : %s'%(self.user.email)
        else:
            return '%s : %s'%(self.app.name, self.user.email)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_profile')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def get_data_json(self, key=None, default=None):
        import json
        try:
            type(self.data_json)
        except:
            try:
                self.data_json = json.loads(self.data)
                if self.data_json is None:
                    self.data_json = {}
            except:
                self.data_json = {}
        if key is not None:
            if key in self.data_json:
                return self.data_json[key]
            else:
                return default

        return self.data_json

    @staticmethod
    def covert_context_param_to_string(key="signup_info",uid="",value=""):
        key_string = "%s__%s" % (key, uid)
        context_string = "%s : %s\n" % (key_string, value)
        return context_string

    def get_context_string_by_uid(self,key="signup_info",uid=""):
        context_string = ""
        interest_data_json = self.get_data_json(key=key)
        if interest_data_json is not None:
            value = interest_data_json.get(uid,None)
            if value is not None and type(value) is not list:
                patial_context_string = Profile.covert_context_param_to_string\
                    (key=key,uid=uid,value=value)
                context_string += patial_context_string
            else:
                value_list = value
                for value in value_list :
                    patial_context_string = self.covert_context_param_to_string\
                        (key=key,uid=uid,value=value)
                    context_string += patial_context_string
                    context_string += "\n"
        return context_string

    def get_context_string(self, key="signup_info"):
        context_string = ""
        interest_data_json = self.get_data_json(key=key,default={})
        for uid,value in interest_data_json.iteritems() :
            context_string += self.get_context_string_by_uid(key=key, uid=uid)
            context_string += "\n"
        return context_string

    def update_data(self, data_dict):
        import json
        data = self.get_data_json()
        if type(data) == type(None):
            data = {}
        data.update(data_dict)
        self.data = json.dumps(data)

    def generate_code(self):
        import random, string
        while True:
            code = ''.join(random.choice(string.ascii_uppercase + string.digits +string.ascii_lowercase) for x in range(32))
            if not Profile.objects.filter(code=code).exists():
                break
        self.code = code

    def get_email(self):
        try:
            email = self.user.email
            if email.find('_') != -1:
                return email[email.find('_')+1:]
            else:
                return email
        except:
            return ''

    def get_info(self):
        from django.conf import settings
        result = {}
        result['code'] = self.code
        result['user_id'] = self.user.id
        result['email'] = self.get_email()
        result['display'] = self.display
        result['first_name'] = self.user.first_name
        result['last_name'] = self.user.last_name
        result['image'] = '%s/image/user/%s'%(settings.URL_API, self.image_name())
        result['gender'] = self.gender
        result['gender_display'] = self.get_gender_display()
        try:
            result['birthday'] = self.birthday.strftime(settings.TIME_FORMAT)
        except:
            result['birthday'] = ''
        result['info'] = self.get_data_json()
        try:
            result['info']['country']
        except:
            result['info'].update({'country': 1,
                                   'country_name': 'Thailand',
                                   'country_code': 'TH'})
        return result

    def get_age(self):
        import datetime, pytz
        year = datetime.datetime.utcnow().replace(tzinfo=pytz.utc, microsecond=0).year
        if self.birthday is None:
            return -1
        year_user = self.birthday.year
        if year < year_user:
            age = -1
        else:
            age = year - year_user
        return age

    def get_display_age(self):
        age  = self.get_age()
        if age < 1 :
            return '-'
        return str(age)

    def image_name(self):
        try:
            blob_profile = self.blob_profile_set.filter(type=1)[0]
            return '%s-%s.jpg'%(self.id, blob_profile.id)
        except:
            return 'default.png'

    def logout(self):
        self.code = ''
        self.save()
    @staticmethod
    def get_native_email(app, email):
        return  '%s_%s'%(app.id, email)
    @staticmethod
    def get_user(app, email,auto_create = False,create_data={'username':None,'password':None}):
        native_email = Profile.get_native_email(app,email)
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=native_email)
            return user
        except:
            if auto_create:
                user = User.objects.create_user(create_data['username'], native_email,create_data['password'] )
                user.is_active = False
                user.is_staff = False
                user.is_superuser = False
                user.save()

            return None

    @staticmethod
    def get_profile(app, user, auto_create = False,auto_gen_code = False):

        create = False
        profile = None
        try :
            profile = Profile.objects.get(app=app,user=user)
        except Profile.MultipleObjectsReturned:
            profiles= list(Profile.objects.filter(app=app,user=user))
            profile = profiles[0]
            for profile_del in profiles[1:]:
                profile_del.delete()

        except Profile.DoesNotExist :
            if auto_create:
                profile = Profile(app=app,
                                  user=user,
                                  gender=0)
                profile.generate_code()
                profile.save()
                create = True

        if auto_gen_code and profile is not None:
            profile.generate_code()
            profile.save()

        return profile, create


    @staticmethod
    def login(app, email, password):
        from django.contrib.auth.models import User
        error_code = 0
        user = None
        profile = None
        email_old = email
        email = '%s_%s'%(app.id, email)
        try:
            user = User.objects.get(email=email)
        except:
            try:
                user = User.objects.get(username=email)
            except:
                error_code = 3302


        if user is not None:
            profiles = Profile.objects.filter(app=app,
                                              user=user)
            count = profiles.count()
            if count == 0:
                profile = Profile(app=app,
                                  user=user,
                                  gender=0)
            else:
                profile = profiles[0]
                for profile_del in profiles[1:]:
                    profile_del.delete()
            if email_old != 'user.api@shoppening.com':
                profile.generate_code()
            profile.save()
            if user.check_password(password):
                pass
            elif ResetPassword.objects.filter(profile=profile, password=password).count() > 0:
                user.set_password(password)
                user.save()
                ResetPassword.objects.filter(profile=profile).delete()
            else:
                error_code = 3303

        return error_code, user, profile
    @staticmethod
    def get_email_from_app_raw_email(app_id,rawemail):
        prefix = '%s_'%(app_id)
        email = rawemail.replace(prefix,'')
        return email

    @staticmethod
    def signup2(app, username, email, password):
        from django.contrib.auth.models import User
        import datetime
        error_code = 0
        user = None
        profile = None
        email_old = email
        username_old = username
        using_username = False
        if username is not None and email is not None:
            using_username = True
            username = '%s_%s'%(app.id, username)
            email = '%s_%s'%(app.id, email)
        elif username is not None:
            username = '%s_%s'%(app.id, username)
            email = '%s_%s'%(app.id, username)
        else:
            username = '%s_%s'%(app.id, email)
            email = '%s_%s'%(app.id, email)
        user_list = User.objects.filter(username=username)

        if user_list.count() > 0:
            user = user_list[0]
        if user is None:
            using_username = False
            user_list = User.objects.filter(email=email)
            if user_list.count() > 0:
                user = user_list[0]
        create_user = (user is None)
        if user is None:
            #user = User.objects.create_user(username, email, password)
            from django.db import IntegrityError
            try:
                user = User.objects.create_user(username, email, password)
                user.is_active = False
                user.is_staff = False
                user.is_superuser = False
                user.save()
            except IntegrityError:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User.objects.get(email=email)
        else:
            if user.check_password(password):
                pass
            else:

                if username is not None and using_username: error_code = 32041
                elif email is not None: error_code = 32042
                else : error_code = 3204
                print'266 %s %s : error_code : %s'%(username,email,error_code)
        if error_code == 0:
            profile_list = Profile.objects.filter(app=app,
                                                  user=user)
            if profile_list.count() == 0:
                profile = Profile(app=app,
                                  user=user)
                profile.generate_code()
            else:
                profile = profile_list[0]
                for profile_delete in profile_list[1:]:
                    profile_delete.delete()
            profile.save()
        return error_code, user, profile

    @staticmethod
    def signup(app, email, password, display='', gender=0, birthday=None, data='null'):
        from django.contrib.auth.models import User
        import datetime
        error_code = 0
        user = None
        profile = None
        email_old = email
        email = '%s_%s'%(app.id, email)
        try:
            user = User.objects.get(email=email)
        except:
            pass

        if user is None:
            #Create User
            try:
                user = User.objects.create_user(email, email, password)
            except Exception as e:
                from django.utils.encoding import force_text
                #print "Error in formatting: %s" % force_text(e, errors="replace")
                users = User.objects.filter(email=email)
                if users.count() == 0 :
                    raise e
                else :# bug something P'Mont found but can not identify what is the root cause
                    user= users[0]
            user.is_active = False
            user.is_staff = False
            user.is_superuser = False
            user.save()

            profile = Profile(app=app,
                              user=user,
                              gender=0)
            profile.generate_code()
            if len(display) > 0:
                profile.display = display
            else:
                profile.display = email_old
            if gender == 'M' or gender == 'm' or gender == '1' or gender == 1:
                profile.gender = 1
            elif gender == 'F' or gender == 'f' or gender == '2' or gender == 2:
                profile.gender = 2
            try:
                profile.birthday = datetime.datetime.strptime(birthday,"%Y-%m-%d")
            except:
                pass
            profile.save()
        else:
            #Found old User
            if user.check_password(password):
                profiles = Profile.objects.filter(app=app,
                                                  user=user)
                count = profiles.count()
                if count == 0:
                    profile = Profile(app=app,
                                      user=user,
                                      gender=0)
                    profile.generate_code()
                else:
                    profile = profiles[0]
                    for profile_del in profiles[1:]:
                        profile_del.delete()
                if len(display) > 0:
                    profile.display = display
                else:
                    profile.display = email_old
                if gender == 'M' or gender == 'm' or gender == '1' or gender == 1:
                    profile.gender = 1
                elif gender == 'F' or gender == 'f' or gender == '2' or gender == 2:
                    profile.gender = 2
                try:
                    profile.birthday = datetime.datetime.strptime(birthday,"%Y-%m-%d")
                except:
                    pass
                profile.save()
            else:
                print'364'
                if email is not None: error_code = 32042
                else : error_code = 3204
        return error_code, user, profile

    @staticmethod
    def forgetpass(app, email):
        from django.contrib.auth.models import User
        if app :
            email_query = '%s_%s'%(app.id, email)
            try:
                user = User.objects.get(email=email_query)
                profile = Profile.objects.get(app=app,
                                              user=user)
            except:
                profile = None
                reset_password = None
        else :
            email_query = '%s'%( email)
            try:
                user = User.objects.get(email=email_query)
                profile = Profile.objects.get(user=user)
            except:
                profile = None
                reset_password = None

        if profile is not None:
            reset_password = ResetPassword(profile=profile)
            reset_password.generate_code()
            if email == 'user.api@shoppening.com':
                reset_password.password = 'qwert'
            reset_password.save()
        return profile, reset_password
    @staticmethod
    def forgetpass_business(email, reseller=None):
        from django.contrib.auth.models import User
        if reseller is None:
            email_query = email
        else:
            email_query = 'r%s_%s'%(reseller.id, email)
        try:
            user = User.objects.get(email=email_query)
            try:
                profile = Profile.objects.get(app=None,
                                              user=user)
            except:
                profile = Profile(app=None,
                                  user=user,
                                  login_apppro=True)
                profile.save()
        except:
            profile = None
            reset_password = None
        if profile is not None:
            reset_password = ResetPassword(profile=profile)
            reset_password.generate_code()
            if email == 'user.api@shoppening.com':
                reset_password.password = 'qwert'
            reset_password.save()
        return profile, reset_password


class ProfileData(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)
    name = models.CharField(max_length=12)
    code = models.CharField(max_length=12)
    type = models.IntegerField(choices=MEMBER_PROFILEDATA_TYPE)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_profiledata')))
            super(ProfileData, self).save(*args, **kwargs)
        else:
            super(ProfileData, self).save(*args, **kwargs)

class ResetPassword(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    profile = models.ForeignKey(Profile)
    password = models.CharField(max_length=12)
    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp_reset = models.DateTimeField(null=True, default=None)
    is_reset = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_resetpassword')))
            super(ResetPassword, self).save(*args, **kwargs)
        else:
            super(ResetPassword, self).save(*args, **kwargs)

    def generate_code(self):
        from django.conf import settings
        import random
        while True:
            code = ''.join([random.choice(settings.SHOPPENING_CODE) for x in xrange(6)])
            if ResetPassword.objects.filter(password=code).count() == 0:
                break
        self.password = code

class Facebook(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)
    user = models.ForeignKey('auth.User')
    profile = models.ForeignKey(Profile)

    facebook_id = models.BigIntegerField(db_index=True)
    token = models.CharField(max_length=1024, null=True, blank=True, default=None)

    email = models.EmailField(null=True, blank=True, default=None)
    username = models.TextField(null=True, blank=True, default=None)
    name = models.TextField(null=True, blank=True, default=None)
    gender = models.IntegerField(choices=MEMBER_GENDER, default=0)

    timestamp_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_facebook')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    @staticmethod
    def get_profile_with_email(email, app):
        email = '%s_%s'%(app.id, email)
        try:
            user = Profile.objects.get(app=app, user__email=email)
        except:
            user = None
        return user

class Twitter(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    user = models.ForeignKey('auth.User')

    twitter_id = models.BigIntegerField(db_index=True ,unique=True)
    name = models.TextField(blank=True)
    screen_name = models.TextField(blank=True)
    email = models.EmailField(null=True, blank=True)

    timestamp_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_twitter')))
            super(Twitter, self).save(*args, **kwargs)
        else:
            super(Twitter, self).save(*args, **kwargs)

#Login/Signup With UUID/Code
class Code(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)
    shoppening = models.CharField(max_length=12)
    code = models.CharField(max_length=120)
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_code')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def generate_code(self):
        from django.conf import settings
        import random
        while True:
            code = ''.join(random.choice(settings.SHOPPENING_CODE) for x in range(6))
            if Code.objects.filter(app=self.app, code=code).count() == 0:
                break
        self.code = code

class UserUUID(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)
    code = models.ForeignKey(Code, null=True, blank=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)
    uuid = models.CharField(max_length=120)
    data = models.TextField(blank=True) #model
    timestamp_create = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True, db_index=True)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_user_uuid')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def profile_code(self):
        profile_list = Profile.objects.filter(user=self.user)
        profile = profile_list[0]
        return profile.code

    def get_email(self):
        try:
            email = self.user.email
            if email.find('_') != -1:
                return email[email.find('_')+1:]
            else:
                return email
        except:
            return ''

    def get_data_json(self):
        try:
            type(self.data_json)
        except:
            import json
            try:
                self.data_json = json.loads(self.data)
                if self.data_json is None:
                    self.data_json = {}
            except:
                self.data_json = {}
        return self.data_json

    def update_data(self, data_dict):
        import json
        data = self.get_data_json()
        if type(data) == type(None):
            data = {}
        data.update(data_dict)
        self.data = json.dumps(data)
        self.data_json = data
        return self.data_json

class FollowApp(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_follow_app')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

class FollowRaw(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)
    user = models.ForeignKey('auth.User')
    facebook_id = models.BigIntegerField(db_index=True)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_follow_raw')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

class Follow(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)
    user = models.ForeignKey('auth.User')
    follow = models.ForeignKey('auth.User', related_name='member_follow_set')
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_follow')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

class T1Card(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    app = models.CharField(max_length=12)
    user = models.ForeignKey('auth.User', null=True, blank=True)
    idcard = models.CharField(max_length=15, blank=True)
    t1card = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True, default=None)
    mobileid = models.CharField(max_length=60, blank=True)
    first_name_th = models.CharField(max_length=60, null=True, blank=True)
    first_name_en = models.CharField(max_length=60, null=True, blank=True)
    last_name_th = models.CharField(max_length=60, null=True, blank=True)
    last_name_en = models.CharField(max_length=60, null=True, blank=True)
    point_balance = models.BigIntegerField(blank=True)
    point_expiring = models.BigIntegerField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_follow')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def get_user(self):
        return self.user

    def get_profile(self):
        profiles = Profile.objects.filter(app=self.app,
                                          user=self.user)

        if not profiles.exists():
            profile = Profile(app=self.app,
                              user=self.user,
                              gender=0)
            profile.save()
        else:
            profile = profiles[0]
            for profile_del in profiles[1:]:
                profile_del.delete()
        return profile

    def get_data(self, auto_remove_on_fail = False):
        from customize.models import App as CustomizeApp
        import requests
        import xml.etree.ElementTree as ET

        if self.mobileid == "":
            # Need login
            return 11001, None

        url = ""
        if CustomizeApp.pull(self.app, 200000):
            url = "https://www.the-1-card.com/T1CWebserviceMobileForCG/Service.asmx/FnCheckPoint"
        elif CustomizeApp.pull(self.app, 200001):
            url = "https://www.the-1-card.com/T1CWebServiceForMobileCDSTest/Service.asmx/FnCheckPoint"
        payload = {
            "CustomerMobileID": self.mobileid
        }

        try:
            r = requests.post(url, data=payload)
        except:
            return 11001, None

        if r.status_code != 200:
            return 11001, None

        root = ET.fromstring(r.text.encode('utf-8'))

        data = {}

        for child in root:
            data[child.tag.replace('{http://tempuri.org/}', '')] = child.text

        if data['isComplete'] == "0":
            if auto_remove_on_fail:
                self.user = None
                self.save()
            return 11006, data

        is_change = False
        if 'CardNo' in data and self.t1card != data['CardNo']:
            is_change = True
            self.t1card = data['CardNo']

        if 'FirstThaiName' in data and self.first_name_th != data['FirstThaiName']:
            is_change = True
            self.first_name_th = data['FirstThaiName']

        if 'FirstEnglishName' in data and self.first_name_th != data['FirstEnglishName']:
            is_change = True
            self.first_name_en = data['FirstEnglishName']

        if 'LastThaiName' in data and self.first_name_th != data['LastThaiName']:
            is_change = True
            self.last_name_th = data['LastThaiName']

        if 'LastEnglishName' in data and self.first_name_th != data['LastEnglishName']:
            is_change = True
            self.last_name_en = data['LastEnglishName']

        if 'ExpiringPoints' in data and self.first_name_th != data['ExpiringPoints']:
            is_change = True
            self.point_expiring = data['ExpiringPoints']

        if 'TotalBalancePoints' in data and self.first_name_th != data['TotalBalancePoints']:
            is_change = True
            self.point_balance = data['TotalBalancePoints']

        if is_change:
            self.save()

        return 0, data

    def get_info(self):
        result = {}
        if self.mobileid == "":
            result["error_msg"] = "Please activate and login by The One card account"
        else:
            result['t1card'] = self.t1card
            result['first_name_th'] = self.first_name_th
            result['first_name_en'] = self.first_name_en
            result['last_name_th'] = self.last_name_th
            result['last_name_en'] = self.last_name_en
            result['point_expiring'] = self.point_expiring
            result['point_balance'] = self.point_balance

        return {'t1data': result}

    @staticmethod
    def get_by_user(app, user):
        t1card = None
        t1cards = T1Card.objects.filter(app=app,
                                        user=user)
        if t1cards.count() == 0:
            return None

        t1card = t1cards[0]
        for t1card_del in t1cards[1:]:
            t1card_del.delete()

        return t1card


    @staticmethod
    def login(app, email, mobileid):
        t1card = None
        # TODO: get or create t1card // update mobileid
        t1cards = T1Card.objects.filter(app=app,
                                        email=email)
        if t1cards.count() == 0:
            t1card = T1Card(app=app,
                            email=email,
                            point_expiring=0,
                            point_balance=0)
        else:
            t1card = t1cards[0]
            for t1card_del in t1cards[1:]:
                t1card_del.delete()

        t1card.mobileid = mobileid
        t1card.save()

        return t1card

    @staticmethod
    def register(app, user, email, t1card_id, idcard):
        t1card = T1Card(app=app,
                        user=user,
                        email=email,
                        t1card=t1card_id,
                        idcard=idcard,
                        point_expiring=0,
                        point_balance=0)
        t1card.save()
        return t1card

class FriendRequest(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    from_user = models.CharField(max_length=12)
    to_user = models.CharField(max_length=12)
    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(choices=FRIENDREQUEST_TYPE,default=1)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('from_user', 'to_user')


    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_follow')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)



    def accept(self):
        relation1 = Friend.objects.create(from_user=self.from_user,to_user=self.to_user)
        relation2 = Friend.objects.create(from_user=self.to_user,to_user=self.from_user)
        self.type = 4
        self.save()
        return True

    def reject(self):
        self.rejected = timezone.now()
        self.type = 2
        self.save()

    def cancel(self):
        self.type = 3
        self.save()
        self.delete()

    def mark_viewed(self):
        self.viewed = timezone.now()


#https://github.com/revsys/django-friendship/blob/master/friendship/models.py
class Friend(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    from_user = models.CharField(max_length=12)
    to_user = models.CharField(max_length=12)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = redis.Redis('127.0.0.1')
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('member_follow')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def find_friend(self,profile):
        status = False
        profile_friend = ''
        print profile
        if (profile == self.from_user):
            profile_friend = self.to_user
            status = True
        elif (profile == self.to_user):
            profile_friend = self.from_user
            status = True
        return profile_friend,status

    # def __unicode__(self):
    #     return "User #%d have a friendship with  #%d" % (self.from_user_id, self.to_user_id)=======
    # profile_subject = models.ForeignKey(Profile, related_name='profile_friend_set')
    # profile_friends = models.ForeignKey(Profile, related_name='friend_requested_set')

